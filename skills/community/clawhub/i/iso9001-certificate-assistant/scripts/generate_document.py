#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISO 9001 Consultant - Step 3: Generate Document
===============================================
Generate or rewrite documents based on templates and gap analysis.
"""

import sys
import json
import os

def load_json_file(file_path):
    """Load JSON file with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load {file_path}: {e}")
        return None

def list_templates(templates):
    """List all available templates"""
    print("\n=== Available Templates ===")
    for i, tpl in enumerate(templates.get("templates", [])):
        print(f"{i+1}. {tpl.get('id', 'Unknown')} - {tpl.get('title_zh', '')} / {tpl.get('title_en', '')}")
    print("")

def generate_template(template_data, output_path):
    """Generate a blank template document"""
    print(f"[INFO] Generating template to {output_path}...")
    
    # Simplified: just write the template content as text
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {template_data.get('title_zh', '')} / {template_data.get('title_en', '')}\n\n")
        f.write(f"Clause: {template_data.get('clause', '')}\n\n")
        
        for section in template_data.get("sections", []):
            f.write(f"## {section.get('heading_zh', '')} / {section.get('heading_en', '')}\n")
            f.write(f"{section.get('content_zh', '')} / {section.get('content_en', '')}\n\n")
    
    print(f"[INFO] Template generated: {output_path}")

def rewrite_document(parsed_data, template_data, gaps, output_path):
    """Rewrite existing document based on template and gap analysis"""
    print(f"[INFO] Rewriting document to {output_path}...")
    
    # Simplified: merge parsed data with template
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {template_data.get('title_zh', '')} / {template_data.get('title_en', '')}\n\n")
        f.write(f"Based on: {parsed_data.get('structure', {}).get('file_name', 'Unknown')}\n\n")
        
        for section in template_data.get("sections", []):
            f.write(f"## {section.get('heading_zh', '')} / {section.get('heading_en', '')}\n")
            
            # Use parsed content if available, otherwise use template placeholder
            content_zh = section.get('content_zh', '[■ 请填写]')
            content_en = section.get('content_en', '[■ Please fill in]')
            
            f.write(f"{content_zh} / {content_en}\n\n")
        
        # Add gap analysis recommendations
        if gaps and "recommendations" in gaps:
            f.write("\n## Recommendations / 建议\n")
            for rec in gaps["recommendations"]:
                f.write(f"- {rec}\n")
    
    print(f"[INFO] Document rewritten: {output_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  List templates: python generate_document.py --list <templates_json>")
        print("  Generate template: python generate_document.py <template_id> <output_path> [--templates <templates_json>]")
        print("  Rewrite document: python generate_document.py <template_id> <output_path> --parsed <parsed_json> --gaps <gaps_json> [--templates <templates_json>]")
        sys.exit(1)
    
    # List templates mode
    if sys.argv[1] == "--list":
        templates_path = sys.argv[2]
        templates = load_json_file(templates_path)
        if templates:
            list_templates(templates)
        sys.exit(0)
    
    # Generate or rewrite mode
    template_id = sys.argv[1]
    output_path = sys.argv[2]
    
    # Load templates
    templates_path = "knowledge/generic_templates.json"
    if "--templates" in sys.argv:
        idx = sys.argv.index("--templates")
        if idx + 1 < len(sys.argv):
            templates_path = sys.argv[idx + 1]
    
    templates = load_json_file(templates_path)
    if not templates:
        print("[ERROR] Failed to load templates")
        sys.exit(1)
    
    # Find the template
    template_data = None
    for tpl in templates.get("templates", []):
        if tpl.get("id") == template_id:
            template_data = tpl
            break
    
    if not template_data:
        print(f"[ERROR] Template {template_id} not found")
        sys.exit(1)
    
    # Check if rewrite mode
    if "--parsed" in sys.argv and "--gaps" in sys.argv:
        # Rewrite mode
        parsed_idx = sys.argv.index("--parsed")
        gaps_idx = sys.argv.index("--gaps")
        
        parsed_data = load_json_file(sys.argv[parsed_idx + 1])
        gaps_data = load_json_file(sys.argv[gaps_idx + 1])
        
        if not parsed_data or not gaps_data:
            print("[ERROR] Failed to load parsed data or gaps data")
            sys.exit(1)
        
        rewrite_document(parsed_data, template_data, gaps_data, output_path)
    else:
        # Generate blank template mode
        generate_template(template_data, output_path)
    
    print(f"\n[INFO] Output saved to {output_path}")

if __name__ == "__main__":
    main()
