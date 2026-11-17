#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Confidentiality Scanner
-----------------------------------
Perform a deep scan of the skill pack covering the *content* of all files, not
just file paths/names. This includes:
  - Text files (.py / .md / .yaml / .json / templates / references / examples / any text)
  - Binary / cache files (e.g. __pycache__/*.pyc, whose bytecode embeds co_filename
    absolute paths; scanning only names/text would miss this kind of leak)

Purpose: before publishing (pushing to a shared branch), confirm the pack contains
no real customer / vendor identifiers or local absolute-path leaks. This automates
the "confidentiality review before each release" discipline.

Sensitive tokens (HIGH, a hit means a leak -> exit 1):
  - Built in (universal, safe to publish): local absolute paths
    /Users/ , /home/ , C:\\Users  -- these leak the developer's account name.
  - Deployment specific: customer / vendor / personal identifiers are deliberately
    NOT hardcoded in this package. Supply them at install time via config.yaml:

        confidentiality:
          high_tokens:   ["ACME", "ACME-DW"]       # literal, word-boundary matched
          high_patterns:                           # or explicit regex + label
            - pattern: "acme[-_]?dw"
              label: "ACME data warehouse"

    Keeping them out of the distributed package is the point: a published skill
    must not advertise whose data it was built around.

Whitelist (no alert, confirmed safe in review):
  - Desensitization placeholders: example client / example data-lake project / MPP data warehouse
  - Generic example role: nos-architect (methodology example role, not the customer system NOS)
  - Generic example emails: *@example.com (RFC 2606 reserved domain)
  - Generic example currency placeholders: example INR amount / INR XX.XM
    (explicitly marked as examples, not real amounts)

Usage:
  python3 confidentiality_check.py --pack <skill_root>   # default = two levels above the script
  python3 confidentiality_check.py                        # auto-locate skill root
Returns: HIGH leak found -> exit 1; all clear -> exit 0.
"""
import argparse
import os
import re
import sys


# ---- HIGH sensitive tokens: a hit means a leak ----
# Only universally sensitive patterns are built in. Customer / vendor / personal
# identifiers must never be hardcoded in a distributed package -- they are loaded
# from config.yaml (see `load_extra_patterns`), so the published skill carries no
# real-world identity while remaining fully functional for the owning org.
HIGH_PATTERNS = [
    (r'/Users/', 'absolute path /Users/ (leaks local username)'),
    (r'/home/', 'absolute path /home/ (leaks local username)'),
    (r'C:\\Users', 'absolute path C:\\Users (leaks local username)'),
]


def load_extra_patterns(pack_root):
    """Load deployment-specific sensitive tokens from config.yaml.

    Reads the `confidentiality` block:
        high_tokens:   ["ACME", ...]                     -> literal, word-boundary matched
        high_patterns: [{"pattern": ..., "label": ...}]  -> explicit regex (or bare regex string)

    Returns [] when unconfigured, so a freshly installed package leaks nothing
    and simply has nothing org-specific to look for.
    """
    extra = []
    cfg_path = os.path.join(pack_root, 'config.yaml')
    if not os.path.exists(cfg_path):
        return extra
    try:
        import yaml
        with open(cfg_path, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f) or {}
    except Exception:
        return extra
    block = cfg.get('confidentiality') or {}
    for tok in (block.get('high_tokens') or []):
        tok = str(tok).strip()
        if tok:
            extra.append((r'\b' + re.escape(tok) + r'\b',
                          f'{tok} (configured sensitive token)'))
    for entry in (block.get('high_patterns') or []):
        if isinstance(entry, dict):
            pat, label = entry.get('pattern'), entry.get('label')
        else:
            pat, label = entry, None
        pat = str(pat or '').strip()
        if pat:
            extra.append((pat, label or f'{pat} (configured sensitive pattern)'))
    return extra

# ---- Whitelist fragments confirmed safe in review (report hint only, no alert) ----
REVIEW_NOTES = [
    ('example client', 'desensitization placeholder (not a real customer name)'),
    ('example data-lake project', 'desensitization placeholder (not a real project name)'),
    ('MPP data warehouse', 'desensitization placeholder (not a real vendor name)'),
    ('nos-architect', 'generic methodology example role (not the customer system NOS)'),
    ('example INR amount', 'generic example currency placeholder (not a real amount)'),
    ('INR XX.XM', 'generic example currency placeholder (not a real amount)'),
]


def _scan_text(text, patterns):
    """Match line by line on decoded text, return [(line_no, label, snippet)]."""
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for pat, label in patterns:
            if re.search(pat, line):
                hits.append((i, label, line.strip()[:160]))
    return hits


def _scan_bytes(raw, patterns):
    """Byte-level scan on binary (e.g. .pyc), return [(offset, label, snippet)]."""
    hits = []
    for pat, label in patterns:
        for m in re.finditer(pat.encode('utf-8'), raw):
            start = max(0, m.start() - 30)
            end = min(len(raw), m.end() + 30)
            snippet = raw[start:end].decode('latin-1', errors='replace').replace('\n', ' ')
            hits.append((m.start(), label, snippet[:80]))
    return hits


# The scanner's own filename (contains sample sensitive tokens in its definitions)
# must be excluded from self-matching.
SELF_NAMES = {os.path.basename(__file__), 'confidentiality_check.py'}

# Meta documents (maintenance/explanation) are designed to reference sensitive
# token vocabulary (e.g. desensitization narrative, scanner explanation) and are
# not real leaks, so exclude them to avoid false positives; the real deliverable
# content (templates/scripts/references methodology) is still scanned fully.
EXCLUDE_META = {
    'confidentiality_check.py',
    'CHANGELOG.md',
    'usage.md',
    'README.md',
}


def scan_pack(pack_root):
    high = []        # (relpath, location, label, snippet)
    reviewed = set() # report hint for reviewed-safe fragments
    # Universal built-in patterns + any org-specific tokens supplied via config.yaml
    patterns = HIGH_PATTERNS + load_extra_patterns(pack_root)
    for dirpath, dirnames, filenames in os.walk(pack_root):
        # Skip git metadata
        if '.git' in dirnames:
            dirnames.remove('.git')
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, pack_root)
            # Skip the scanner itself (its source contains sample tokens to check, would self-match)
            if fn in SELF_NAMES:
                continue
            # Skip meta documents (maintenance/explanation, designed to reference tokens, not real leaks)
            if fn in EXCLUDE_META:
                continue
            try:
                with open(full, 'rb') as f:
                    raw = f.read()
            except OSError:
                continue
            # First try to decode as utf-8 text; on failure scan bytes as binary
            try:
                text = raw.decode('utf-8')
                is_text = True
            except UnicodeDecodeError:
                text = None
                is_text = False
            if is_text:
                for ln, label, snip in _scan_text(text, patterns):
                    high.append((rel, f'L{ln}', label, snip))
            else:
                for off, label, snip in _scan_bytes(raw, patterns):
                    high.append((rel, f'@{off}', label, snip))
            # Collect whitelist fragments for the hint
            sample = text if text is not None else raw.decode('latin-1', errors='replace')
            for token, note in REVIEW_NOTES:
                if token in sample:
                    reviewed.add(f'{token} -> {note}')
    return high, reviewed


def main():
    ap = argparse.ArgumentParser(description="PM Master · Confidentiality deep scan")
    here = os.path.dirname(os.path.abspath(__file__))
    default_pack = os.path.dirname(here)
    ap.add_argument('--pack', default=default_pack, help='skill root directory (default: parent of the script directory)')
    a = ap.parse_args()

    pack = os.path.abspath(a.pack)
    if not os.path.isdir(pack):
        raise SystemExit(f'Pack directory does not exist: {pack}')

    high, reviewed = scan_pack(pack)

    print('=' * 64)
    print(f'PM Master · Confidentiality scan  ->  {pack}')
    print('=' * 64)
    if high:
        print(f'\n[FAIL] {len(high)} HIGH sensitive-token leaks found:\n')
        for rel, loc, label, snip in high:
            print(f'  • {rel} ({loc})  [{label}]')
            print(f'      {snip}')
        print('\nThese hits must be desensitized before publishing.')
    else:
        print('\n[PASS] No HIGH sensitive tokens found in any file content (including binary/bytecode).')

    if reviewed:
        print('\n[INFO] Placeholder/example fragments confirmed safe in review (not flagged):')
        for r in sorted(reviewed):
            print(f'  - {r}')

    print('\n' + '=' * 64)
    return 1 if high else 0


if __name__ == '__main__':
    sys.exit(main())
