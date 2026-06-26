#!/usr/bin/env bash
# generate-budget-report.sh — Generate a visual budget report as PNG/PDF
# Usage: ./generate-budget-report.sh [YYYY-MM] [output_format]
# Example: ./generate-budget-report.sh 2026-03 png
#
# Requires: Python 3.8+, Playwright (pip install playwright && playwright install chromium)
# Output: reports/budget-report-YYYY-MM.{png|pdf}

set -euo pipefail
umask 077

# --- Workspace root detection ---
find_skill_root() {
    # Stay within the skill directory — do not traverse outside
    cd "$(dirname "$0")/.." && pwd
}

SKILL_DIR="$(find_skill_root)"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
REPORTS_DIR="$SKILL_DIR/reports"

# --- Args ---
PERIOD="${1:-$(date +%Y-%m)}"
FORMAT="${2:-png}"

if [[ ! "$PERIOD" =~ ^[0-9]{4}-(0[1-9]|1[0-2])$ ]]; then
    echo "Error: Invalid period '$PERIOD'. Expected YYYY-MM."
    exit 1
fi

if [[ "$FORMAT" != "png" && "$FORMAT" != "pdf" ]]; then
    echo "Error: Invalid format '$FORMAT'. Use 'png' or 'pdf'."
    exit 1
fi

# --- Validate ---
if [ ! -f "$DATA_DIR/transactions/$PERIOD.json" ]; then
    echo "Error: No transaction data found for $PERIOD"
    echo "Expected file: data/transactions/$PERIOD.json"
    exit 1
fi

if [ ! -f "$DATA_DIR/budget.json" ]; then
    echo "Error: No budget found. Create one first."
    exit 1
fi

mkdir -p "$REPORTS_DIR"

# --- Generate HTML report ---
REPORT_HTML="$(mktemp -t "budget-report-$PERIOD.XXXXXX.html")"
trap 'rm -f "$REPORT_HTML"' EXIT

python3 - "$DATA_DIR" "$PERIOD" "$REPORT_HTML" << 'PYTHON_SCRIPT'
import json
import sys
import html
from pathlib import Path
from datetime import datetime

data_dir = Path(sys.argv[1])
period = sys.argv[2]
output_path = sys.argv[3]

# Load data
with open(data_dir / "budget.json") as f:
    budget = json.load(f)

with open(data_dir / "transactions" / f"{period}.json") as f:
    tx_data = json.load(f)

transactions = tx_data.get("transactions", [])

# Load savings goals if present
goals = []
goals_path = data_dir / "savings-goals.json"
if goals_path.exists():
    with open(goals_path) as f:
        goals = json.load(f)

# Calculate category totals
category_totals = {}
total_income = 0
total_expenses = 0

for tx in transactions:
    cat = tx.get("category", "Uncategorized")
    amt = tx.get("amount", 0)
    if amt > 0:
        total_income += amt
    else:
        total_expenses += abs(amt)
        category_totals[cat] = category_totals.get(cat, 0) + abs(amt)

# Build budget comparison
budget_cats = {c["name"]: c["limit"] for c in budget.get("categories", [])}

# Generate HTML
month_label = datetime.strptime(period, "%Y-%m").strftime("%B %Y")
currency = budget.get("currency", "USD")
symbol = "$" if currency == "USD" else currency + " "

rows = ""
for cat_name, spent in sorted(category_totals.items(), key=lambda x: -x[1]):
    cat_label = html.escape(str(cat_name))
    limit = budget_cats.get(cat_name, 0)
    pct = (spent / limit * 100) if limit > 0 else 0
    color = "#22c55e" if pct < 80 else "#eab308" if pct < 100 else "#ef4444"
    bar_width = min(pct, 100)
    rows += f"""
    <tr>
        <td>{cat_label}</td>
        <td class="num">{symbol}{spent:,.2f}</td>
        <td class="num">{symbol}{limit:,.2f}</td>
        <td>
            <div class="bar-bg"><div class="bar" style="width:{bar_width}%;background:{color}"></div></div>
        </td>
        <td class="num" style="color:{color}">{pct:.0f}%</td>
    </tr>"""

goal_rows = ""
for g in goals:
    if g.get("status") == "active":
        goal_name = html.escape(str(g.get("name", "Untitled Goal")))
        pct = (g["current_amount"] / g["target_amount"] * 100) if g["target_amount"] > 0 else 0
        goal_rows += f"""
        <div class="goal">
            <div class="goal-name">{goal_name}</div>
            <div class="goal-bar-bg"><div class="goal-bar" style="width:{min(pct,100)}%"></div></div>
            <div class="goal-label">{symbol}{g['current_amount']:,.0f} / {symbol}{g['target_amount']:,.0f} ({pct:.1f}%)</div>
        </div>"""

net = total_income - total_expenses

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; background:#0f172a; color:#e2e8f0; padding:32px; width:960px; }}
  h1 {{ color:#14b8a6; font-size:28px; margin-bottom:4px; }}
  .subtitle {{ color:#94a3b8; font-size:14px; margin-bottom:24px; }}
  .cards {{ display:flex; gap:16px; margin-bottom:24px; }}
  .card {{ flex:1; background:#1e293b; border-radius:12px; padding:20px; }}
  .card-label {{ color:#94a3b8; font-size:12px; text-transform:uppercase; letter-spacing:1px; }}
  .card-value {{ font-size:28px; font-weight:700; margin-top:4px; }}
  .income {{ color:#22c55e; }}
  .expense {{ color:#f97316; }}
  .net {{ color:#14b8a6; }}
  table {{ width:100%; border-collapse:collapse; margin-bottom:24px; }}
  th {{ text-align:left; color:#94a3b8; font-size:12px; text-transform:uppercase; letter-spacing:1px; padding:8px 12px; border-bottom:1px solid #334155; }}
  td {{ padding:10px 12px; border-bottom:1px solid #1e293b; font-size:14px; }}
  .num {{ text-align:right; font-variant-numeric:tabular-nums; }}
  .bar-bg {{ background:#334155; border-radius:4px; height:8px; width:120px; }}
  .bar {{ border-radius:4px; height:8px; }}
  .section-title {{ color:#14b8a6; font-size:18px; margin:24px 0 12px; }}
  .goal {{ background:#1e293b; border-radius:8px; padding:16px; margin-bottom:8px; }}
  .goal-name {{ font-weight:600; margin-bottom:6px; }}
  .goal-bar-bg {{ background:#334155; border-radius:4px; height:10px; margin-bottom:6px; }}
  .goal-bar {{ background:#14b8a6; border-radius:4px; height:10px; }}
  .goal-label {{ color:#94a3b8; font-size:13px; }}
  .footer {{ color:#475569; font-size:11px; margin-top:24px; text-align:center; }}
</style></head><body>
<h1>💰 Budget Report — {month_label}</h1>
<div class="subtitle">Generated by Budget Buddy Pro</div>

<div class="cards">
  <div class="card"><div class="card-label">Income</div><div class="card-value income">{symbol}{total_income:,.2f}</div></div>
  <div class="card"><div class="card-label">Expenses</div><div class="card-value expense">{symbol}{total_expenses:,.2f}</div></div>
  <div class="card"><div class="card-label">Net</div><div class="card-value net">{symbol}{net:,.2f}</div></div>
</div>

<div class="section-title">Budget vs. Actual</div>
<table>
  <tr><th>Category</th><th class="num">Spent</th><th class="num">Budget</th><th>Progress</th><th class="num">%</th></tr>
  {rows}
</table>

{"<div class='section-title'>Savings Goals</div>" + goal_rows if goal_rows else ""}

<div class="footer">Budget Buddy Pro &bull; Financial tracking tool, not financial advice &bull; {datetime.now().strftime('%Y-%m-%d')}</div>
</body></html>"""

with open(output_path, "w") as f:
    f.write(html)

print(f"HTML report generated: {output_path}")
PYTHON_SCRIPT

# --- Render with Playwright ---
OUTPUT_FILE="$REPORTS_DIR/budget-report-$PERIOD.$FORMAT"

python3 - "$REPORT_HTML" "$OUTPUT_FILE" "$FORMAT" << 'RENDER_SCRIPT'
import sys
from playwright.sync_api import sync_playwright

html_path = sys.argv[1]
output_path = sys.argv[2]
fmt = sys.argv[3]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 960, "height": 1200})
    page.goto(f"file://{html_path}")
    page.wait_for_load_state("networkidle")

    if fmt == "pdf":
        page.pdf(path=output_path, format="A4", print_background=True)
    else:
        page.screenshot(path=output_path, full_page=True)

    browser.close()
    print(f"Report saved: {output_path}")
RENDER_SCRIPT

echo "✅ Budget report generated: $OUTPUT_FILE"
