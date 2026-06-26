#!/usr/bin/env python3
"""
paper_lark_report.py - Entry point for paper-lark-report daily/weekly digest.

Imports:
    arxiv_search - arXiv API: query building, paper fetch, detail fetch
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

from arxiv_search import Paper, build_arxiv_query, fetch_arxiv_papers, fetch_arxiv_details

# ============================================================================
# PATHS
# ============================================================================
SKILL_DIR = Path(__file__).parent.parent
PROCESSED_IDS_PATH = SKILL_DIR / "data" / "processed_ids.json"
DOC_REGISTRY_PATH = SKILL_DIR / "data" / "doc_registry.json"
PROCESSED_LOG_DIR = SKILL_DIR / "processed_log"
OUTPUT_PATH = SKILL_DIR / "data" / "daily_papers.json"

# ============================================================================
# CONFIG
# ============================================================================
def load_config() -> dict:
    import yaml
    with open(SKILL_DIR / "config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# ============================================================================
# PROCESSED IDS (cross-day dedup)
# ============================================================================
def load_processed_ids() -> dict:
    if not PROCESSED_IDS_PATH.exists():
        return {"processed": [], "last_updated": ""}
    with open(PROCESSED_IDS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_processed_ids(data: dict):
    PROCESSED_IDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_processed(paper_id: str, processed_data: dict) -> bool:
    return paper_id in processed_data.get("processed", [])


def add_processed(paper_id: str, processed_data: dict):
    processed_data.setdefault("processed", []).append(paper_id)
    processed_data["last_updated"] = datetime.now().isoformat()

# ============================================================================
# DOC REGISTRY (daily dedup)
# ============================================================================
def load_doc_registry() -> dict:
    if not DOC_REGISTRY_PATH.exists():
        return {}
    with open(DOC_REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_doc_registry(registry: dict):
    with open(DOC_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def get_today_doc_info() -> dict | None:
    return load_doc_registry().get(datetime.now().strftime("%Y-%m-%d"))


def register_doc(node_token: str, obj_token: str, doc_url: str, title: str = ""):
    today = datetime.now().strftime("%Y-%m-%d")
    registry = load_doc_registry()
    registry[today] = {
        "node_token": node_token,
        "obj_token": obj_token,
        "url": doc_url,
        "title": title or f"Research Daily {today}",
        "registered_at": datetime.now().isoformat(),
    }
    save_doc_registry(registry)
    print(f"Registered: {today} -> {doc_url}")

# ============================================================================
# DAILY RUN
# ============================================================================
def run_daily():
    print("=" * 60)
    print("paper-lark-report  |  daily run")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

    config = load_config()
    processed_data = load_processed_ids()
    today_str = datetime.now().strftime("%Y-%m-%d")

    feishu_root = config.get("feishu_root", "")
    research_direction = config.get("research_direction", "")
    max_search = config.get("max_search_results", 20)
    max_daily = config.get("max_daily_papers", 3)

    if not feishu_root:
        print("ERROR: feishu_root not configured")
        return
    if not research_direction:
        print("ERROR: research_direction not configured")
        return

    if get_today_doc_info() is not None:
        print("Today's document already exists. Skip.")
        return

    query = build_arxiv_query(research_direction)
    print(f"arXiv query: {query}")

    papers = fetch_arxiv_papers(query, max_results=max_search)
    filtered = [p for p in papers if not is_processed(p.paper_id, processed_data)]
    print(f"After dedup: {len(filtered)} papers")

    if not filtered:
        print("No new papers. Skip.")
        return

    filtered = fetch_arxiv_details(filtered[:20])

    output = {
        "date": today_str,
        "research_direction": research_direction,
        "arxiv_query": query,
        "papers": [p.__dict__ for p in filtered],
        "max_daily_papers": max_daily,
        "skip": False,
        "config": {"feishu_root": feishu_root},
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Output saved to {OUTPUT_PATH}")
    print(f"{len(filtered)} papers ready for LLM scoring")

# ============================================================================
# WEEKLY RUN
# ============================================================================
def run_weekly():
    print("=" * 60)
    print("paper-lark-report  |  weekly run")
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)

    config = load_config()
    today = datetime.now()
    week_papers = []
    dates_included = []

    for i in range(1, 6):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        log_file = PROCESSED_LOG_DIR / f"{date}.json"
        if log_file.exists():
            with open(log_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                week_papers.extend(data.get("papers", []))
                dates_included.append(date)

    if not week_papers:
        print("No papers this week. Skip.")
        return

    output = {
        "week": f"{today.year}-W{today.isocalendar()[1]:02d}",
        "start_date": dates_included[0],
        "end_date": dates_included[-1],
        "research_direction": config.get("research_direction", ""),
        "dates_included": dates_included,
        "papers": week_papers,
        "config": {"feishu_root": config.get("feishu_root", "")},
    }

    output_path = SKILL_DIR / "data" / "weekly_papers.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Week: {', '.join(dates_included)} | {len(week_papers)} papers")
    print(f"Weekly data saved to {output_path}")

# ============================================================================
# SAVE SELECTED PAPERS (called by LLM after scoring)
# ============================================================================
def save_selected_papers(date: str, papers: list):
    PROCESSED_LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = PROCESSED_LOG_DIR / f"{date}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({
            "date": date,
            "papers": papers,
            "generated_at": datetime.now().isoformat(),
        }, f, ensure_ascii=False, indent=2)

    processed_data = load_processed_ids()
    for paper in papers:
        pid = paper.get("paper_id", "")
        if pid:
            add_processed(pid, processed_data)
    save_processed_ids(processed_data)

    print(f"Saved {len(papers)} selected papers for {date}")

# ============================================================================
# CLI
# ============================================================================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="paper-lark-report")
    parser.add_argument("--weekly", action="store_true", help="Generate weekly report")
    parser.add_argument("--register-doc", nargs=3,
                        metavar=("NODE_TOKEN", "OBJ_TOKEN", "DOC_URL"),
                        help="Register a created Feishu wiki doc (NODE_TOKEN OBJ_TOKEN DOC_URL)")
    parser.add_argument("--save-selected", nargs=2,
                        metavar=("DATE", "PAPERS_JSON"),
                        help="Save LLM-selected papers (DATE PAPERS_JSON_FILE)")
    args = parser.parse_args()

    if args.save_selected:
        date_str, papers_json = args.save_selected
        with open(papers_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Support both a bare list and a {"date":..., "papers":[...]} wrapper
        papers = data if isinstance(data, list) else data.get("papers", [])
        save_selected_papers(date_str, papers)

    elif args.register_doc:
        node_token, obj_token, doc_url = args.register_doc
        register_doc(node_token, obj_token, doc_url)

    elif args.weekly:
        run_weekly()

    else:
        run_daily()
