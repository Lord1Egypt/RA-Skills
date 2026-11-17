# -*- coding: utf-8 -*-
"""
Skeleton Checker v1.0
文书骨架完整性检查器 — 从 skeleton_checker v1.1 适配为 SkillHub 版本。
提供: check_skeleton, check_parties, precheck_and_warn, sniff_doc_type
"""

import os
import re
import json

SKELETON_CONFIG = {
    "起诉状": {
        "struct_elements": [
            ["民事起诉状", "标题"],
            ["原告", "原告"],
            ["被告", "被告"],
            ["诉讼请求", "诉讼请求"],
            ["事实与理由", "事实与理由"],
            ["此致", "此致"],
            ["人民法院", "法院名称"],
            ["具状人", "具状人"],
        ],
        "date_pattern": r"\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日",
        "requires_party_coverage": True,
        "party_roles": ["原告", "被告", "第三人"],
    },
    "答辩状": {
        "struct_elements": [
            ["民事答辩状", "标题"],
            ["答辩人", "答辩人"],
            ["被答辩人", "被答辩人"],
            ["答辩意见", "答辩意见"],
            ["此致", "此致"],
            ["人民法院", "法院名称"],
            ["答辩人", "答辩人落款"],
        ],
        "date_pattern": r"\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日",
        "requires_party_coverage": True,
        "party_roles": ["原告", "被告"],
    },
    "授权委托书": {
        "struct_elements": [
            ["授权委托书", "标题"],
            ["委托人", "委托人"],
            ["受委托人", "受委托人"],
            ["委托权限", "委托权限"],
            ["律师事务所", "律所名称"],
        ],
        "date_pattern": r"\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日",
        "requires_party_coverage": True,
        "party_roles": ["被告"],
    },
    "出庭函": {
        "struct_elements": [
            ["律师参加诉讼", "律师标识"],
            ["贵院", "法院称呼"],
            ["律师事务所", "律所名称"],
        ],
        "requires_party_coverage": False,
    },
    "委托代理协议": {
        "struct_elements": [
            ["委托代理协议", "标题"],
            ["甲方", "甲方信息"],
            ["乙方", "乙方信息"],
            ["代理事项", "代理事项"],
            ["代理权限", "代理权限"],
        ],
        "date_pattern": r"\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日",
        "requires_party_coverage": True,
        "party_roles": ["被告"],
    },
    "证据目录": {
        "struct_elements": [
            ["证据目录", "标题"],
            ["证据名称", "证据名称"],
            ["提交人", "提交人"],
        ],
        "requires_party_coverage": False,
    },
    "代理词": {
        "struct_elements": [
            ["代理意见", "标题"],
            ["尊敬的审判长", "法院称呼"],
            ["以上意见", "结尾"],
        ],
        "requires_party_coverage": False,
    },
    "谈话笔录": {
        "struct_elements": [
            ["律师接待当事人谈话笔录", "标题"],
            ["律师", "律师标识"],
            ["服务风险", "风险告知"],
            ["签字", "签字"],
        ],
        "requires_party_coverage": False,
    },
}


def _get_critical_labels(config):
    """提取关键结构元素（hard fail if missing）"""
    critical = {"标题", "此致", "法院名称", "具状人", "答辩人落款",
                "代理人落款", "律师标识", "法院称呼", "律所名称",
                "委托人", "甲方信息", "乙方信息"}
    return critical


def check_skeleton(doc_text, doc_type=""):
    """检查文书是否包含所有必需结构元素"""
    config = SKELETON_CONFIG.get(doc_type)
    if config is None:
        return {"passed": True, "reason": "无骨架配置", "missing": [], "skipped": True, "critical_missing": []}

    critical_labels = _get_critical_labels(config)
    missing = []
    for item in config["struct_elements"]:
        if item[0] not in doc_text:
            missing.append(item[1])

    date_pat = config.get("date_pattern", r"\d{4}\s*年")
    if not re.search(date_pat, doc_text):
        missing.append("日期")

    critical_missing = [m for m in missing if m in critical_labels]
    passed = len(missing) == 0

    return {
        "passed": passed,
        "reason": "" if passed else f"缺少结构元素: {missing}",
        "missing": missing,
        "critical_missing": critical_missing,
        "skipped": False,
    }


def check_parties(doc_text, doc_type="", case_data_path=None):
    """检查当事人覆盖完整性"""
    config = SKELETON_CONFIG.get(doc_type, {})
    if not config.get("requires_party_coverage", False):
        return {"passed": True, "reason": "不需要当事人覆盖检查", "missing": [], "skipped": False}

    if case_data_path is None or not os.path.exists(case_data_path):
        return {"passed": True, "reason": "无案件数据JSON", "missing": [], "skipped": True}

    try:
        with open(case_data_path, "r", encoding="utf-8") as f:
            case_data = json.load(f)
    except Exception as e:
        return {"passed": True, "reason": f"JSON读取失败: {e}", "missing": [], "skipped": True}

    parties_table = case_data.get("诉讼地位表", {})
    if not parties_table:
        return {"passed": True, "reason": "当事人表为空", "missing": [], "skipped": True}

    required_roles = set(config.get("party_roles", []))
    missing = []
    for name, info in parties_table.items():
        role = info.get("角色", "")
        if role in required_roles:
            if name not in doc_text:
                short = name.replace("有限公司", "").replace("有限责任公司", "")
                if short not in doc_text:
                    missing.append(f"{role}:{name}")

    passed = len(missing) == 0
    return {
        "passed": passed,
        "reason": "" if passed else f"缺失当事人: {missing}",
        "missing": missing,
        "skipped": False,
    }


def precheck_and_warn(doc, doc_type, case_data_path=None):
    """生成前骨架预检：关键缺失阻断，非关键预警"""
    full_text = "\n".join([p.text for p in doc.paragraphs])
    sk_result = check_skeleton(full_text, doc_type)
    pt_result = check_parties(full_text, doc_type, case_data_path)

    if sk_result["critical_missing"]:
        raise RuntimeError(
            f"[阻断] [{doc_type}] 关键骨架缺失: {sk_result['critical_missing']}。请修正后重新生成。"
        )

    warnings = []
    if sk_result["missing"]:
        warnings.append(f"骨架({','.join(sk_result['missing'])})")
    if pt_result["missing"]:
        warnings.append(f"当事人({','.join(pt_result['missing'])})")

    if warnings:
        print(f"\n[预警] [{doc_type}] 预检发现问题（QC阶段将硬失败）:")
        for w in warnings:
            print(f"    - {w}")

    return {"passed": len(warnings) == 0, "skeleton": sk_result, "parties": pt_result, "warnings": warnings}


SNIFF_PATTERNS = [
    ("民事起诉状", "起诉状"),
    ("民事答辩状", "答辩状"),
    ("代理意见", "代理词"),
    ("证据目录", "证据目录"),
    ("证据名称", "证据目录"),
    ("授权委托书", "授权委托书"),
    ("委托代理协议", "委托代理协议"),
    ("律师接待当事人谈话笔录", "谈话笔录"),
]


def sniff_doc_type(doc_text):
    """内容嗅探兜底：从文书全文识别类型"""
    for keyword, dtype in SNIFF_PATTERNS:
        if keyword in doc_text:
            return dtype
    return ""
