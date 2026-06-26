"""
法眼（LawEye）— 合同审查引擎
基于规则 + 模式的合同风险自动分析
"""

import re
import json
import time
from typing import List, Dict

# ==================== 风险规则库 ====================

RISK_RULES = [
    # (规则名称, 正则模式, 风险等级, 问题描述, 修改建议)
    ("违约责任不对等", r'(违约).{0,10}(仅|只|单方|甲方.{0,5}乙方|乙方.{0,5}甲方).{0,15}(承担|赔偿|责任)', "高",
     "违约责任条款存在不对等，可能加重一方责任",
     "建议将违约金比例或责任范围调整为双方对等，明确各自的违约责任"),
    ("无限责任条款", r'(无限|无上限|全部损失|所有损失).{0,10}(责任|赔偿|承担)', "高",
     "存在无限责任条款，可能导致承担远超预期的损失",
     "建议设置赔偿上限，如约定赔偿总额不超过合同金额的X倍"),
    ("知识产权归属模糊", r'(知识产权|著作权|专利权|商标权).{0,15}(归属|属于|所有)', "中",
     "知识产权归属条款不够明确，可能引发权属争议",
     "明确约定知识产权归属方、使用许可范围及限制"),
    ("管辖法院约定不明", r'(管辖|仲裁|诉讼).{0,10}(法院|机构|地点|所在地)', "低",
     "争议解决条款未明确管辖法院或仲裁机构",
     "明确约定管辖法院为乙方/甲方所在地人民法院，或指定具体仲裁机构"),
    ("保密义务不对称", r'(保密).{0,10}(义务|责任).{0,10}(仅|单方|甲方.{0,10}乙方|乙方.{0,10}甲方)', "中",
     "保密义务仅约束一方，缺乏双向保护",
     "建议保密义务双向对等，明确保密期限、范围和违约后果"),
    ("验收标准缺失", r'(验收|交付|完成).{0,15}(标准|条件|时间)', "中",
     "验收标准或交付条件不够明确",
     "明确验收标准、验收流程、验收期限及未通过验收的处理方式"),
    ("解除权不对等", r'(解除|终止).{0,15}(合同|协议).{0,10}(有权|可以).{0,10}(单方|任意)', "高",
     "合同解除权可能存在不对等",
     "建议明确解除条件，避免任意单方解除权，约定解除后的清算安排"),
    ("违约金过高", r'(违约金|罚款|罚金).{0,10}(每日.{0,5}|每.{0,2}日).{0,10}(%|‰|千分|百分)', "中",
     "违约金计算标准可能过高",
     "违约金日费率不宜超过万分之五，总额不宜超过合同金额的30%"),
    ("自动续期陷阱", r'(自动.{0,5}(续期|续约|延长|展期))|(期满.{0,10}(自动|默认).{0,5}(续期|续约|延长))', "低",
     "包含自动续期/续约条款，可能导致被动续约",
     "建议设置续约前的书面通知义务，或改为到期需双方另行确认"),
    ("空白填写项", r'(＿＿|___|——|……)|（\s*）|\(\s*\)', "高",
     "存在未填写的空白项或占位符",
     "请填写完整所有空白项后再签署，避免后续争议"),
    ("付款条件模糊", r'(付款|支付|费用).{0,20}(另行|协商|不确定|待定)', "中",
     "付款条件表述模糊，缺少明确的支付节点和金额",
     "明确付款节点、金额、方式和期限，避免歧义"),
    ("免责条款过宽", r'(免责|免除责任).{0,20}(任何|一切|所有|全部)', "高",
     "免责条款范围过宽，可能排除基本合同义务",
     "免责条款应符合法律规定，不可排除故意或重大过失责任"),
    ("竞业限制模糊", r'(竞业|竞争.{0,5}(禁止|限制)).{0,10}(范围|期限|补偿)', "中",
     "竞业限制范围、期限或补偿标准不明确",
     "明确竞业限制的地域、行业范围、期限及经济补偿标准"),
    ("数据合规缺失", r'(数据|信息|隐私|个人信息).{0,20}(收集|使用|处理|共享|转让)', "中",
     "涉及数据处理但缺少合规条款",
     "建议增加数据保护条款，明确数据处理目的、方式、范围及合规义务"),
    ("不可抗力模糊", r'(不可抗力).{0,5}(范围|定义)', "低",
     "不可抗力条款的定义或范围不够具体",
     "明确列举不可抗力事件类型，并约定发生后的通知和处理流程"),
]

# ==================== 条文提取 ====================

def extract_clauses(text: str) -> List[Dict]:
    """从合同文本中提取条款"""
    clauses = []
    # 匹配 "第X条" 或 "第X款" 或 "X." 开头的条款
    pattern = r'(第[一二三四五六七八九十百零\d]+[条条款项])\s*(.*?)(?=第[一二三四五六七八九十百零\d]+[条条款项]|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)
    for i, (title, content) in enumerate(matches):
        clauses.append({
            "index": i + 1,
            "title": title.strip(),
            "content": content.strip()[:500],  # 截取前500字符
        })
    if not clauses:
        # 回退: 按段落拆分
        paragraphs = [p.strip() for p in text.split('\n') if len(p.strip()) > 20]
        for i, p in enumerate(paragraphs[:30]):
            clauses.append({
                "index": i + 1,
                "title": f"条款{i+1}",
                "content": p[:500],
            })
    return clauses


def analyze_clause(clause_text: str) -> List[Dict]:
    """对单个条款执行风险检测"""
    findings = []
    for rule_name, pattern, level, issue, suggestion in RISK_RULES:
        if re.search(pattern, clause_text):
            findings.append({
                "rule": rule_name,
                "risk": level,
                "issue": issue,
                "suggestion": suggestion,
            })
    return findings


def review_contract(content: str, tier: str = "basic") -> Dict:
    """
    合同审查入口
    tier: basic = 快速扫描（最多10页，仅标记不修改）
          pro = 深度审查（含修改建议、法条引用）
    """
    clauses = extract_clauses(content)
    all_findings = []
    risk_stats = {"高": 0, "中": 0, "低": 0}

    for clause in clauses:
        findings = analyze_clause(clause["title"] + clause["content"])
        for f in findings:
            f["clause"] = clause["title"]
            f["clause_index"] = clause["index"]
            all_findings.append(f)
            risk_stats[f["risk"]] += 1

    # 去重合并（同一规则同一条款只保留一个）
    seen = set()
    unique_findings = []
    for f in all_findings:
        key = (f["rule"], f["clause"])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    total = sum(risk_stats.values())

    # 生成审查摘要
    if total == 0:
        summary = "未检测到明显风险条款，合同整体风险较低。建议仍由专业律师复核。"
    else:
        parts = []
        if risk_stats["高"] > 0:
            parts.append(f"{risk_stats['高']} 处高风险")
        if risk_stats["中"] > 0:
            parts.append(f"{risk_stats['中']} 处中风险")
        if risk_stats["低"] > 0:
            parts.append(f"{risk_stats['低']} 处低风险")
        summary = f"检测到 {total} 处风险条款（{'、'.join(parts)}）："
        for f in unique_findings[:5]:
            summary += f" {f['rule']}（{f['clause']}）；"
        if len(unique_findings) > 5:
            summary += f" 等共{len(unique_findings)}项"

    result = {
        "service": "法眼·AI合同审查",
        "tier": tier,
        "risks_found": total,
        "risk_stats": risk_stats,
        "summary": summary,
        "details": unique_findings,
        "legal_reference": [
            {"law": "《中华人民共和国民法典》", "articles": ["第496条（格式条款）", "第497条（无效格式条款）", "第585条（违约金调整）"]},
        ] if tier == "pro" else [],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    return result


# ==================== 测试 ====================

if __name__ == "__main__":
    test_contract = """
第一条 委托事项
甲方委托乙方进行软件开发，具体内容见附件。

第二条 违约责任
乙方未按期交付，每日按合同金额的5%支付违约金。甲方单方解除合同，不承担任何责任。

第三条 知识产权
项目产生的一切知识产权归甲方所有，乙方不得有任何使用权利。

第四条 管辖
因本合同产生的争议，由甲方所在地法院管辖。

第五条 保密
乙方对甲方提供的所有信息承担保密责任，保密期限为无限期。

第六条 付款
付款条件另行协商确定。

第七条 免责
乙方对因使用软件产生的任何损失不承担责任。

第八条 验收
验收标准由甲方自行确定。
"""
    result = review_contract(test_contract, "pro")
    print(json.dumps(result, ensure_ascii=False, indent=2))
