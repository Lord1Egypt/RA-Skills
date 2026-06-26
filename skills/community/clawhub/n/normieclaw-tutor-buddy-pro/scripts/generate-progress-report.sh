#!/bin/bash
# generate-progress-report.sh — Generate a visual progress report (HTML → PNG)
# Usage: ./generate-progress-report.sh [output_path]
#
# Reads data/learner-profile.json and data/quiz-history.json to create
# a styled HTML progress report, then renders it to PNG via Playwright.
#
# Requirements: python3, playwright (with chromium installed)

set -euo pipefail

# --- Workspace root detection ---
find_skill_root() {
    # Stay within the skill directory — do not traverse outside
    cd "$(dirname "$0")/.." && pwd
}

SKILL_DIR=$(find_skill_root)
if [ -z "$SKILL_DIR" ]; then
    echo "❌ Error: Could not find workspace root. Run from within your workspace." >&2
    exit 1
fi

# --- Paths ---
LEARNER_PROFILE="$SKILL_DIR/data/learner-profile.json"
QUIZ_HISTORY="$SKILL_DIR/data/quiz-history.json"
OUTPUT_PATH="${1:-$SKILL_DIR/reports/tutor-progress-report.png}"
TEMP_HTML="$(mktemp /tmp/tutor-progress-report.XXXXXX.html)"

# --- Validate inputs ---
if [ ! -f "$LEARNER_PROFILE" ]; then
    echo "❌ Error: Learner profile not found at $LEARNER_PROFILE" >&2
    echo "   Run setup first — see SETUP-PROMPT.md" >&2
    exit 1
fi

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT_PATH")"

# --- Generate HTML report ---
SKILL_DIR="$SKILL_DIR" TEMP_HTML="$TEMP_HTML" python3 << 'PYEOF'
import json
import sys
import os
from datetime import datetime

workspace = os.environ.get("SKILL_DIR", ".")
output_html = os.environ.get("TEMP_HTML", "/tmp/tutor-progress-report.html")

# Load data
try:
    with open(os.path.join(workspace, "data/learner-profile.json"), "r") as f:
        profile = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    profile = {}

try:
    with open(os.path.join(workspace, "data/quiz-history.json"), "r") as f:
        quizzes = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    quizzes = []

name = profile.get("name", "Student")
grade = profile.get("grade_level", "N/A")
total_sessions = profile.get("total_sessions", 0)
total_minutes = profile.get("total_study_minutes", 0)
streak = profile.get("streak_days", 0)
subjects = profile.get("subjects", {})

# Build topic rows
topic_rows = ""
for subj_name, subj_data in subjects.items():
    for topic_name, topic_data in subj_data.get("topics", {}).items():
        pct = topic_data.get("proficiency_pct", 0)
        sessions = topic_data.get("sessions", 0)
        last = topic_data.get("last_studied", "N/A")
        color = "#22c55e" if pct >= 75 else "#eab308" if pct >= 50 else "#ef4444"
        display_name = topic_name.replace("_", " ").title()
        topic_rows += f"""
        <div style="display:flex;align-items:center;margin-bottom:12px;">
            <div style="width:180px;font-weight:500;">{display_name}</div>
            <div style="flex:1;background:#e5e7eb;border-radius:8px;height:24px;margin:0 12px;overflow:hidden;">
                <div style="width:{pct}%;background:{color};height:100%;border-radius:8px;transition:width 0.3s;"></div>
            </div>
            <div style="width:50px;text-align:right;font-weight:600;color:{color};">{pct}%</div>
        </div>"""

# Build quiz rows
quiz_rows = ""
for q in (quizzes[-10:] if quizzes else []):
    score = q.get("score_pct", 0)
    color = "#22c55e" if score >= 80 else "#eab308" if score >= 60 else "#ef4444"
    quiz_rows += f"""
    <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #f3f4f6;">
        <span>{q.get('date', 'N/A')}</span>
        <span>{q.get('topic', 'N/A').replace('_',' ').title()}</span>
        <span style="color:{color};font-weight:600;">{score}%</span>
        <span>{q.get('questions_correct',0)}/{q.get('questions_total',0)}</span>
    </div>"""

html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 32px; background: #ffffff; color: #1f2937; }}
    .header {{ text-align: center; margin-bottom: 32px; }}
    .header h1 {{ font-size: 28px; margin: 0; color: #1e40af; }}
    .header p {{ color: #6b7280; margin: 4px 0; }}
    .stats {{ display: flex; gap: 16px; margin-bottom: 32px; }}
    .stat-card {{ flex: 1; background: #f0f9ff; border-radius: 12px; padding: 20px; text-align: center; }}
    .stat-card .number {{ font-size: 32px; font-weight: 700; color: #1e40af; }}
    .stat-card .label {{ font-size: 13px; color: #6b7280; margin-top: 4px; }}
    .section {{ margin-bottom: 28px; }}
    .section h2 {{ font-size: 18px; color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; }}
</style>
</head>
<body>
<div class="header">
    <h1>🎓 Tutor Buddy Pro — Progress Report</h1>
    <p>{name} • Grade {grade} • Generated {datetime.now().strftime('%B %d, %Y')}</p>
</div>
<div class="stats">
    <div class="stat-card"><div class="number">{total_sessions}</div><div class="label">Sessions</div></div>
    <div class="stat-card"><div class="number">{total_minutes}</div><div class="label">Minutes Studied</div></div>
    <div class="stat-card"><div class="number">🔥 {streak}</div><div class="label">Day Streak</div></div>
    <div class="stat-card"><div class="number">{len(quizzes)}</div><div class="label">Quizzes Taken</div></div>
</div>
<div class="section">
    <h2>📊 Topic Proficiency</h2>
    {topic_rows if topic_rows else '<p style="color:#9ca3af;">No topics tracked yet. Start a tutoring session to begin!</p>'}
</div>
<div class="section">
    <h2>📝 Recent Quizzes</h2>
    {quiz_rows if quiz_rows else '<p style="color:#9ca3af;">No quizzes taken yet. Try "quiz me on algebra" to get started!</p>'}
</div>
</body>
</html>"""

with open(output_html, "w") as f:
    f.write(html)

print(f"✅ HTML report written to {output_html}")
PYEOF

# --- Render to PNG ---
SKILL_DIR="$SKILL_DIR" TEMP_HTML="$TEMP_HTML" OUTPUT_PATH="$OUTPUT_PATH" python3 << 'PYEOF'
import os
temp_html = os.environ["TEMP_HTML"]
output_path = os.environ["OUTPUT_PATH"]

try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 800, "height": 600})
        page.goto(f"file://{temp_html}")
        page.wait_for_load_state("networkidle")
        # Auto-size to content
        height = page.evaluate("document.body.scrollHeight")
        page.set_viewport_size({"width": 800, "height": height + 64})
        page.screenshot(path=output_path)
        browser.close()
    print(f"✅ Progress report saved to {output_path}")
except ImportError:
    print("⚠️ Playwright not installed. HTML report saved at: " + temp_html)
    print("   Install with: pip3 install playwright && playwright install chromium")
except Exception as e:
    print(f"⚠️ Playwright rendering failed: {e}")
    print(f"   HTML report available at: {temp_html}")
PYEOF

# --- Cleanup ---
rm -f "$TEMP_HTML"
