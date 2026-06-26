#!/usr/bin/env python3
"""
Generate a professional PDF invoice from an HTML template using Playwright.

Usage: python3 generate-invoice-pdf.py <input.html> <output.pdf>
"""

import os
import sys
from playwright.sync_api import sync_playwright

def generate_pdf(input_html, output_pdf):
    # Resolve canonical paths to prevent symlink and relative path bypasses.
    input_path = os.path.realpath(os.path.abspath(input_html))
    output_path = os.path.realpath(os.path.abspath(output_pdf))

    if not os.path.exists(input_path):
        print(f"Error: HTML template '{input_path}' not found.")
        sys.exit(1)

    # SECURITY: Validate output path is within invoices/ directory
    # Prevent path traversal attacks (e.g., ../../.bash_profile)
    invoices_dir = os.path.realpath(os.path.abspath(os.path.join(os.getcwd(), "invoices")))
    if os.path.commonpath([output_path, invoices_dir]) != invoices_dir:
        print(f"Error: Output path must be within the invoices/ directory.")
        print(f"Got: {output_path}")
        print(f"Expected directory: {invoices_dir}")
        sys.exit(1)

    print(f"Rendering PDF from {input_path} to {output_path}...")

    with sync_playwright() as p:
        # Launch Chromium (headless)
        browser = p.chromium.launch()
        # SECURITY: Disable JavaScript to prevent XSS from malicious invoice content
        page = browser.new_page(viewport={"width": 1200, "height": 1600}, java_script_enabled=False)
        
        # Load the HTML file
        page.goto(f"file://{input_path}")
        
        # Brief pause for font rendering (no JS needed)
        page.wait_for_timeout(500)
        
        # Print to PDF
        page.pdf(
            path=output_path,
            format="Letter",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        
        browser.close()
        print(f"Successfully generated PDF: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generate-invoice-pdf.py <input.html> <output.pdf>")
        sys.exit(1)
        
    generate_pdf(sys.argv[1], sys.argv[2])
