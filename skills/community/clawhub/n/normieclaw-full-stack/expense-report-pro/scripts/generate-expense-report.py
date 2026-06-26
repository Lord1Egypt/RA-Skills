#!/usr/bin/env python3
"""
Generate a professional expense report PDF from logged expenses.
Uses Playwright to render HTML → PDF.

Usage: python3 generate-expense-report.py <YYYY-MM> <output.pdf>
Output path must be within the expenses/ directory.

Dependencies: pip install playwright && playwright install chromium
"""
import json
import os
import re
import sys
import tempfile
from datetime import datetime
from playwright.sync_api import sync_playwright

# SECURITY: Determine script and expenses directory locations
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
# Default expense data location (relative to CWD)
EXPENSES_DIR = os.path.join(os.getcwd(), "expenses")

def generate_report(month_str, output_path):
    # SECURITY: Strictly validate month format and values
    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", month_str):
        print("Error: month must be in YYYY-MM format.")
        sys.exit(1)

    # SECURITY: Validate output path is within expenses/ directory
    abs_output = os.path.abspath(output_path)
    abs_expenses = os.path.abspath(EXPENSES_DIR)
    try:
        is_within_expenses = os.path.commonpath([abs_output, abs_expenses]) == abs_expenses
    except ValueError:
        is_within_expenses = False
    if not is_within_expenses:
        print(f"Error: Output path must be within the expenses/ directory.")
        print(f"Got: {abs_output}")
        print(f"Expected prefix: {abs_expenses}")
        sys.exit(1)

    # Load expenses from relative path
    log_path = os.path.join(EXPENSES_DIR, "expense-log.json")
    if not os.path.exists(log_path):
        print(f"Error: No expense log found at {log_path}")
        sys.exit(1)

    with open(log_path, 'r') as f:
        expenses = json.load(f)

    # Filter by month
    monthly_expenses = [e for e in expenses if e.get('date', '').startswith(month_str)]

    # Calculate totals
    total = sum(e.get('total', 0) for e in monthly_expenses)

    # Load template (relative to skill directory)
    template_path = os.path.join(SKILL_DIR, "config", "report-template.html")
    if not os.path.exists(template_path):
        print(f"Error: No template found at {template_path}")
        sys.exit(1)

    with open(template_path, 'r') as f:
        html = f.read()

    # Generate rows — SECURITY: escape HTML in vendor names to prevent XSS
    import html as html_module
    rows = ""
    for exp in monthly_expenses:
        vendor = html_module.escape(str(exp.get('vendor', '')))
        category = html_module.escape(str(exp.get('category', '')))
        date = html_module.escape(str(exp.get('date', '')))
        rows += f"<tr><td>{date}</td><td>{vendor}</td><td>{category}</td><td>${exp.get('total', 0):.2f}</td></tr>\n"

    # Replace placeholders
    html = html.replace("{{MONTH}}", html_module.escape(month_str))
    html = html.replace("{{TOTAL}}", f"${total:.2f}")
    html = html.replace("{{ROWS}}", rows)
    html = html.replace("{{GENERATED_DATE}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Write temp html using an OS-managed temporary file
    temp_file = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".html",
        prefix=f"expense_report_{month_str}_",
        delete=False,
        dir="/tmp",
    )
    temp_html = temp_file.name
    with temp_file:
        temp_file.write(html)

    # Render PDF via Playwright
    # SECURITY: java_script_enabled=False prevents code execution from malicious content
    print(f"Rendering expense report for {month_str}...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(java_script_enabled=False)
            page = context.new_page()
            page.goto(f"file://{temp_html}")
            page.pdf(path=abs_output, format="Letter", print_background=True)
            browser.close()
    finally:
        # Clean up temp file even if rendering fails
        if os.path.exists(temp_html):
            os.remove(temp_html)
    print(f"Successfully generated report: {abs_output}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generate-expense-report.py <YYYY-MM> <output.pdf>")
        sys.exit(1)
    generate_report(sys.argv[1], sys.argv[2])
