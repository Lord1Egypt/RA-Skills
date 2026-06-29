#!/usr/bin/env python3
import argparse
import csv
import html
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
QUALITY_FILE_NAMES = {
    "journals": "journal_scores.json",
    "ccf": "ccf_conferences.json",
    "ei": "eiiRankingName.json",
    "chinese": "chinese_journal_tags.json",
}


def normalize(value):
    value = html.unescape(str(value or "")).lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json_optional(path):
    path = Path(path)
    if not path.exists():
        return {}
    return load_json(path)


def normalized_mapping(data):
    if not isinstance(data, dict):
        return {}
    return {normalize(k): v for k, v in data.items() if normalize(k)}


def load_quality_data(data_dir):
    data_dir = Path(data_dir)
    loaded = {
        key: load_json_optional(data_dir / file_name)
        for key, file_name in QUALITY_FILE_NAMES.items()
    }
    missing = [
        file_name
        for key, file_name in QUALITY_FILE_NAMES.items()
        if not loaded.get(key)
    ]
    if missing:
        print(
            f"warning: missing or empty quality data in {data_dir}: {', '.join(missing)}",
            file=sys.stderr,
        )

    return {
        "journals": normalized_mapping(loaded["journals"]),
        "ccf": normalized_mapping(loaded["ccf"]),
        "ei": normalized_mapping(loaded["ei"]),
        "chinese": normalized_mapping(loaded["chinese"]),
    }


def read_candidates(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        data = load_json(path)
        if isinstance(data, dict):
            for key in ("papers", "results", "items"):
                if isinstance(data.get(key), list):
                    return data[key]
        if isinstance(data, list):
            return data
        raise ValueError("JSON input must be a list or contain papers/results/items list")

    if path.suffix.lower() == ".csv":
        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    raise ValueError("Input must be .json or .csv")


def first_value(item, *keys):
    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return value
    return ""


def contains_match(norm_venue, mapping):
    if not norm_venue:
        return None, None
    if norm_venue in mapping:
        return norm_venue, mapping[norm_venue]
    return None, None


def has_cjk(value):
    return bool(re.search(r"[\u4e00-\u9fff]", str(value or "")))


def contains_cjk_match(norm_venue, mapping):
    if not norm_venue or not has_cjk(norm_venue):
        return None, None
    for key in sorted(mapping, key=len, reverse=True):
        if not has_cjk(key) or len(key) < 4:
            continue
        if key in norm_venue or norm_venue in key:
            return key, mapping[key]
    return None, None


def quality_score(signals):
    score = 0
    journal = signals.get("journal") or {}
    quartile = str(journal.get("quartile", "")).upper()
    csa_zone = journal.get("csa_zone")
    impact = journal.get("if")
    ccf = signals.get("ccf")
    ei = signals.get("ei")
    tags = set(signals.get("chinese_tags") or [])

    if ccf == "A":
        score += 45
    elif ccf == "B":
        score += 32
    elif ccf == "C":
        score += 18

    if quartile == "Q1":
        score += 35
    elif quartile == "Q2":
        score += 24
    elif quartile == "Q3":
        score += 10
    elif quartile == "Q4":
        score += 4

    if csa_zone == 1:
        score += 22
    elif csa_zone == 2:
        score += 15
    elif csa_zone == 3:
        score += 6

    if isinstance(impact, (int, float)):
        if impact >= 10:
            score += 15
        elif impact >= 5:
            score += 10
        elif impact >= 2:
            score += 5

    if "CSSCI" in tags:
        score += 30
    if "北大核心" in tags:
        score += 25
    if "科技核心" in tags:
        score += 16
    if "AMI核心" in tags:
        score += 14
    if ei:
        score += 12

    return score


def relevance_score(item):
    value = first_value(item, "relevance", "relevance_score", "topic_fit", "fit")
    if value == "":
        return None
    try:
        number = float(value)
        if number <= 1:
            return int(number * 100)
        return int(number)
    except ValueError:
        text = str(value).lower()
        if text in {"high", "高度相关", "core"}:
            return 90
        if text in {"medium", "中等相关", "relevant"}:
            return 70
        if text in {"low", "低相关"}:
            return 35
    return None


def tier(relevance, quality):
    if relevance is None:
        if quality >= 55:
            return "Check"
        return "Reference"
    if relevance >= 80 and quality >= 55:
        return "Core"
    if relevance >= 65 and quality >= 35:
        return "Priority"
    if relevance >= 65:
        return "Reference"
    if relevance >= 45 and quality >= 55:
        return "Check"
    return "Remove"


def citation_number(value):
    text = str(value or "")
    match = re.search(r"\d[\d,]*", text)
    if not match:
        return 0
    return int(match.group(0).replace(",", ""))


def ranking_key(row):
    order = {"Core": 0, "Priority": 1, "Reference": 2, "Check": 3, "Remove": 4}
    relevance = row.get("relevance_score")
    try:
        relevance = int(relevance)
    except (TypeError, ValueError):
        relevance = 0
    quality = int(row.get("quality_score") or 0)
    citations = citation_number(row.get("citations"))
    year = row.get("year")
    try:
        year = int(str(year)[:4])
    except (TypeError, ValueError):
        year = 0
    return (order.get(row.get("tier"), 9), -relevance, -quality, -citations, -year)


def enrich_paper(item, data):
    venue = first_value(item, "venue", "journal", "conference", "publication")
    norm_venue = normalize(venue)

    _, journal = contains_match(norm_venue, data["journals"])
    _, ccf = contains_match(norm_venue, data["ccf"])
    _, ei = contains_match(norm_venue, data["ei"])
    _, chinese_tags = contains_match(norm_venue, data["chinese"])
    if not chinese_tags:
        _, chinese_tags = contains_cjk_match(norm_venue, data["chinese"])

    signals = {
        "journal": journal or {},
        "ccf": ccf,
        "ei": ei,
        "chinese_tags": chinese_tags or [],
    }
    q_score = quality_score(signals)
    r_score = relevance_score(item)
    rec_tier = tier(r_score, q_score)

    rank_parts = []
    if journal:
        if journal.get("quartile"):
            rank_parts.append(str(journal.get("quartile")))
        if journal.get("csa_zone"):
            rank_parts.append(f"CAS {journal.get('csa_zone')}")
    if ccf:
        rank_parts.append(f"CCF {ccf}")
    if ei:
        rank_parts.append("EI")
    rank_parts.extend(chinese_tags or [])

    reason = first_value(item, "reason", "why_keep", "note")
    if not reason:
        if rec_tier == "Core":
            reason = "Highly relevant and strong venue-quality signals."
        elif rec_tier == "Priority":
            reason = "Relevant paper with good venue-quality signals."
        elif rec_tier == "Reference":
            reason = "Relevant or potentially useful, but venue quality is modest or unknown."
        elif rec_tier == "Check":
            reason = "Potentially useful, but relevance or metadata needs manual verification."
        else:
            reason = "Low relevance or insufficient quality signals."

    out = dict(item)
    out.update({
        "source": first_value(item, "source", "database", "retrieval_source", "source_database") or "Google Scholar",
        "source_query": first_value(item, "source_query", "query", "search_query"),
        "title": first_value(item, "title", "paper_title"),
        "authors": first_value(item, "authors", "author"),
        "year": first_value(item, "year", "date"),
        "venue": venue,
        "impact_factor": journal.get("if") if journal else "",
        "quartile": journal.get("quartile") if journal else "",
        "cas_zone": journal.get("csa_zone") if journal else "",
        "ccf_rank": ccf or "",
        "ei": "EI" if ei else "",
        "chinese_core_tags": "; ".join(chinese_tags or []),
        "rank_tags": " / ".join(rank_parts) or "unknown venue",
        "citations": first_value(item, "citations", "citation_count", "cited_by"),
        "access_link": first_value(item, "pdf_link", "download_link", "url", "link", "scholar_link", "doi"),
        "quality_score": q_score,
        "relevance_score": "" if r_score is None else r_score,
        "tier": rec_tier,
        "why_keep": reason,
    })
    return out


def markdown_link(value):
    value = str(value or "").strip()
    if not value:
        return ""
    label = "PDF" if ".pdf" in value.lower() else "Link"
    if value.startswith("http"):
        return f"[{label}]({value})"
    return value


def write_markdown(rows, path):
    headers = ["Tier", "Source", "Title", "Authors", "Year", "Venue", "IF", "Rank/Tags", "Citations", "Access", "Why keep"]
    lines = [
        "| " + " | ".join(headers) + " |",
        "|---|---|---|---:|---:|---|---:|---|---:|---|---|",
    ]
    rows = sorted(rows, key=ranking_key)
    for row in rows:
        values = [
            row.get("tier", ""),
            row.get("source", ""),
            row.get("title", ""),
            row.get("authors", ""),
            row.get("year", ""),
            row.get("venue", ""),
            row.get("impact_factor", ""),
            row.get("rank_tags", ""),
            row.get("citations", ""),
            markdown_link(row.get("access_link", "")),
            row.get("why_keep", ""),
        ]
        clean = [str(v).replace("\n", " ").replace("|", "\\|") for v in values]
        lines.append("| " + " | ".join(clean) + " |")
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Enrich candidate papers with local venue-quality metadata.")
    parser.add_argument("input", help="Candidate papers as JSON or CSV")
    parser.add_argument(
        "--data-dir",
        default=os.environ.get("SCHOLAR_QUALITY_DATA_DIR", str(DEFAULT_DATA_DIR)),
        help="Directory containing journal_scores.json, ccf_conferences.json, eiiRankingName.json, and chinese_journal_tags.json. Defaults to SCHOLAR_QUALITY_DATA_DIR or the skill data/ folder.",
    )
    parser.add_argument("--json", dest="json_out", help="Write enriched JSON")
    parser.add_argument("--markdown", dest="markdown_out", help="Write Markdown table")
    parser.add_argument("--limit", type=int, default=50, help="Maximum rows to output after ranking. Use 0 for all rows.")
    args = parser.parse_args()

    data = load_quality_data(args.data_dir)
    candidates = read_candidates(args.input)
    enriched = sorted((enrich_paper(item, data) for item in candidates), key=ranking_key)
    if args.limit > 0:
        enriched = enriched[:args.limit]

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.markdown_out:
        write_markdown(enriched, args.markdown_out)
    if not args.json_out and not args.markdown_out:
        print(json.dumps(enriched, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
