#!/usr/bin/env python3
"""
Premium: Analyze candidate-job match and generate a match report.
Compares candidate profile against job description.
"""

import json
import argparse
import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALARY_PATH = os.path.join(SKILL_DIR, "references", "salary_data.json")


def load_salary_data():
    with open(SALARY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze_match(
    candidate_skills: list,
    candidate_years: int,
    candidate_education: str,
    candidate_location: str,
    job_skills: list,
    job_min_years: int,
    job_education: str,
    job_location: str,
    job_role: str = "software_engineer",
    job_seniority: str = "mid",
) -> dict:
    """Analyze candidate-job fit and generate match analysis."""
    # Skill overlap
    cand_set = {s.lower().strip() for s in candidate_skills}
    job_set = {s.lower().strip() for s in job_skills}
    matched = cand_set & job_set
    missing = job_set - cand_set
    extra = cand_set - job_set

    skill_match = len(matched) / max(len(job_set), 1)

    # Experience match
    if candidate_years >= job_min_years:
        exp_match = 1.0
    elif candidate_years >= job_min_years * 0.7:
        exp_match = 0.6
    else:
        exp_match = 0.3

    # Education match
    edu_levels = {"high_school": 0, "associates": 1, "bachelors": 2, "masters": 3, "phd": 4}
    cand_edu = edu_levels.get(candidate_education.lower(), 0)
    req_edu = edu_levels.get(job_education.lower(), 0)
    edu_match = min(cand_edu / max(req_edu, 1), 1.0) if req_edu > 0 else 1.0

    # Location match
    location_match = 1.0 if job_location.lower() in ("remote", "any") or candidate_location.lower() == job_location.lower() else 0.5

    # Weighted overall
    overall = skill_match * 45 + exp_match * 25 + edu_match * 15 + location_match * 15

    # Salary context
    salary_info = None
    try:
        salary_db = load_salary_data()
        if job_role in salary_db["regions"]["us"]["roles"]:
            role_data = salary_db["regions"]["us"]["roles"][job_role]
            if job_seniority in role_data:
                salary_info = role_data[job_seniority]
    except Exception:
        pass

    # Rating
    if overall >= 85:
        rating = "Excellent Match"
        action = "Fast-track to interview"
    elif overall >= 70:
        rating = "Strong Match"
        action = "Proceed to interview"
    elif overall >= 55:
        rating = "Moderate Match"
        action = "Consider with additional screening"
    elif overall >= 40:
        rating = "Weak Match"
        action = "Review carefully before proceeding"
    else:
        rating = "Poor Match"
        action = "Not recommended"

    return {
        "overall_match": round(overall, 1),
        "rating": rating,
        "recommended_action": action,
        "breakdown": {
            "skills": {"score": round(skill_match * 100, 1), "weight": "45%"},
            "experience": {"score": round(exp_match * 100, 1), "weight": "25%"},
            "education": {"score": round(edu_match * 100, 1), "weight": "15%"},
            "location": {"score": round(location_match * 100, 1), "weight": "15%"},
        },
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),
        "extra_skills": sorted(list(extra)),
        "experience": {
            "candidate_years": candidate_years,
            "required_years": job_min_years,
            "gap": candidate_years - job_min_years,
        },
        "education": {
            "candidate": candidate_education,
            "required": job_education,
        },
        "salary_context": salary_info,
    }


def format_match_report(data: dict) -> str:
    """Format match analysis as markdown."""
    lines = []
    lines.append("# Candidate-Job Match Analysis")
    lines.append("")
    lines.append(f"## Overall Match: {data['overall_match']}/100")
    lines.append(f"**Rating:** {data['rating']}")
    lines.append(f"**Action:** {data['recommended_action']}")
    lines.append("")

    lines.append("## Breakdown")
    lines.append("| Dimension | Score | Weight |")
    lines.append("|-----------|-------|--------|")
    for dim, info in data["breakdown"].items():
        lines.append(f"| {dim.title()} | {info['score']} | {info['weight']} |")
    lines.append("")

    if data["matched_skills"]:
        lines.append(f"## ✅ Matched Skills ({len(data['matched_skills'])})")
        for s in data["matched_skills"]:
            lines.append(f"- {s}")
        lines.append("")

    if data["missing_skills"]:
        lines.append(f"## ⚠️ Missing Skills ({len(data['missing_skills'])})")
        for s in data["missing_skills"]:
            lines.append(f"- {s}")
        lines.append("")

    if data["extra_skills"]:
        lines.append(f"## ➕ Additional Skills ({len(data['extra_skills'])})")
        for s in data["extra_skills"]:
            lines.append(f"- {s}")
        lines.append("")

    exp = data["experience"]
    gap_str = f"+{exp['gap']}" if exp['gap'] >= 0 else str(exp['gap'])
    lines.append("## Experience")
    lines.append(f"- Candidate: {exp['candidate_years']} years")
    lines.append(f"- Required: {exp['required_years']} years")
    lines.append(f"- Gap: {gap_str} years")
    lines.append("")

    edu = data["education"]
    lines.append("## Education")
    lines.append(f"- Candidate: {edu['candidate']}")
    lines.append(f"- Required: {edu['required']}")
    lines.append("")

    if data["salary_context"]:
        sc = data["salary_context"]
        lines.append("## Salary Context (US Market)")
        lines.append(f"- Median: ${sc.get('median', 'N/A'):,}")
        lines.append(f"- Range: ${sc.get('min', 'N/A'):,} - ${sc.get('max', 'N/A'):,}")
        lines.append(f"- P75: ${sc.get('p75', 'N/A'):,}")
        lines.append(f"- P90: ${sc.get('p90', 'N/A'):,}")
        lines.append("")

    lines.append("---")
    lines.append("*Generated by HireMate AI Recruiting Assistant (Premium)*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze candidate-job match (Premium)")
    parser.add_argument("--candidate-skills", required=True, nargs="+", help="Candidate's skills")
    parser.add_argument("--candidate-years", type=int, required=True, help="Candidate years of experience")
    parser.add_argument("--candidate-edu", default="bachelors", help="Candidate education level")
    parser.add_argument("--candidate-location", default="Remote", help="Candidate location")
    parser.add_argument("--job-skills", required=True, nargs="+", help="Required skills for the job")
    parser.add_argument("--job-min-years", type=int, default=3, help="Minimum years required")
    parser.add_argument("--job-edu", default="bachelors", help="Required education level")
    parser.add_argument("--job-location", default="Remote", help="Job location")
    parser.add_argument("--job-role", default="software_engineer", help="Job role for salary context")
    parser.add_argument("--job-seniority", default="mid", help="Job seniority level")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    data = analyze_match(
        candidate_skills=args.candidate_skills,
        candidate_years=args.candidate_years,
        candidate_education=args.candidate_edu,
        candidate_location=args.candidate_location,
        job_skills=args.job_skills,
        job_min_years=args.job_min_years,
        job_education=args.job_edu,
        job_location=args.job_location,
        job_role=args.job_role,
        job_seniority=args.job_seniority,
    )

    if args.format == "json":
        output = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        output = format_match_report(data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Match report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
