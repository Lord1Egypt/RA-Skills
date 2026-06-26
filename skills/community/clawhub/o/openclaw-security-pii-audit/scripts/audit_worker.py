#!/usr/bin/env python3
"""OpenClaw Security Audit Worker — PII detection and local NDJSON logging.

Usage:
    echo "text" | python audit_worker.py --session-id S001 --source-type input
    python audit_worker.py --session-id S001 --source-type input --text "short text"
    python audit_worker.py --session-id S001 --source-type knowledge_base --file path.txt
    python audit_worker.py --session-id S001 --source-type input --file tmp.txt --delete-after-read
    python audit_worker.py --session-id S001 --source-type input --text "text" --json
    python audit_worker.py --session-id S001 --source-type input --text "text" --no-cache

Security note:
    --text passes content via command-line args, which are visible in the
    process list.  For background / automated scans, prefer --file with
    --delete-after-read to avoid exposing PII in process metadata.
"""

import argparse
import hashlib
import json
import os
import random
import stat
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Ensure detectors package is importable
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from detectors import ALL_DETECTORS
from detectors.base import Match
from file_lock import FileLock

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
VERSION = "0.3.0"

DEFAULT_AUDIT_DIR = os.environ.get(
    'OPENCLAW_AUDIT_DIR',
    str(SCRIPT_DIR.parent / 'openclaw-security-audit')
)

HIGH_RISK_LABELS = {'NATIONAL_ID', 'PASSPORT', 'BANK_CARD'}

# Maximum input size in characters.  Content exceeding this limit is truncated
# to the first MAX_INPUT_CHARS characters; the audit record will carry
# ``truncated: true`` and the original ``input_chars`` count.
MAX_INPUT_CHARS = 32768

# Smart sampling configuration per source_type.
# rate:      probability [0.0, 1.0] of scanning content that is NOT in cache.
# cache_ttl: seconds before a cached content_hash expires and becomes eligible
#            for re-scanning.  Set to 0 to disable caching for a source type.
SAMPLE_CONFIG = {
    'input':          {'rate': 1.00, 'cache_ttl': 300},     # 100%, 5-min cache
    'prompt':         {'rate': 0.20, 'cache_ttl': 86400},   # 20%,  24-hour cache
    'context':        {'rate': 0.20, 'cache_ttl': 3600},    # 20%,  1-hour cache
    'knowledge_base': {'rate': 1.00, 'cache_ttl': 86400},   # 100%, 24-hour cache (dedup)
}

CACHE_MAX_ENTRIES = 5000   # Hard cap; prune to 3000 when exceeded
CACHE_FILE_NAME = '.scan-cache.json'


# ---------------------------------------------------------------------------
# Scan Cache — file-backed dedup + sampling gate
# ---------------------------------------------------------------------------
class ScanCache:
    """Lightweight file-backed cache tracking recently scanned content hashes.

    The cache is stored as a JSON object ``{content_hash: epoch_seconds}`` in
    the audit directory.  All file I/O is protected by a FileLock to support
    concurrent background scans.
    """

    def __init__(self, audit_dir: str):
        self.path = Path(audit_dir) / CACHE_FILE_NAME
        self._lock_path = str(self.path) + '.lock'
        self.data: dict = self._load()

    # -- persistence --------------------------------------------------------
    def _load(self) -> dict:
        if self.path.exists():
            try:
                with FileLock(self._lock_path):
                    return json.loads(self.path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with FileLock(self._lock_path):
            self.path.write_text(
                json.dumps(self.data, ensure_ascii=False),
                encoding='utf-8',
            )

    # -- query / update -----------------------------------------------------
    def is_fresh(self, content_hash: str, ttl: int) -> bool:
        """Return True if *content_hash* was scanned within the last *ttl* seconds."""
        ts = self.data.get(content_hash)
        if ts is None:
            return False
        return (time.time() - ts) < ttl

    def record(self, content_hash: str) -> None:
        """Mark *content_hash* as just-scanned and prune if over capacity."""
        self.data[content_hash] = time.time()
        if len(self.data) > CACHE_MAX_ENTRIES:
            # Keep the most recent 3000 entries
            ranked = sorted(self.data.items(), key=lambda kv: kv[1], reverse=True)
            self.data = dict(ranked[:3000])

    # -- decision -----------------------------------------------------------
    def should_scan(self, content_hash: str, source_type: str) -> bool:
        """Decide whether to scan based on cache freshness + sampling rate.

        Returns ``False`` (skip) when either:
        1. The content was scanned within the TTL window, OR
        2. The random draw exceeds the sampling rate for this source_type.
        """
        cfg = SAMPLE_CONFIG.get(source_type, SAMPLE_CONFIG['input'])
        if cfg['cache_ttl'] > 0 and self.is_fresh(content_hash, cfg['cache_ttl']):
            return False
        return random.random() < cfg['rate']


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def dedupe_overlapping(matches):
    """Remove lower-confidence matches whose character ranges overlap with
    higher-confidence matches.  Higher confidence wins."""
    sorted_matches = sorted(matches, key=lambda m: -m.confidence)
    result = []
    used_ranges = []
    for m in sorted_matches:
        overlaps = False
        for s, e in used_ranges:
            if m.start < e and m.end > s:
                overlaps = True
                break
        if not overlaps:
            result.append(m)
            used_ranges.append((m.start, m.end))
    return result


def compute_risk(labels):
    """Determine risk level based on detected label set.

    HIGH: any single high-risk label, or the combo PERSON_NAME + contact + ADDRESS.
    LOW:  everything else.
    """
    label_set = set(labels)
    if label_set & HIGH_RISK_LABELS:
        return 'high'
    has_name = 'PERSON_NAME' in label_set
    has_contact = bool(label_set & {'PHONE', 'EMAIL'})
    has_address = 'ADDRESS' in label_set
    if has_name and has_contact and has_address:
        return 'high'
    return 'low'


def _write_audit_record(record: dict, audit_dir: str) -> str:
    """Persist an audit record to the day-partitioned NDJSON file.

    File writes are protected by a FileLock to support concurrent processes.
    Returns the path of the output file.
    """
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    day_dir = Path(audit_dir) / today
    day_dir.mkdir(parents=True, exist_ok=True)

    # Best-effort restrictive permissions (owner-only) — limited on Windows
    try:
        day_dir.chmod(stat.S_IRWXU)
    except OSError:
        pass

    out_file = day_dir / 'events.ndjson'
    line = json.dumps(record, ensure_ascii=False) + '\n'

    with FileLock(str(out_file) + '.lock'):
        with open(out_file, 'a', encoding='utf-8') as f:
            f.write(line)

    return str(out_file)


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------
def scan(text, session_id, source_type, audit_dir, *,
         use_cache=True, input_chars=0, truncated=False):
    """Run all detectors, dedupe, compute risk, write NDJSON record.

    When *use_cache* is True (default), the scan cache and per-source-type
    sampling rates are respected — identical content is not re-scanned within
    the configured TTL, and low-priority sources may be randomly skipped.

    Every invocation writes an audit record (detected, clean, OR skipped)
    to ensure a complete audit trail.

    Returns a summary dict (never raises on detection failure).
    """
    content_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
    now = datetime.now(timezone.utc).isoformat()
    base_fields = {
        "event_id": str(uuid.uuid4()),
        "session_id": session_id,
        "source_type": source_type,
        "detector_version": VERSION,
        "content_hash": content_hash,
        "input_chars": input_chars,
        "truncated": truncated,
        "created_at": now,
    }

    def _safe_write(record):
        """Write audit record; log warning instead of crashing on I/O errors."""
        try:
            return _write_audit_record(record, audit_dir)
        except Exception as exc:
            print(f'[WARN] Failed to write audit record: {exc}', file=sys.stderr)
            return None

    # --- Smart sampling gate -----------------------------------------------
    cache = None
    if use_cache:
        try:
            cache = ScanCache(audit_dir)
        except Exception as exc:
            print(f'[WARN] Cache load failed, scanning without cache: {exc}',
                  file=sys.stderr)
            cache = None
        if cache is not None and not cache.should_scan(content_hash, source_type):
            skip_record = {
                **base_fields,
                "status": "skipped",
                "reason": "cached_or_sampled_out",
                "matched_count": 0,
            }
            _safe_write(skip_record)
            return {
                "status": "skipped",
                "reason": "cached_or_sampled_out",
                "content_hash": content_hash,
                "matched_count": 0,
            }

    # --- Detection ---------------------------------------------------------
    all_matches = []
    for detector in ALL_DETECTORS:
        try:
            hits = detector.detect(text)
            all_matches.extend(hits)
        except Exception as exc:
            print(f'[WARN] Detector {detector.label} error: {exc}', file=sys.stderr)

    all_matches = dedupe_overlapping(all_matches)

    # Update cache regardless of detection result
    if cache is not None:
        try:
            cache.record(content_hash)
            cache.save()
        except Exception as exc:
            print(f'[WARN] Cache save failed: {exc}', file=sys.stderr)

    # --- No PII found → clean ---------------------------------------------
    if not all_matches:
        clean_record = {
            **base_fields,
            "status": "clean",
            "matched_count": 0,
        }
        _safe_write(clean_record)
        return {"status": "clean", "matched_count": 0}

    # --- PII detected → full record ----------------------------------------
    labels = sorted(set(m.label for m in all_matches))
    risk = compute_risk(labels)
    regions = sorted(set(m.region for m in all_matches if m.region))

    record = {
        **base_fields,
        "status": "detected",
        "labels": labels,
        "regions": regions,
        "risk_level": risk,
        "matched_count": len(all_matches),
        "matches": [
            {
                "label": m.label,
                "confidence": m.confidence,
                "masked_preview": m.masked_preview,
                "region": m.region,
            }
            for m in all_matches
        ],
    }

    audit_file = _safe_write(record)

    result = {
        "status": "detected",
        "risk_level": risk,
        "labels": labels,
        "regions": regions,
        "matched_count": len(all_matches),
    }
    if audit_file:
        result["audit_file"] = audit_file
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description='OpenClaw PII Audit Worker — detect and log sensitive data'
    )
    parser.add_argument('--session-id', default='unknown',
                        help='Session identifier (default: unknown, warns if not set)')
    parser.add_argument('--source-type',
                        choices=['input', 'prompt', 'context', 'knowledge_base'],
                        default='input',
                        help='Content source type (default: input)')
    parser.add_argument('--file',
                        help='Read content from file instead of stdin')
    parser.add_argument('--text',
                        help='Inline text to scan (WARNING: visible in process list)')
    parser.add_argument('--delete-after-read', action='store_true',
                        help='Delete the --file after reading (for temp-file workflow)')
    parser.add_argument('--audit-dir', default=DEFAULT_AUDIT_DIR,
                        help='Audit output directory')
    parser.add_argument('--json', action='store_true',
                        help='Output result as JSON')
    parser.add_argument('--no-cache', action='store_true',
                        help='Bypass scan cache and sampling (force full scan)')
    args = parser.parse_args()

    # --- Validate flags ---
    if args.session_id == 'unknown':
        print('[WARN] --session-id not set, using "unknown". '
              'Provide a session ID for proper audit correlation.',
              file=sys.stderr)

    if args.text and args.file:
        print('[WARN] Both --text and --file provided; --file is ignored.',
              file=sys.stderr)

    if args.delete_after_read and not args.file:
        print('[WARN] --delete-after-read has no effect without --file.',
              file=sys.stderr)

    # --- Read input (with size cap applied during read) ---
    read_limit = MAX_INPUT_CHARS + 1  # read one extra char to detect truncation

    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read(read_limit)
        except OSError as exc:
            print(f'[ERROR] Cannot read file {args.file}: {exc}', file=sys.stderr)
            sys.exit(1)
        if args.delete_after_read:
            try:
                os.remove(args.file)
            except OSError as exc:
                print(f'[WARN] Could not delete temp file {args.file}: {exc}',
                      file=sys.stderr)
    else:
        text = sys.stdin.read(read_limit)

    if not text.strip():
        print('No input provided.', file=sys.stderr)
        sys.exit(1)

    # --- Size cap ---
    original_chars = len(text)
    truncated = False
    if original_chars > MAX_INPUT_CHARS:
        text = text[:MAX_INPUT_CHARS]
        truncated = True
        # original_chars is approximate when reading from file (could be larger)
        print(f'[INFO] Input truncated to {MAX_INPUT_CHARS} chars',
              file=sys.stderr)

    # --- Scan ---
    result = scan(
        text, args.session_id, args.source_type, args.audit_dir,
        use_cache=not args.no_cache,
        input_chars=original_chars,
        truncated=truncated,
    )

    # --- Output ---
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result['status'] == 'skipped':
            print(f'[SKIP] Content already scanned or sampled out '
                  f'(hash={result["content_hash"]})')
        elif result['status'] == 'clean':
            print('[CLEAN] No PII detected.')
        else:
            print(f'[{result["risk_level"].upper()}] '
                  f'Detected {result["matched_count"]} PII match(es)')
            print(f'  Labels:  {", ".join(result["labels"])}')
            print(f'  Regions: {", ".join(result["regions"])}')
            print(f'  Audit:   {result["audit_file"]}')


if __name__ == '__main__':
    main()
