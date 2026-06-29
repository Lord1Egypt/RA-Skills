#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISO 9001 Consultant - Step 2: Gap Analysis
============================================
Analyze gaps between client document and ISO 9001:2015 requirements.
"""

import sys
import json

def load_json_file(file_path):
    """Load JSON file with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load {file_path}: {e}")
        return None

def map_clause(parsed_data, framework):
    """Map document to ISO 9001 clause"""
    # Simplified mapping logic
    headings = parsed_data.get("structure", {}).get("headings", [])
    
    mapping = {
        "clause": "Unknown",
        "confidence": 0.0,
        "matched_keywords": []
    }
    
    # Simple keyword matching
    for heading in headings:
        if "目的" in heading or "purpose" in heading.lower():
            mapping["matched_keywords"].append("purpose")
        if "范围" in heading or "scope" in heading.lower():
            mapping["matched_keywords"].append("scope")
        if "职责" in heading or "responsibility" in heading.lower():
            mapping["matched_keywords"].append("responsibility")
    
    mapping["confidence"] = len(mapping["matched_keywords"]) / 4.0
    
    return mapping

def check_technical_service(key, title, purpose):
    """Check technical service industry specific requirements"""
    checks = {
        "7.1.6": {"name": "Knowledge Management", "name_zh": "知识管理", "status": "Unknown"},
        "8.5.1": {"name": "Service Delivery", "name_zh": "服务交付", "status": "Unknown"},
        "9.1.2": {"name": "Customer Satisfaction", "name_zh": "客户满意度", "status": "Unknown"}
    }
    
    # Simplified check
    if "知识" in title or "knowledge" in title.lower():
        checks["7.1.6"]["status"] = "Present"
    else:
        checks["7.1.6"]["status"] = "Missing"
    
    if "服务" in title or "service" in title.lower():
        checks["8.5.1"]["status"] = "Present"
    else:
        checks["8.5.1"]["status"] = "Missing"
    
    if "客户" in title or "customer" in title.lower():
        checks["9.1.2"]["status"] = "Present"
    else:
        checks["9.1.2"]["status"] = "Missing"
    
    return checks

def generate_status_table(checklist):
    """Generate Red-Yellow-Green status table"""
    status_table = {
        "red": [],  # Missing/Non-compliant
        "yellow": [],  # Partial
        "green": []  # Compliant
    }
    
    for item in checklist:
        status = item.get("status", "Unknown")
        if status == "Missing" or status == "Non-compliant":
            status_table["red"].append(item)
        elif status == "Partial":
            status_table["yellow"].append(item)
        elif status == "Present" or status == "Compliant":
            status_table["green"].append(item)
    
    return status_table

def analyze_gap(parsed_data, templates, framework):
    """Main gap analysis function"""
    print("[INFO] Starting gap analysis...")
    
    # Map clause
    clause_mapping = map_clause(parsed_data, framework)
    
    # Check technical service requirements
    technical_service_checks = check_technical_service(
        clause_mapping.get("clause", "Unknown"),
        parsed_data.get("structure", {}).get("headings", [""])[0] if parsed_data.get("structure", {}).get("headings") else "",
        ""
    )
    
    # Generate gap report
    gap_report = {
        "clause_mapping": clause_mapping,
        "technical_service_checks": technical_service_checks,
        "missing_clauses": [],
        "missing_content": [],
        "recommendations": []
    }
    
    # Simplified gap analysis
    for key, value in technical_service_checks.items():
        if value["status"] == "Missing":
            gap_report["missing_clauses"].append(key)
            gap_report["recommendations"].append(f"Add {value['name_zh']} ({value['name']})")
    
    # Generate status table
    checklist = []
    for key, value in technical_service_checks.items():
        checklist.append({
            "clause": key,
            "name": value["name"],
            "name_zh": value["name_zh"],
            "status": value["status"]
        })
    
    status_table = generate_status_table(checklist)
    gap_report["status_table"] = status_table
    gap_report["checklist"] = checklist
    
    return gap_report

def main():
    if len(sys.argv) < 3:
        print("Usage: python analyze_gap.py <parsed_json> <audit_report>")
        sys.exit(1)
    
    parsed_json_path = sys.argv[1]
    audit_report_path = sys.argv[2]
    
    # Load files
    parsed_data = load_json_file(parsed_json_path)
    audit_report = load_json_file(audit_report_path)
    
    if not parsed_data:
        print("[ERROR] Failed to load parsed data")
        sys.exit(1)
    
    # Load framework and templates (simplified)
    framework = {"clauses": {}}
    templates = {"templates": []}
    
    # Perform gap analysis
    gap_report = analyze_gap(parsed_data, templates, framework)
    
    # Output gap report
    print("\n=== Gap Analysis Report ===")
    print(json.dumps(gap_report, ensure_ascii=False, indent=2))
    
    # Save to file
    output_file = parsed_json_path + ".gap.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(gap_report, f, ensure_ascii=False, indent=2)
    
    print(f"\n[INFO] Gap analysis report saved to {output_file}")

if __name__ == "__main__":
    main()
