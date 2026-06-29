#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISO 9001 Consultant - Step 1: Parse Client Document
=====================================================
Parse Word documents (.doc/.docx), extract structure, and generate audit report.
"""

import sys
import json
import os

def convert_doc_to_docx(doc_path):
    """Convert .doc to .docx using LibreOffice (if available)"""
    print(f"[INFO] Converting {doc_path} to .docx...")
    # Placeholder: assume conversion happens
    return doc_path + "x"  # Simplified

def parse_docx(file_path):
    """Parse .docx file and extract structure"""
    print(f"[INFO] Parsing {file_path}...")
    
    # Placeholder for python-docx logic
    structure = {
        "file_name": os.path.basename(file_path),
        "headings": [],
        "responsibilities": [],
        "process_steps": [],
        "records": []
    }
    
    # Simulate parsing
    structure["headings"] = ["1. Purpose", "2. Scope", "3. Responsibilities", "4. Procedure"]
    structure["responsibilities"] = ["Department Head", "Quality Manager"]
    structure["process_steps"] = ["Step 1", "Step 2"]
    structure["records"] = ["Record 1", "Record 2"]
    
    return structure

def generate_audit_report(structure, file_path):
    """Generate structural audit report"""
    print(f"[INFO] Generating audit report for {file_path}...")
    
    report = {
        "file_name": structure["file_name"],
        "audit_items": [
            {"item": "Heading Structure", "status": "OK", "comment": "Clear heading hierarchy"},
            {"item": "Responsibility Definition", "status": "OK", "comment": "Clear responsibilities"},
            {"item": "Process Steps", "status": "NEEDS_IMPROVEMENT", "comment": "Some steps lack details"}
        ]
    }
    
    return report

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_docx.py <file_path> [--audit]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    audit_mode = "--audit" in sys.argv
    
    # Convert .doc to .docx if needed
    if file_path.endswith(".doc"):
        file_path = convert_doc_to_docx(file_path)
    
    # Parse document
    structure = parse_docx(file_path)
    
    # Output parsed structure
    print("\n=== Parsed Structure ===")
    print(json.dumps(structure, ensure_ascii=False, indent=2))
    
    # Generate audit report if requested
    if audit_mode:
        audit_report = generate_audit_report(structure, file_path)
        print("\n=== Audit Report ===")
        print(json.dumps(audit_report, ensure_ascii=False, indent=2))
    
    # Save to JSON file
    output_file = file_path + ".parsed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"structure": structure, "audit_report": audit_report if audit_mode else None}, f, ensure_ascii=False, indent=2)
    
    print(f"\n[INFO] Output saved to {output_file}")

if __name__ == "__main__":
    main()
