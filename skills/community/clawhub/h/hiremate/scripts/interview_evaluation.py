#!/usr/bin/env python3
"""
Premium: Generate interview evaluation report from interview notes.
"""

import json
import argparse
import os
from datetime import datetime


EVALUATION_CRITERIA = {
    "technical_competence": {
        "name": "Technical Competence",
        "weight": 30,
        "description": "Depth and breadth of technical knowledge relevant to the role",
    },
    "problem_solving": {
        "name": "Problem Solving",
        "weight": 20,
        "description": "Ability to analyze problems, think critically, and propose solutions",
    },
    "communication": {
        "name": "Communication",
        "weight": 15,
        "description": "Clarity, conciseness, and effectiveness of communication",
    },
    "cultural_fit": {
        "name": "Cultural Fit",
        "weight": 15,
        "description": "Alignment with company values and team dynamics",
    },
    "experience_relevance": {
        "name": "Experience Relevance",
        "weight": 10,
        "description": "How relevant past experience is to the role requirements",
    },
    "learning_agility": {
        "name": "Learning Agility",
        "weight": 10,
        "description": "Ability and willingness to learn new skills and adapt",
    },
}


def generate_evaluation(
    candidate_name: str,
    role: str,
    interview_date: str = None,
    interviewer: str = "",
    technical_score: int = None,
    problem_solving_score: int = None,
    communication_score: int = None,
    cultural_fit_score: int = None,
    experience_score: int = None,
    learning_score: int = None,
    notes: str = "",
    strengths: list = None,
    concerns: list = None,
) -> dict:
    """Generate an interview evaluation report."""
    if interview_date is None:
        interview_date = datetime.now().strftime("%Y-%m-%d")

    scores = {
        "technical_competence": technical_score,
        "problem_solving": problem_solving_score,
        "communication": communication_score,
        "cultural_fit": cultural_fit_score,
        "experience_relevance": experience_score,
        "learning_agility": learning_score,
    }

    # Calculate weighted score
    total_weight = 0
    weighted_sum = 0
    for key, criterion in EVALUATION_CRITERIA.items():
        score = scores.get(key)
        if score is not None:
            weighted_sum += score * criterion["weight"]
            total_weight += criterion["weight"]

    overall = round(weighted_sum / max(total_weight, 1), 1) if total_weight > 0 else None

    # Determine recommendation
    if overall is not None:
        if overall >= 85:
            recommendation = "Strong Hire"
            next_step = "Proceed to next round / Make offer"
        elif overall >= 75:
            recommendation = "Hire"
            next_step = "Proceed to next round"
        elif overall >= 65:
            recommendation = "Lean Hire"
            next_step = "Consider with reservations / Additional interview recommended"
        elif overall >= 50:
            recommendation = "Lean No Hire"
            next_step = "Consider only if no stronger candidates"
        else:
            recommendation = "No Hire"
            next_step = "Do not proceed"
    else:
        recommendation = "Incomplete"
        next_step = "Complete all scores to generate recommendation"

    return {
        "candidate_name": candidate_name,
        "role": role,
        "interview_date": interview_date,
        "interviewer": interviewer,
        "scores": {
            key: {
                "score": scores[key],
                "name": EVALUATION_CRITERIA[key]["name"],
                "weight": EVALUATION_CRITERIA[key]["weight"],
                "description": EVALUATION_CRITERIA[key]["description"],
            }
            for key in EVALUATION_CRITERIA
        },
        "overall_score": overall,
        "recommendation": recommendation,
        "next_step": next_step,
        "strengths": strengths or [],
        "concerns": concerns or [],
        "notes": notes,
    }


def format_evaluation(data: dict) -> str:
    """Format evaluation report as markdown."""
    lines = []
    lines.append(f"# Interview Evaluation Report")
    lines.append("")
    lines.append(f"**Candidate:** {data['candidate_name']}")
    lines.append(f"**Role:** {data['role']}")
    lines.append(f"**Date:** {data['interview_date']}")
    lines.append(f"**Interviewer:** {data['interviewer']}")
    lines.append("")

    if data["overall_score"] is not None:
        lines.append(f"## Overall Score: {data['overall_score']}/100")
    lines.append(f"**Recommendation:** {data['recommendation']}")
    lines.append(f"**Next Step:** {data['next_step']}")
    lines.append("")

    lines.append("## Score Breakdown")
    lines.append("| Criterion | Score (0-100) | Weight | Description |")
    lines.append("|-----------|---------------|--------|-------------|")
    for key, info in data["scores"].items():
        score = info["score"] if info["score"] is not None else "—"
        lines.append(f"| {info['name']} | {score} | {info['weight']}% | {info['description']} |")
    lines.append("")

    if data["strengths"]:
        lines.append("## ✅ Strengths")
        for s in data["strengths"]:
            lines.append(f"- {s}")
        lines.append("")

    if data["concerns"]:
        lines.append("## ⚠️ Concerns")
        for c in data["concerns"]:
            lines.append(f"- {c}")
        lines.append("")

    if data["notes"]:
        lines.append("## Notes")
        lines.append(data["notes"])
        lines.append("")

    lines.append("---")
    lines.append("*Generated by HireMate AI Recruiting Assistant (Premium)*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate interview evaluation report (Premium)")
    parser.add_argument("--candidate", required=True, help="Candidate name")
    parser.add_argument("--role", required=True, help="Role applied for")
    parser.add_argument("--date", default=None, help="Interview date (YYYY-MM-DD)")
    parser.add_argument("--interviewer", default="", help="Interviewer name")
    parser.add_argument("--technical", type=int, default=None, help="Technical competence score (0-100)")
    parser.add_argument("--problem-solving", type=int, default=None, dest="problem_solving", help="Problem solving score (0-100)")
    parser.add_argument("--communication", type=int, default=None, help="Communication score (0-100)")
    parser.add_argument("--cultural-fit", type=int, default=None, dest="cultural_fit", help="Cultural fit score (0-100)")
    parser.add_argument("--experience", type=int, default=None, help="Experience relevance score (0-100)")
    parser.add_argument("--learning", type=int, default=None, help="Learning agility score (0-100)")
    parser.add_argument("--strengths", nargs="*", default=None, help="Candidate strengths")
    parser.add_argument("--concerns", nargs="*", default=None, help="Areas of concern")
    parser.add_argument("--notes", default="", help="Additional notes")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    data = generate_evaluation(
        candidate_name=args.candidate,
        role=args.role,
        interview_date=args.date,
        interviewer=args.interviewer,
        technical_score=args.technical,
        problem_solving_score=args.problem_solving,
        communication_score=args.communication,
        cultural_fit_score=args.cultural_fit,
        experience_score=args.experience,
        learning_score=args.learning,
        notes=args.notes,
        strengths=args.strengths,
        concerns=args.concerns,
    )

    if args.format == "json":
        output = json.dumps(data, indent=2, ensure_ascii=False)
    else:
        output = format_evaluation(data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Evaluation report saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
