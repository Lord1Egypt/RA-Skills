#!/usr/bin/env python3
"""
JobClaw Search Engine

Multi-platform job search using python-jobspy (LinkedIn + Indeed).
Scores jobs against user profile and writes qualified results to CSV.

Usage:
    python3 search.py --mode coding
    python3 search.py --mode noncoding
    python3 search.py --mode all
    python3 search.py --mode coding --dry-run
    python3 search.py --mode coding --keyword "machine learning" --location "London"
"""

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

# ── Dependency check ──────────────────────────────────────────────────────────
def check_dependencies():
    missing = []
    try:
        import jobspy  # noqa
    except ImportError:
        missing.append("python-jobspy")
    if missing:
        print(f"[error] Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install python-jobspy")
        sys.exit(1)

check_dependencies()

from jobspy import scrape_jobs  # noqa: E402

# ── Config loading ────────────────────────────────────────────────────────────

def get_jobclaw_dir() -> Path:
    env_dir = os.environ.get("JOBCLAW_DIR")
    if env_dir and Path(env_dir).exists():
        return Path(env_dir)
    return Path.home() / "Documents" / "JobClaw"

def load_config() -> dict:
    config_path = get_jobclaw_dir() / "config.json"
    if not config_path.exists():
        print(f"[error] Config not found at {config_path}. Run setup.py first.")
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)

# ── Keyword defaults (used when not overridden in config) ─────────────────────

DEFAULT_CODING_KEYWORDS = [
    "machine learning engineer",
    "deep learning engineer",
    "AI engineer",
    "LLM engineer",
    "MLOps engineer",
    "ML platform engineer",
    "computer vision engineer",
    "NLP engineer",
    "research engineer machine learning",
    "reinforcement learning engineer",
    "data scientist",
    "applied scientist",
]

# Supported platforms (Glassdoor removed — unstable API, frequent errors)
SUPPORTED_PLATFORMS = ["linkedin", "indeed"]

DEFAULT_NONCODING_KEYWORDS = [
    "wearable AI",
    "human activity recognition",
    "affective computing",
    "emotion AI",
    "healthcare AI",
    "digital health machine learning",
    "health data scientist",
    "clinical AI",
    "fintech data scientist",
    "fraud detection machine learning",
    "AI product manager",
    "research associate machine learning",
    "postdoctoral machine learning",
    "AI consultant",
    "research scientist",
]

# ── Scoring ───────────────────────────────────────────────────────────────────

POSITIVE_CODING = [
    "machine learning", "deep learning", "pytorch", "tensorflow", "llm",
    "nlp", "computer vision", "mlops", "reinforcement learning", "generative ai",
    "multimodal", "transformer", "rlhf", "fine-tuning", "model training",
    "data scientist", "applied scientist", "research scientist",
]
POSITIVE_NONCODING = [
    "wearable", "healthcare", "clinical", "health", "sensor", "iot",
    "affective", "emotion", "fintech", "risk", "fraud", "research scientist",
    "research associate", "postdoc", "product manager", "quantitative",
    "digital health", "remote patient", "clinical ai", "data scientist",
]
NEGATIVE_ALL = ["intern", "unpaid", "data entry"]


def score_job(row: dict, mode: str, user_keywords: list[str] = None) -> int:
    """Score a job 0-100 based on keyword matches."""
    text = f"{row.get('title','') or ''} {row.get('description','') or ''}".lower()

    positives = POSITIVE_CODING if mode == "coding" else POSITIVE_NONCODING

    # Boost with user-specific keywords from config
    if user_keywords:
        positives = positives + [k.lower() for k in user_keywords]

    hits = sum(1 for kw in positives if kw in text)
    bad = sum(1 for kw in NEGATIVE_ALL if kw in text)

    score = min(100, 50 + hits * 5 - bad * 15)
    return max(0, score)


def infer_interview_type(mode: str, title: str, description: str = "") -> str:
    text = f"{title} {description or ''}".lower()
    if mode == "noncoding":
        if any(w in text for w in ["research", "postdoc", "academic", "clinical", "fellow"]):
            return "Research Talk"
        if any(w in text for w in ["product", "pm ", "strategy", "consulting", "consultant"]):
            return "Case Study"
        return "No Leetcode"
    else:
        if any(w in text for w in ["platform", "infrastructure", "mlops", "sre", "devops"]):
            return "Standard Coding"
        if any(w in text for w in ["research", "scientist"]):
            return "Fair Coding"
        return "Standard Coding"


def infer_ml_direction(title: str, description: str = "") -> str:
    text = f"{title} {description or ''}".lower()
    mapping = [
        (["wearable", "sensor", "iot", "har", "activity", "ubicomp"], "Wearable/IoT"),
        (["health", "clinical", "medical", "patient", "biomedical"], "Healthcare AI"),
        (["nlp", "language", "llm", "text", "speech", "conversation"], "NLP/LLM"),
        (["vision", "image", "video", "cv ", "computer vision"], "Computer Vision"),
        (["multimodal", "audio", "fusion"], "Multimodal"),
        (["fintech", "fraud", "risk", "finance", "quant"], "FinTech"),
        (["reinforcement", "rlhf", "robot"], "RL/Robotics"),
        (["mlops", "platform", "infrastructure"], "ML Platform"),
        (["emotion", "affective", "sentiment"], "Affective Computing"),
    ]
    for keywords, direction in mapping:
        if any(k in text for k in keywords):
            return direction
    return "General ML/AI"


def infer_seniority(title: str) -> str:
    t = title.lower()
    if any(w in t for w in ["head ", "vp ", "chief ", "director"]):
        return "Lead"
    if any(w in t for w in ["senior", "sr.", "lead ", "principal", "staff", "ii ", "iii "]):
        return "Senior"
    if any(w in t for w in ["junior", "jr.", "graduate", "intern", "associate", "i "]):
        return "Junior"
    return "Mid"


# ── Main search ───────────────────────────────────────────────────────────────

def run_search(
    mode: str,
    config: dict,
    dry_run: bool = False,
    custom_keywords: list[str] = None,
    custom_location: str = None,
) -> tuple[int, str]:
    """
    Run job search for the given mode.

    Returns:
        (added_count, top_match_str)
    """
    from tracker import JobTracker

    search_cfg = config.get("search", {})
    user_cfg = config.get("user", {})

    # Determine keywords
    if custom_keywords:
        keywords = custom_keywords
    elif mode == "coding":
        keywords = search_cfg.get("coding_keywords", DEFAULT_CODING_KEYWORDS)
    elif mode == "noncoding":
        keywords = search_cfg.get("noncoding_keywords", DEFAULT_NONCODING_KEYWORDS)
    else:
        keywords = DEFAULT_CODING_KEYWORDS + DEFAULT_NONCODING_KEYWORDS

    # Locations
    if custom_location:
        locations = [custom_location]
    else:
        locations = search_cfg.get("locations", ["London, UK"])

    min_score = search_cfg.get("min_score", 70)
    hours_old = search_cfg.get("hours_old", 48)
    results_per_search = search_cfg.get("results_per_search", 10)
    # Only allow supported platforms; glassdoor removed due to unstable API
    configured = search_cfg.get("platforms", ["linkedin", "indeed"])
    platforms = [p for p in configured if p in SUPPORTED_PLATFORMS]
    if not platforms:
        platforms = ["linkedin", "indeed"]

    # User's skill keywords for scoring boost
    user_keywords = user_cfg.get("skill_keywords", [])

    today = date.today().isoformat()
    all_rows = []
    seen_urls = set()

    print(f"\n{'='*60}")
    print(f"  JobClaw Search: {mode.upper()} | {today}")
    print(f"  Platforms: {', '.join(platforms)}")
    print(f"  Keywords: {len(keywords)} | Locations: {len(locations)}")
    print(f"  Min score: {min_score} | Hours old: {hours_old}")
    print(f"{'='*60}\n")

    for keyword in keywords:
        for location in locations:
            try:
                print(f"  🔍 '{keyword}' @ {location} [{'+'.join(platforms)}]...", end=" ", flush=True)
                results = scrape_jobs(
                    site_name=platforms,
                    search_term=keyword,
                    location=location,
                    results_wanted=results_per_search,
                    hours_old=hours_old,
                    verbose=0,
                )
                print(f"{len(results)} found")
                for _, row in results.iterrows():
                    url = str(row.get("job_url") or "")
                    if url and url in seen_urls:
                        continue
                    if url:
                        seen_urls.add(url)
                    all_rows.append(row)
            except Exception as e:
                print(f"ERROR: {e}")

    print(f"\n📦 Total raw results: {len(all_rows)} (deduped by URL)")

    # Score and filter
    scored = []
    for row in all_rows:
        score = score_job(row.to_dict(), mode, user_keywords)
        if score >= min_score:
            scored.append((score, row))

    scored.sort(key=lambda x: -x[0])
    print(f"✅ Above score threshold ({min_score}): {len(scored)} jobs")

    if dry_run:
        print("\n[DRY RUN] Top 10 that would be added:")
        for score, row in scored[:10]:
            print(f"  [{score:3d}] {row.get('company',''):<25} {row.get('title','')[:45]}")
        return 0, "None"

    # Convert to tracker format
    jobs_to_add = []
    for score, row in scored:
        row_dict = row.to_dict() if hasattr(row, "to_dict") else dict(row)
        title = str(row_dict.get("title") or "")
        company = str(row_dict.get("company") or "")
        location_str = str(row_dict.get("location") or "")
        url = str(row_dict.get("job_url") or "")
        description = str(row_dict.get("description") or "")

        date_posted = ""
        if row_dict.get("date_posted"):
            try:
                date_posted = str(row_dict["date_posted"])[:10]
            except Exception:
                pass

        is_remote = str(row_dict.get("is_remote") or "").lower()
        work_mode = "Remote" if is_remote in ("true", "1", "yes", "remote") else "Unknown"

        salary = str(row_dict.get("min_amount") or "")
        site = str(row_dict.get("site") or "")

        jobs_to_add.append({
            "company": company,
            "role": title,
            "location": location_str,
            "work_mode": work_mode,
            "salary": salary,
            "job_url": url,
            "date_posted": date_posted,
            "date_found": today,
            "source": "Daily Search",
            "match_score": score,
            "ml_direction": infer_ml_direction(title, description),
            "seniority": infer_seniority(title),
            "interview_type": infer_interview_type(mode, title, description),
            "status": "New",
            "priority": "High" if score >= 85 else ("Medium" if score >= 75 else "Low"),
            "notes": f"[jobspy:{site}] {description[:300]}",
            "job_category": mode,
        })

    tracker = JobTracker()
    added, skipped = tracker.add_jobs(jobs_to_add)
    print(f"📝 Written: {added} added, {skipped} skipped duplicates")

    top_str = "None"
    if scored:
        top_row = scored[0][1]
        top_row_dict = top_row.to_dict() if hasattr(top_row, "to_dict") else dict(top_row)
        top_str = f"{top_row_dict.get('company','')} — {top_row_dict.get('title','')} (Score: {scored[0][0]})"
        print(f"🏆 Top match: {top_str}")

    return added, top_str


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JobClaw multi-platform job search")
    parser.add_argument("--mode", choices=["coding", "noncoding", "all"], default="all",
                        help="Search mode")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--keyword", help="Override keywords (single keyword)")
    parser.add_argument("--location", help="Override location (e.g. 'London, UK')")
    args = parser.parse_args()

    config = load_config()

    keywords = [args.keyword] if args.keyword else None
    modes = ["coding", "noncoding"] if args.mode == "all" else [args.mode]

    results_summary = {}
    for m in modes:
        added, top = run_search(
            mode=m,
            config=config,
            dry_run=args.dry_run,
            custom_keywords=keywords,
            custom_location=args.location,
        )
        results_summary[m] = {"added": added, "top": top}
        print(f"\nSUMMARY_{m.upper()}: Added {added} jobs. Top match: {top}")

    # Write summary JSON for run_daily.sh
    if not args.dry_run:
        from pathlib import Path
        summary_path = get_jobclaw_dir() / "data" / "search_summary.json"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        import json as _json
        with open(summary_path, "w") as f:
            _json.dump({**results_summary, "date": date.today().isoformat()}, f, indent=2)
        print(f"\n[search] Summary written to {summary_path}")
