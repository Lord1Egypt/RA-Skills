#!/usr/bin/env python3
"""
Job Match Scorer - scores how well a job fits a candidate profile.
Returns 0-100 score + breakdown.
Configure profile in config.json under "candidate".
"""
import re
import json
import sqlite3
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"


def load_profile():
    """Load candidate profile from config.json."""
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    return config.get("candidate", {})


def score_job(title, company, location, description, requirements_json, required_years, profile=None):
    """Score a job 0-100 with breakdown."""
    if profile is None:
        profile = load_profile()

    desc = (description or "").lower()
    title_lower = (title or "").lower()
    loc_lower = (location or "").lower()

    try:
        reqs = json.loads(requirements_json) if requirements_json else []
    except:
        reqs = []

    all_text = f"{desc} {' '.join(str(r) for r in reqs)}".lower()
    breakdown = []
    score = 0

    # 1. Title match (0-30)
    title_score = 0
    for t in profile.get("target_titles", []):
        if t.lower() in title_lower:
            title_score = 30
            breakdown.append(f"Title perfect match: {t}")
            break
    if title_score == 0:
        for t in profile.get("good_titles", []):
            if t.lower() in title_lower:
                title_score = 15
                breakdown.append(f"Title partial match: {t}")
                break
    if title_score == 0:
        breakdown.append("Title: no match")
    score += title_score

    # 2. Skills match (0-30)
    core_found = [s for s in profile.get("core_skills", []) if s.lower() in all_text]
    bonus_found = [s for s in profile.get("bonus_skills", []) if s.lower() in all_text]
    skill_score = min(20, len(core_found) * 5) + min(10, len(bonus_found) * 2)
    if core_found:
        breakdown.append(f"Core skills: {', '.join(core_found)}")
    if bonus_found:
        breakdown.append(f"Bonus skills: {', '.join(bonus_found)}")
    if not core_found and not bonus_found:
        breakdown.append("No matching skills found")
    score += skill_score

    # 3. Experience level (0-40)
    max_years = profile.get("max_years", 2)
    if required_years == 0:
        score += 40
        breakdown.append("No experience required - perfect!")
    elif required_years <= 1:
        score += 30
        breakdown.append(f"{required_years} year - great fit")
    elif required_years <= max_years:
        score += 10
        breakdown.append(f"{required_years} years - on the edge")
    else:
        score -= 20
        breakdown.append(f"{required_years} years - too high")

    # 4. Location (0-25)
    preferred = [loc.lower() for loc in profile.get("preferred_locations", [])]
    metro = [loc.lower() for loc in profile.get("metro_locations", [])]
    if any(loc in loc_lower for loc in preferred):
        score += 25
        breakdown.append("Location: preferred area")
    elif any(loc in loc_lower for loc in metro):
        score += 15
        breakdown.append("Location: metro area")
    elif "israel" in loc_lower or "remote" in loc_lower:
        score += 5
        breakdown.append("Location: same country / remote")
    else:
        breakdown.append("Location: not in preferred area")

    # 5. Junior/entry keywords (0-10)
    junior_kw = ["junior", "entry", "graduate", "0-1", "0-2"]
    if any(kw in title_lower or kw in desc for kw in junior_kw):
        score += 10
        breakdown.append("Junior / entry-level position")

    score = max(0, min(100, score))

    if score >= 70:
        rec = "APPLY"
    elif score >= 50:
        rec = "REVIEW"
    else:
        rec = "SKIP"

    return {"score": score, "recommendation": rec, "breakdown": breakdown}


def score_all_jobs(db_path="jobs.db"):
    """Score all jobs in DB."""
    profile = load_profile()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT job_id, title, company, location, description, requirements, required_years FROM jobs ORDER BY title")
    rows = c.fetchall()
    conn.close()

    results = []
    for job_id, title, company, location, desc, reqs, years in rows:
        r = score_job(title, company, location, desc, reqs, years or 0, profile)
        r["job_id"] = job_id
        r["title"] = title
        r["company"] = company
        results.append(r)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


if __name__ == "__main__":
    results = score_all_jobs()
    for r in results:
        print(f"{r['score']:3d}% [{r['recommendation']}] {r['title']} @ {r['company']}")
        for b in r["breakdown"]:
            print(f"  - {b}")
        print()
