#!/usr/bin/env python3
"""
MAGI Risk Matrix Generator
===========================
Generates 5x5 probability-impact risk matrices in terminal text and HTML formats.

INTERFACE CONTRACT
==================
Input:  Command-line arguments (optional --html, --output=PATH, --json flags); sample data is hardcoded
Output: Risk matrix to stdout (text mode) or HTML file (HTML mode); optional JSON to stdout
Side effects: File write to output_path when --html is specified
Exit codes: 0 = success, 1 = input validation error, 2 = runtime error
Dependencies: Python standard library only
"""

import argparse
import json
import sys


# Risk level definitions
RISK_LEVELS = {
    "red":    {"range": (20, 25), "label": "Critical", "action": "Escalate immediately, consider suspending related activities"},
    "orange": {"range": (12, 19), "label": "High",     "action": "Develop specialized mitigation plan, monitor closely"},
    "yellow": {"range": (5, 11),  "label": "Medium",   "action": "Routine monitoring, prepare contingency plans"},
    "green":  {"range": (1, 4),   "label": "Low",      "action": "Accept risk, periodic review"},
}

PROBABILITY_LABELS = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Very High"}
IMPACT_LABELS = {1: "Negligible", 2: "Minor", 3: "Moderate", 4: "Severe", 5: "Catastrophic"}


def classify_risk(score: int) -> dict:
    """Classify a risk score into severity level."""
    for level, info in RISK_LEVELS.items():
        if info["range"][0] <= score <= info["range"][1]:
            return {"level": level, **info}
    return {"level": "unknown", "label": "Unknown", "action": "Requires manual assessment"}


def build_risk_entry(name, probability, impact, domain="", source="", reversibility="", detectability="", mitigation=""):
    """Build a risk entry dictionary."""
    if not (1 <= probability <= 5):
        raise ValueError(f"Probability must be 1-5, got {probability}")
    if not (1 <= impact <= 5):
        raise ValueError(f"Impact must be 1-5, got {impact}")

    score = probability * impact
    risk_info = classify_risk(score)
    return {
        "name": name,
        "domain": domain,
        "source": source,
        "probability": probability,
        "probability_label": PROBABILITY_LABELS.get(probability, "Unknown"),
        "impact": impact,
        "impact_label": IMPACT_LABELS.get(impact, "Unknown"),
        "score": score,
        "risk_level": risk_info["level"],
        "risk_label": risk_info["label"],
        "action": risk_info["action"],
        "reversibility": reversibility,
        "detectability": detectability,
        "mitigation": mitigation,
    }


def generate_text_matrix(risks: list) -> str:
    """Generate terminal text format risk matrix."""
    lines = []
    lines.append("=" * 70)
    lines.append("  MAGI Risk Matrix")
    lines.append("=" * 70)

    # 5x5 matrix grid
    lines.append("")
    lines.append("  Impact ->")
    lines.append("  Prob  |  Negl(1)  Minor(2)  Moderate(3)  Severe(4)  Catast(5)")
    lines.append("  " + "-" * 62)

    for p in range(5, 0, -1):
        row = f"  {PROBABILITY_LABELS[p]}({p}) |"
        for i in range(1, 6):
            score = p * i
            info = classify_risk(score)
            row += f"  {score:>2}({info['level'][:3]})  "
        lines.append(row)

    lines.append("  " + "-" * 62)

    # Risk list
    lines.append("")
    lines.append("  Risk List (sorted by severity)")
    lines.append("  " + "-" * 62)

    sorted_risks = sorted(risks, key=lambda r: r["score"], reverse=True)
    for i, r in enumerate(sorted_risks, 1):
        lines.append(f"  {i}. {r['name']}")
        lines.append(f"     Score: {r['score']} ({r['risk_label']})")
        lines.append(f"     Probability: {r['probability_label']}({r['probability']}) x Impact: {r['impact_label']}({r['impact']})")
        if r["domain"]:
            lines.append(f"     Domain: {r['domain']} | Source: {r['source']}")
        if r["reversibility"]:
            lines.append(f"     Reversibility: {r['reversibility']} | Detectability: {r['detectability']}")
        if r["mitigation"]:
            lines.append(f"     Mitigation: {r['mitigation']}")
        lines.append(f"     Action: {r['action']}")
        lines.append("")

    # Summary
    level_counts = {"red": 0, "orange": 0, "yellow": 0, "green": 0}
    for r in risks:
        level_counts[r["risk_level"]] = level_counts.get(r["risk_level"], 0) + 1

    lines.append("  " + "-" * 62)
    lines.append("  Summary")
    lines.append(f"  Critical: {level_counts['red']} items")
    lines.append(f"  High:     {level_counts['orange']} items")
    lines.append(f"  Medium:   {level_counts['yellow']} items")
    lines.append(f"  Low:      {level_counts['green']} items")
    lines.append(f"  Total:    {len(risks)} items")

    # Veto warning
    red_count = level_counts["red"]
    if red_count > 0:
        lines.append("")
        lines.append(f"  VETO WARNING: {red_count} critical risk(s) found. Recommend suspending decision until risks are mitigated.")

    lines.append("=" * 70)
    return "\n".join(lines)


def generate_html_matrix(risks: list, output_path: str = "risk_matrix.html") -> str:
    """Generate HTML risk matrix visualization."""
    # Build 5x5 grid data
    grid = {}
    for r in risks:
        key = (r["probability"], r["impact"])
        if key not in grid:
            grid[key] = []
        grid[key].append(r)

    color_map = {
        "red": "#e74c3c",
        "orange": "#e67e22",
        "yellow": "#f1c40f",
        "green": "#2ecc71",
    }

    html = []
    html.append('<!DOCTYPE html>')
    html.append('<html lang="en">')
    html.append('<head>')
    html.append('<meta charset="UTF-8">')
    html.append('<title>MAGI Risk Matrix</title>')
    html.append('<style>')
    html.append('body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 40px; }')
    html.append('h1 { text-align: center; color: #e94560; }')
    html.append('.matrix-container { display: flex; justify-content: center; margin: 30px 0; }')
    html.append('table { border-collapse: collapse; }')
    html.append('th, td { width: 100px; height: 60px; text-align: center; border: 2px solid #333; font-size: 14px; }')
    html.append('th { background: #16213e; color: #e94560; }')
    html.append('.cell-red { background: rgba(231,76,60,0.3); }')
    html.append('.cell-orange { background: rgba(230,126,34,0.3); }')
    html.append('.cell-yellow { background: rgba(241,196,15,0.2); }')
    html.append('.cell-green { background: rgba(46,204,113,0.2); }')
    html.append('.risk-list { max-width: 800px; margin: 30px auto; }')
    html.append('.risk-card { background: #16213e; border-radius: 8px; padding: 16px; margin: 12px 0; border-left: 4px solid #e94560; }')
    html.append('.risk-card.orange { border-left-color: #e67e22; }')
    html.append('.risk-card.yellow { border-left-color: #f1c40f; }')
    html.append('.risk-card.green { border-left-color: #2ecc71; }')
    html.append('.risk-card h3 { margin: 0 0 8px 0; }')
    html.append('.risk-card .meta { color: #aaa; font-size: 13px; }')
    html.append('.summary { text-align: center; margin: 30px 0; font-size: 18px; }')
    html.append('.summary span { margin: 0 15px; }')
    html.append('</style>')
    html.append('</head>')
    html.append('<body>')
    html.append('<h1>MAGI Risk Matrix</h1>')

    # Matrix table
    html.append('<div class="matrix-container"><table>')
    html.append('<tr><th>Prob / Impact</th>')
    for i in range(1, 6):
        html.append(f'<th>{IMPACT_LABELS[i]}({i})</th>')
    html.append('</tr>')

    for p in range(5, 0, -1):
        html.append(f'<tr><th>{PROBABILITY_LABELS[p]}({p})</th>')
        for i in range(1, 6):
            score = p * i
            info = classify_risk(score)
            cell_class = f"cell-{info['level']}"
            risks_in_cell = grid.get((p, i), [])
            count = len(risks_in_cell)
            cell_content = f"{score}"
            if count > 0:
                cell_content += f" ({count})"
            html.append(f'<td class="{cell_class}">{cell_content}</td>')
        html.append('</tr>')

    html.append('</table></div>')

    # Summary
    level_counts = {"red": 0, "orange": 0, "yellow": 0, "green": 0}
    for r in risks:
        level_counts[r["risk_level"]] = level_counts.get(r["risk_level"], 0) + 1

    html.append('<div class="summary">')
    html.append(f'<span>Critical: {level_counts["red"]}</span>')
    html.append(f'<span>High: {level_counts["orange"]}</span>')
    html.append(f'<span>Medium: {level_counts["yellow"]}</span>')
    html.append(f'<span>Low: {level_counts["green"]}</span>')
    html.append('</div>')

    # Risk cards
    html.append('<div class="risk-list">')
    sorted_risks = sorted(risks, key=lambda r: r["score"], reverse=True)
    for r in sorted_risks:
        card_class = r["risk_level"]
        html.append(f'<div class="risk-card {card_class}">')
        html.append(f'<h3>{r["name"]} <small>(Score: {r["score"]})</small></h3>')
        html.append('<div class="meta">')
        html.append(f'Probability: {r["probability_label"]} x Impact: {r["impact_label"]} | ')
        if r["domain"]:
            html.append(f'Domain: {r["domain"]} | ')
        if r["source"]:
            html.append(f'Source: {r["source"]} | ')
        if r["reversibility"]:
            html.append(f'Reversibility: {r["reversibility"]}')
        html.append('</div>')
        if r["mitigation"]:
            html.append(f'<p>Mitigation: {r["mitigation"]}</p>')
        html.append(f'<p><strong>Action:</strong> {r["action"]}</p>')
        html.append('</div>')

    html.append('</div>')
    html.append('</body></html>')

    html_content = "\n".join(html)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate a MAGI risk matrix.")
    parser.add_argument("--html", action="store_true", help="Write an HTML risk matrix.")
    parser.add_argument("--output", default="risk_matrix.html", help="HTML output path.")
    parser.add_argument("--json", action="store_true", help="Also print JSON risk data.")
    args = parser.parse_args()
    try:
        # Sample risk data
        sample_risks = [
            build_risk_entry(
                name="Key personnel departure",
                probability=3, impact=5,
                domain="Execution",
                source="BALTHASAR",
                reversibility="Partially reversible",
                detectability="Early warning",
                mitigation="Build knowledge documentation, develop backup candidates",
            ),
            build_risk_entry(
                name="Regulatory policy shift",
                probability=2, impact=5,
                domain="Compliance",
                source="BALTHASAR",
                reversibility="Irreversible",
                detectability="Post-event only",
                mitigation="Maintain compliance buffer, establish policy tracking mechanism",
            ),
            build_risk_entry(
                name="Competitor launches similar product first",
                probability=4, impact=3,
                domain="Timing",
                source="CASPER",
                reversibility="Irreversible",
                detectability="Early warning",
                mitigation="Accelerate MVP launch, strengthen differentiation",
            ),
            build_risk_entry(
                name="Budget overrun",
                probability=3, impact=3,
                domain="Financial",
                source="MELCHIOR",
                reversibility="Partially reversible",
                detectability="Early warning",
                mitigation="Implement phased budget review gates, maintain 15% contingency reserve",
            ),
            build_risk_entry(
                name="Team morale decline",
                probability=3, impact=2,
                domain="Human",
                source="CASPER",
                reversibility="Reversible",
                detectability="Post-event only",
                mitigation="Regular 1-on-1 communications, milestone celebration checkpoints",
            ),
        ]

        # Determine output mode
        if args.html:
            result = generate_html_matrix(sample_risks, args.output)
            print(f"HTML risk matrix generated: {result}")
        else:
            print(generate_text_matrix(sample_risks))

        # Optional JSON output
        if args.json:
            print()
            print("--- JSON Output ---")
            print(json.dumps(sample_risks, ensure_ascii=False, indent=2))

        return 0

    except ValueError as e:
        print(f"Input validation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Runtime error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
    
