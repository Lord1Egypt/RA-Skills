# -*- coding: utf-8 -*-
"""
IRAC 法律逻辑分析引擎 v1.0
SkillHub 适配版 — 标准 IRAC 推理框架。

六阶段：
  1. Jurisdiction — 管辖权确认
  2. Facts       — 事实梳理
  3. Issues      — 争议焦点提炼
  4. Law         — 法律适用分析
  5. Application — 法律→事实适用
  6. Risk        — 风险识别与量化

IRAC Schema（标准化 JSON 输出格式）：
  {
    "jurisdiction": {...},
    "facts": {...},
    "issues": [...],
    "analysis": {
      "issue_id": {
        "rule": {...},
        "application": {...},
        "conclusion": {...}
      }
    },
    "risks": [...],
    "summary": {...}
  }
"""

import json
import re
from typing import List, Dict, Any


def build_irac_schema(case_info: Dict[str, Any]) -> Dict[str, Any]:
    """从案件信息构建 IRAC Schema 骨架"""
    schema = {
        "jurisdiction": {
            "court_level": case_info.get("court_level", "基层人民法院"),
            "court_location": case_info.get("court_location", "待确认"),
            "case_type": case_info.get("case_type", "民事一审"),
            "case_cause": case_info.get("case_cause", ""),
            "notes": [],
        },
        "facts": {
            "timeline": case_info.get("timeline", []),
            "contract_info": case_info.get("contract_info", {}),
            "payment_info": case_info.get("payment_info", {}),
            "key_documents": case_info.get("key_documents", []),
            "outstanding_amount": case_info.get("outstanding_amount", "待核实"),
        },
        "issues": [],
        "analysis": {},
        "risks": [],
        "summary": {
            "favorable_factors": [],
            "unfavorable_factors": [],
            "recommended_actions": [],
            "estimated_success_rate": "待评估",
        },
    }
    return schema


def extract_issues_from_facts(facts: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从事实中提炼争议焦点"""
    issues = []

    # 合同纠纷标准焦点
    if facts.get("contract_info"):
        issues.append({
            "id": "I001",
            "title": "合同效力与履行",
            "question": "合同是否合法有效？双方是否按约履行？",
            "party_claim": "",
            "counterparty_position": "",
        })

    # 欠款/货款焦点
    if facts.get("outstanding_amount") and facts["outstanding_amount"] != "待核实":
        issues.append({
            "id": "I002",
            "title": "欠款金额确认",
            "question": f"欠款金额{facts['outstanding_amount']}元是否有充分证据支撑？",
            "party_claim": "",
            "counterparty_position": "",
        })

    # 违约责任
    if facts.get("breach_info"):
        issues.append({
            "id": "I003",
            "title": "违约责任认定",
            "question": "对方是否存在违约行为？应承担何种违约责任？",
            "party_claim": "",
            "counterparty_position": "",
        })

    return issues


def build_issue_analysis(issue: Dict[str, Any], law_refs: List[str], case_refs: List[str]) -> Dict[str, Any]:
    """构建单个争议焦点的 IRAC 分析"""
    return {
        "issue_id": issue.get("id", ""),
        "issue_title": issue.get("title", ""),
        "rule": {
            "applicable_laws": [{"ref": ref, "status": "有效", "relevance": "直接相关"} for ref in law_refs],
            "legal_principle": "",
            "burden_of_proof": "原告对主张的事实承担举证责任（《民事诉讼法》第67条）",
        },
        "application": {
            "facts_proved": [],
            "facts_unproved": [],
            "case_analogies": [{"case_ref": ref, "similarity": "待评估"} for ref in case_refs],
            "analysis": "",
        },
        "conclusion": {
            "finding": "",
            "confidence": "中等",
            "alternative_arguments": [],
        },
        "risk": {
            "risk_level": "中等",
            "main_risk": "",
            "mitigation": "",
        },
    }


def validate_irac_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """验证 IRAC Schema 完整性"""
    errors = []
    warnings = []

    if not schema.get("jurisdiction", {}).get("case_cause"):
        errors.append("缺少案由")

    if not schema.get("facts", {}).get("timeline"):
        warnings.append("缺少时间线")

    if not schema.get("issues"):
        errors.append("缺少争议焦点")

    if not schema.get("analysis"):
        errors.append("缺少法律分析")

    for issue_id, analysis in schema.get("analysis", {}).items():
        if not analysis.get("rule", {}).get("applicable_laws"):
            warnings.append(f"Issue {issue_id}: 缺少适用法条")
        if not analysis.get("conclusion", {}).get("finding"):
            warnings.append(f"Issue {issue_id}: 缺少分析结论")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def format_irac_markdown(schema: Dict[str, Any]) -> str:
    """将 IRAC Schema 格式化为 Markdown 报告"""
    lines = []
    lines.append("# IRAC 法律逻辑分析报告")
    lines.append("")

    # Jurisdiction
    j = schema.get("jurisdiction", {})
    lines.append("## 一、管辖权确认")
    lines.append(f"- 管辖法院: {j.get('court_level', '')}")
    lines.append(f"- 管辖地: {j.get('court_location', '')}")
    lines.append(f"- 案件类型: {j.get('case_type', '')}")
    lines.append(f"- 案由: {j.get('case_cause', '')}")
    lines.append("")

    # Facts
    facts = schema.get("facts", {})
    lines.append("## 二、事实梳理")
    if facts.get("timeline"):
        lines.append("### 时间线")
        for event in facts["timeline"]:
            lines.append(f"- {event.get('date', '')}: {event.get('event', '')}")
    lines.append("")

    # Issues
    lines.append("## 三、争议焦点")
    for issue in schema.get("issues", []):
        lines.append(f"### {issue.get('id', '')} {issue.get('title', '')}")
        lines.append(f"- 核心问题: {issue.get('question', '')}")
        lines.append("")
        analysis = schema.get("analysis", {}).get(issue.get("id", ""), {})
        if analysis:
            rule = analysis.get("rule", {})
            if rule.get("applicable_laws"):
                lines.append("适用法律:")
                for law in rule["applicable_laws"]:
                    lines.append(f"  - {law['ref']}")
            conclusion = analysis.get("conclusion", {})
            if conclusion.get("finding"):
                lines.append(f"分析结论: {conclusion['finding']}")
        lines.append("")

    # Risks
    lines.append("## 四、风险识别")
    for risk in schema.get("risks", []):
        lines.append(f"- [{risk.get('level', '')}] {risk.get('description', '')}")
        if risk.get("mitigation"):
            lines.append(f"  应对: {risk['mitigation']}")
    lines.append("")

    # Summary
    s = schema.get("summary", {})
    lines.append("## 五、综合评估")
    lines.append(f"有利因素: {', '.join(s.get('favorable_factors', [])) or '待补充'}")
    lines.append(f"不利因素: {', '.join(s.get('unfavorable_factors', [])) or '待补充'}")
    lines.append(f"建议: {', '.join(s.get('recommended_actions', [])) or '待补充'}")

    return "\n".join(lines)
