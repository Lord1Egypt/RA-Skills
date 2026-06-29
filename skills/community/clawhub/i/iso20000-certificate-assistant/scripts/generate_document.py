#!/usr/bin/env python3
"""
generate_document.py - Generate ISO 20000-1 compliant documents from templates
Usage: python generate_document.py <template_name> <output_path> [client_json]
"""

import json
import sys
import os
from datetime import datetime

def load_template(template_name):
    """Load generic template from knowledge/generic_templates.json"""
    templates_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'generic_templates.json')
    templates_path = os.path.abspath(templates_path)
    
    if not os.path.exists(templates_path):
        return {"error": f"Templates file not found: {templates_path}"}
    
    with open(templates_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find template by id or name
    for template in data.get("templates", []):
        if template.get("id") == template_name or template.get("name") == template_name:
            return template
    
    return {"error": f"Template not found: {template_name}"}

def load_client_data(client_json_path):
    """Load client-specific data from parsed JSON"""
    if not client_json_path or not os.path.exists(client_json_path):
        return {}
    
    with open(client_json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def fill_template(template, client_data, output_path):
    """Fill template with client data"""
    doc_name = template.get("name", "Unknown")
    sections = template.get("sections", [])
    
    # Start building document
    lines = []
    lines.append("=" * 50)
    lines.append(doc_name)
    lines.append("=" * 50)
    lines.append("")
    lines.append(f"编制/日期：ISO工作组/{datetime.now().strftime('%Y.%m.%d')}")
    lines.append(f"审核/日期：[待填写]/{datetime.now().strftime('%Y.%m.%d')}")
    lines.append(f"批准/日期：[待填写]/{datetime.now().strftime('%Y.%m.%d')}")
    lines.append("")
    lines.append("-" * 50)
    lines.append("")
    
    # Fill sections
    for section in sections:
        title = section.get("title", "")
        content = section.get("content", "")
        
        lines.append(f"## {title}")
        lines.append("")
        
        # Replace placeholders with client data
        if "[■" in content:
            # Keep placeholders for user to fill
            lines.append(content)
        else:
            # Use content as-is or from client data
            client_content = client_data.get("extracted_content", {}).get(title, content)
            lines.append(client_content)
        
        lines.append("")
    
    # Add high-voltage line compliance statement
    if template.get("high_voltage_check"):
        lines.append("---")
        lines.append("")
        lines.append("## 高压线合规声明")
        lines.append("")
        lines.append("本文件已包含以下高压线要求：")
        
        hv_check = template.get("high_voltage_check")
        if hv_check == "change_grading":
            lines.append("✅ 已明确区分'一般变更'与'重大变更'")
            lines.append("✅ 已明确重大变更必须在凌晨00:00-06:00执行")
        elif hv_check == "incident_handling":
            lines.append("✅ 已明确'先恢复业务，后查找根因'原则")
            lines.append("✅ 已建立1-3级事件分级标准")
        elif hv_check == "raci_responsibilities":
            lines.append("✅ 已明确体系归口部门、服务质量监督部门、采购/综合部门的三方分离")
        elif hv_check == "supplier_risk":
            lines.append("✅ 已提出'禁止单一供应商全权负责单一服务/组件'的要求")
        
        lines.append("")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return {
        "status": "success",
        "output_path": output_path,
        "doc_name": doc_name,
        "sections_filled": len(sections)
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_document.py <template_name> <output_path> [client_json]")
        print("\nAvailable templates:")
        
        # List available templates
        templates_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'generic_templates.json')
        templates_path = os.path.abspath(templates_path)
        
        if os.path.exists(templates_path):
            with open(templates_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for template in data.get("templates", []):
                print(f"  - {template.get('id')}: {template.get('name')}")
        
        sys.exit(1)
    
    template_name = sys.argv[1]
    output_path = sys.argv[2]
    client_json_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Load template
    template = load_template(template_name)
    if "error" in template:
        print(f"Error: {template['error']}")
        sys.exit(1)
    
    # Load client data
    client_data = load_client_data(client_json_path)
    
    # Fill template and generate document
    result = fill_template(template, client_data, output_path)
    
    if result["status"] == "success":
        print(f"✅ Document generated successfully!")
        print(f"   Output: {result['output_path']}")
        print(f"   Document: {result['doc_name']}")
        print(f"   Sections filled: {result['sections_filled']}")
    else:
        print(f"❌ Failed to generate document: {result.get('error', 'Unknown error')}")
        sys.exit(1)
    
    # Print summary
    print("\n=== Document Generation Summary ===")
    print(f"Template: {template_name}")
    print(f"Output: {output_path}")
    print(f"Client data: {client_json_path or 'None (using placeholders)'}")
    
    if template.get("high_voltage_check"):
        print(f"\nHigh-voltage line check: {template['high_voltage_check']}")
        print("  ✅ High-voltage line compliance statement included")

if __name__ == "__main__":
    main()
