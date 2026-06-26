#!/usr/bin/env python3
"""
Premium: Score a resume against job requirements.
Accepts resume text and job requirements, returns a structured score.
"""

import json
import argparse
import re
import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Keywords commonly associated with skills/experience
TECH_KEYWORDS = {
    "python": {"category": "programming", "weight": 3},
    "java": {"category": "programming", "weight": 3},
    "javascript": {"category": "programming", "weight": 3},
    "typescript": {"category": "programming", "weight": 3},
    "go": {"category": "programming", "weight": 3},
    "rust": {"category": "programming", "weight": 3},
    "c++": {"category": "programming", "weight": 2},
    "react": {"category": "framework", "weight": 2},
    "django": {"category": "framework", "weight": 2},
    "flask": {"category": "framework", "weight": 2},
    "spring": {"category": "framework", "weight": 2},
    "node.js": {"category": "framework", "weight": 2},
    "aws": {"category": "cloud", "weight": 2},
    "gcp": {"category": "cloud", "weight": 2},
    "azure": {"category": "cloud", "weight": 2},
    "docker": {"category": "devops", "weight": 2},
    "kubernetes": {"category": "devops", "weight": 2},
    "sql": {"category": "database", "weight": 2},
    "postgresql": {"category": "database", "weight": 2},
    "mongodb": {"category": "database", "weight": 2},
    "machine learning": {"category": "ml", "weight": 3},
    "tensorflow": {"category": "ml", "weight": 2},
    "pytorch": {"category": "ml", "weight": 2},
    "scikit-learn": {"category": "ml", "weight": 2},
    "figma": {"category": "design", "weight": 2},
    "sketch": {"category": "design", "weight": 2},
    "agile": {"category": "methodology", "weight": 1},
    "scrum": {"category": "methodology", "weight": 1},
    "salesforce": {"category": "crm", "weight": 2},
    "hubspot": {"category": "crm", "weight": 2},
}


def extract_years_experience(resume_text: str) -> float:
    """Estimate total years of experience from resume text."""
    patterns = [
        r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)",
        r"(?:experience|exp)(?:d)?\s*:?\s*(\d+)\+?\s*(?:years?|yrs?)",
    ]
    max_years = 0
    for pattern in patterns:
        matches = re.findall(pattern, resume_text, re.IGNORECASE)
        for m in matches:
            try:
                years = int(m)
                if years > max_years:
                    max_years = years
            except ValueError:
                pass
    return max_years


def extract_education(resume_text: str) -> list:
    """Extract education level from resume text."""
    levels = []
    text_lower = resume_text.lower()
    if "phd" in text_lower or "ph.d" in text_lower or "doctorate" in text_lower:
        levels.append("phd")
    if "master" in text_lower or "ms " in text_lower or "m.s" in text_lower or "mba" in text_lower:
        levels.append("masters")
    if "bachelor" in text_lower or "bs " in text_lower or "b.s" in text_lower or "ba " in text_lower or "b.a" in text_lower:
        levels.append("bachelors")
    return levels


def find_keywords(resume_text: str, required_keywords: list) -> dict:
    """Check which required keywords appear in the resume."""
    text_lower = resume_text.lower()
    found = {}
    missing = []
    for kw in required_keywords:
        if kw.lower() in text_lower:
            found[kw] = True
        else:
            missing.append(kw)
    return {"found": list(found.keys()), "missing": missing, "match_rate": len(found) / max(len(required_keywords), 1)}


def score_resume(
    resume_text: str,
    required_keywords: list,
    min_years: int = 3,
    required_education: str = "bachelors",
) -> dict:
    """Score a resume against requirements."""
    # Keyword matching
    keyword_result = find_keywords(resume_text, required_keywords)

    # Years of experience
    years_exp = extract_years_experience(resume_text)
    years_score = min(years_exp / max(min_years, 1), 1.0) * 100

    # Education check
    education_levels = extract_education(resume_text)
    edu_hierarchy = {"bachelors": 1, "masters": 2, "phd": 3}
    req_edu_level = edu_hierarchy.get(required_education, 0)
    max_edu = max([edu_hierarchy.get(e, 0) for e in education_levels], default=0)
    edu_score = min(max_edu / max(req_edu_level, 1), 1.0) * 100 if req_edu_level > 0 else 100

    # Tech keyword bonus
    tech_score = 0
    tech_found = 0
    tech_total = 0
    text_lower = resume_text.lower()
    for kw, info in TECH_KEYWORDS.items():
        if kw in text_lower:
            tech_found += info["weight"]
        tech_total += info["weight"]
    tech_score = (tech_found / max(tech_total, 1)) * 100

    # Overall weighted score (all components on 0-100 scale)
    keyword_score_100 = keyword_result["match_rate"] * 100
    overall = (
        keyword_score_100 * 0.40
        + years_score * 0.25
        + edu_score * 0.15
        + tech_score * 0.20
    )

    # Determine level
    if overall >= 85:
        rating = "Strong Match"
        recommendation = "Highly recommend for interview"
    elif overall >= 70:
        rating = "Good Match"
        recommendation = "Recommend for interview"
    elif overall >= 55:
        rating = "Moderate Match"
        recommendation = "Consider with additional screening"
    elif overall >= 40:
        rating = "Weak Match"
        recommendation = "Not recommended unless pool is limited"
    else:
        rating = "Poor Match"
        recommendation = "Do not proceed"

    return {
        "overall_score": round(overall, 1),
        "rating": rating,
        "recommendation": recommendation,
        "breakdown": {
            "keyword_match": {"score": round(keyword_score_100, 1), "weight": "40%"},
            "experience_years": {"score": round(years_score, 1), "years_found": years_exp, "years_required": min_years, "weight": "25%"},
            "education": {"score": round(edu_score, 1), "levels_found": education_levels, "weight": "15%"},
            "technical_skills": {"score": round(tech_score, 1), "weight": "20%"},
        },
        "keywords_found": keyword_result["found"],
        "keywords_missing": keyword_result["missing"],
    }


def format_score(score: dict) -> str:
    """Format score report as markdown."""
    lines = []
    lines.append(f"# Resume Score Report")
    lines.append("")
    lines.append(f"## Overall Score: {score['overall_score']}/100")
    lines.append(f"**Rating:** {score['rating']}")
    lines.append(f"**Recommendation:** {score['recommendation']}")
    lines.append("")
    lines.append("## Score Breakdown")
    lines.append("| Category | Score | Weight |")
    lines.append("|----------|-------|--------|")
    bd = score["breakdown"]
    for cat, data in bd.items():
        s = data.get("score", "N/A")
        w = data.get("weight", "N/A")
        cat_name = cat.replace("_", " ").title()
        lines.append(f"| {cat_name} | {s} | {w} |")
    lines.append("")

    if score["keywords_found"]:
        lines.append("## ✅ Keywords Found")
        for kw in score["keywords_found"]:
            lines.append(f"- {kw}")
        lines.append("")

    if score["keywords_missing"]:
        lines.append("## ❌ Keywords Missing")
        for kw in score["keywords_missing"]:
            lines.append(f"- {kw}")
        lines.append("")

    lines.append("---")
    lines.append("*Generated by HireMate AI Recruiting Assistant (Premium)*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Score a resume against job requirements (Premium)")
    parser.add_argument("--resume", required=True, help="Resume text (or file path with @ prefix)")
    parser.add_argument("--keywords", required=True, nargs="+", help="Required keywords/skills")
    parser.add_argument("--min-years", type=int, default=3, help="Minimum years of experience")
    parser.add_argument("--education", default="bachelors", choices=["bachelors", "masters", "phd"], help="Required education level")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    # Load resume from file if @ prefix
    resume_text = args.resume
    if resume_text.startswith("@"):
        filepath = resume_text[1:]
        with open(filepath, "r", encoding="utf-8") as f:
            resume_text = f.read()

    score = score_resume(
        resume_text=resume_text,
        required_keywords=args.keywords,
        min_years=args.min_years,
        required_education=args.education,
    )

    if args.format == "json":
        output = json.dumps(score, indent=2, ensure_ascii=False)
    else:
        output = format_score(score)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Score report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
