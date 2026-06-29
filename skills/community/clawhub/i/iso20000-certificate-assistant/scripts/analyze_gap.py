#!/usr/bin/env python3
"""
analyze_gap.py v2.0 - Analyze gap between documents and ISO 20000-1:2018 standard
Improvements:
1. Better error handling and logging
2. More accurate gap analysis algorithm
3. Support for bilingual templates
4. Detailed gap reporting
5. Command-line argument validation
"""

import json
import sys
import os
import logging
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analyze_gap.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ISO 20000-1:2018 clauses structure
ISO_CLAUSES = {
    "4": "Context of the organization",
    "4.1": "Understanding the organization and its context",
    "7": "Support",
    "7.1": "Resources",
    "7.1.2": "Information security",
    "7.2": "Competence",
    "7.3": "Awareness",
    "7.5": "Documented information",
    "8": "Operation",
    "8.2": "Service portfolio",
    "8.2.1": "Service delivery",
    "8.2.2": "Service catalog",
    "8.2.3": "Capacity management",
    "8.3": "Relationship and agreement",
    "8.3.3": "Suppliers",
    "8.4": "Resolution and fulfillment",
    "8.4.1": "Incident and service request",
    "8.4.2": "Problem",
    "8.5": "Service assurance",
    "8.5.1": "Change",
    "9": "Performance evaluation",
    "9.2": "Internal audit",
    "9.3": "Management review",
    "9.4": "Service reporting",
    "9.5": "Service continuity and availability",
    "9.5.2": "Availability",
    "9.5.3": "Service continuity",
    "9.5.4": "Information security",
    "9.6": "Improvement",
    "9.6.1": "Corrective actions",
    "9.6.2": "Problem management"
}

# High-voltage line check items
HIGH_VOLTAGE_CHECKS = {
    "change_grading": {
        "name_zh": "变更分级与时效",
        "name_en": "Change Grading and Timing",
        "keywords_zh": ["变更", "重大变更", "窗口", "00:00", "06:00"],
        "keywords_en": ["change", "major change", "window", "00:00", "06:00"],
        "required": True
    },
    "incident_handling": {
        "name_zh": "事件处理原则",
        "name_en": "Incident Handling Principle",
        "keywords_zh": ["先恢复", "业务恢复", "临时措施", "workaround"],
        "keywords_en": ["restore service first", "business recovery", "workaround", "temporary measure"],
        "required": True
    },
    "raci_responsibilities": {
        "name_zh": "RACI职责矩阵",
        "name_en": "RACI Responsibility Matrix",
        "keywords_zh": ["归口", "负责", "部门", "角色"],
        "keywords_en": ["responsible", "accountable", "consulted", "informed", "department", "role"],
        "required": True
    },
    "supplier_risk": {
        "name_zh": "供应商风险防范",
        "name_en": "Supplier Risk Prevention",
        "keywords_zh": ["供应商", "单一", "风险", "备份", "依赖"],
        "keywords_en": ["supplier", "single", "risk", "backup", "dependency"],
        "required": True
    },
    "sla_reporting": {
        "name_zh": "SLA报告指标",
        "name_en": "SLA Reporting Metrics",
        "keywords_zh": ["报告", "SLA", "指标", "可用性", "解决时长"],
        "keywords_en": ["report", "SLA", "metric", "availability", "resolution time"],
        "required": True
    }
}

def load_template(templates_path: str, language: str = "zh") -> List[Dict]:
    """
    Load template from JSON file
    Args:
        templates_path: Path to templates JSON file
        language: "zh" (Chinese only), "en" (English only), "bilingual"
    Returns:
        List of templates
    """
    logger.info(f"Loading templates from: {templates_path}")
    
    if not os.path.exists(templates_path):
        error_msg = f"Templates file not found: {templates_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    try:
        with open(templates_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        templates = data.get('templates', [])
        logger.info(f"Loaded {len(templates)} templates")
        
        # Filter by language if needed
        if language == "zh":
            # Return Chinese only (original templates)
            return templates
        elif language == "en":
            # Return English only (need bilingual file)
            bilingual_path = templates_path.replace('.json', '_bilingual.json')
            if os.path.exists(bilingual_path):
                with open(bilingual_path, 'r', encoding='utf-8') as f:
                    bilingual_data = json.load(f)
                return bilingual_data.get('templates', [])
        # Default: return as-is
        return templates
    
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in templates file: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    except Exception as e:
        error_msg = f"Failed to load templates: {str(e)}"
        logger.error(error_msg)
        raise

def analyze_gap(parsed_doc: Dict, templates: List[Dict], check_high_voltage: bool = True) -> Dict:
    """
    Analyze gap between parsed document and ISO 20000-1 standard
    Args:
        parsed_doc: Parsed document structure from parse_docx.py
        templates: List of templates to compare against
        check_high_voltage: Whether to check high-voltage lines
    Returns:
        Gap analysis result
    """
    logger.info(f"Starting gap analysis for: {parsed_doc.get('file_name', 'Unknown')}")
    
    # Initialize result
    result = {
        "file_name": parsed_doc.get('file_name', 'Unknown'),
        "file_path": parsed_doc.get('file_path', ''),
        "analyzed_at": datetime.now().isoformat(),
        "overall_match_rate": 0.0,
        "clause_coverage": {},
        "missing_sections": [],
        "existing_sections": [],
        "high_voltage_check": {},
        "recommendations": [],
        "status": "success"
    }
    
    # Get document content
    content = ""
    if 'content' in parsed_doc:
        content = parsed_doc['content']
    else:
        # Try to read file content
        file_path = parsed_doc.get('file_path', '')
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                logger.warning(f"Could not read file content from: {file_path}")
    
    content_lower = content.lower()
    
    # Match against templates
    best_match = None
    best_match_rate = 0.0
    
    for template in templates:
        match_rate = calculate_match_rate(parsed_doc, template, content)
        
        if match_rate > best_match_rate:
            best_match_rate = match_rate
            best_match = template
    
    result["overall_match_rate"] = best_match_rate
    result["best_match_template"] = best_match['id'] if best_match else None
    
    # Check clause coverage
    result["clause_coverage"] = check_clause_coverage(parsed_doc, content)
    
    # Check missing sections
    result["missing_sections"] = identify_missing_sections(parsed_doc, best_match)
    result["existing_sections"] = identify_existing_sections(parsed_doc, best_match)
    
    # Check high-voltage lines
    if check_high_voltage:
        result["high_voltage_check"] = check_high_voltage_lines(content, content_lower)
    
    # Generate recommendations
    result["recommendations"] = generate_recommendations(result)
    
    logger.info(f"Gap analysis complete: match rate = {best_match_rate:.1%}")
    return result

def calculate_match_rate(parsed_doc: Dict, template: Dict, content: str) -> float:
    """
    Calculate match rate between document and template
    Returns:
        Match rate as float (0.0 to 1.0)
    """
    logger.debug(f"Calculating match rate for template: {template['id']}")
    
    # Get template sections
    template_sections = template.get('sections', [])
    if not template_sections:
        return 0.0
    
    # Get document headings
    doc_headings = parsed_doc.get('headings', [])
    doc_heading_texts = [h['text'] for h in doc_headings]
    
    # Calculate section match
    matched_sections = 0
    total_sections = len(template_sections)
    
    for section in template_sections:
        section_title = section.get('title', '')
        
        # Check if section title exists in document (fuzzy match)
        if is_section_present(section_title, doc_heading_texts):
            matched_sections += 1
        elif is_content_present(section, content):
            # Section title not found, but content might be present
            matched_sections += 0.5  # Partial match
    
    match_rate = matched_sections / total_sections if total_sections > 0 else 0.0
    
    logger.debug(f"Template {template['id']}: {matched_sections}/{total_sections} sections matched, rate = {match_rate:.1%}")
    
    return match_rate

def is_section_present(section_title: str, doc_heading_texts: List[str]) -> bool:
    """
    Check if a section is present in document headings
    Supports fuzzy matching (ignores numbering, extra spaces, etc.)
    """
    import re
    
    # Exact match
    if section_title in doc_heading_texts:
        return True
    
    # Remove numbering from section title (e.g., "1. 目的" -> "目的")
    clean_title = re.sub(r'^\d+[\.\、]\s*', '', section_title).strip()
    
    # Check if clean title matches any heading
    for heading in doc_heading_texts:
        # Remove numbering from heading
        clean_heading = re.sub(r'^\d+[\.\、]\s*', '', heading).strip()
        
        # Exact match after cleaning
        if clean_title == clean_heading:
            return True
        
        # Partial match (section title is contained in heading)
        if clean_title in clean_heading or clean_heading in clean_title:
            return True
        
        # Keyword overlap match (at least 1 common keyword)
        title_keywords = set(clean_title.replace(' ', '').lower().split())
        heading_keywords = set(clean_heading.replace(' ', '').lower().split())
        
        # Check if key words overlap
        if len(title_keywords & heading_keywords) >= 1:
            return True
    
    return False

def is_content_present(section: Dict, content: str) -> bool:
    """Check if section content is present in document"""
    section_content = section.get('content', '')
    
    # Extract key phrases from section content
    key_phrases = [phrase.strip() for phrase in section_content.split('；') if phrase.strip()]
    
    # Check if any key phrase is present in content
    for phrase in key_phrases[:3]:  # Check first 3 phrases
        if len(phrase) > 5 and phrase in content:
            return True
    
    return False

def check_clause_coverage(parsed_doc: Dict, content: str) -> Dict:
    """Check ISO 20000-1 clause coverage"""
    logger.debug("Checking clause coverage")
    
    coverage = {}
    
    for clause, description in ISO_CLAUSES.items():
        # Check if clause keywords are present
        clause_num = clause.split('.')[-1] if '.' in clause else clause
        
        # Simple heuristic: check if clause number or keywords are mentioned
        if clause in content or clause_num in content:
            coverage[clause] = {
                "description": description,
                "covered": True,
                "confidence": "high"
            }
        else:
            # Check for related keywords
            keywords = get_clause_keywords(clause)
            if any(keyword in content.lower() for keyword in keywords):
                coverage[clause] = {
                    "description": description,
                    "covered": True,
                    "confidence": "medium"
                }
            else:
                coverage[clause] = {
                    "description": description,
                    "covered": False,
                    "confidence": "low"
                }
    
    return coverage

def get_clause_keywords(clause: str) -> List[str]:
    """Get keywords for a clause"""
    keywords_map = {
        "4": ["环境", "context", "内外部", "相关方"],
        "7.1": ["资源", "resource", "预算", "budget"],
        "7.2": ["能力", "competence", "培训", "training"],
        "7.5": ["文件", "document", "成文信息"],
        "8.2": ["服务目录", "service catalog", "服务交付"],
        "8.3": ["供应商", "supplier", "SLA"],
        "8.4": ["事件", "incident", "问题", "problem"],
        "8.5": ["变更", "change", "发布", "release"],
        "9.2": ["内审", "internal audit", "审核"],
        "9.3": ["管理评审", "management review"],
        "9.4": ["报告", "report", "SLA"],
        "9.5": ["可用性", "availability", "连续性", "continuity"],
        "9.6": ["改进", "improvement", "纠正", "corrective"]
    }
    
    return keywords_map.get(clause, [])

def identify_missing_sections(parsed_doc: Dict, template: Dict) -> List[str]:
    """Identify missing sections compared to template"""
    if not template:
        return []
    
    missing = []
    doc_headings = [h['text'] for h in parsed_doc.get('headings', [])]
    
    for section in template.get('sections', []):
        section_title = section.get('title', '')
        if not is_section_present(section_title, doc_headings):
            missing.append(section_title)
    
    return missing

def identify_existing_sections(parsed_doc: Dict, template: Dict) -> List[str]:
    """Identify existing sections compared to template"""
    if not template:
        return []
    
    existing = []
    doc_headings = [h['text'] for h in parsed_doc.get('headings', [])]
    
    for section in template.get('sections', []):
        section_title = section.get('title', '')
        if is_section_present(section_title, doc_headings):
            existing.append(section_title)
    
    return existing

def check_high_voltage_lines(content: str, content_lower: str) -> Dict:
    """Check high-voltage line compliance"""
    logger.debug("Checking high-voltage lines")
    
    results = {}
    
    for check_id, check_info in HIGH_VOLTAGE_CHECKS.items():
        # Check Chinese keywords
        zh_found = any(keyword in content for keyword in check_info['keywords_zh'])
        
        # Check English keywords
        en_found = any(keyword.lower() in content_lower for keyword in check_info.get('keywords_en', []))
        
        passed = zh_found or en_found
        
        results[check_id] = {
            "name_zh": check_info['name_zh'],
            "name_en": check_info['name_en'],
            "passed": passed,
            "required": check_info['required'],
            "keywords_found": {
                "chinese": [kw for kw in check_info['keywords_zh'] if kw in content],
                "english": [kw for kw in check_info.get('keywords_en', []) if kw.lower() in content_lower]
            }
        }
        
        logger.debug(f"High-voltage check {check_id}: {'PASS' if passed else 'FAIL'}")
    
    return results

def generate_recommendations(gap_result: Dict) -> List[str]:
    """Generate improvement recommendations based on gap analysis"""
    recommendations = []
    
    # Low match rate
    if gap_result['overall_match_rate'] < 0.6:
        recommendations.append("文档整体匹配度较低（<60%），建议参考标准模板重新组织文档结构")
    
    # Missing sections
    missing = gap_result.get('missing_sections', [])
    if missing:
        recommendations.append(f"缺少以下章节：{', '.join(missing[:5])}（共{len(missing)}个）")
    
    # High-voltage line failures
    hv_checks = gap_result.get('high_voltage_check', {})
    failed_checks = [k for k, v in hv_checks.items() if not v['passed'] and v['required']]
    
    if failed_checks:
        recommendations.append("⚠️ 高压线检查未通过，存在合规风险：")
        for check_id in failed_checks:
            check_name = hv_checks[check_id]['name_zh']
            recommendations.append(f"  - {check_name}：未满足要求")
    
    # Clause coverage gaps
    clause_coverage = gap_result.get('clause_coverage', {})
    uncovered_clauses = [k for k, v in clause_coverage.items() if not v['covered']]
    
    if uncovered_clauses:
        recommendations.append(f"以下ISO条款未覆盖：{', '.join(uncovered_clauses[:5])}（共{len(uncovered_clauses)}个）")
    
    return recommendations

def main():
    """Main function with command-line interface"""
    logger.info("=" * 60)
    logger.info("analyze_gap.py v2.0 - ISO 20000-1 Gap Analyzer")
    logger.info("=" * 60)
    
    # Validate command-line arguments
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  python analyze_gap.py <parsed_json_path> <templates_json_path> [output_json_path]")
        print("\nExamples:")
        print("  python analyze_gap.py parsed.json templates/generic_templates.json")
        print("  python analyze_gap.py parsed.json templates/bilingual_templates.json output.json")
        print("\nOptions:")
        print("  --no-high-voltage  Disable high-voltage line checking")
        sys.exit(1)
    
    parsed_json_path = sys.argv[1]
    templates_json_path = sys.argv[2]
    output_json_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Parse optional arguments
    check_high_voltage = "--no-high-voltage" not in sys.argv
    
    logger.info(f"Input parsed JSON: {parsed_json_path}")
    logger.info(f"Input templates JSON: {templates_json_path}")
    if output_json_path:
        logger.info(f"Output JSON: {output_json_path}")
    logger.info(f"Check high-voltage lines: {check_high_voltage}")
    
    # Load parsed document
    try:
        with open(parsed_json_path, 'r', encoding='utf-8') as f:
            parsed_doc = json.load(f)
        logger.info(f"Loaded parsed document: {parsed_doc.get('file_name', 'Unknown')}")
    except Exception as e:
        logger.error(f"Failed to load parsed JSON: {str(e)}")
        print(f"\n❌ Failed to load parsed JSON: {str(e)}")
        sys.exit(1)
    
    # Load templates
    try:
        templates = load_template(templates_json_path)
    except Exception as e:
        logger.error(f"Failed to load templates: {str(e)}")
        print(f"\n❌ Failed to load templates: {str(e)}")
        sys.exit(1)
    
    # Perform gap analysis
    try:
        result = analyze_gap(parsed_doc, templates, check_high_voltage)
    except Exception as e:
        logger.error(f"Gap analysis failed: {str(e)}")
        print(f"\n❌ Gap analysis failed: {str(e)}")
        sys.exit(1)
    
    # Output results
    if output_json_path:
        try:
            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logger.info(f"Output written to: {output_json_path}")
            print(f"\n✅ Output written to: {output_json_path}")
        except Exception as e:
            logger.error(f"Failed to write output file: {str(e)}")
            print(f"\n❌ Failed to write output file: {str(e)}")
            sys.exit(1)
    else:
        # Print to stdout
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Gap Analysis Summary")
    print("=" * 60)
    print(f"File: {result['file_name']}")
    print(f"Overall Match Rate: {result['overall_match_rate']:.1%}")
    print(f"Best Match Template: {result['best_match_template']}")
    print(f"Missing Sections: {len(result['missing_sections'])}")
    print(f"Existing Sections: {len(result['existing_sections'])}")
    
    # High-voltage line results
    hv_checks = result.get('high_voltage_check', {})
    if hv_checks:
        print(f"\nHigh-Voltage Line Checks:")
        for check_id, check_result in hv_checks.items():
            status = "✅ PASS" if check_result['passed'] else "❌ FAIL"
            print(f"  {check_result['name_zh']}: {status}")
    
    # Recommendations
    recommendations = result.get('recommendations', [])
    if recommendations:
        print(f"\nRecommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    print("=" * 60)
    
    # Exit with appropriate code
    if result['status'] == 'success':
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
