#!/usr/bin/env python3

"""

Export search results to BibTeX / RIS for Zotero, EndNote, JabRef, etc.



Usage:

    # 标准模式（merged/ranked JSON）

    python export_citations.py --bibtex --files merged.json  -o output.bib



    # 主题模式（themed.json — 自动注入 tier + theme + 英文摘要）

    python export_citations.py --bibtex --themed memory/themed.json -o results.bib



Design:

    - Zero external dependencies (no browser, no login, no network)

    - Handles missing/incomplete metadata gracefully

    - Citation keys auto-generated from first author + year + title

    - Unicode-safe: authors/venues with Chinese characters handled correctly

    - 🆕 --themed mode: reads abstracts from _abstract_file (file I/O only, no context pollution)

"""



import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse

import json

import os

import re

import sys

from pathlib import Path

from collections import OrderedDict



from utils.pipeline_schema import validate, report, check_version



import sys, os




# Fix Windows console encoding

if sys.platform == "win32":

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")





# ═══════════════════════════════════════════════════════════════════

# Tier computation (shared logic with make_output.py)

# ═══════════════════════════════════════════════════════════════════



def composite_score(paper: dict, weights=(0.4, 0.3, 0.3)) -> float:

    ai = paper.get("_ai_scores", {})

    r = ai.get("relevance", 0)

    q = ai.get("quality", 0)

    n = ai.get("novelty", 0)

    return r * weights[0] + q * weights[1] + n * weights[2]





def assign_tiers(papers: list, mode: str = "percentile") -> None:

    """原地给论文添加 _tier 字段。"""

    scored = [(composite_score(p), p) for p in papers]

    scored.sort(key=lambda x: x[0], reverse=True)

    n = len(scored)



    if mode == "threshold":

        for score, p in scored:

            if score >= 75:

                p["_tier"] = "core"

            elif score >= 60:

                p["_tier"] = "solid"

            else:

                p["_tier"] = "frontier"

    elif mode == "equal":

        chunk = max(1, n // 3)

        for idx, (score, p) in enumerate(scored):

            if idx < chunk:

                p["_tier"] = "core"

            elif idx < chunk * 2:

                p["_tier"] = "solid"

            else:

                p["_tier"] = "frontier"

    else:  # percentile

        top_n = max(1, int(n * 0.3))

        mid_n = max(1, int(n * 0.4))

        for idx, (score, p) in enumerate(scored):

            if idx < top_n:

                p["_tier"] = "core"

            elif idx < top_n + mid_n:

                p["_tier"] = "solid"

            else:

                p["_tier"] = "frontier"





TIER_EMOJI = {"core": "\U0001f7e2", "solid": "\U0001f7e1", "frontier": "\U0001f7e0"}

TIER_LABEL = {"core": "Core", "solid": "Solid", "frontier": "Frontier"}





def tier_keywords(p: dict) -> str:

    """生成 tier + theme 关键词: '🟢 Core, End-to-End Autonomous Discovery'"""

    parts = []

    tier = p.get("_tier", "")

    if tier:

        emoji = TIER_EMOJI.get(tier, "")

        label = TIER_LABEL.get(tier, tier)

        parts.append(f"{emoji} {label}")

    theme = p.get("_theme", "")

    if theme:

        parts.append(theme)

    return ", ".join(parts)





# ═══════════════════════════════════════════════════════════════════

# Abstract reader (file I/O only — NEVER prints or passes to context)

# ═══════════════════════════════════════════════════════════════════



def read_abstract(paper: dict) -> str:

    """Read English abstract from _abstract_file. Zero context pollution."""

    af = paper.get("_abstract_file", "")

    if af and os.path.exists(af):

        try:

            with open(af, "r", encoding="utf-8") as f:

                content = f.read()

            idx = content.find("\nAbstract:\n")

            if idx >= 0:

                text = content[idx + len("\nAbstract:\n"):].strip()

                # Filter out the Chinese summary marker if present

                cn_idx = text.find("【中文摘要】")

                if cn_idx >= 0:

                    text = text[:cn_idx].strip()

                return text

        except (IOError, UnicodeDecodeError):

            pass

    # Fallback: inline abstract (old format)

    inline = paper.get("abstract", "")

    if inline and len(inline) > 50:

        return inline.strip()

    return ""





# -- Metadata cleaning -----------------------------------------------------



def safe_str(value, default=""):

    if value is None:

        return default

    return str(value).strip()





def normalize_authors(authors_str):

    if not authors_str or not authors_str.strip():

        return ""



    authors = [a.strip() for a in authors_str.split(";") if a.strip()]

    if not authors:

        return ""



    def has_cjk(s):

        return any("\u4e00" <= c <= "\u9fff" or "\u3040" <= c <= "\u30ff" for c in s)



    result = []

    for author in authors:

        author = re.sub(r"\s+", " ", author).strip()

        if not author:

            continue

        if has_cjk(author):

            result.append(author)

        elif "," in author:

            result.append(author)

        else:

            parts = author.split()

            if len(parts) == 1:

                result.append(parts[0])

            elif len(parts) == 2:

                result.append(f"{parts[1]}, {parts[0]}")

            else:

                result.append(f"{parts[-1]}, {' '.join(parts[:-1])}")



    return " and ".join(result)





def generate_citation_key(authors_str, year, title):

    author_part = "unknown"

    if authors_str and authors_str.strip():

        first_author = authors_str.split(" and ")[0].strip()

        if "," in first_author:

            author_part = first_author.split(",")[0].strip().lower()

        else:

            author_part = first_author.lower()

    author_part = re.sub(r"[^\w]", "", author_part, flags=re.UNICODE).lower()

    if not author_part:

        author_part = "unknown"



    year_part = str(year) if year else "????"

    year_part = re.sub(r"[^0-9]", "", year_part)

    if not year_part:

        year_part = "????"



    title_part = "paper"

    if title and title.strip():

        stop_words = {"a", "an", "the", "on", "in", "of", "for", "to", "and",

                      "or", "is", "are", "was", "be", "with", "from", "by",

                      "using", "via", "its", "not", "but", "new", "two",

                      "one", "based", "can", "has", "had", "been", "this",

                      "that", "these", "those", "into", "over", "under"}

        words = re.findall(r"[a-zA-Z0-9]+", title.lower())

        for w in words:

            if w not in stop_words and len(w) > 1:

                title_part = w

                break



    key = f"{author_part}{year_part}{title_part}"

    return re.sub(r"[^a-zA-Z0-9]", "", key)





def map_paper_type(paper_type):

    if not paper_type:

        return "article"

    t = paper_type.lower().strip()

    if "conference" in t or "proceeding" in t:

        return "inproceedings"

    if "review" in t:

        return "article"

    if "book" in t:

        return "book"

    if "chapter" in t:

        return "incollection"

    if "thesis" in t or "dissertation" in t:

        return "phdthesis"

    if "patent" in t:

        return "patent"

    return "article"





def map_ris_type(paper_type):

    if not paper_type:

        return "JOUR"

    t = paper_type.lower().strip()

    if "conference" in t or "proceeding" in t:

        return "CONF"

    if "book" in t:

        return "BOOK"

    if "chapter" in t:

        return "CHAP"

    if "thesis" in t or "dissertation" in t:

        return "THES"

    if "patent" in t:

        return "PAT"

    return "JOUR"





def escape_bibtex(value):

    value = value.replace("\\", r"\\")

    value = value.replace("{", r"\{")

    value = value.replace("}", r"\}")

    value = value.replace("$", r"\$")

    value = value.replace("%", r"\%")

    value = value.replace("&", r"\&")

    value = value.replace("#", r"\#")

    value = value.replace("_", r"\_")

    value = value.replace("~", r"\\textasciitilde{}")

    value = value.replace("^", r"\\textasciicircum{}")

    return value





def wrap_long_field(text: str, indent: int = 12) -> str:

    """Wrap long text (like abstracts) into BibTeX-safe lines ~80 chars."""

    text = escape_bibtex(text)

    if len(text) <= 70 - indent:

        return text

    # Break into ~65 char chunks for readability

    chunks = []

    for i in range(0, len(text), 65):

        chunks.append(text[i:i+65])

    return "\n" + " " * indent + "\n" + " " * indent + ("\n" + " " * indent).join(chunks)





# -- Exporters -------------------------------------------------------------



def export_bibtex(papers: list, themed: bool = False) -> str:

    entries = []

    used_keys = set()



    for paper in papers:

        title = safe_str(paper.get("title"))

        authors = normalize_authors(safe_str(paper.get("authors")))

        year = safe_str(paper.get("year"), "????")

        venue = safe_str(paper.get("venue"))

        doi = safe_str(paper.get("doi"))

        link = safe_str(paper.get("link"))

        paper_type = safe_str(paper.get("type"))

        volume = safe_str(paper.get("volume"))

        number = safe_str(paper.get("number"))

        pages = safe_str(paper.get("pages"))

        publisher = safe_str(paper.get("publisher"))



        bib_type = map_paper_type(paper_type)

        cite_key = generate_citation_key(authors, year, title)



        # Ensure unique key

        base_key = cite_key

        counter = 0

        while cite_key in used_keys:

            counter += 1

            cite_key = f"{base_key}{chr(96 + counter)}"  # a, b, c...

        used_keys.add(cite_key)



        lines = [f"@{bib_type}{{{cite_key},"]



        if title:

            lines.append(f"  title     = {{{escape_bibtex(title)}}},")



        if authors:

            lines.append(f"  author    = {{{escape_bibtex(authors)}}},")

        else:

            lines.append(f"  author    = {{[Unknown]}},")



        if venue:

            if bib_type == "inproceedings":

                lines.append(f"  booktitle = {{{escape_bibtex(venue)}}},")

            elif bib_type == "article":

                lines.append(f"  journal   = {{{escape_bibtex(venue)}}},")

            else:

                lines.append(f"  journal   = {{{escape_bibtex(venue)}}},")



        if year and year != "????":

            lines.append(f"  year      = {{{year}}},")



        if doi:

            lines.append(f"  doi       = {{{escape_bibtex(doi)}}},")



        if link:

            lines.append(f"  url       = {{{escape_bibtex(link)}}},")



        if volume:

            lines.append(f"  volume    = {{{volume}}},")



        if number:

            lines.append(f"  number    = {{{number}}},")



        if pages:

            lines.append(f"  pages     = {{{pages}}},")



        if publisher:

            lines.append(f"  publisher = {{{escape_bibtex(publisher)}}},")



        # ── 🆕 Themed mode extras ──

        if themed:

            # Keywords: tier + theme

            kw = tier_keywords(paper)

            if kw:

                lines.append(f"  keywords  = {{{escape_bibtex(kw)}}},")



            # Abstract: original English from file

            abstract = read_abstract(paper)

            if abstract:

                wrapped = wrap_long_field(abstract)

                lines.append(f"  abstract  = {{{wrapped}}},")



        # Note: source info only (AI scores intentionally excluded per USER.md)

        source_db = paper.get("_source_db", [])

        if isinstance(source_db, list):

            source_db = ", ".join(source_db)

        note_parts = []

        citations = safe_str(paper.get("citations"))

        if citations:

            note_parts.append(f"cited: {citations}")

        if source_db:

            note_parts.append(f"from: {source_db}")

        if note_parts:

            lines.append(f"  note      = {{{' | '.join(note_parts)}}},")



        # Close entry

        lines[-1] = lines[-1].rstrip(",")

        lines.append("}")

        lines.append("")



        entries.extend(lines)



    return "\n".join(entries)





def export_ris(papers: list, themed: bool = False) -> str:

    entries = []



    for paper in papers:

        title = safe_str(paper.get("title"))

        authors_raw = safe_str(paper.get("authors"))

        year = safe_str(paper.get("year"), "")

        venue = safe_str(paper.get("venue"))

        doi = safe_str(paper.get("doi"))

        link = safe_str(paper.get("link"))

        paper_type = safe_str(paper.get("type"))

        volume = safe_str(paper.get("volume"))

        number = safe_str(paper.get("number"))

        pages = safe_str(paper.get("pages"))

        publisher = safe_str(paper.get("publisher"))

        citations = safe_str(paper.get("citations"))



        ris_type = map_ris_type(paper_type)



        lines = [f"TY  - {ris_type}"]



        if title:

            lines.append(f"TI  - {title}")



        if authors_raw:

            for author in [a.strip() for a in authors_raw.split(";") if a.strip()]:

                author = re.sub(r"\s+", " ", author).strip()

                if author:

                    lines.append(f"AU  - {author}")



        if venue:

            if ris_type == "CONF":

                lines.append(f"T2  - {venue}")

            else:

                lines.append(f"JO  - {venue}")

            lines.append(f"JF  - {venue}")



        if year:

            lines.append(f"PY  - {year}")



        if volume:

            lines.append(f"VL  - {volume}")



        if number:

            lines.append(f"IS  - {number}")



        if pages:

            lines.append(f"SP  - {pages}")



        if publisher:

            lines.append(f"PB  - {publisher}")



        if doi:

            lines.append(f"DO  - {doi}")



        if link:

            lines.append(f"UR  - {link}")



        # Notes with tier/theme/abstract (AI scores intentionally excluded)

        notes = []

        if themed:

            kw = tier_keywords(paper)

            if kw:

                notes.append(kw)

            abstract = read_abstract(paper)

            if abstract:

                notes.append(f"Abstract: {abstract[:500]}")



        citations = safe_str(paper.get("citations"))

        if citations:

            notes.append(f"Citations: {citations}")

        source_db = paper.get("_source_db", [])

        if isinstance(source_db, list):

            source_db = ", ".join(source_db)

        if source_db:

            notes.append(f"Source: {source_db}")

        if notes:

            lines.append(f"N1  - {' | '.join(notes)}")



        if themed:

            kw = tier_keywords(paper)

            if kw:

                lines.append(f"KW  - {kw}")



        lines.append("ER  - ")

        lines.append("")



        entries.extend(lines)



    return "\n".join(entries)





# -- Main ----------------------------------------------------------------



def main():

    parser = argparse.ArgumentParser(description="Export citations to BibTeX / RIS")

    parser.add_argument("--bibtex", action="store_true", help="BibTeX format")

    parser.add_argument("--ris", action="store_true", help="RIS format")

    parser.add_argument("--both", action="store_true", help="Both formats")

    parser.add_argument("--themed", help="Themed JSON input (auto tier + theme + abstract)")

    parser.add_argument("--tier-mode", choices=["percentile", "equal", "threshold"],

                        default="percentile", help="Tier assignment mode")

    parser.add_argument("--files", nargs="+", help="Standard JSON input files")

    parser.add_argument("-o", "--output", help="Output file path")

    args = parser.parse_args()



    do_bibtex = args.bibtex or args.both or (not args.bibtex and not args.ris and not args.both)

    do_ris = args.ris or args.both



    # Load papers

    papers = []

    themed_mode = False



    if args.themed:

        themed_mode = True

        with open(args.themed, "r", encoding="utf-8") as f:

            data = json.load(f)

        papers = data.get("papers", data if isinstance(data, list) else [])



        # --- 入口校验 ---

        ver_issues = check_version(data, stage="themed")

        if ver_issues:

            report(ver_issues, stage="export_citations")

        ok, issues = validate(papers, stage="themed")

        if issues:

            report(issues, stage="export_citations")



        # Compute tiers

        assign_tiers(papers, mode=args.tier_mode)



        # Summary

        tier_counts = {}

        for p in papers:

            t = p.get("_tier", "?")

            tier_counts[t] = tier_counts.get(t, 0) + 1

        tier_summary = " | ".join(

            f"{TIER_EMOJI.get(k, '')} {k}: {v}" for k, v in tier_counts.items()

        )

        with_abs = sum(1 for p in papers if read_abstract(p))

        print(f"[Export] {len(papers)} papers, themed mode | {tier_summary} | {with_abs} with abstracts")



    elif args.files:

        for fpath in args.files:

            try:

                with open(fpath, "r", encoding="utf-8") as f:

                    data = json.load(f)

            except (FileNotFoundError, json.JSONDecodeError) as e:

                print(f"Warning: {fpath}: {e}", file=sys.stderr)

                continue

            if isinstance(data, dict):

                papers.extend(data.get("papers", []))

            elif isinstance(data, list):

                papers.extend(data)

    else:

        raw = sys.stdin.read().strip()

        if raw:

            try:

                data = json.loads(raw)

                papers = data.get("papers", []) if isinstance(data, dict) else data

            except json.JSONDecodeError as e:

                print(f"Error: JSON parse failed: {e}", file=sys.stderr)

                sys.exit(1)



    if not papers:

        print("No papers to export.", file=sys.stderr)

        sys.exit(1)



    # Export BibTeX

    if do_bibtex:

        bibtex_output = export_bibtex(papers, themed=themed_mode)

        if args.output:

            out_path = Path(args.output)

            if out_path.suffix != ".bib":

                out_path = out_path.with_suffix(".bib")

            out_path.parent.mkdir(parents=True, exist_ok=True)

            out_path.write_text(bibtex_output + "\n", encoding="utf-8")

            print(f"BibTeX: {len(papers)} entries -> {out_path}")

        else:

            print(bibtex_output)



    # Export RIS

    if do_ris:

        ris_output = export_ris(papers, themed=themed_mode)

        if args.output:

            out_path = Path(args.output)

            if args.both:

                out_path = out_path.with_suffix(".ris")

            elif out_path.suffix != ".ris":

                out_path = out_path.with_suffix(".ris")

            out_path.parent.mkdir(parents=True, exist_ok=True)

            out_path.write_text(ris_output + "\n", encoding="utf-8")

            print(f"RIS: {len(papers)} entries -> {out_path}")

        else:

            if do_bibtex:

                print("\n" + "=" * 60 + "\nRIS\n" + "=" * 60 + "\n")

            print(ris_output)





if __name__ == "__main__":

    main()

