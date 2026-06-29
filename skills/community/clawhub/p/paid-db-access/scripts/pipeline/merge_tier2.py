#!/usr/bin/env python3

"""

merge_tier2.py — Tier 2 子代理结果合并回 enriched.json

======================================================



读取 tier2_result.json（子代理输出），将提取的摘要写入 paper-abstracts/，

并更新 enriched.json 中的 _abstract_file 引用。



用法：

  python scripts/merge_tier2.py -r memory/tier2_result.json -e memory/enriched.json -o memory/enriched.json

"""



import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse, json

from pathlib import Path

from utils.doi_utils import (
    normalize as _norm_doi,

    extract as _extract_doi,

    to_filename as _doi_to_filename,

    title_hash as _title_hash,

    doc_id_filename as _doc_id_filename,

    extract_doc_id as _extract_doc_id,

    title_similarity,

)





def main():

    parser = argparse.ArgumentParser(description="Merge Tier 2 sub-agent results into enriched.json")

    parser.add_argument("-r", "--result", required=True, help="tier2_result.json from sub-agent")

    parser.add_argument("-e", "--enriched", required=True, help="Current enriched.json")

    parser.add_argument("-o", "--output", required=True, help="Output enriched.json")

    parser.add_argument("--abstracts-dir", default="memory/paper-abstracts")

    args = parser.parse_args()



    # Load tier2 results

    with open(args.result, "r", encoding="utf-8") as f:

        tier2_results = json.load(f)



    # Load enriched

    with open(args.enriched, "r", encoding="utf-8") as f:

        data = json.load(f)

    papers = data.get("papers", data)



    os.makedirs(args.abstracts_dir, exist_ok=True)



    written = 0

    failed = 0

    matched = 0



    for result in tier2_results:

        status = result.get("status", "failed")

        doi = result.get("doi", "")

        title = result.get("title", "")

        doc_id = result.get("docId", "")

        abstract = (result.get("abstract") or "").strip()



        if status != "ok" or not abstract or len(abstract) < 80:

            failed += 1

            print(f"  SKIP: {title[:60]}... ({result.get('reason', 'no reason')})")

            continue



        # Find matching paper — docId → DOI → title

        found = None

        norm_doi = _norm_doi(doi)



        for p in papers:

            # Match by docId (IEEE)

            if doc_id:

                p_doc_id = _extract_doc_id(p)

                if p_doc_id and p_doc_id == doc_id:

                    found = p

                    break



            # Match by DOI

            if norm_doi and not found:

                p_doi = _extract_doi(p)

                if p_doi and _norm_doi(p_doi) == norm_doi:

                    found = p

                    break



        # Fallback: title similarity

        if not found and title:

            best_score = 0.0

            for p in papers:

                p_title = p.get("title", "")

                score = title_similarity(title, p_title)

                if score > best_score and score >= 0.75:

                    best_score = score

                    found = p

            if found:

                print(f"  [title-match {best_score:.0%}] ", end="")



        if not found:

            print(f"  NO MATCH: {title[:60]}...")

            failed += 1

            continue



        # Write abstract file — docId > DOI > title_hash

        if doc_id:

            sources = found.get("_source_db", [])

            if not isinstance(sources, list):

                sources = [sources] if sources else []

            db = "ieee" if "ieee" in sources else "unknown"

            filename = _doc_id_filename(doc_id, db)

        elif doi:

            filename = _doi_to_filename(norm_doi)

        else:

            filename = _title_hash(title)



        filepath = os.path.join(args.abstracts_dir, filename)



        content = (

            f"Title: {found.get('title', title)}\n"

            f"Authors: {found.get('authors', result.get('authors', ''))}\n"

            f"Year: {found.get('year', result.get('year', ''))}\n"

            f"Venue: {found.get('venue', result.get('venue', ''))}\n"

            f"DOI: {doi or found.get('doi', '')}\n"

            f"Citations: {found.get('citations', result.get('citations', ''))}\n"

            f"\nAbstract:\n{abstract}"

        )



        with open(filepath, "w", encoding="utf-8") as f:

            f.write(content)



        # Update paper — write DOI back to JSON, clear inline abstract

        found["_abstract_file"] = filepath.replace("\\", "/")

        if doi and not found.get("doi"):

            found["doi"] = doi   # Tier 2 提取的 DOI 回填

        found.pop("_needs_tier2", None)

        found.pop("_tier2_reason", None)

        found["abstract"] = ""  # inline → file ref



        written += 1

        matched += 1

        print(f"  OK: {title[:60]}... → {filename}")



    # Save enriched

    out_path = Path(args.output)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:

        json.dump(data, f, ensure_ascii=False, indent=2)



    print(f"\n[MergeTier2] {written} written, {failed} failed/skipped, "

          f"{matched} matched → {args.output}")





if __name__ == "__main__":

    main()

