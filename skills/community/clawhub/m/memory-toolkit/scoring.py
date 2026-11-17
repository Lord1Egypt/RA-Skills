#!/usr/bin/env python3
"""
Memory Scoring — Temporal decay, category weights, and frequency boosting.

Scores all memory items from daily notes and MEMORY.md using:
  1. Exponential recency decay (half-life 14 days by default)
  2. Category weights (DECISIONS > ERRORS > FACTS > PATTERNS > TRANSIENT)
  3. Frequency boost (memories mentioned across multiple days get boosted)
  4. Entity boost (memories with many entities are more important)

Output: memory/scores.json — ranking of all scored memories.

Designed to run after trace-extractor in the nightly pipeline.
No LLM required — pure Python, zero API cost.

Usage:
    python3 scoring.py                    # Score all memories
    python3 scoring.py --verbose          # Show top 20 scored items
    python3 scoring.py --threshold 0.3    # Only show items above score 0.3
    python3 scoring.py --archive          # Also auto-archive low-score items
"""

import argparse
import json
import math
import os
import re
import sys
import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw/workspace")).resolve()
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
SCORES_FILE = MEMORY_DIR / "scores.json"
ONTOLOGY_FILE = MEMORY_DIR / "ontology" / "graph.jsonl"

# Security: validate MEMORY_DIR is within WORKSPACE
if not MEMORY_DIR.resolve().is_relative_to(WORKSPACE):
    raise RuntimeError(f"Security: MEMORY_DIR escapes workspace: {MEMORY_DIR}")

# Security: restrict file scanning to MEMORY_DIR only — no parent traversal, no sibling skills/
ALLOWED_SCAN_DIR = MEMORY_DIR

# --- Configuration ---
HALF_LIFE_DAYS = 14
MAX_SCORE = 5.0

CATEGORY_WEIGHTS = {
    "decision": 3.0,
    "error": 2.0,
    "fact": 1.5,
    "pattern": 1.2,
    "transient": 1.0,
}

FREQUENCY_BOOST_BASE = 1.3  # multiplier per additional occurrence
ARCHIVE_THRESHOLD = 0.05    # items below this score are archive candidates
PROMOTE_THRESHOLD = 2.0     # items above this score are promotion candidates

# Category detection patterns (order matters — first match wins)
CATEGORY_PATTERNS = [
    ("decision", re.compile(
        r"(?:décidé|decided|choisi|chosen|validé|validated|"
        r"mis en place|deployed|désactivé|disabled|activé|enabled|"
        r"supprimé|deleted|créé|created|configuré|configured|"
        r"migré|migrated|installé|installed|livré|shipped|"
        r"GO|✅|fais-le|approuvé|approved|renamed|"
        r"changé|changed|switched|updated to|upgraded to)",
        re.IGNORECASE
    )),
    ("error", re.compile(
        r"(?:erreur|error|bug|fail|échec|crash|broken|corrompu|"
        r"corrupted|fixé|fixed|résolu|resolved|workaround|"
        r"⚠️|❌|panic|exception|timeout|429|500|502|503)",
        re.IGNORECASE
    )),
    ("fact", re.compile(
        r"(?:version|v\d+\.\d+|released|publié|annoncé|announced|"
        r"status|état|config|settings|port|url|ip address|"
        r"token|key|password|api|endpoint|"
        r"✅|mis à jour|updated|ajouté|added)",
        re.IGNORECASE
    )),
    ("pattern", re.compile(
        r"(?:toujours|always|jamais|never|récurrence|recurring|"
        r"pattern|habit|chaque|every|quotidien|daily|"
        r"cron|schedule|régulier|regular)",
        re.IGNORECASE
    )),
]

# Lines to skip (noise)
SKIP_PATTERNS = re.compile(
    r"^\s*[-*]\s*$|"        # empty bullet lines
    r"^#{1,6}\s|"           # headers (keep section context though)
    r"^\s*```|"             # code fences
    r"^\s*\|.*\|\s*$|"      # table rows
    r"^---+|"               # horizontal rules
    r"^\s*(?:HEARTBEAT_OK|NO_REPLY)",
    re.MULTILINE
)

DAILY_NOTE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-.+)?\.md$")

# Secret/sensitive file patterns to skip (never index or read these).
# Applied to the RESOLVED path (see safe_path below), not the literal one, so a
# symlink with an innocuous name cannot smuggle a secret into the index.
SECRET_SKIP_PATTERNS = [
    re.compile(r"\.secrets", re.IGNORECASE),
    re.compile(r"\.env", re.IGNORECASE),
    re.compile(r"credential", re.IGNORECASE),
    re.compile(r"token", re.IGNORECASE),
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"\.git/", re.IGNORECASE),
    re.compile(r"\.git$", re.IGNORECASE),
    re.compile(r"\.ssh", re.IGNORECASE),
    re.compile(r"id_rsa|id_ed25519|\.pem$|\.key$", re.IGNORECASE),
    re.compile(r"\.aws|\.config/google", re.IGNORECASE),
]


def is_safe_memory_file(path: Path) -> bool:
    """True only for a regular, non-symlink file whose RESOLVED path is innocuous.

    A symlink named like a daily note is the classic way to pull ~/.ssh/id_rsa
    into an index that then ships it to the embedding endpoint. Resolve first,
    then match, then require a regular file.
    """
    if path.is_symlink():
        print(f"  ⏭️  Skipping symlink: {path.name}", file=sys.stderr)
        return False
    resolved = os.path.realpath(str(path))
    for pattern in SECRET_SKIP_PATTERNS:
        if pattern.search(resolved):
            print(f"  ⏭️  Skipping sensitive file: {path.name}", file=sys.stderr)
            return False
    return os.path.isfile(resolved)


def detect_category(text: str) -> str:
    """Detect memory category from text content."""
    for category, pattern in CATEGORY_PATTERNS:
        if pattern.search(text):
            return category
    return "transient"


def parse_date_from_filename(filename: str) -> datetime | None:
    """Extract date from daily note filename."""
    match = DAILY_NOTE_RE.match(filename)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y-%m-%d")
        except ValueError:
            return None
    return None


def calculate_decay(date: datetime, reference: datetime, half_life: int = HALF_LIFE_DAYS) -> float:
    """Exponential decay: score * 0.5^(days_old / half_life)."""
    days_old = max((reference - date).days, 0)
    if days_old == 0:
        return 1.0
    return 0.5 ** (days_old / half_life)


def calculate_frequency_boost(text_key: str, frequency_map: Counter) -> float:
    """Logarithmic boost for items appearing across multiple days."""
    freq = frequency_map.get(text_key, 1)
    if freq <= 1:
        return 1.0
    return 1.0 + math.log(freq) * (FREQUENCY_BOOST_BASE - 1.0)


def normalize_text_for_grouping(text: str, max_chars: int = 60) -> str:
    """Normalize text for frequency detection across daily notes."""
    text = text.lower().strip()
    # Remove bullet prefixes
    text = re.sub(r"^[-*]\s+", "", text)
    text = re.sub(r"^(?:TODO|DONE|✅|❌|⚠️)\s*", "", text)
    # Remove dates (they vary but content is same)
    text = re.sub(r"\d{4}-\d{2}-\d{2}", "", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text[:max_chars].strip()


def extract_memory_items_from_file(filepath: Path, file_date: datetime) -> list[dict]:
    """Extract individual memory items from a markdown file."""
    items = []

    # Security guard: symlinks refused, sensitive/sensitive-resolved paths skipped
    if not is_safe_memory_file(filepath):
        return items

    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  ⚠️ Error reading {filepath.name}: {e}", file=sys.stderr)
        return items

    # Split into meaningful lines/bullets
    lines = content.split("\n")
    current_section = "general"

    for line in lines:
        stripped = line.strip()

        # Track sections
        if stripped.startswith("## "):
            current_section = stripped.lstrip("# ").strip().lower()
            continue

        # Skip noise
        if not stripped or SKIP_PATTERNS.match(stripped):
            continue

        # Skip very short lines
        if len(stripped) < 15:
            continue

        # Extract bullet points and meaningful lines
        # Remove markdown formatting for analysis
        clean = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped)  # bold
        clean = re.sub(r"`(.+?)`", r"\1", clean)            # inline code
        clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)  # links
        clean = clean.lstrip("-* ").strip()

        if len(clean) < 15:
            continue

        category = detect_category(clean)
        text_key = normalize_text_for_grouping(clean)

        items.append({
            "text": clean[:200],  # cap for storage
            "text_key": text_key,
            "category": category,
            "section": current_section,
            "source": filepath.name,
            "date": file_date.isoformat(),
            "entities": extract_entities(clean),
        })

    return items


def extract_entities(text: str) -> list[str]:
    """Simple entity extraction — capitalized words, tech terms, project names."""
    entities = []

    # Capitalized words (names, projects, products)
    for m in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b", text):
        entity = m.group(1)
        if entity not in ("The", "This", "That", "These", "Those", "Today", "Tonight",
                          "Yesterday", "Tomorrow", "Morning", "Evening", "Afternoon",
                          "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                          "Saturday", "Sunday"):
            entities.append(entity)

    # Tech terms (versions, acronyms)
    for m in re.finditer(r"\b(v\d+\.\d+(?:\.\d+)?)\b", text):
        entities.append(m.group(1))

    for m in re.finditer(r"\b([A-Z]{2,5})\b", text):
        acro = m.group(1)
        if acro not in ("API", "URL", "IP", "SSH", "HTTP", "HTTPS", "DNS", "TCP",
                        "UDP", "XML", "HTML", "CSS", "SQL", "JSON", "YAML", "TOML",
                        "CSV", "PDF", "PNG", "JPG", "SVG", "UTC", "GMT", "CET"):
            entities.append(acro)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for e in entities:
        if e.lower() not in seen:
            seen.add(e.lower())
            unique.append(e)
    return unique[:5]  # cap at 5 entities per item


def score_item(item: dict, reference_date: datetime, frequency_map: Counter) -> dict:
    """Calculate score for a single memory item."""
    # Base score
    score = 1.0

    # Category weight
    category = item.get("category", "transient")
    score *= CATEGORY_WEIGHTS.get(category, 1.0)

    # Recency decay
    item_date = datetime.fromisoformat(item["date"])
    decay = calculate_decay(item_date, reference_date)
    score *= decay

    # Frequency boost
    freq_boost = calculate_frequency_boost(item["text_key"], frequency_map)
    score *= freq_boost

    # Entity boost (memories with many entities are more information-rich)
    num_entities = len(item.get("entities", []))
    if num_entities > 2:
        score *= 1.0 + 0.1 * min(num_entities - 2, 3)

    # Completion penalty for completed action items
    if category == "decision" and re.search(r"\[x\]|completed|done|terminé|livré",
                                              item["text"], re.IGNORECASE):
        score *= 0.5  # completed items are less relevant going forward

    return {**item, "score": round(min(score, MAX_SCORE), 4)}


def load_existing_scores() -> dict:
    """Load previous scores for delta calculation."""
    if SCORES_FILE.exists():
        try:
            return json.loads(SCORES_FILE.read_text())
        except (json.JSONDecodeError, Exception):
            pass
    return {}


def run_scoring(verbose: bool = False, threshold: float = 0.0,
                archive: bool = False, dry_run: bool = False):
    """Main scoring routine."""
    reference_date = datetime.now()
    all_items = []

    # 1. Extract items from active daily notes
    if MEMORY_DIR.exists():
        for entry in sorted(MEMORY_DIR.iterdir()):
            if entry.is_symlink() or not entry.is_file() or not DAILY_NOTE_RE.match(entry.name):
                continue
            file_date = parse_date_from_filename(entry.name)
            if not file_date:
                continue
            items = extract_memory_items_from_file(entry, file_date)
            all_items.extend(items)

    # 2. Extract items from MEMORY.md (always relevant, no decay)
    if MEMORY_FILE.exists():
        memory_items = extract_memory_items_from_file(MEMORY_FILE, reference_date)
        # MEMORY.md items get no decay (always current)
        for item in memory_items:
            item["date"] = reference_date.isoformat()
            item["source"] = "MEMORY.md"
        all_items.extend(memory_items)

    if not all_items:
        print("📭 No memory items found to score.")
        return {"total": 0, "scored": 0, "promotions": 0, "archive_candidates": 0}

    # 3. Build frequency map (how many different days mention similar content)
    frequency_map = Counter()
    day_keys = defaultdict(set)  # text_key -> set of dates
    for item in all_items:
        key = item["text_key"]
        day_keys[key].add(item["date"][:10])
    for key, days in day_keys.items():
        frequency_map[key] = len(days)

    # 4. Deduplicate — if an item exists in both MEMORY.md and daily notes,
    #    keep the MEMORY.md version (higher priority, no decay) and drop the daily note copy
    seen_keys = set()
    deduped_items = []
    # Sort so MEMORY.md items come first (they win dedup)
    all_items.sort(key=lambda x: 0 if x["source"] == "MEMORY.md" else 1)
    for item in all_items:
        key = item["text_key"]
        if key in seen_keys:
            continue
        seen_keys.add(key)
        deduped_items.append(item)
    all_items = deduped_items

    # 5. Score all items
    scored_items = [score_item(item, reference_date, frequency_map) for item in all_items]

    # 6. Sort by score descending
    scored_items.sort(key=lambda x: x["score"], reverse=True)

    # 7. Categorize results
    promotions = [i for i in scored_items if i["score"] >= PROMOTE_THRESHOLD
                  and i["source"] != "MEMORY.md"]
    archive_candidates = [i for i in scored_items if i["score"] < ARCHIVE_THRESHOLD]

    # 8. Category distribution
    cat_dist = Counter(i["category"] for i in scored_items)

    # 9. Build output — SECURITY: store hashes + metadata only, not raw note text
    def _item_hash(text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()[:16]

    result = {
        "generated_at": reference_date.isoformat(),
        "config": {
            "half_life_days": HALF_LIFE_DAYS,
            "max_score": MAX_SCORE,
            "category_weights": CATEGORY_WEIGHTS,
            "frequency_boost_base": FREQUENCY_BOOST_BASE,
            "promote_threshold": PROMOTE_THRESHOLD,
            "archive_threshold": ARCHIVE_THRESHOLD,
        },
        "stats": {
            "total_items": len(scored_items),
            "promotions": len(promotions),
            "archive_candidates": len(archive_candidates),
            "category_distribution": dict(cat_dist),
            "avg_score": round(sum(i["score"] for i in scored_items) / len(scored_items), 4) if scored_items else 0,
            "max_score_seen": round(max(i["score"] for i in scored_items), 4) if scored_items else 0,
        },
        "top_items": [
            {
                "hash": _item_hash(i["text"]),
                "score": i["score"],
                "category": i["category"],
                "source": i["source"],
                "date": i["date"],
                "frequency": frequency_map.get(i["text_key"], 1),
            }
            for i in scored_items[:50]  # top 50
        ],
        "promotions": [
            {
                "hash": _item_hash(i["text"]),
                "score": i["score"],
                "category": i["category"],
                "source": i["source"],
                "date": i["date"],
                "frequency": frequency_map.get(i["text_key"], 1),
            }
            for i in promotions[:20]  # top 20 promotion candidates
        ],
        "archive_candidates": [
            {
                "hash": _item_hash(i["text"]),
                "score": i["score"],
                "source": i["source"],
                "date": i["date"],
            }
            for i in archive_candidates[:20]  # bottom 20
        ],
        "all_scores": [
            {
                "hash": _item_hash(i["text"]),
                "score": i["score"],
                "category": i["category"],
                "source": i["source"],
                "date": i["date"],
                "frequency": frequency_map.get(i["text_key"], 1),
            }
            for i in scored_items
        ],
    }

    # 10. Calculate delta from previous run
    previous = load_existing_scores()
    if previous and "stats" in previous:
        prev_total = previous["stats"].get("total_items", 0)
        delta = len(scored_items) - prev_total
        result["stats"]["delta_from_previous"] = delta
        if verbose and delta != 0:
            print(f"  📊 Delta from last run: {delta:+d} items")

    # 11. Save scores — SECURITY: restrict file permissions to owner-only
    if not dry_run:
        SCORES_FILE.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        try:
            SCORES_FILE.chmod(0o600)
        except (OSError, PermissionError):
            pass  # Best-effort on filesystems that don't support chmod

    # 12. Print summary
    print(f"\n📊 Memory Scoring Report — {reference_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Total items scored: {len(scored_items)}")
    print(f"   Average score: {result['stats']['avg_score']}")
    print(f"   Max score: {result['stats']['max_score_seen']}")
    print(f"   Promotions (>{PROMOTE_THRESHOLD}): {len(promotions)}")
    print(f"   Archive candidates (<{ARCHIVE_THRESHOLD}): {len(archive_candidates)}")
    print(f"   Category distribution: {dict(cat_dist)}")

    if verbose:
        print(f"\n🏆 Top 20 scored items:")
        for i, item in enumerate(scored_items[:20], 1):
            freq = frequency_map.get(item["text_key"], 1)
            print(f"  {i:2d}. [{item['score']:.3f}] ({item['category']:8s}) "
                  f"×{freq} {item['text'][:80]}")

        if promotions:
            print(f"\n⬆️  Promotion candidates (score ≥ {PROMOTE_THRESHOLD}):")
            for item in promotions[:10]:
                print(f"  [{item['score']:.3f}] {item['text'][:80]} "
                      f"({item['source']})")

        if archive_candidates:
            print(f"\n📦 Archive candidates (score < {ARCHIVE_THRESHOLD}):")
            for item in archive_candidates[:10]:
                print(f"  [{item['score']:.3f}] {item['text'][:80]} "
                      f"({item['source']})")

    # 13. Optional: archive low-score items
    if archive and archive_candidates and not dry_run:
        print(f"\n📦 Auto-archiving {len(archive_candidates)} low-score items...")
        # This would move source files to archive — but we archive whole files,
        # not individual lines. So we flag the source files instead.
        archive_sources = set(i["source"] for i in archive_candidates
                              if i["source"] != "MEMORY.md")
        flagged_file = MEMORY_DIR / "archive_candidates.json"
        flagged_file.write_text(json.dumps({
            "generated_at": reference_date.isoformat(),
            "sources": list(archive_sources),
            "count": len(archive_candidates),
        }, indent=2))
        print(f"   Flagged {len(archive_sources)} source files in archive_candidates.json")

    return result


def main():
    parser = argparse.ArgumentParser(description="Memory scoring with temporal decay")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show top 20 items")
    parser.add_argument("--threshold", type=float, default=0.0,
                        help="Minimum score to display")
    parser.add_argument("--archive", action="store_true",
                        help="Flag low-score items for archiving")
    parser.add_argument("--dry-run", action="store_true",
                        help="Don't write scores.json")
    parser.add_argument("--workspace", type=str, default=None,
                        help="Override workspace path")
    args = parser.parse_args()

    global WORKSPACE, MEMORY_DIR, MEMORY_FILE, SCORES_FILE
    if args.workspace:
        WORKSPACE = Path(args.workspace)
        MEMORY_DIR = WORKSPACE / "memory"
        MEMORY_FILE = WORKSPACE / "MEMORY.md"
        SCORES_FILE = MEMORY_DIR / "scores.json"

    result = run_scoring(
        verbose=args.verbose,
        threshold=args.threshold,
        archive=args.archive,
        dry_run=args.dry_run,
    )
    sys.exit(0 if result["stats"]["total_items"] > 0 else 1)


if __name__ == "__main__":
    main()