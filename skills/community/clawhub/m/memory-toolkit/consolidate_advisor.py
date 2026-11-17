#!/usr/bin/env python3
"""
Consolidation Advisor — Semi-automatic memory consolidation suggestions.

Analyzes recent daily notes + scores.json to identify:
  1. CLUSTERS — memories mentioned across multiple days that could be merged
  2. PROMOTIONS — high-score items from daily notes worth promoting to MEMORY.md
  3. STALE — items in MEMORY.md that have decayed and could be trimmed
  4. DUPLICATES — near-duplicate text across daily notes

Writes consolidation_report.json by default. Modifies MEMORY.md only with --apply-promotions flag.
The agent reviews suggestions, the user validates, then changes are applied.

Uses Ollama (local LLM) for semantic grouping of similar memories.
No external API required.

Usage:
    python3 consolidate_advisor.py                    # Analyze last 7 days
    python3 consolidate_advisor.py --days 14          # Custom window
    python3 consolidate_advisor.py --dry-run          # Preview only (default)
    python3 consolidate_advisor.py --verbose          # Show all suggestions
    python3 consolidate_advisor.py --apply-promotions # Write promotions to MEMORY.md
"""

import argparse
import json
import os
import re
import sys
import shutil
import urllib.request
import urllib.error
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

# PII / secret patterns to scrub before sending text to LLM
PII_PATTERNS = [
    re.compile(r'gh[pousr]_[A-Za-z0-9]{36}'),                      # GitHub PAT
    re.compile(r'sk-[A-Za-z0-9]{20,}'),                            # OpenAI-style keys
    re.compile(r'AIza[A-Za-z0-9_\\-]{35}'),                       # Google API keys
    re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}'), # emails
    re.compile(r'(?:password|passwd|pwd|secret|token|api_key)\s*[:=]\s*\S+', re.IGNORECASE),
    re.compile(r'Bearer\s+[A-Za-z0-9._-]+'),                       # Bearer tokens
    re.compile(r'xox[baprs]-[A-Za-z0-9-]+'),                        # Slack tokens
    re.compile(r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC )?PRIVATE KEY-----'),  # PEM keys
]

def sanitize_pii(text: str) -> str:
    """Remove API keys, tokens, emails, and passwords from text before LLM submission."""
    for pattern in PII_PATTERNS:
        text = pattern.sub('[REDACTED]', text)
    return text

WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw/workspace")).resolve()
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
SCORES_FILE = MEMORY_DIR / "scores.json"
CONSOLIDATION_REPORT = MEMORY_DIR / "consolidation_report.json"

# Security: validate derived paths are within WORKSPACE. Re-run after
# --workspace rebinds the globals (import-time-only checking missed that).
def validate_paths() -> None:
    """Re-validate that all derived paths stay inside WORKSPACE."""
    for label, path in (
        ("MEMORY_DIR", MEMORY_DIR),
        ("MEMORY_FILE", MEMORY_FILE),
        ("SCORES_FILE", SCORES_FILE),
        ("CONSOLIDATION_REPORT", CONSOLIDATION_REPORT),
    ):
        if not path.resolve().is_relative_to(WORKSPACE):
            raise RuntimeError(f"Security: {label} escapes workspace: {path}")


validate_paths()

DAILY_NOTE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-.+)?\.md$")
ALLOWED_OLLAMA_HOSTS = {"localhost", "127.0.0.1", "::1"}


def get_safe_ollama_url(env_var: str, default: str) -> str:
    """Validate and return OLLAMA_URL, restricting to localhost only."""
    raw_url = os.environ.get(env_var, default)
    parsed = urlparse(raw_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid scheme for {env_var}: {parsed.scheme}")
    hostname = parsed.hostname or ""
    if hostname not in ALLOWED_OLLAMA_HOSTS:
        raise ValueError(f"Host '{hostname}' not allowed for {env_var}. Only localhost is permitted.")
    return raw_url


OLLAMA_URL = get_safe_ollama_url("OLLAMA_URL", "http://localhost:11434")
# Model resolution is centralised in llm_resolution.py (v4.0). The old local
# PREFERRED_MODELS tuple + resolve_llm_model() were a copy of conflict_resolver's,
# and that duplication broke production twice (a hard-coded "glm-5.2" answering
# 404 silently disabled this advisor). The single source of truth is now
# agents.defaults.model.primary, read from the gateway config.
# Import is tolerant so this script still runs if the module is absent.
try:
    from llm_resolution import resolve_llm_model as _resolve_llm_model

except ImportError:  # pragma: no cover - defensive: keep the advisor runnable
    def _resolve_llm_model(explicit=None, override_env=None,
                           require_local_presence=False):
        return explicit or os.environ.get("OLLAMA_MODEL") or "qwen2.5:7b"


def resolve_llm_model(explicit: str | None = None) -> str:
    """Pick the model to use, from llm_resolution (single source of truth)."""
    return _resolve_llm_model(explicit=explicit, override_env="OLLAMA_MODEL")


OLLAMA_MODEL = resolve_llm_model(os.environ.get("OLLAMA_MODEL"))

PROMOTE_THRESHOLD = 2.0
STALE_THRESHOLD = 0.15
MIN_CLUSTER_SIZE = 2  # need at least 2 mentions across days to form a cluster

# Same ceiling as memory-health.py: MEMORY.md is injected into every main-session
# context, so it has a hard budget. Consolidation must never push it past this.
MEMORY_MAX_SIZE = int(os.environ.get("MEMORY_MAX_SIZE", 5000))


def load_scores():
    """Load scores.json if available."""
    if SCORES_FILE.exists():
        try:
            return json.loads(SCORES_FILE.read_text())
        except (json.JSONDecodeError, Exception):
            pass
    return None


def read_daily_notes(days_back: int) -> list[dict]:
    """Read daily notes from the last N days."""
    cutoff = datetime.now() - timedelta(days=days_back)
    notes = []

    if not MEMORY_DIR.exists():
        return notes

    for entry in sorted(MEMORY_DIR.iterdir()):
        if entry.is_symlink() or not entry.is_file() or not DAILY_NOTE_RE.match(entry.name):
            continue
        match = DAILY_NOTE_RE.match(entry.name)
        if not match:
            continue
        try:
            file_date = datetime.strptime(match.group(1), "%Y-%m-%d")
        except ValueError:
            continue
        if file_date < cutoff:
            continue

        try:
            content = entry.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        # Extract meaningful lines
        lines = []
        current_section = "general"
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("## "):
                current_section = stripped.lstrip("# ").strip()
                continue
            if not stripped or len(stripped) < 15:
                continue
            if stripped.startswith("```") or stripped.startswith("|"):
                continue
            clean = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped)
            clean = re.sub(r"`(.+?)`", r"\1", clean)
            clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
            clean = clean.lstrip("-* ").strip()
            if len(clean) >= 15:
                lines.append({
                    "text": clean[:200],
                    "section": current_section,
                    "source": entry.name,
                    "date": match.group(1),
                })

        if lines:
            notes.extend(lines)

    return notes


def find_clusters(notes: list[dict]) -> list[dict]:
    """Find clusters of similar memories across multiple days.

    Uses simple text similarity (keyword overlap) — no LLM needed for this step.
    """
    # Group by normalized text key
    text_groups = defaultdict(list)
    for note in notes:
        key = normalize_for_clustering(note["text"])
        if key:
            text_groups[key].append(note)

    # Filter to clusters that span multiple days
    clusters = []
    for key, items in text_groups.items():
        dates = set(item["date"] for item in items)
        if len(dates) >= MIN_CLUSTER_SIZE:
            clusters.append({
                "key": key,
                "items": items,
                "date_count": len(dates),
                "dates": sorted(dates),
                "sample_text": items[0]["text"],
                "sources": sorted(set(item["source"] for item in items)),
            })

    # Sort by cluster size (most connections first)
    clusters.sort(key=lambda x: x["date_count"], reverse=True)
    return clusters


def normalize_for_clustering(text: str, max_chars: int = 60) -> str:
    """Normalize text for clustering similarity."""
    text = text.lower().strip()
    text = re.sub(r"^[-*]\s+", "", text)
    text = re.sub(r"^(?:TODO|DONE|✅|❌|⚠️|🔵)\s*", "", text)
    text = re.sub(r"\d{4}-\d{2}-\d{2}", "", text)
    text = re.sub(r"\d+:\d+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text[:max_chars].strip()


def find_promotions(scores: dict) -> list[dict]:
    """Find high-score items from daily notes worth promoting to MEMORY.md."""
    if not scores or "all_scores" not in scores:
        return []

    promotions = []
    seen_keys = set()

    for item in scores["all_scores"]:
        if item["score"] < PROMOTE_THRESHOLD:
            continue
        if item["source"] == "MEMORY.md":
            continue  # already in MEMORY.md

        # Deduplicate by hash (scoring.py stores hash, not text)
        item_key = item.get("text") or item.get("hash", "")
        key = normalize_for_clustering(item_key)
        if key in seen_keys:
            continue
        seen_keys.add(key)

        promotions.append({
            "text": item.get("text", item.get("hash", "")),
            "score": item["score"],
            "category": item["category"],
            "source": item["source"],
            "date": item["date"],
            "frequency": item.get("frequency", 1),
        })

    return promotions[:20]  # top 20


def find_stale_memory_items(scores: dict) -> list[dict]:
    """Find items in MEMORY.md that have low scores and could be trimmed."""
    if not scores or "all_scores" not in scores:
        return []

    stale = []
    for item in scores["all_scores"]:
        if item["source"] != "MEMORY.md":
            continue
        if item["score"] < STALE_THRESHOLD:
            stale.append({
                "text": item["text"],
                "score": item["score"],
                "category": item["category"],
            })

    return stale[:10]


def find_duplicates(notes: list[dict]) -> list[dict]:
    """Find near-duplicate text within daily notes."""
    seen = {}
    duplicates = []

    for note in notes:
        key = normalize_for_clustering(note["text"])
        if key in seen:
            original = seen[key]
            # Only report if from different files
            if original["source"] != note["source"]:
                duplicates.append({
                    "text": note["text"][:100],
                    "source1": original["source"],
                    "source2": note["source"],
                    "date1": original["date"],
                    "date2": note["date"],
                })
        else:
            seen[key] = note

    return duplicates[:10]


def llm_summarize_cluster(cluster: dict) -> str | None:
    """Use Ollama to generate a one-line summary of a memory cluster.

    SECURITY: Memory text is sanitized (PII/secrets removed) before LLM submission.
    """
    items_text = "\n".join(f"- {i['text']}" for i in cluster["items"][:5])
    items_text = sanitize_pii(items_text)

    print("   [Security] Sending sanitized excerpt to LLM...")

    prompt = f"""Summarize these related memory entries into ONE concise line (max 80 chars).
Return ONLY the summary, nothing else.

Entries:
{items_text}

Summary:"""

    try:
        payload = json.dumps({
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 50},
        }).encode()

        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        # SECURITY: urlopen sends to OLLAMA_URL (default localhost:11434) — keep local for privacy
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            return result.get("response", "").strip()[:100]
    except Exception as e:
        return None


def read_memory_md_sections() -> dict[str, list[str]]:
    """Read MEMORY.md and return sections with their lines."""
    if not MEMORY_FILE.exists():
        return {}

    sections = {}
    current_section = "Header"
    current_lines = []

    for line in MEMORY_FILE.read_text().split("\n"):
        if line.startswith("## "):
            sections[current_section] = current_lines
            current_section = line.strip()
            current_lines = []
        else:
            current_lines.append(line)
    sections[current_section] = current_lines

    return sections


def generate_consolidation_report(days_back: int, use_llm: bool = True,
                                   verbose: bool = False, dry_run: bool = False) -> dict:
    """Generate full consolidation report."""
    now = datetime.now()
    print(f"🔍 Analyzing daily notes from last {days_back} days...")

    # 1. Read recent daily notes
    notes = read_daily_notes(days_back)
    print(f"   Found {len(notes)} meaningful lines across {len(set(n['source'] for n in notes))} files")

    # 2. Load scores
    scores = load_scores()
    if scores:
        print(f"   Loaded scores.json: {scores['stats']['total_items']} items scored")
    else:
        print("   ⚠️ No scores.json found — run scoring.py first")

    # 3. Find clusters
    print("   Finding clusters...")
    clusters = find_clusters(notes)
    print(f"   Found {len(clusters)} clusters (≥{MIN_CLUSTER_SIZE} days)")

    # 4. Find promotions
    print("   Finding promotion candidates...")
    promotions = find_promotions(scores) if scores else []
    print(f"   Found {len(promotions)} promotion candidates (score ≥ {PROMOTE_THRESHOLD})")

    # 5. Find stale MEMORY.md items
    print("   Finding stale MEMORY.md items...")
    stale = find_stale_memory_items(scores) if scores else []
    print(f"   Found {len(stale)} stale items (score < {STALE_THRESHOLD})")

    # 6. Find duplicates
    print("   Finding duplicates...")
    duplicates = find_duplicates(notes)
    print(f"   Found {len(duplicates)} duplicate pairs")

    # 7. LLM summaries for top clusters
    if use_llm and clusters:
        print(f"   Generating LLM summaries for top {min(5, len(clusters))} clusters...")
        for cluster in clusters[:5]:
            summary = llm_summarize_cluster(cluster)
            if summary:
                cluster["summary"] = summary
                if verbose:
                    print(f"   → {summary}")

    # 8. Build report
    report = {
        "generated_at": now.isoformat(),
        "analysis_window_days": days_back,
        "stats": {
            "notes_analyzed": len(notes),
            "files_analyzed": len(set(n["source"] for n in notes)),
            "clusters_found": len(clusters),
            "promotions_found": len(promotions),
            "stale_items_found": len(stale),
            "duplicates_found": len(duplicates),
        },
        "clusters": [
            {
                "summary": c.get("summary", c["sample_text"][:80]),
                "date_count": c["date_count"],
                "dates": c["dates"],
                "sources": c["sources"],
                "sample_text": c["sample_text"],
                "suggested_action": "merge",
                "suggested_target": "MEMORY.md (relevant section)",
            }
            for c in clusters[:10]
        ],
        "promotions": promotions,
        "stale_items": stale,
        "duplicates": duplicates,
        "recommendations": generate_recommendations(clusters, promotions, stale, duplicates),
    }

    # 9. Save report (skip in dry-run mode)
    if not dry_run:
        CONSOLIDATION_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("\n--- Report (dry-run, not saved to file) ---")
        print(json.dumps(report, indent=2, ensure_ascii=False))

    # 10. Print summary
    print(f"\n📊 Consolidation Report — {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Notes analyzed: {len(notes)} lines from {report['stats']['files_analyzed']} files")
    print(f"   Clusters: {len(clusters)} (merge candidates)")
    print(f"   Promotions: {len(promotions)} (→ MEMORY.md)")
    print(f"   Stale items: {len(stale)} (trim candidates)")
    print(f"   Duplicates: {len(duplicates)} pairs")

    if verbose:
        if clusters:
            print(f"\n🔗 Top clusters (merge candidates):")
            for c in report["clusters"][:5]:
                print(f"  [{c['date_count']} days] {c['summary']}")
                print(f"    Sources: {', '.join(c['sources'][:3])}")

        if promotions:
            print(f"\n⬆️  Top promotions (→ MEMORY.md):")
            for p in promotions[:10]:
                print(f"  [{p['score']:.2f}] {p['text'][:80]}")
                print(f"    Source: {p['source']}")

        if stale:
            print(f"\n📉 Stale MEMORY.md items (trim candidates):")
            for s in stale[:5]:
                print(f"  [{s['score']:.3f}] {s['text'][:80]}")

        if duplicates:
            print(f"\n👯 Duplicates:")
            for d in duplicates[:5]:
                print(f"  {d['text'][:60]}")
                print(f"    {d['source1']} ↔ {d['source2']}")

    if report["recommendations"]:
        print(f"\n💡 Recommendations:")
        for rec in report["recommendations"]:
            print(f"  {rec}")

    return report


def generate_recommendations(clusters, promotions, stale, duplicates) -> list[str]:
    """Generate human-readable recommendations."""
    recs = []

    if len(clusters) >= 3:
        recs.append(f"🔗 {len(clusters)} memory clusters detected — consider merging related daily notes into MEMORY.md sections")

    if len(promotions) >= 5:
        recs.append(f"⬆️  {len(promotions)} high-score items worth promoting to MEMORY.md — review and add the most relevant")

    if len(stale) >= 3:
        recs.append(f"📉 {len(stale)} stale items in MEMORY.md — consider trimming or archiving outdated entries")

    if len(duplicates) >= 2:
        recs.append(f"👯 {len(duplicates)} duplicate pairs found — consolidate to avoid redundancy")

    if not recs:
        recs.append("✅ Memory system is healthy — no consolidation needed")

    return recs


def apply_promotions(promotions: list[dict], dry_run: bool = True, force: bool = False) -> int:
    """Apply promotions by appending to MEMORY.md."""
    if not promotions:
        print("No promotions to apply.")
        return 0

    if not MEMORY_FILE.exists():
        print("❌ MEMORY.md not found")
        return 0

    content = MEMORY_FILE.read_text()

    # Find the last section or end of file
    lines = content.split("\n")

    # Build new entries
    new_lines = ["", "<!-- Auto-promoted by consolidate_advisor.py -->"]
    count = 0
    for p in promotions:
        if p["text"][:50].lower() in content.lower():
            continue  # skip if already present
        entry = f"- {p['text']}"
        new_lines.append(entry)
        count += 1

    if count == 0:
        print("All promotions already in MEMORY.md — nothing to add.")
        return 0

    if dry_run:
        print(f"🔍 Dry run — would add {count} entries to MEMORY.md:")
        for line in new_lines[2:]:
            print(f"  {line}")
        return count

    # Confirmation prompt (skip if --force)
    if not force:
        print(f"\n📝 The following {count} entries will be added to MEMORY.md:")
        for line in new_lines[2:]:
            print(f"  {line}")
        print()
        if not sys.stdin.isatty():
            print("❌ Non-interactive mode detected. Use --force to apply without confirmation.")
            return 0
        response = input("Proceed? (y/n): ").strip().lower()
        if response not in ("y", "yes"):
            print("Aborted. No changes made.")
            return 0

    # Backup MEMORY.md before writing
    if MEMORY_FILE.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = MEMORY_FILE.with_suffix(f".{timestamp}.bak")
        shutil.copy2(str(MEMORY_FILE), str(backup_path))
        print(f"📦 Backup created: {backup_path}")

    # Append to MEMORY.md
    updated = content.rstrip() + "\n" + "\n".join(new_lines) + "\n"

    # ── Size guard ────────────────────────────────────────────────────────
    # MEMORY.md is injected into every main-session context; an unbounded
    # append is how it silently grew to 19.6 KB against a 5 KB budget (10/10).
    # Refuse to write past the ceiling: the overflow would be pure context
    # cost, and promotions are suggestions, not obligations.
    projected = len(updated.encode("utf-8"))
    if projected > MEMORY_MAX_SIZE:
        print(f"❌ Size guard: refusing to write — projected MEMORY.md "
              f"{projected} bytes > limit {MEMORY_MAX_SIZE} bytes "
              f"(+{projected - len(content.encode('utf-8'))} would be added).")
        print(f"   Trim/archive MEMORY.md first, or promote fewer entries.")
        return 0

    MEMORY_FILE.write_text(updated)
    print(f"✅ Added {count} promoted entries to MEMORY.md "
          f"({projected}/{MEMORY_MAX_SIZE} bytes)")
    return count


def main():
    parser = argparse.ArgumentParser(description="Semi-automatic memory consolidation advisor")
    parser.add_argument("--days", type=int, default=7, help="Analysis window in days (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Don't modify any files (default)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all suggestions")
    parser.add_argument("--no-llm", action="store_true", help="Skip LLM cluster summaries")
    parser.add_argument("--apply-promotions", action="store_true",
                        help="Write promotions to MEMORY.md (requires confirmation or --force)")
    parser.add_argument("--force", action="store_true",
                        help="Apply changes non-interactively. Requires existing verified backup in workspace. "
                             "Creates timestamped .bak backup before modifying MEMORY.md.")
    parser.add_argument("--workspace", type=str, default=None, help="Override workspace path")
    args = parser.parse_args()

    global WORKSPACE, MEMORY_DIR, MEMORY_FILE, SCORES_FILE, CONSOLIDATION_REPORT
    if args.workspace:
        WORKSPACE = Path(args.workspace).resolve()
        MEMORY_DIR = WORKSPACE / "memory"
        MEMORY_FILE = WORKSPACE / "MEMORY.md"
        SCORES_FILE = MEMORY_DIR / "scores.json"
        CONSOLIDATION_REPORT = MEMORY_DIR / "consolidation_report.json"
        # Re-run the confinement guard on the overridden values.
        validate_paths()

    report = generate_consolidation_report(
        days_back=args.days,
        use_llm=not args.no_llm,
        verbose=args.verbose,
        dry_run=args.dry_run,
    )

    if args.apply_promotions and report.get("promotions"):
        print("\n📝 Applying promotions to MEMORY.md...")
        apply_promotions(report["promotions"], dry_run=args.dry_run, force=args.force)

    sys.exit(0)


if __name__ == "__main__":
    main()