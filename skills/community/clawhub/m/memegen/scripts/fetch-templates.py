#!/usr/bin/env python3
"""Fetch meme templates from memegen.link and Imgflip APIs.

Creates reference files for template mappings between the two services.
Zero external dependencies — stdlib only.

Usage:
    python3 fetch-templates.py [--dry-run]

Outputs:
    references/all-templates.json     — full memegen.link template list
    references/imgflip-mapping.json   — Imgflip-to-memegen mapping
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REFS_DIR = REPO_ROOT / "references"

MEMEGEN_API = "https://api.memegen.link/templates"
IMGFLIP_API = "https://api.imgflip.com/get_memes"

REQUEST_TIMEOUT = 15


def fetch_memegen_templates():
    """Fetch all templates from the memegen.link API.

    Returns:
        list: Template dicts as returned by the API.

    Raises:
        SystemExit: On network or parse errors.
    """
    req = urllib.request.Request(MEMEGEN_API, headers={
        "User-Agent": "MemeSkill/1.0 (template-fetcher)",
        "Accept": "application/json",
    })

    try:
        response = urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT)
        data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        print("Error fetching memegen.link: {}".format(exc), file=sys.stderr)
        sys.exit(1)
    except (json.JSONDecodeError, ValueError) as exc:
        print("Error parsing memegen.link response: {}".format(exc), file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print("Unexpected memegen.link response format (expected list)", file=sys.stderr)
        sys.exit(1)

    return data


def fetch_imgflip_memes():
    """Fetch top 100 memes from the Imgflip API.

    Returns:
        list: Meme dicts with id, name, url, width, height, box_count.

    Raises:
        SystemExit: On network, parse, or API errors.
    """
    req = urllib.request.Request(IMGFLIP_API, headers={
        "User-Agent": "MemeSkill/1.0 (template-fetcher)",
        "Accept": "application/json",
    })

    try:
        response = urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT)
        data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        print("Error fetching Imgflip: {}".format(exc), file=sys.stderr)
        sys.exit(1)
    except (json.JSONDecodeError, ValueError) as exc:
        print("Error parsing Imgflip response: {}".format(exc), file=sys.stderr)
        sys.exit(1)

    if not data.get("success"):
        print("Imgflip API returned failure", file=sys.stderr)
        sys.exit(1)

    memes = data.get("data", {}).get("memes", [])
    if not memes:
        print("No memes found in Imgflip response", file=sys.stderr)
        sys.exit(1)

    return memes


def _normalize(name):
    """Normalize a template name for comparison.

    Lowercases, strips non-alphanumeric chars (keeping spaces),
    and collapses whitespace.
    """
    text = name.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _tokenize(name):
    """Split a normalized name into a set of word tokens."""
    return set(_normalize(name).split())


def compute_similarity(name1, name2):
    """Compute a similarity score between two template names.

    Uses a combination of:
      - Exact normalized match (score 1.0)
      - Substring containment (score 0.8)
      - Word-overlap Jaccard coefficient (score 0.0-0.7)

    Args:
        name1: First template name.
        name2: Second template name.

    Returns:
        float: Similarity score between 0.0 and 1.0.
    """
    norm1 = _normalize(name1)
    norm2 = _normalize(name2)

    if norm1 == norm2:
        return 1.0

    if norm1 in norm2 or norm2 in norm1:
        shorter = min(len(norm1), len(norm2))
        longer = max(len(norm1), len(norm2))
        if longer > 0 and shorter > 2:
            return 0.6 + 0.2 * (shorter / longer)

    tokens1 = _tokenize(name1)
    tokens2 = _tokenize(name2)

    if not tokens1 or not tokens2:
        return 0.0

    intersection = tokens1 & tokens2
    union = tokens1 | tokens2

    if not union:
        return 0.0

    jaccard = len(intersection) / len(union)
    return round(min(jaccard * 0.7, 0.7), 4)


def create_mapping(memegen_templates, imgflip_memes):
    """Create a mapping from Imgflip memes to memegen.link templates.

    For each Imgflip meme, finds the best-matching memegen template
    by name similarity. A match is only accepted if the score exceeds
    the threshold.

    Args:
        memegen_templates: List of memegen.link template dicts.
        imgflip_memes: List of Imgflip meme dicts.

    Returns:
        dict: Mapping result with 'mappings', 'unmapped_imgflip', and 'stats'.
    """
    match_threshold = 0.3

    memegen_lookup = []
    for tpl in memegen_templates:
        tpl_id = tpl.get("id", "")
        tpl_name = tpl.get("name", "")
        memegen_lookup.append({
            "id": tpl_id,
            "name": tpl_name,
        })

    mappings = []
    unmapped = []

    for meme in imgflip_memes:
        imgflip_id = str(meme.get("id", ""))
        imgflip_name = meme.get("name", "")

        best_score = 0.0
        best_match = None

        for entry in memegen_lookup:
            score = compute_similarity(imgflip_name, entry["name"])

            # Also check against the memegen ID as a name
            id_score = compute_similarity(
                _normalize(imgflip_name),
                entry["id"].replace("-", " ").replace("_", " "),
            )
            score = max(score, id_score)

            if score > best_score:
                best_score = score
                best_match = entry

        if best_score >= match_threshold and best_match is not None:
            mappings.append({
                "imgflip_id": imgflip_id,
                "imgflip_name": imgflip_name,
                "memegen_id": best_match["id"],
                "memegen_name": best_match["name"],
                "match_score": round(best_score, 2),
            })
        else:
            unmapped.append({
                "imgflip_id": imgflip_id,
                "imgflip_name": imgflip_name,
            })

    return {
        "mappings": sorted(mappings, key=lambda m: m["match_score"], reverse=True),
        "unmapped_imgflip": sorted(unmapped, key=lambda m: m["imgflip_name"]),
        "stats": {
            "total_memegen": len(memegen_templates),
            "total_imgflip": len(imgflip_memes),
            "mapped": len(mappings),
            "unmapped": len(unmapped),
        },
    }


def _detect_new_templates(templates):
    """Compare fetched templates against the previous all-templates.json.

    Returns:
        tuple: (new_count, is_first_run) where new_count is the number of
               templates not present in the previous file, and is_first_run
               is True if no previous file was found.
    """
    previous_path = REFS_DIR / "all-templates.json"
    if not previous_path.exists():
        return 0, True

    try:
        with open(str(previous_path), "r") as fh:
            previous = json.load(fh)
    except (json.JSONDecodeError, IOError):
        return 0, True

    if not isinstance(previous, list):
        return 0, True

    previous_ids = set()
    for tpl in previous:
        tid = tpl.get("id", "")
        if tid:
            previous_ids.add(tid)

    current_ids = set()
    for tpl in templates:
        tid = tpl.get("id", "")
        if tid:
            current_ids.add(tid)

    new_ids = current_ids - previous_ids
    return len(new_ids), False


def _write_json(path, data):
    """Write data as formatted JSON to the given path."""
    parent = path.parent
    if not parent.exists():
        os.makedirs(str(parent), exist_ok=True)

    with open(str(path), "w") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def main():
    """Fetch templates, create mappings, and write reference files."""
    dry_run = "--dry-run" in sys.argv

    print("Fetching memegen.link templates...")
    memegen_templates = fetch_memegen_templates()
    print("  Found {} templates".format(len(memegen_templates)))

    new_count, is_first_run = _detect_new_templates(memegen_templates)

    print("Fetching Imgflip memes...")
    imgflip_memes = fetch_imgflip_memes()
    print("  Found {} memes".format(len(imgflip_memes)))

    print("Creating mapping...")
    mapping = create_mapping(memegen_templates, imgflip_memes)

    if dry_run:
        print("\n[DRY RUN] Skipping file writes.")
    else:
        templates_path = REFS_DIR / "all-templates.json"
        _write_json(templates_path, memegen_templates)
        print("  Wrote {}".format(templates_path))

        mapping_path = REFS_DIR / "imgflip-mapping.json"
        _write_json(mapping_path, mapping)
        print("  Wrote {}".format(mapping_path))

    stats = mapping["stats"]
    new_label = "first run" if is_first_run else "{} new".format(new_count)

    print("")
    print("=== Template Fetch Report ===")
    print("memegen.link: {} templates".format(stats["total_memegen"]))
    print("Imgflip: {} memes".format(stats["total_imgflip"]))
    print("Mapped: {} (imgflip -> memegen)".format(stats["mapped"]))
    print("Unmapped: {} (imgflip only)".format(stats["unmapped"]))
    print("New since last run: {}".format(new_label))

    if dry_run:
        print("\n[DRY RUN] No files were modified.")


if __name__ == "__main__":
    main()
