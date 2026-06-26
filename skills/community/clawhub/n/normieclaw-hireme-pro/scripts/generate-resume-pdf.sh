#!/usr/bin/env bash
# generate-resume-pdf.sh — Render an HTML resume template to PDF using Playwright
#
# Usage: ./generate-resume-pdf.sh <html_template> <json_data> <output_pdf>
#
# Arguments:
#   html_template  — Path to the HTML template file (e.g., templates/modern.html)
#   json_data      — Path to the resume JSON data file (e.g., data/resume-data.json)
#   output_pdf     — Path for the output PDF (e.g., data/resumes/2026-03-08-modern-v1.pdf)
#
# Requirements:
#   - Python 3
#   - Playwright (pip3 install playwright && playwright install chromium)
#
# Security:
#   - No hardcoded secrets
#   - No network access required
#   - Workspace root detection via marker files

set -euo pipefail

# --- Workspace root detection ---
find_skill_root() {
    # Stay within the skill directory — do not traverse outside
    cd "$(dirname "$0")/.." && pwd
}

# Resolve absolute path using Python for portability (macOS/Linux).
resolve_path() {
  python3 - "$1" << 'PYEOF'
import os
import sys
print(os.path.realpath(sys.argv[1]))
PYEOF
}

# Ensure a path is inside an allowed root directory.
require_path_within() {
  local path="$1"
  local root="$2"
  case "$path" in
    "$root"|"$root"/*) ;;
    *)
      echo "Error: Path escapes workspace root: $path"
      exit 1
      ;;
  esac
}

# --- Argument validation ---
if [ $# -ne 3 ]; then
  echo "Usage: $0 <html_template> <json_data> <output_pdf>"
  echo ""
  echo "Example:"
  echo "  $0 templates/modern.html data/resume-data.json data/resumes/2026-03-08-modern-v1.pdf"
  exit 1
fi

HTML_TEMPLATE="$1"
JSON_DATA="$2"
OUTPUT_PDF="$3"

# --- Determine workspace root and enforce path boundaries ---
SKILL_DIR="$(find_skill_root || true)"
if [ -z "$SKILL_DIR" ]; then
    # Skill directory detection (stay within skill boundary)
  exit 1
fi
SKILL_DIR="$(resolve_path "$SKILL_DIR")"

# --- Validate inputs ---
if [ ! -f "$HTML_TEMPLATE" ]; then
  echo "Error: Template file not found: $HTML_TEMPLATE"
  exit 1
fi

if [ ! -f "$JSON_DATA" ]; then
  echo "Error: JSON data file not found: $JSON_DATA"
  exit 1
fi

ABS_TEMPLATE="$(resolve_path "$HTML_TEMPLATE")"
ABS_JSON_DATA="$(resolve_path "$JSON_DATA")"
ABS_OUTPUT_PDF="$(resolve_path "$OUTPUT_PDF")"

require_path_within "$ABS_TEMPLATE" "$SKILL_DIR"
require_path_within "$ABS_JSON_DATA" "$SKILL_DIR"
require_path_within "$ABS_OUTPUT_PDF" "$SKILL_DIR"

if [[ "$ABS_OUTPUT_PDF" != *.pdf ]]; then
  echo "Error: Output file must end with .pdf"
  exit 1
fi

HTML_TEMPLATE="$ABS_TEMPLATE"
JSON_DATA="$ABS_JSON_DATA"
OUTPUT_PDF="$ABS_OUTPUT_PDF"

# --- Create output directory if needed ---
OUTPUT_DIR="$(dirname "$OUTPUT_PDF")"
if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir -p "$OUTPUT_DIR"
  chmod 700 "$OUTPUT_DIR"
fi

# --- Generate the populated HTML ---
TEMP_HTML=$(mktemp /tmp/hireme-resume-XXXXXX.html)
trap 'rm -f "$TEMP_HTML"' EXIT

python3 << 'PYEOF' "$HTML_TEMPLATE" "$JSON_DATA" "$TEMP_HTML"
import sys
import json
import html as html_lib

template_path = sys.argv[1]
data_path = sys.argv[2]
output_path = sys.argv[3]

# Read template
with open(template_path, 'r') as f:
    html_content = f.read()

# Read resume data
with open(data_path, 'r') as f:
    data = json.load(f)

# Simple template variable replacement: {{variable_name}}
def replace_vars(html_text, data, prefix=''):
    for key, value in data.items():
        placeholder = '{{' + (f'{prefix}.{key}' if prefix else key) + '}}'
        if isinstance(value, str):
            # Escape HTML in user content
            safe_value = html_lib.escape(value, quote=True)
            html_text = html_text.replace(placeholder, safe_value)
        elif isinstance(value, dict):
            html_text = replace_vars(html_text, value, prefix=key if not prefix else f'{prefix}.{key}')
        elif isinstance(value, list):
            # Lists are handled by the template engine section below
            pass
        elif value is None:
            html_text = html_text.replace(placeholder, '')
        else:
            html_text = html_text.replace(placeholder, str(value))
    return html_text

html_content = replace_vars(html_content, data)

# Generate experience section HTML
experience_html = ''
for exp in data.get('experience', []):
    bullets = ''.join(f'<li>{html_lib.escape(str(b), quote=True)}</li>' for b in exp.get('bullets', []))
    end = html_lib.escape(str(exp.get('end_date', 'Present')), quote=True)
    title = html_lib.escape(str(exp.get('title', '')), quote=True)
    company = html_lib.escape(str(exp.get('company', '')), quote=True)
    start = html_lib.escape(str(exp.get('start_date', '')), quote=True)
    experience_html += f"""
    <div class="experience-entry">
      <div class="entry-header">
        <h3>{title}</h3>
        <span class="company">{company}</span>
        <span class="dates">{start} — {end}</span>
      </div>
      <ul>{bullets}</ul>
    </div>"""

html_content = html_content.replace('{{experience_section}}', experience_html)

# Generate education section HTML
education_html = ''
for edu in data.get('education', []):
    honors = f' — {html_lib.escape(str(edu["honors"]), quote=True)}' if edu.get('honors') else ''
    degree = html_lib.escape(str(edu.get('degree', '')), quote=True)
    institution = html_lib.escape(str(edu.get('institution', '')), quote=True)
    graduation_date = html_lib.escape(str(edu.get('graduation_date', '')), quote=True)
    education_html += f"""
    <div class="education-entry">
      <h3>{degree}{honors}</h3>
      <span class="institution">{institution}</span>
      <span class="dates">{graduation_date}</span>
    </div>"""

html_content = html_content.replace('{{education_section}}', education_html)

# Generate skills section
skills = data.get('skills', [])
skills_html = ' • '.join(html_lib.escape(str(skill), quote=True) for skill in skills) if skills else ''
html_content = html_content.replace('{{skills_list}}', skills_html)

# Write populated HTML
with open(output_path, 'w') as f:
    f.write(html_content)

print(f"Generated populated HTML: {output_path}")
PYEOF

# --- Render HTML to PDF via Playwright ---
python3 << PYEOF "$TEMP_HTML" "$OUTPUT_PDF"
import sys
from playwright.sync_api import sync_playwright

html_path = sys.argv[1]
pdf_path = sys.argv[2]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    # Prevent any outbound network requests when rendering local resume HTML.
    page.route("**/*", lambda route, request: route.continue_() if request.url.startswith("file://") else route.abort())
    page.goto(f"file://{html_path}")
    page.pdf(
        path=pdf_path,
        format="Letter",
        margin={"top": "0.5in", "bottom": "0.5in", "left": "0.6in", "right": "0.6in"},
        print_background=True
    )
    browser.close()

print(f"PDF generated: {pdf_path}")
PYEOF

# --- Set secure permissions on output ---
chmod 600 "$OUTPUT_PDF"

echo "✅ Resume PDF created: $OUTPUT_PDF"
