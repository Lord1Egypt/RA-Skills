#!/usr/bin/env python3

"""

Cross-database result merger: deduplication only.



Scoring is now handled exclusively by paper_ranker.py.

This script only does: load → deduplicate → write.



Usage:

    python scripts/merge_results.py --files ieee.json scopus.json -o merged.json

    python scripts/merge_results.py --files ieee.json -o merged.json    # single DB (N=1)

    echo '<papers_json>' | python scripts/merge_results.py -o merged.json   # stdin JSON



Input format (per database):

    {

      "database": "ieee",        # or scopus / engineering_village / acm / wos

      "totalResults": "59",

      "papers": [

        {

          "title": "...",

          "authors": "Author1; Author2",

          "year": "2024",

          "venue": "IEEE Trans. on ...",

          "type": "Conference Paper",

          "link": "https://...",

          "doi": "10.1109/...",

          "abstract": "...",

          "citations": 42

        }

      ]

    }



Deduplication strategy:

    1. Exact DOI match (case-insensitive, normalize prefix/suffix)

    2. Fuzzy title match: >= 80% token overlap after normalization

    3. For merged papers, keep richest metadata (longest abstract, most fields)

"""



import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse

import json

import re

import sys

from pathlib import Path



from utils.doi_utils import normalize as normalize_doi

from utils.pipeline_schema import validate, report, stamp, check_version, PIPELINE_VERSION



import sys, os




# Fix Windows console encoding

if sys.platform == "win32":

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")





# -- Title normalization ----------------------------------------------------



def normalize_title(title):

    """Normalize title for fuzzy comparison."""

    if not title:

        return ""

    t = title.lower()

    t = re.sub(r'[^\w\s]', ' ', t)  # remove punctuation -> spaces

    t = re.sub(r'\s+', ' ', t).strip()

    return t



def title_similarity(t1, t2):

    """Token overlap ratio between two normalized titles."""

    tokens1 = set(normalize_title(t1).split())

    tokens2 = set(normalize_title(t2).split())

    if not tokens1 or not tokens2:

        return 0.0

    overlap = tokens1 & tokens2

    return len(overlap) / min(len(tokens1), len(tokens2))





# -- Merging ---------------------------------------------------------------



def merge_duplicates(papers_a, papers_b):

    """

    When two papers are duplicates, merge metadata: keep the richer record.

    """

    # Start with b as base (second DB usually has more metadata)

    merged = dict(papers_b)



    # For each field, keep the longer/more complete version

    for field in ["abstract", "title", "authors", "venue", "type"]:

        val_a = papers_a.get(field, "")

        val_b = papers_b.get(field, "")

        if len(val_a) > len(val_b):

            merged[field] = val_a



    # Keep the non-null DOI

    if not merged.get("doi") and papers_a.get("doi"):

        merged["doi"] = papers_a["doi"]



    # Take max citations (conservatively - the DB seeing it might be broader)

    try:

        c_a = int(papers_a.get("citations") or 0)

        c_b = int(papers_b.get("citations") or 0)

        merged["citations"] = max(c_a, c_b)

    except (ValueError, TypeError):

        merged["citations"] = papers_a.get("citations") or papers_b.get("citations") or 0



    # Track source databases

    sources = set()

    for paper in [papers_a, papers_b]:

        src = paper.get("_source_db", [])

        if isinstance(src, list):

            sources.update(src)

        else:

            sources.add(src)

    merged["_source_db"] = sorted(sources)



    return merged





def merge_all(all_papers_by_db):

    """

    Merge papers from multiple databases, deduplicating by DOI + title.



    Input: list of {database: "ieee", papers: [...]}

    Returns: list of merged paper dicts (unsorted — scoring is done by paper_ranker.py).

    """

    # Flatten with source DB tags

    all_papers = []

    for db_result in all_papers_by_db:

        db_name = db_result.get("database", "unknown")

        for paper in db_result.get("papers", []):

            paper["_source_db"] = [db_name]

            all_papers.append(paper)



    # Phase 1: Exact DOI dedup

    doi_index = {}

    unmatched = []

    for paper in all_papers:

        doi = normalize_doi(paper.get("doi"))

        if doi and doi in doi_index:

            doi_index[doi] = merge_duplicates(doi_index[doi], paper)

        elif doi:

            doi_index[doi] = paper

        else:

            unmatched.append(paper)



    merged = list(doi_index.values())



    # Phase 2: Fuzzy title dedup for papers without DOI

    # Use greedy matching: for each unmatched paper, find best match in merged

    threshold = 0.80

    for paper in unmatched:

        best_match = None

        best_score = 0.0

        for candidate in merged:

            sim = title_similarity(paper.get("title", ""), candidate.get("title", ""))

            if sim > best_score:

                best_score = sim

                best_match = candidate



        if best_score >= threshold and best_match:

            # Merge into existing

            idx = merged.index(best_match)

            merged[idx] = merge_duplicates(best_match, paper)

        else:

            merged.append(paper)



    # Phase 3: Cross-check among merged for any remaining fuzzy matches

    # (two separate DOI entries might be the same paper with different DOIs)

    final = []

    while merged:

        paper = merged.pop(0)

        found = False

        for i, candidate in enumerate(final):

            sim = title_similarity(paper.get("title", ""), candidate.get("title", ""))

            if sim >= threshold:

                final[i] = merge_duplicates(candidate, paper)

                found = True

                break

        if not found:

            final.append(paper)



    return final





# -- Main ----------------------------------------------------------------



def main():

    parser = argparse.ArgumentParser(

        description="Merge & deduplicate papers from multiple databases"

    )

    parser.add_argument(

        "--files", nargs="+",

        help="JSON files to merge (one per database)"

    )

    parser.add_argument(

        "--output", "-o", required=True,

        help="Output file (required — prevents paper data entering AI context)"

    )

    args = parser.parse_args()



    # Load papers

    all_by_db = []



    if args.files:

        for fpath in args.files:

            try:

                with open(fpath, "r", encoding="utf-8") as f:

                    data = json.load(f)

                if isinstance(data, list):

                    # list of paper dicts (single DB)

                    all_by_db.append({"database": Path(fpath).stem, "papers": data})

                elif isinstance(data, dict):

                    # full DB result

                    all_by_db.append(data)

            except Exception as e:

                print(f"Warning: failed to read {fpath}: {e}", file=sys.stderr)

    else:

        # Read from stdin

        raw = sys.stdin.read().strip()

        if raw:

            try:

                data = json.loads(raw)

                if isinstance(data, list):

                    # List of DB results, e.g. [{"database": "ieee", "papers": [...]}, ...]

                    if data and isinstance(data[0], dict) and "papers" in data[0]:

                        all_by_db = data

                    else:

                        # Single DB's paper list

                        all_by_db = [{"database": "stdin", "papers": data}]

                elif isinstance(data, dict) and "papers" in data:

                    all_by_db = [data]

                else:

                    all_by_db = [{"database": "stdin", "papers": data}]

            except json.JSONDecodeError as e:

                print(f"Error: invalid JSON from stdin: {e}", file=sys.stderr)

                sys.exit(1)



    if not all_by_db:

        print("No input provided. Use --files or pipe JSON to stdin.", file=sys.stderr)

        sys.exit(1)



    # Merge & deduplicate

    merged = merge_all(all_by_db)



    # 🔧 类型归一化：跨库统一 paper type 标签

    TYPE_MAP = {

        # → Journal Article

        "research-article": "Journal Article", "journal article": "Journal Article",

        "journal_article": "Journal Article", "journals": "Journal Article",

        "article": "Journal Article", "journal": "Journal Article",

        "early access": "Journal Article",

        # → Conference Paper

        "conference paper": "Conference Paper", "conferencepaper": "Conference Paper",

        "conference_article": "Conference Paper", "conference article": "Conference Paper",

        "conference": "Conference Paper", "proceedings": "Conference Paper",

        "proceeding": "Conference Paper", "inproceedings": "Conference Paper",

        "poster": "Conference Paper", "abstract": "Conference Paper",

        "panel": "Conference Paper", "invited-talk": "Conference Paper",

        # → Review

        "review": "Review", "review-article": "Review", "review_article": "Review",

        "surveys": "Review",

        # → Short Paper

        "short paper": "Short Paper", "short-paper": "Short Paper", "shortpaper": "Short Paper",

        # → Preprint

        "preprint": "Preprint",

        # → Book Chapter

        "book chapter": "Book Chapter", "book-chapter": "Book Chapter", "bookchapter": "Book Chapter",

        # → Magazine Article

        "magazine": "Magazine Article", "magazine article": "Magazine Article",

    }

    for paper in merged:

        raw_type = (paper.get("type") or "").strip().lower()

        if raw_type in TYPE_MAP:

            paper["type"] = TYPE_MAP[raw_type]

        elif raw_type and raw_type != "unknown" and len(raw_type) < 30:

            # Already a clean type (e.g. "Journal Article" from IEEE), keep as-is

            paper["type"] = raw_type.title().replace("_", " ")



    # --- 校验 + 报告 ---

    ok, issues = validate(merged, stage="merged")

    if issues:

        report(issues, stage="merged")



    # Output

    output = {

        "total": len(merged),

        "databases": list(set(

            db.get("database", "unknown")

            for db in all_by_db

        )),

        "deduplicated_from": sum(len(db.get("papers", [])) for db in all_by_db),

        "papers": merged,

    }

    stamp(output, stage="merged")



    json_str = json.dumps(output, ensure_ascii=False, indent=2)



    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:

        f.write(json_str + "\n")

    print(f"[Merge] {len(merged)} papers merged (from {len(all_by_db)} databases) → {args.output}")





if __name__ == "__main__":

    main()

