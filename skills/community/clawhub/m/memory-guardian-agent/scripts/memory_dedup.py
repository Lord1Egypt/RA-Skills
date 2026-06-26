#!/usr/bin/env python3
"""memory-guardian: Nearest-neighbor distance dedup with four-zone classification (v0.4.1).

Replaces v0.3 coverage threshold with nearest-neighbor distance zones:
  - distance < 0.2: ABSORB (merge into nearest — very similar)
  - [0.2, 0.5):     DERIVE (create derivative candidate)
  - [0.5, 0.8):     NEW_TYPE (new case type)
  - distance ≥ 0.8:  SUSPEND (hold for N=2 confirmation — very different)

Uses bigram Jaccard + TF-IDF cosine as distance metrics.
No embedding service required.

v0.4.1 fix: zone thresholds were inverted (distance vs similarity swapped).

Usage:
  python3 memory_dedup.py [--meta <path>] [--threshold <float>] [--dry-run]
  python3 memory_dedup.py [--zone absorb|derive|new|suspend] [--limit 10]
"""
import json, math, re, os, argparse, sys
from collections import Counter
from datetime import datetime
from mg_utils import CST, tokenize, jaccard_distance, load_meta as _load_meta, save_meta as _save_meta, safe_print

print = safe_print

# ─── Zone Thresholds (v0.4.1 fix: LOW distance = similar = absorb) ──
ZONE_ABSORB = 0.20       # <0.2: merge into nearest (very similar)
ZONE_DERIVE_LOW = 0.20   # lower bound of derive zone
ZONE_DERIVE_HIGH = 0.50  # upper bound of derive zone
ZONE_NEW_LOW = 0.50      # lower bound of new_type zone
ZONE_SUSPEND = 0.80      # ≥0.8: suspend (very different)

# ─── Tokenization ────────────────────────────────────────────
def cosine_sim(vec_a, vec_b):
    """TF-IDF cosine similarity."""
    dot = sum(vec_a.get(k, 0) * vec_b.get(k, 0) for k in vec_a)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def tfidf_vectors(texts):
    """Build TF-IDF vectors for a list of texts."""
    N = len(texts)
    df = Counter()
    tfs = []
    for text in texts:
        tokens = tokenize(text)
        tf = Counter(tokens)
        tfs.append(tf)
        for t in set(tokens):
            df[t] += 1
    vectors = []
    for tf in tfs:
        vec = {}
        for t, count in tf.items():
            idf = math.log((N + 1) / (df[t] + 1)) + 1
            vec[t] = count * idf
        vectors.append(vec)
    return vectors


def combined_distance(text_a, text_b, vectors=None, idx_a=None, idx_b=None):
    """Combined distance: 0.6 × Jaccard + 0.4 × (1 - cosine)."""
    tokens_a = set(tokenize(text_a))
    tokens_b = set(tokenize(text_b))
    j_dist = jaccard_distance(tokens_a, tokens_b)

    cos_sim_val = 0.0
    if vectors and idx_a is not None and idx_b is not None:
        cos_sim_val = cosine_sim(vectors[idx_a], vectors[idx_b])
    cos_dist = 1.0 - cos_sim_val

    return 0.6 * j_dist + 0.4 * cos_dist


def classify_zone(distance):
    """Classify a distance into one of four zones.

    distance=0 means identical, distance=1 means completely different.
    - absorb:   very similar (distance < 0.2) → merge into nearest
    - derive:   somewhat similar (0.2–0.5) → derivative candidate
    - new_type: somewhat different (0.5–0.8) → new case type
    - suspend:  very different (≥ 0.8) → hold for confirmation
    """
    if distance >= ZONE_SUSPEND:
        return "suspend"
    elif distance >= ZONE_NEW_LOW:
        return "new_type"
    elif distance >= ZONE_DERIVE_LOW:
        return "derive"
    else:
        return "absorb"


def find_nearest_neighbor(target_idx, memories, vectors):
    """Find the nearest neighbor for a memory among active/observing cases."""
    target = memories[target_idx]
    target_content = target.get("content", "")
    target_situation = target.get("situation", "") or ""
    target_text = f"{target_content} {target_situation}".strip()

    best_dist = 1.0
    best_idx = -1

    for i, mem in enumerate(memories):
        if i == target_idx:
            continue
        status = mem.get("status", "active")
        if status not in ("active", "observing"):
            continue
        mem_content = mem.get("content", "")
        mem_situation = mem.get("situation", "") or ""
        mem_text = f"{mem_content} {mem_situation}".strip()

        dist = combined_distance(target_text, mem_text, vectors, target_idx, i)
        if dist < best_dist:
            best_dist = dist
            best_idx = i

    return best_idx, best_dist


def run(meta_path, threshold, dry_run, zone_filter, limit, force_absorb=False):
    meta = _load_meta(meta_path)
    now = datetime.now(CST).isoformat()

    # Only process active + observing memories
    memories = [m for m in meta.get("memories", [])
                if m.get("status", "active") in ("active", "observing")]

    if len(memories) < 2:
        print("Not enough active/observing memories to analyze.")
        return {"results": []}

    texts = [m.get("content", "") for m in memories]
    vectors = tfidf_vectors(texts)

    # Compute nearest neighbor for each memory
    results = []
    zone_counts = {"absorb": 0, "derive": 0, "new_type": 0, "suspend": 0}

    for i in range(len(memories)):
        nn_idx, nn_dist = find_nearest_neighbor(i, memories, vectors)
        zone = classify_zone(nn_dist)
        zone_counts[zone] += 1

        result = {
            "id": memories[i].get("id", "?"),
            "content": memories[i].get("content", "")[:80],
            "nn_id": memories[nn_idx].get("id", "?") if nn_idx >= 0 else None,
            "nn_content": memories[nn_idx].get("content", "")[:80] if nn_idx >= 0 else None,
            "distance": round(nn_dist, 4),
            "zone": zone,
            "status": memories[i].get("status", "active"),
        }
        results.append(result)

    # Filter by zone if requested
    if zone_filter:
        zone_map = {"absorb": "absorb", "derive": "derive", "new": "new_type", "suspend": "suspend"}
        filter_zone = zone_map.get(zone_filter, zone_filter)
        filtered = [r for r in results if r["zone"] == filter_zone]
    else:
        filtered = results

    # Sort by distance (most similar first)
    filtered.sort(key=lambda x: x["distance"])

    if limit:
        filtered = filtered[:limit]

    # Print report
    zone_icons = {"absorb": "🔄", "derive": "🔬", "new_type": "🆕", "suspend": "⏸️"}
    print(f"Nearest-Neighbor Distance Analysis ({len(memories)} memories)")
    print(f"  Zones: {', '.join(f'{zone_icons[z]} {z}: {zone_counts[z]}' for z in ['absorb', 'derive', 'new_type', 'suspend'])}")
    print(f"  Thresholds: absorb<{ZONE_ABSORB} derive[{ZONE_DERIVE_LOW}-{ZONE_DERIVE_HIGH}] new[{ZONE_NEW_LOW}-{ZONE_SUSPEND}] suspend≥{ZONE_SUSPEND}")
    print()

    if not filtered:
        print(f"  No results in zone '{zone_filter or 'all'}'")
    else:
        for r in filtered:
            icon = zone_icons.get(r["zone"], "?")
            status_icon = "👁️" if r["status"] == "observing" else "🟢"
            print(f"  {icon} {status_icon} [{r['id']}] dist={r['distance']:.3f} zone={r['zone']}")
            print(f"      {r['content']}")
            if r["nn_id"]:
                print(f"      → NN: [{r['nn_id']}] {r['nn_content']}")

    # Density trend: average distance by status
    active_dists = [r["distance"] for r in results if r["status"] == "active"]
    observing_dists = [r["distance"] for r in results if r["status"] == "observing"]
    avg_active = sum(active_dists) / len(active_dists) if active_dists else 0
    avg_observing = sum(observing_dists) / len(observing_dists) if observing_dists else 0
    print(f"\n📊 Density trend:")
    print(f"  Active avg distance: {avg_active:.3f} (lower = more clustered)")
    print(f"  Observing avg distance: {avg_observing:.3f}")

    # Apply actions in non-dry-run mode
    if not dry_run:
        applied = 0
        for r in results:
            if r["zone"] == "absorb" and r["nn_id"]:
                # Mark for merge
                for mem in meta["memories"]:
                    if mem.get("id") == r["id"]:
                        # Skip already-processed memories (idempotency)
                        if mem.get("status") not in ("active", "observing"):
                            break
                        if force_absorb:
                            mem["status"] = "archived"
                            mem["merged_into"] = r["nn_id"]
                            mem["archived_at"] = now
                        else:
                            # Default: mark as merge_candidate (reversible)
                            mem["status"] = "merge_candidate"
                            mem["merge_candidate_reason"] = "dedup_absorb"
                            mem["merged_into"] = r["nn_id"]
                            mem["archived_at"] = now
                        applied += 1
                        break
        if applied:
            _save_meta(meta_path, meta)
            action_desc = "archived (absorbed)" if force_absorb else "marked as merge_candidate"
            print(f"\n✅ Applied: {applied} memories {action_desc} (absorbed into nearest)")

    return {"results": results, "zone_counts": zone_counts, "avg_distance": {"active": avg_active, "observing": avg_observing}}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian nearest-neighbor dedup (v0.4)")
    p.add_argument("--workspace", default=None, help="Workspace root path")
    p.add_argument("--meta", default=None, help="Path to meta.json")
    p.add_argument("--threshold", type=float, default=0.75, help="Legacy threshold (kept for compat)")
    p.add_argument("--dry-run", action="store_true", help="Show results without applying")
    p.add_argument("--zone", default=None, choices=["absorb", "derive", "new", "suspend"],
                   help="Filter by zone")
    p.add_argument("--limit", type=int, default=None, help="Max results to show")
    p.add_argument("--force-absorb", action="store_true",
                   help="Directly archive absorbed memories (default: mark as merge_candidate)")
    args = p.parse_args()

    workspace = args.workspace or os.environ.get(
        "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
    )
    meta_path = args.meta or os.path.join(workspace, "memory", "meta.json")
    run(meta_path, args.threshold, args.dry_run, args.zone, args.limit, force_absorb=args.force_absorb)
