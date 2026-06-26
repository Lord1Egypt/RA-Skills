#!/usr/bin/env python3
"""
Generate an HTML leaderboard from skill cards.

Usage:
    python3 generate_leaderboard.py --cards-dir skill-cards --output leaderboard/index.html

This script reads all skill card markdown files from the cards directory
and generates a sortable HTML leaderboard.
"""

import argparse
import os
import re
import sys
from pathlib import Path


def parse_skill_card(filepath):
    """Parse a skill card markdown file and extract metadata."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return None
    
    card = {
        "file": os.path.basename(filepath),
        "path": str(filepath),
        "name": "Unknown",
        "slug": "unknown",
        "eval_date": "N/A",
        "model": "N/A",
        "overall_score": 0,
        "quality": 0,
        "delta": 0,
        "efficiency": 0,
        "recommendation": "N/A",
        "strengths": [],
        "weaknesses": [],
    }
    
    # Extract skill name
    match = re.search(r'\*\*Skill\*\*:\s*(.+)', content)
    if match:
        card["name"] = match.group(1).strip()
    
    # Extract slug
    match = re.search(r'\*\*Slug\*\*:\s*(.+)', content)
    if match:
        card["slug"] = match.group(1).strip()
    
    # Extract eval date
    match = re.search(r'\*\*Eval Date\*\*:\s*(.+)', content)
    if match:
        card["eval_date"] = match.group(1).strip()
    
    # Extract model
    match = re.search(r'\*\*Model\*\*:\s*(.+)', content)
    if match:
        card["model"] = match.group(1).strip()
    
    # Extract overall score
    match = re.search(r'\*\*Overall:\s*(\d+)/10\*\*', content)
    if match:
        card["overall_score"] = int(match.group(1))
    
    # Extract component scores
    score_matches = re.findall(r'\|\s*(\w+)\s*\|\s*(\d+)\s*\|', content)
    for name, score in score_matches:
        if name == "Quality":
            card["quality"] = int(score)
        elif name == "Delta":
            card["delta"] = int(score)
        elif name == "Efficiency":
            card["efficiency"] = int(score)
    
    # Extract recommendation
    match = re.search(r'#{1,3}\s*[✅⚠️⚡❌]\s*\*\*(Recommended|Conditional|Marginal|Not Recommended)\*\*', content)
    if match:
        card["recommendation"] = match.group(1)
    
    # Extract strengths
    strengths_section = re.search(r'## Strengths\s*\n\s*\n(.*?)(?=\n##|\n---)', content, re.DOTALL)
    if strengths_section:
        strengths = re.findall(r'✅\s*(.+)', strengths_section.group(1))
        card["strengths"] = [s.strip() for s in strengths]
    
    # Extract weaknesses
    weaknesses_section = re.search(r'## Weaknesses\s*\n\s*\n(.*?)(?=\n##|\n---)', content, re.DOTALL)
    if weaknesses_section:
        weaknesses = re.findall(r'❌\s*(.+)', weaknesses_section.group(1))
        card["weaknesses"] = [w.strip() for w in weaknesses]
    
    return card


def generate_html(cards, args):
    """Generate HTML leaderboard from cards data."""
    
    # Sort cards by overall score (descending)
    cards.sort(key=lambda x: x.get("overall_score", 0), reverse=True)
    
    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='zh-CN'>")
    html.append("<head>")
    html.append("  <meta charset='UTF-8'>")
    html.append("  <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
    html.append(f"  <title>Skill Leaderboard | {args.title}</title>")
    html.append("  <style>")
    html.append("    * { box-sizing: border-box; margin: 0; padding: 0; }")
    html.append("    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;")
    html.append("          background: #f5f5f5; color: #333; padding: 20px; }")
    html.append("    .container { max-width: 1200px; margin: 0 auto; }")
    html.append("    h1 { text-align: center; margin-bottom: 30px; color: #1a1a2e; }")
    html.append("    .stats { display: flex; justify-content: center; gap: 40px; margin-bottom: 30px; }")
    html.append("    .stat { text-align: center; }")
    html.append("    .stat-value { font-size: 2em; font-weight: bold; color: #4361ee; }")
    html.append("    .stat-label { color: #666; font-size: 0.9em; }")
    html.append("    table { width: 100%; background: white; border-radius: 10px;")
    html.append("           box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }")
    html.append("    th { background: #4361ee; color: white; padding: 15px; text-align: left; }")
    html.append("    td { padding: 12px 15px; border-bottom: 1px solid #eee; }")
    html.append("    tr:hover { background: #f8f9fa; }")
    html.append("    .score { font-weight: bold; font-size: 1.2em; }")
    html.append("    .score-high { color: #22c55e; }")
    html.append("    .score-mid { color: #f59e0b; }")
    html.append("    .score-low { color: #ef4444; }")
    html.append("    .badge { display: inline-block; padding: 4px 10px; border-radius: 20px;")
    html.append("             font-size: 0.8em; font-weight: 500; }")
    html.append("    .badge-recommended { background: #dcfce7; color: #166534; }")
    html.append("    .badge-conditional { background: #fef9c3; color: #854d0e; }")
    html.append("    .badge-marginal { background: #fed7aa; color: #9a3412; }")
    html.append("    .badge-not-recommended { background: #fee2e2; color: #991b1b; }")
    html.append("    .strengths, .weaknesses { font-size: 0.85em; color: #666; }")
    html.append("    .sort-btn { background: none; border: none; color: inherit; cursor: pointer;")
    html.append("              font-weight: inherit; padding: 0; }")
    html.append("    .sort-btn:hover { color: white; }")
    html.append("    .footer { text-align: center; margin-top: 20px; color: #666; font-size: 0.9em; }")
    html.append("  </style>")
    html.append("</head>")
    html.append("<body>")
    html.append("  <div class='container'>")
    html.append(f"    <h1>{args.title}</h1>")
    html.append("    <div class='stats'>")
    html.append(f"      <div class='stat'><div class='stat-value'>{len(cards)}</div><div class='stat-label'>已评估技能</div></div>")
    
    recommended = sum(1 for c in cards if c.get("recommendation") == "Recommended")
    html.append(f"      <div class='stat'><div class='stat-value'>{recommended}</div><div class='stat-label'>推荐使用</div></div>")
    
    avg_score = sum(c.get("overall_score", 0) for c in cards) / max(len(cards), 1)
    html.append(f"      <div class='stat'><div class='stat-value'>{avg_score:.1f}</div><div class='stat-label'>平均分</div></div>")
    
    html.append("    </div>")
    html.append("    <table id='leaderboard'>")
    html.append("      <thead>")
    html.append("        <tr>")
    html.append("          <th>#</th>")
    html.append("          <th>技能名称</th>")
    html.append("          <th>Slug</th>")
    html.append("          <th>总分</th>")
    html.append("          <th>质量</th>")
    html.append("          <th>提升</th>")
    html.append("          <th>效率</th>")
    html.append("          <th>推荐</th>")
    html.append("          <th>评估日期</th>")
    html.append("          <th>优劣势</th>")
    html.append("        </tr>")
    html.append("      </thead>")
    html.append("      <tbody>")
    
    for i, card in enumerate(cards, 1):
        score = card.get("overall_score", 0)
        if score >= 7:
            score_class = "score-high"
        elif score >= 5:
            score_class = "score-mid"
        else:
            score_class = "score-low"
        
        rec = card.get("recommendation", "N/A")
        badge_class = f"badge-{rec.lower().replace(' ', '-')}"
        
        strengths = ", ".join(card.get("strengths", [])[:2]) if card.get("strengths") else "-"
        weaknesses = ", ".join(card.get("weaknesses", [])[:2]) if card.get("weaknesses") else "-"
        
        html.append("        <tr>")
        html.append(f"          <td>{i}</td>")
        html.append(f"          <td><strong>{card.get('name', 'Unknown')}</strong></td>")
        html.append(f"          <td>{card.get('slug', 'N/A')}</td>")
        html.append(f"          <td class='score {score_class}'>{score}/10</td>")
        html.append(f"          <td>{card.get('quality', 0)}/5</td>")
        html.append(f"          <td>{card.get('delta', 0)}/3</td>")
        html.append(f"          <td>{card.get('efficiency', 0)}/2</td>")
        html.append(f"          <td><span class='badge {badge_class}'>{rec}</span></td>")
        html.append(f"          <td>{card.get('eval_date', 'N/A')}</td>")
        html.append(f"          <td><div class='strengths'>👍 {strengths}</div><div class='weaknesses'>👎 {weaknesses}</div></td>")
        html.append("        </tr>")
    
    html.append("      </tbody>")
    html.append("    </table>")
    html.append(f"    <div class='footer'>Generated by multi-skill-eval v1.0.0 | {len(cards)} skills evaluated</div>")
    html.append("  </div>")
    html.append("</body>")
    html.append("</html>")
    
    return "\n".join(html)


def main():
    parser = argparse.ArgumentParser(
        description="Generate an HTML leaderboard from skill cards"
    )
    parser.add_argument(
        "--cards-dir", "-c", required=True,
        help="Directory containing skill card markdown files"
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Output HTML file path"
    )
    parser.add_argument(
        "--title", "-t", default="OpenClaw Skill Leaderboard",
        help="Leaderboard title"
    )
    args = parser.parse_args()
    
    cards_dir = Path(args.cards_dir)
    if not cards_dir.exists():
        print(f"Error: Cards directory not found: {cards_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Find all markdown files
    card_files = list(cards_dir.glob("*.md"))
    
    if not card_files:
        print(f"Warning: No skill card files found in {cards_dir}", file=sys.stderr)
        # Generate empty leaderboard
        cards = []
    else:
        # Parse each card
        cards = []
        for filepath in card_files:
            card = parse_skill_card(filepath)
            if card:
                cards.append(card)
    
    # Generate HTML
    html = generate_html(cards, args)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Leaderboard generated: {args.output}")
    print(f"  Total skills: {len(cards)}")


if __name__ == "__main__":
    main()
