#!/usr/bin/env python3
"""Generate resume screening criteria for a given role."""

import json
import argparse
import sys
import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SCREENING_TEMPLATES = {
    "software_engineer": {
        "must_have": [
            {"field": "education", "criteria": "BS in Computer Science or equivalent practical experience", "weight": 10},
            {"field": "experience_years", "criteria": "Minimum {years} years of professional software development", "weight": 20},
            {"field": "programming_languages", "criteria": "Proficiency in at least one of: {languages}", "weight": 20},
            {"field": "frameworks", "criteria": "Hands-on experience with {frameworks}", "weight": 15},
            {"field": "systems", "criteria": "Experience with version control (Git) and CI/CD pipelines", "weight": 10},
        ],
        "nice_to_have": [
            {"field": "cloud", "criteria": "Experience with AWS/GCP/Azure", "weight": 10},
            {"field": "open_source", "criteria": "Active GitHub profile or open-source contributions", "weight": 5},
            {"field": "leadership", "criteria": "Experience mentoring junior developers", "weight": 5},
            {"field": "domain", "criteria": "Background in {industry} domain", "weight": 5},
        ],
        "red_flags": [
            "No code samples or portfolio available",
            "Job-hopping without clear progression (3+ jobs in 2 years)",
            "Vague descriptions of technical contributions",
            "Cannot explain technical decisions in past projects",
        ],
    },
    "product_manager": {
        "must_have": [
            {"field": "education", "criteria": "Bachelor's degree in relevant field", "weight": 10},
            {"field": "experience_years", "criteria": "Minimum {years} years in product management", "weight": 20},
            {"field": "product_launches", "criteria": "Track record of shipping products from concept to launch", "weight": 20},
            {"field": "analytics", "criteria": "Experience with data analysis and metrics-driven decisions", "weight": 15},
            {"field": "methodology", "criteria": "Familiarity with Agile/Scrum methodologies", "weight": 10},
        ],
        "nice_to_have": [
            {"field": "technical", "criteria": "Technical background or engineering degree", "weight": 10},
            {"field": "industry", "criteria": "Domain expertise in {industry}", "weight": 5},
            {"field": "mba", "criteria": "MBA or equivalent business education", "weight": 5},
            {"field": "tools", "criteria": "Experience with product management tools (Jira, Aha!, etc.)", "weight": 5},
        ],
        "red_flags": [
            "Cannot articulate specific product outcomes or metrics",
            "No experience collaborating with engineering teams",
            "Vague about their specific contributions vs team contributions",
            "No examples of handling product failures or pivots",
        ],
    },
    "data_scientist": {
        "must_have": [
            {"field": "education", "criteria": "MS or PhD in Statistics, Computer Science, Mathematics, or related field", "weight": 15},
            {"field": "experience_years", "criteria": "Minimum {years} years in data science or ML roles", "weight": 20},
            {"field": "programming", "criteria": "Proficiency in Python and SQL", "weight": 20},
            {"field": "ml_frameworks", "criteria": "Experience with ML frameworks (scikit-learn, TensorFlow, PyTorch)", "weight": 15},
            {"field": "statistics", "criteria": "Strong foundation in statistics and experimental design", "weight": 10},
        ],
        "nice_to_have": [
            {"field": "big_data", "criteria": "Experience with big data tools (Spark, Hadoop)", "weight": 5},
            {"field": "publications", "criteria": "Published research, Kaggle rankings, or technical blog", "weight": 5},
            {"field": "deployment", "criteria": "Experience deploying ML models to production", "weight": 5},
            {"field": "industry", "criteria": "Domain expertise in {industry}", "weight": 5},
        ],
        "red_flags": [
            "Only theoretical knowledge, no practical implementation experience",
            "Cannot explain model choices or trade-offs",
            "No experience with real-world messy data",
            "Cannot communicate findings to non-technical audiences",
        ],
    },
    "ux_designer": {
        "must_have": [
            {"field": "portfolio", "criteria": "Strong portfolio demonstrating user-centered design process", "weight": 25},
            {"field": "experience_years", "criteria": "Minimum {years} years of UX design experience", "weight": 20},
            {"field": "tools", "criteria": "Proficiency with Figma, Sketch, or Adobe XD", "weight": 15},
            {"field": "research", "criteria": "Experience conducting user research and usability testing", "weight": 15},
            {"field": "process", "criteria": "Clear design process from research to deliverable", "weight": 10},
        ],
        "nice_to_have": [
            {"field": "frontend", "criteria": "Front-end development skills (HTML/CSS/JS)", "weight": 5},
            {"field": "design_systems", "criteria": "Experience building or maintaining design systems", "weight": 5},
            {"field": "motion", "criteria": "Motion design or prototyping skills", "weight": 5},
            {"field": "industry", "criteria": "Experience designing for {industry} products", "weight": 5},
        ],
        "red_flags": [
            "Portfolio only contains visual designs without process documentation",
            "Cannot articulate design decisions or user impact",
            "No experience with user research methods",
            "Unable to handle constructive design criticism",
        ],
    },
    "marketing_manager": {
        "must_have": [
            {"field": "experience_years", "criteria": "Minimum {years} years in marketing roles", "weight": 20},
            {"field": "channel_expertise", "criteria": "Proven expertise in {channels}", "weight": 20},
            {"field": "analytics", "criteria": "Data-driven approach with experience in marketing analytics", "weight": 15},
            {"field": "communication", "criteria": "Excellent written and verbal communication skills", "weight": 15},
            {"field": "campaigns", "criteria": "Track record of successful campaign execution", "weight": 10},
        ],
        "nice_to_have": [
            {"field": "automation", "criteria": "Experience with marketing automation platforms (HubSpot, Marketo)", "weight": 10},
            {"field": "saas", "criteria": "B2B SaaS marketing experience", "weight": 5},
            {"field": "budget", "criteria": "Experience managing marketing budgets", "weight": 5},
            {"field": "industry", "criteria": "Domain expertise in {industry}", "weight": 5},
        ],
        "red_flags": [
            "Cannot provide specific campaign results or ROI metrics",
            "No experience with digital marketing analytics tools",
            "Inability to explain marketing strategy vs tactics",
            "No examples of cross-functional collaboration",
        ],
    },
    "sales_representative": {
        "must_have": [
            {"field": "experience_years", "criteria": "Minimum {years} years of B2B sales experience", "weight": 20},
            {"field": "track_record", "criteria": "Proven track record of exceeding sales quotas", "weight": 25},
            {"field": "negotiation", "criteria": "Strong negotiation and closing skills", "weight": 15},
            {"field": "crm", "criteria": "Experience with CRM systems (Salesforce, HubSpot)", "weight": 10},
            {"field": "pipeline", "criteria": "Demonstrated pipeline management capability", "weight": 10},
        ],
        "nice_to_have": [
            {"field": "industry_network", "criteria": "Existing network in {industry}", "weight": 10},
            {"field": "product_expertise", "criteria": "Experience selling {product_type}", "weight": 5},
            {"field": "languages", "criteria": "Multilingual capabilities", "weight": 5},
        ],
        "red_flags": [
            "Cannot provide specific revenue numbers or quota attainment",
            "No experience with consultative/solution selling",
            "Frequently changing industries without clear reason",
            "Cannot articulate their sales process methodology",
        ],
    },
}

GENERAL_CRITERIA = {
    "must_have": [
        {"field": "communication", "criteria": "Clear and professional written communication in resume", "weight": 10},
        {"field": "progression", "criteria": "Clear career progression and growing responsibility", "weight": 10},
        {"field": "achievements", "criteria": "Quantified achievements and measurable impact", "weight": 15},
    ],
    "nice_to_have": [
        {"field": "certifications", "criteria": "Relevant professional certifications", "weight": 5},
        {"field": "continuous_learning", "criteria": "Evidence of ongoing professional development", "weight": 5},
        {"field": "cultural_fit", "criteria": "Alignment with company values and mission", "weight": 10},
    ],
    "red_flags": [
        "Unexplained employment gaps exceeding 6 months",
        "Significant inconsistencies in dates or responsibilities",
        "Typos and grammatical errors in resume",
        "Generic resume not tailored to the role",
    ],
}


def generate_screening(role: str, years: str = "3", languages: str = "Python, Java, JavaScript",
                       frameworks: str = "React, Django, Spring Boot", industry: str = "technology",
                       channels: str = "digital marketing, content marketing, SEO",
                       product_type: str = "SaaS products") -> dict:
    """Generate screening criteria for a given role."""
    result = {"role": role, "screening_criteria": {}}

    if role in SCREENING_TEMPLATES:
        role_data = SCREENING_TEMPLATES[role]
        result["screening_criteria"]["role_specific"] = {
            "must_have": [
                {**item, "criteria": item["criteria"].format(years=years, languages=languages,
                                                             frameworks=frameworks, industry=industry,
                                                             channels=channels, product_type=product_type)}
                for item in role_data["must_have"]
            ],
            "nice_to_have": [
                {**item, "criteria": item["criteria"].format(years=years, industry=industry,
                                                             product_type=product_type)}
                for item in role_data["nice_to_have"]
            ],
            "red_flags": role_data["red_flags"],
        }

    result["screening_criteria"]["general"] = GENERAL_CRITERIA
    result["scoring_guide"] = {
        "total_possible": 100,
        "pass_threshold": 65,
        "shortlist_threshold": 80,
        "scoring_method": "Sum weights of all met criteria. Must-have items carry more weight.",
        "auto_reject": "Any red flag triggered → manual review required. Multiple red flags → reject.",
    }

    return result


def format_screening(criteria: dict) -> str:
    """Format screening criteria as readable markdown."""
    lines = []
    lines.append(f"# Resume Screening Criteria: {criteria['role'].replace('_', ' ').title()}")
    lines.append("")

    # Role-specific
    if "role_specific" in criteria["screening_criteria"]:
        rs = criteria["screening_criteria"]["role_specific"]
        lines.append("## Must-Have Requirements")
        lines.append("| # | Field | Criteria | Weight |")
        lines.append("|---|-------|----------|--------|")
        for i, item in enumerate(rs["must_have"], 1):
            lines.append(f"| {i} | {item['field']} | {item['criteria']} | {item['weight']} |")
        lines.append("")

        lines.append("## Nice to Have")
        for i, item in enumerate(rs["nice_to_have"], 1):
            lines.append(f"{i}. **{item['field']}**: {item['criteria']} (Weight: {item['weight']})")
        lines.append("")

        lines.append("## 🚩 Red Flags")
        for flag in rs["red_flags"]:
            lines.append(f"- {flag}")
        lines.append("")

    # General
    gen = criteria["screening_criteria"]["general"]
    lines.append("## General Requirements")
    lines.append("### Must-Have")
    for item in gen["must_have"]:
        lines.append(f"- **{item['field']}**: {item['criteria']} (Weight: {item['weight']})")
    lines.append("")

    lines.append("### Nice to Have")
    for item in gen["nice_to_have"]:
        lines.append(f"- **{item['field']}**: {item['criteria']} (Weight: {item['weight']})")
    lines.append("")

    lines.append("### 🚩 General Red Flags")
    for flag in gen["red_flags"]:
        lines.append(f"- {flag}")
    lines.append("")

    # Scoring
    sg = criteria["scoring_guide"]
    lines.append("## Scoring Guide")
    lines.append(f"- **Total Possible Score**: {sg['total_possible']}")
    lines.append(f"- **Pass Threshold**: {sg['pass_threshold']}")
    lines.append(f"- **Shortlist Threshold**: {sg['shortlist_threshold']}")
    lines.append(f"- **Method**: {sg['scoring_method']}")
    lines.append(f"- **Auto-Reject**: {sg['auto_reject']}")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by HireMate AI Recruiting Assistant*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate resume screening criteria")
    parser.add_argument("--role", required=True, help="Role (software_engineer, product_manager, data_scientist, ux_designer, marketing_manager, sales_representative)")
    parser.add_argument("--years", default="3", help="Minimum years of experience")
    parser.add_argument("--languages", default="Python, Java, JavaScript", help="Required programming languages (for tech roles)")
    parser.add_argument("--frameworks", default="React, Django", help="Required frameworks (for tech roles)")
    parser.add_argument("--industry", default="technology", help="Industry domain")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--output", help="Output file path (default: stdout)")

    args = parser.parse_args()

    criteria = generate_screening(
        role=args.role, years=args.years, languages=args.languages,
        frameworks=args.frameworks, industry=args.industry,
    )

    if args.format == "json":
        output = json.dumps(criteria, indent=2, ensure_ascii=False)
    else:
        output = format_screening(criteria)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Screening criteria saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
