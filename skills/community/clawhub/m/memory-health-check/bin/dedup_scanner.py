#!/usr/bin/env python3
"""Dedup scanner — fast duplicate/near-duplicate detection using hashing."""
import argparse
import hashlib
import json
import logging
import re
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from config_loader import load_config
from health_models import DimResult
from log_utils import get_logger

logger = get_logger("memory-health-check.dedup_scanner")

# Shared stop words for dedup
STOP_WORDS = {
    "的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都",
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "to", "of", "in", "for", "on", "with", "at", "by",
}


def normalize_text(text: str) -> set[str]:
    """Normalize text to token set for similarity comparison."""
    text = text.lower()
    text = re.sub(r"[^\w\s\u4e00-\u9fff]", " ", text)
    tokens = text.split()
    return {t for t in tokens if t not in STOP_WORDS and len(t) >= 2}


def token_similarity(a: str, b: str) -> float:
    """Compute token-overlap similarity between two texts."""
    if not a or not b:
        return 0.0
    tokens_a = normalize_text(a)
    tokens_b = normalize_text(b)
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = len(tokens_a & tokens_b)
    union = len(tokens_a | tokens_b)
    jaccard = intersection / union if union > 0 else 0.0
    overlap = intersection / min(len(tokens_a), len(tokens_b)) if min(len(tokens_a), len(tokens_b)) > 0 else 0.0
    return round(0.4 * jaccard + 0.6 * overlap, 4)


def scan_for_duplicates(
    base_dir: Path,
    threshold: float = 0.85,
    limit: int = 5000,
) -> dict:
    """Legacy compatibility stub — delegates to dedup_scan()."""
    return dedup_scan(base_dir=base_dir, threshold=threshold)


def dedup_scan(
    base_dir: Optional[Path] = None,
    threshold: float = 0.85,
) -> dict:
    """Fast dedup scan using multi-phase approach.
    
    Phase 1: MD5 full-content hash → exact duplicates (O(n), instant)
    Phase 2: Size + prefix hash grouping → near-duplicates (O(n), fast)
    Phase 3: Only compare within candidate groups (minimal comparisons)
    """
    if base_dir is None:
        base_dir = Path.home() / ".openclaw" / "workspace" / "memory"

    if not base_dir.exists():
        return {
            "score": 100, "status": "healthy",
            "dup_count": 0, "total_entries": 0,
            "dup_rate": 0.0, "exact_dups": 0,
            "near_dups": 0, "duplicate_pairs": [],
        }

    # Collect all .md files
    all_files = []
    for f in base_dir.rglob("*.md"):
        try:
            size = f.stat().st_size
            if size > 0:
                all_files.append(f)
        except Exception:
            pass

    total = len(all_files)
    if total < 2:
        return {
            "score": 100, "status": "healthy",
            "dup_count": 0, "total_entries": total,
            "dup_rate": 0.0, "exact_dups": 0,
            "near_dups": 0, "duplicate_pairs": [],
        }

    # ============ Phase 1: Exact MD5 duplicates (instant) ============
    by_full_hash: dict[str, list[Path]] = {}
    by_size_and_prefix: dict[tuple, list[tuple]] = {}  # (size, first_token_hash) -> [(path, prefix_hash)]

    exact_dup_groups = 0
    near_dup_pairs = []
    near_dup_set: set[tuple] = set()

    # Read and hash all files in one pass
    file_data: dict[Path, tuple[str, str, int]] = {}  # path -> (full_hash, prefix_hash, size)
    for f in all_files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            # Full content MD5
            full_hash = hashlib.md5(content.encode("utf-8", errors="ignore")).hexdigest()
            # Prefix hash (first 500 chars) for near-dupe grouping
            prefix = content[:500].lower()
            prefix_hash = hashlib.md5(prefix.encode("utf-8", errors="ignore")).hexdigest()[:16]
            file_data[f] = (full_hash, prefix_hash, len(content))
        except Exception:
            pass

    # Exact duplicates
    hash_groups: dict[str, list[Path]] = {}
    for f, (full_hash, _, _) in file_data.items():
        hash_groups.setdefault(full_hash, []).append(f)

    exact_dup_files = 0
    exact_dup_pairs_out = []
    for h, paths in hash_groups.items():
        if len(paths) > 1:
            exact_dup_files += len(paths)
            exact_dup_groups += 1
            # Record pairs (max 3 per group to avoid huge output)
            for i in range(min(3, len(paths))):
                for j in range(i + 1, min(3, len(paths))):
                    exact_dup_pairs_out.append({
                        "type": "exact",
                        "file_a": str(paths[i]),
                        "file_b": str(paths[j]),
                        "similarity": 1.0,
                })

    # ============ Phase 2: Near-duplicate detection via grouping ============
    # Group by (size_bucket, prefix_hash_bucket) to limit comparisons
    # Size buckets: <1KB, 1-5KB, 5-20KB, 20-100KB, >100KB
    def size_bucket(s: int) -> int:
        if s < 1024: return 0
        if s < 5*1024: return 1
        if s < 20*1024: return 2
        if s < 100*1024: return 3
        return 4

    groups: dict[tuple, list[tuple]] = {}  # (size_bucket, prefix_hash[:8]) -> [(path, prefix_hash)]
    for f, (full_hash, prefix_hash, size) in file_data.items():
        bucket = size_bucket(size)
        key = (bucket, prefix_hash[:8])
        groups.setdefault(key, []).append((f, prefix_hash))

    # Only compare within groups (files with similar size + similar prefix)
    # Cap comparisons per group to avoid blow-up
    MAX_PAIRS_PER_GROUP = 200
    compared = 0
    for key, group_files in groups.items():
        if len(group_files) < 2:
            continue
        if len(group_files) > 100:
            # Too many in same bucket, sample to avoid O(n^2)
            import random
            sample = random.sample(group_files, min(100, len(group_files)))
            group_files = sample

        for i in range(len(group_files)):
            for j in range(i + 1, len(group_files)):
                if compared >= 5000:  # Global cap on comparisons
                    break
                path_i, ph_i = group_files[i]
                path_j, ph_j = group_files[j]
                compared += 1

                # Skip if already exact dup
                if file_data[path_i][0] == file_data[path_j][0]:
                    continue

                # Read content for similarity (already in file_data but we only stored hash)
                try:
                    c1 = path_i.read_text(encoding="utf-8", errors="ignore")[:2000]
                    c2 = path_j.read_text(encoding="utf-8", errors="ignore")[:2000]
                    sim = token_similarity(c1, c2)
                    if sim >= threshold:
                        pair = tuple(sorted([str(path_i), str(path_j)]))
                        if pair not in near_dup_set:
                            near_dup_set.add(pair)
                            near_dup_pairs.append({
                                "type": "near",
                                "file_a": str(path_i),
                                "file_b": str(path_j),
                                "similarity": sim,
                            })
                except Exception:
                    pass

    total_dup_files = exact_dup_files + len(near_dup_set) * 2
    dup_rate = total_dup_files / max(total, 1)

    config = load_config()
    thresholds = config.get("thresholds", {}).get("dedup_rate", {})
    healthy_rate = thresholds.get("healthy", 0.02)
    warning_rate = thresholds.get("warning", 0.10)

    if dup_rate <= healthy_rate:
        score = 100
        status = "healthy"
    elif dup_rate <= warning_rate:
        score = 60
        status = "warning"
    else:
        score = 20
        status = "critical"

    all_pairs = exact_dup_pairs_out + near_dup_pairs[:47 - len(exact_dup_pairs_out)]

    return {
        "score": score,
        "status": status,
        "dup_count": total_dup_files,
        "total_entries": total,
        "dup_rate": round(dup_rate * 100, 4),
        "exact_dups": exact_dup_files,
        "near_dups": len(near_dup_set),
        "exact_groups": exact_dup_groups,
        "comparisons_done": compared,
        "duplicate_pairs": all_pairs[:50],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan for duplicate entries")
    parser.add_argument("--base-dir", type=Path, default=None)
    parser.add_argument("--threshold", type=float, default=0.85)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        import logging
        get_logger().setLevel(logging.DEBUG)

    result = dedup_scan(base_dir=args.base_dir, threshold=args.threshold)
    print(f"[dedup_scanner] Status: {result['status']}, Dups: {result['dup_count']}/{result['total_entries']}, Score: {result['score']}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
