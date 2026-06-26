#!/usr/bin/env bash
# budget-report.sh — Generate a budget summary report for a party event
# Usage: ./budget-report.sh <event-slug> [output_format]
# Example: ./budget-report.sh sarah-30th-birthday png
# Output: reports/budget-report-EVENT_SLUG.{md|png}
#
# Requires: Python 3.8+ (for JSON parsing)
# Optional: Playwright (pip install playwright && playwright install chromium) for PNG output

set -euo pipefail
umask 077

# --- Workspace root detection ---
find_workspace_root() {
    local dir="$PWD"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/AGENTS.md" ] || [ -f "$dir/SOUL.md" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "$PWD"
    return 1
}

WORKSPACE_ROOT="$(find_workspace_root)"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$SKILL_DIR/data"
REPORTS_DIR="$WORKSPACE_ROOT/reports"

# --- Args ---
if [ $# -lt 1 ]; then
    echo "Usage: $0 <event-slug> [md|png]"
    echo "Example: $0 sarah-30th-birthday png"
    exit 1
fi

EVENT_SLUG="$1"
FORMAT="${2:-md}"

# --- Input validation ---
if [[ ! "$EVENT_SLUG" =~ ^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$ ]]; then
    echo "Error: Invalid event slug '$EVENT_SLUG'."
    exit 1
fi

if [[ "$FORMAT" != "md" && "$FORMAT" != "png" ]]; then
    echo "Error: Invalid format '$FORMAT'. Use 'md' or 'png'."
    exit 1
fi

EVENT_FILE="$DATA_DIR/events/$EVENT_SLUG.json"
BUDGET_FILE="$DATA_DIR/events/$EVENT_SLUG/budget.json"

if [ ! -f "$EVENT_FILE" ]; then
    echo "Error: Event '$EVENT_SLUG' not found at $EVENT_FILE"
    exit 1
fi

if [ ! -f "$BUDGET_FILE" ]; then
    echo "Error: No budget data found for '$EVENT_SLUG'"
    echo "Expected: $BUDGET_FILE"
    exit 1
fi

mkdir -p "$REPORTS_DIR"
chmod 700 "$REPORTS_DIR"
TMP_DIR="$WORKSPACE_ROOT/.tmp"
mkdir -p "$TMP_DIR"
chmod 700 "$TMP_DIR"

# --- Generate report ---
EVENT_FILE_ENV="$EVENT_FILE" \
BUDGET_FILE_ENV="$BUDGET_FILE" \
REPORTS_DIR_ENV="$REPORTS_DIR" \
EVENT_SLUG_ENV="$EVENT_SLUG" \
FORMAT_ENV="$FORMAT" \
TMP_DIR_ENV="$TMP_DIR" \
python3 << 'PYEOF'
import json, os
from datetime import datetime
from pathlib import Path

event_file = os.environ["EVENT_FILE_ENV"]
budget_file = os.environ["BUDGET_FILE_ENV"]
reports_dir = os.environ["REPORTS_DIR_ENV"]
event_slug = os.environ["EVENT_SLUG_ENV"]
fmt = os.environ["FORMAT_ENV"]
tmp_dir = os.environ["TMP_DIR_ENV"]

with open(event_file) as f:
    event = json.load(f)
with open(budget_file) as f:
    budget = json.load(f)

event_name = event.get("name", event_slug)
total_budget = budget.get("total_budget", 0)
total_spent = budget.get("total_spent", 0)
total_remaining = budget.get("total_remaining", total_budget - total_spent)
cost_per_head = budget.get("cost_per_head", 0)
confirmed = budget.get("confirmed_guests", event.get("guest_count_estimate", 0))
categories = budget.get("categories", [])

# Generate markdown report
lines = []
lines.append(f"# 💰 Budget Report: {event_name}")
lines.append(f"*Generated {datetime.now().strftime('%B %d, %Y')}*")
lines.append(f"")
lines.append(f"## Summary")
lines.append(f"- **Total Budget:** \${total_budget:,.2f}")
lines.append(f"- **Total Spent:** \${total_spent:,.2f}")
lines.append(f"- **Remaining:** \${total_remaining:,.2f}")
pct_used = (total_spent / total_budget * 100) if total_budget > 0 else 0
lines.append(f"- **Budget Used:** {pct_used:.1f}%")
if cost_per_head > 0:
    lines.append(f"- **Cost Per Head:** \${cost_per_head:,.2f} ({confirmed} guests)")
lines.append(f"")

lines.append(f"## Category Breakdown")
for cat in categories:
    name = cat.get("name", "Unknown")
    allocated = cat.get("allocated", 0)
    spent = cat.get("spent", 0)
    remaining = allocated - spent
    pct = (spent / allocated * 100) if allocated > 0 else 0
    status = "✅" if pct <= 80 else ("⚠️" if pct <= 100 else "🚨")
    lines.append(f"")
    lines.append(f"### {status} {name}")
    lines.append(f"- Allocated: \${allocated:,.2f}")
    lines.append(f"- Spent: \${spent:,.2f} ({pct:.0f}%)")
    lines.append(f"- Remaining: \${remaining:,.2f}")
    items = cat.get("items", [])
    if items:
        lines.append(f"- Expenses:")
        for item in items:
            paid_str = "✅" if item.get("paid") else "⏳"
            lines.append(f"  - {paid_str} {item.get('description', 'N/A')} — \${item.get('amount', 0):,.2f} ({item.get('date', 'N/A')})")

lines.append(f"")
lines.append(f"---")
lines.append(f"*Party Planner Pro — Budget Report*")

md_content = "\n".join(lines)
md_path = os.path.join(reports_dir, f"budget-report-{event_slug}.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_content)
print(f"✅ Markdown report: {md_path}")

if fmt == "png":
    # Generate HTML for Playwright rendering
    html_rows = ""
    for cat in categories:
        name = cat.get("name", "Unknown")
        allocated = cat.get("allocated", 0)
        spent = cat.get("spent", 0)
        pct = (spent / allocated * 100) if allocated > 0 else 0
        bar_color = "#22c55e" if pct <= 80 else ("#f59e0b" if pct <= 100 else "#ef4444")
        html_rows += f"""
        <div style="margin-bottom:12px;">
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="font-weight:600;">{name}</span>
            <span>\${spent:,.2f} / \${allocated:,.2f} ({pct:.0f}%)</span>
          </div>
          <div style="background:#1e293b;border-radius:6px;height:20px;overflow:hidden;">
            <div style="background:{bar_color};height:100%;width:{min(pct,100):.1f}%;border-radius:6px;"></div>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; padding: 32px; margin: 0; width: 720px; }}
  h1 {{ color: #f8fafc; margin-bottom: 4px; font-size: 24px; }}
  .subtitle {{ color: #94a3b8; margin-bottom: 24px; font-size: 14px; }}
  .summary {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 32px; }}
  .card {{ background: #1e293b; border-radius: 12px; padding: 16px; text-align: center; }}
  .card .label {{ color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }}
  .card .value {{ font-size: 28px; font-weight: 700; margin-top: 4px; }}
  .green {{ color: #22c55e; }}
  .orange {{ color: #f97316; }}
  .teal {{ color: #14b8a6; }}
</style></head><body>
<h1>💰 {event_name} — Budget Report</h1>
<div class="subtitle">{datetime.now().strftime('%B %d, %Y')}</div>
<div class="summary">
  <div class="card"><div class="label">Budget</div><div class="value green">\${total_budget:,.0f}</div></div>
  <div class="card"><div class="label">Spent</div><div class="value orange">\${total_spent:,.0f}</div></div>
  <div class="card"><div class="label">Remaining</div><div class="value teal">\${total_remaining:,.0f}</div></div>
</div>
<h2 style="font-size:18px;margin-bottom:16px;">Category Breakdown</h2>
{html_rows}
</body></html>"""

    html_path = os.path.join(tmp_dir, f"budget-report-{event_slug}.html")
    png_path = os.path.join(reports_dir, f"budget-report-{event_slug}.png")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 784, "height": 800})
            page.goto(Path(html_path).resolve().as_uri())
            page.screenshot(path=png_path, full_page=True)
            browser.close()
        os.remove(html_path)
        print(f"✅ PNG report: {png_path}")
    except ImportError:
        print("⚠️  Playwright not installed — PNG output requires: pip install playwright && playwright install chromium")
        print(f"HTML saved at: {html_path}")
    except Exception as e:
        print(f"⚠️  PNG generation failed: {e}")
        print(f"HTML saved at: {html_path}")
PYEOF
