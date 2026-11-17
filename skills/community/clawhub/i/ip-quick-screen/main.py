#!/usr/bin/env python3
"""
IP快速筛查（尽调初筛） - 核心脚本
面向技术尽调场景，对企业的专利组合进行快速筛查和风险预警

数据源：USPTO PatentsView API（免费，无需认证）
         Google Patents 公开查询（备选）
"""

import os
import sys
import json
import re
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from coze_workload_identity import requests

# ============================================================
# 常量定义
# ============================================================

USPTO_API_URL = "https://api.patentsview.org/patents/query"

# IPC大类 - 技术领域映射（常用）
IPC_SECTION_MAP = {
    "A": "人类生活必需（农/医/轻工）",
    "B": "作业与运输",
    "C": "化学与冶金",
    "D": "纺织与造纸",
    "E": "固定建筑物",
    "F": "机械工程/照明/加热/武器",
    "G": "物理学（计算/测量/控制）",
    "H": "电学（电信/电力/电子）",
}

IPC_CLASS_MAP = {
    "A01": "农业/林业/畜牧业",
    "A23": "食品/烟草",
    "A61": "医学/卫生学",
    "A63": "体育/娱乐",
    "B01": "物理/化学工艺设备",
    "B23": "机床/金属加工",
    "B25": "手工工具",
    "B60": "一般车辆",
    "B65": "输送/包装/存储",
    "C02": "水/废水处理",
    "C07": "有机化学",
    "C08": "有机高分子化合物",
    "C12": "生物化学/微生物学",
    "E04": "建筑物",
    "E21": "钻进/采矿",
    "F16": "工程元件",
    "F24": "供热/制冷/通风",
    "G01": "测量/测试",
    "G02": "光学",
    "G06": "计算/推算/计数",
    "G08": "信号装置",
    "G09": "教育/密码",
    "G10": "乐器/声学",
    "G11": "信息存储",
    "G16": "专门适用ICT的",
    "H01": "基本电气元件",
    "H02": "发电/变电/配电",
    "H03": "基本电子电路",
    "H04": "电通信技术",
    "H05": "其他电学",
}

# ============================================================
# 数据查询层
# ============================================================

def search_patents_by_assignee(company_name: str, limit: int = 100) -> List[Dict]:
    """
    通过USPTO PatentsView API按专利权人（公司名）搜索专利
    """
    query = {
        "q": {
            "_and": [
                {"assignee_organization": {"_like": company_name}}
            ]
        },
        "f": [
            "patent_number", "patent_title", "patent_abstract",
            "patent_date", "patent_issue_date",
            "patent_kind", "patent_type",
            "patent_number",
            "cpc_subsection_id",
            "cited_patent_count",
            "citedby_patent_count",
            "patent_year"
        ],
        "o": {"per_page": limit, "page": 1}
    }

    try:
        resp = requests.post(
            USPTO_API_URL,
            json=query,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        if resp.status_code != 200:
            raise Exception(f"API请求失败: HTTP {resp.status_code}")

        data = resp.json()
        patents = data.get("patents", [])

        # 补充查询同族信息
        if patents:
            patent_ids = [p.get("patent_number") for p in patents if p.get("patent_number")]
            families = _get_patent_family_info(patent_ids)
            for p in patents:
                pn = p.get("patent_number", "")
                if pn in families:
                    p["_family_info"] = families[pn]

        return patents

    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("API返回数据格式异常")
    except Exception as e:
        raise Exception(f"查询专利失败: {str(e)}")


def search_patents_by_numbers(patent_numbers: List[str]) -> List[Dict]:
    """
    按专利号列表查询专利详情
    """
    # 标准化专利号格式
    formatted_numbers = []
    for pn in patent_numbers:
        pn = pn.strip().upper()
        # 去除可能的US前缀已存在的情况
        if not pn.startswith("US"):
            pn = f"US{pn}"
        formatted_numbers.append(pn)

    query = {
        "q": {
            "patent_number": formatted_numbers
        },
        "f": [
            "patent_number", "patent_title", "patent_abstract",
            "patent_date", "patent_issue_date",
            "patent_kind", "patent_type",
            "cpc_subsection_id",
            "cited_patent_count",
            "citedby_patent_count",
            "patent_year",
            "assignee_organization"
        ],
        "o": {"per_page": len(formatted_numbers), "page": 1}
    }

    try:
        resp = requests.post(
            USPTO_API_URL,
            json=query,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        if resp.status_code != 200:
            raise Exception(f"API请求失败: HTTP {resp.status_code}")

        data = resp.json()
        patents = data.get("patents", [])

        # 补充同族信息
        if patents:
            patent_ids = [p.get("patent_number") for p in patents if p.get("patent_number")]
            families = _get_patent_family_info(patent_ids)
            for p in patents:
                pn = p.get("patent_number", "")
                if pn in families:
                    p["_family_info"] = families[pn]

        return patents

    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("API返回数据格式异常")
    except Exception as e:
        raise Exception(f"查询专利失败: {str(e)}")


def _get_patent_family_info(patent_numbers: List[str]) -> Dict[str, Dict]:
    """
    查询专利族信息（同族专利）
    使用PatentsView的同族查询功能，统计同族专利数量
    """
    if not patent_numbers:
        return {}

    # 分批查询（API限制）
    families = {}
    batch_size = 25
    # 先收集所有family_id
    family_id_to_patents = {}
    for i in range(0, len(patent_numbers), batch_size):
        batch = patent_numbers[i:i+batch_size]
        try:
            query = {
                "q": {"patent_number": batch},
                "f": [
                    "patent_number",
                    "patent_family_id",
                    "patent_kind"
                ],
                "o": {"per_page": len(batch), "page": 1}
            }
            resp = requests.post(
                USPTO_API_URL,
                json=query,
                timeout=15,
                headers={"Content-Type": "application/json"}
            )
            if resp.status_code == 200:
                data = resp.json()
                for p in data.get("patents", []):
                    pn = p.get("patent_number", "")
                    family_id = p.get("patent_family_id")
                    if pn and family_id:
                        if family_id not in family_id_to_patents:
                            family_id_to_patents[family_id] = []
                        family_id_to_patents[family_id].append(pn)
        except Exception:
            pass

    # 第二步：查询每个family_id下的同族专利数量
    unique_family_ids = list(family_id_to_patents.keys())
    for i in range(0, len(unique_family_ids), batch_size):
        batch_fids = unique_family_ids[i:i+batch_size]
        try:
            query = {
                "q": {"patent_family_id": batch_fids},
                "f": ["patent_number", "patent_family_id"],
                "o": {"per_page": 200, "page": 1}
            }
            resp = requests.post(
                USPTO_API_URL,
                json=query,
                timeout=15,
                headers={"Content-Type": "application/json"}
            )
            if resp.status_code == 200:
                data = resp.json()
                # 统计每个family_id的专利数量
                family_member_count = {}
                for p in data.get("patents", []):
                    fid = p.get("patent_family_id")
                    if fid:
                        family_member_count[fid] = family_member_count.get(fid, 0) + 1
                # 回填到每个专利
                for fid, pns in family_id_to_patents.items():
                    count = family_member_count.get(fid, len(pns))
                    for pn in pns:
                        families[pn] = {
                            "family_id": fid,
                            "family_size": count
                        }
        except Exception:
            # 如果第二步查询失败，至少返回family_id
            for fid, pns in family_id_to_patents.items():
                for pn in pns:
                    families[pn] = {"family_id": fid, "family_size": len(pns)}

    return families


# ============================================================
# 分析处理层
# ============================================================

def analyze_patent_portfolio(patents: List[Dict], company_name: str = "") -> Dict:
    """
    分析专利组合，生成概览报告
    """
    if not patents:
        return {"error": "未查询到专利数据", "company_name": company_name, "total": 0}

    # 1. 基本信息统计
    total = len(patents)
    today = date.today()

    # 2. 技术领域分布（按CPC大组）
    tech_distribution = {}
    for p in patents:
        cpc = p.get("cpc_subsection_id") or ""
        if cpc and len(cpc) >= 3:
            section = cpc[0:1]
            ipc_class = cpc[0:3]
        else:
            section = "X"
            ipc_class = "X00"

        tech_name = IPC_CLASS_MAP.get(ipc_class) or IPC_SECTION_MAP.get(section) or "其他"
        if tech_name not in tech_distribution:
            tech_distribution[tech_name] = {"count": 0, "patents": []}
        tech_distribution[tech_name]["count"] += 1
        tech_distribution[tech_name]["patents"].append(p.get("patent_number", ""))

    # 3. 法律状态推断（基于kind code和年份）
    legal_status = {"授权有效": 0, "审查中": 0, "已失效": 0, "未知": 0}
    for p in patents:
        kind = p.get("patent_kind", "")
        year = p.get("patent_year")
        issue_date = p.get("patent_issue_date") or p.get("patent_date", "")

        if not year and issue_date:
            try:
                year = int(issue_date[:4])
            except (ValueError, IndexError):
                year = None

        # 专利有效期 = 申请日起20年（简化处理）
        # 授权后专利（B1/B2）且距今超过20年 → 可能失效
        expiry_year = (year + 20) if year else None

        if kind in ("B1", "B2", "B") and expiry_year:
            if expiry_year < today.year:
                legal_status["已失效"] += 1
            elif expiry_year <= today.year + 3:
                legal_status["授权有效"] += 1  # 即将到期，但仍在有效期内
            else:
                legal_status["授权有效"] += 1
        elif kind in ("A", "A1", "A2"):
            legal_status["审查中"] += 1
        elif kind in ("E", "P", "S"):
            legal_status["已失效"] += 1
        else:
            legal_status["未知"] += 1

    # 调整：无数据的status归到未知
    unknown_count = legal_status["未知"]
    effective_total = total - unknown_count
    if effective_total <= 0 and total > 0:
        # 如果都是未知，根据年份逻辑重新估算
        for p in patents:
            year = p.get("patent_year")
            issue_date = p.get("patent_issue_date") or p.get("patent_date", "")
            if not year and issue_date:
                try:
                    year = int(issue_date[:4])
                except (ValueError, IndexError):
                    year = None
            if year:
                expiry = year + 20
                if expiry < today.year:
                    legal_status["已失效"] += 1
                else:
                    legal_status["授权有效"] += 1
                unknown_count -= 1

        legal_status["未知"] = max(0, unknown_count)

    # 4. 质量初筛指标
    quality_scores = []
    for p in patents:
        pn = p.get("patent_number", "")
        citedby = p.get("citedby_patent_count", 0) or 0
        cited = p.get("cited_patent_count", 0) or 0

        # 申请日/公开日
        pub_date_str = p.get("patent_issue_date") or p.get("patent_date", "")

        # 剩余保护期估算
        year = p.get("patent_year")
        if not year and pub_date_str:
            try:
                year = int(pub_date_str[:4])
            except (ValueError, IndexError):
                year = None

        if year:
            expiry_year = year + 20
            remaining = max(0, expiry_year - today.year)
        else:
            remaining = None

        # 同族信息
        family_info = p.get("_family_info", {})
        family_size = family_info.get("family_size", 1) if family_info else 1  # 从同族信息获取实际数量，默认至少自身

        # 综合标记逻辑
        indicators = []
        score_level = "一般"

        if citedby is not None:
            if citedby >= 50:
                indicators.append("被引量高")
            elif citedby >= 20:
                indicators.append("被引量中")
            elif citedby >= 1:
                indicators.append("有被引")

        if remaining is not None:
            if remaining >= 10:
                indicators.append(f"剩余{remaining}年·保护期长")
            elif remaining >= 3:
                indicators.append(f"剩余{remaining}年·保护期中")
            elif remaining >= 0:
                indicators.append(f"即将到期·剩余{remaining}年")
            else:
                indicators.append("已过保护期")

        # 综合标记
        high_score = 0
        if citedby is not None and citedby >= 50:
            high_score += 1
        if remaining is not None and remaining >= 10:
            high_score += 1
        if family_size >= 5 if family_info else False:
            high_score += 1

        if high_score >= 2:
            score_level = "高"
        elif high_score >= 1:
            score_level = "中"

        quality_scores.append({
            "patent_number": pn,
            "title": p.get("patent_title", ""),
            "citedby_count": citedby,
            "cited_count": cited,
            "remaining_years": remaining,
            "family_size": family_size,
            "indicators": indicators,
            "score_level": score_level,
            "year": year,
            "kind": p.get("patent_kind", ""),
        })

    # 5. 风险预警
    risk_warnings = []

    # 已失效
    expired = [qs for qs in quality_scores if qs.get("kind") in ("E", "P", "S") or
               (qs.get("remaining_years") is not None and qs["remaining_years"] < 0)]
    if expired:
        risk_warnings.append({
            "type": "已失效专利",
            "level": "高危",
            "count": len(expired),
            "patents": [e["patent_number"] for e in expired[:10]],
            "detail": "以下专利已失效或已过保护期"
        })

    # 即将到期
    expiring = [qs for qs in quality_scores if qs.get("remaining_years") is not None
                and 0 <= qs["remaining_years"] <= 3]
    if expiring:
        risk_warnings.append({
            "type": "即将到期",
            "level": "中危",
            "count": len(expiring),
            "patents": [e["patent_number"] for e in expiring[:10]],
            "detail": "以下专利剩余保护期不足3年"
        })

    # 被引异常（过高可能涉及诉讼关联）
    high_cited = [qs for qs in quality_scores if (qs.get("citedby_count", 0) or 0) >= 100]
    if high_cited:
        risk_warnings.append({
            "type": "被引异常偏高",
            "level": "提示",
            "count": len(high_cited),
            "patents": [h["patent_number"] for h in high_cited[:10]],
            "detail": "以下专利被引次数异常偏高，可能涉及标准必要专利或诉讼关联"
        })

    # 无引用
    no_citation = [qs for qs in quality_scores
                   if (qs.get("citedby_count", 0) or 0) == 0
                   and qs.get("remaining_years") is not None
                   and qs["remaining_years"] >= 5]
    if no_citation and len(no_citation) >= total * 0.5:
        risk_warnings.append({
            "type": "整体引用偏低",
            "level": "提示",
            "count": len(no_citation),
            "detail": f"近半数专利({len(no_citation)}件)未被引用，技术影响力可能有限"
        })

    # 6. 综合报告
    # 技术领域排序
    sorted_tech = sorted(tech_distribution.items(), key=lambda x: x[1]["count"], reverse=True)

    # 质量排序（按被引次数排序前10）
    quality_scores_sorted = sorted(quality_scores,
                                    key=lambda x: x.get("citedby_count", 0) or 0,
                                    reverse=True)

    # 按section汇总
    section_distribution = {}
    for p in patents:
        cpc = p.get("cpc_subsection_id") or ""
        section = cpc[0:1] if cpc and len(cpc) >= 1 else "X"
        section_name = IPC_SECTION_MAP.get(section, "其他")
        if section_name not in section_distribution:
            section_distribution[section_name] = 0
        section_distribution[section_name] += 1

    return {
        "company_name": company_name,
        "total": total,
        "tech_distribution": sorted_tech,
        "section_distribution": section_distribution,
        "legal_status": legal_status,
        "quality_scores": quality_scores_sorted[:20],  # top 20
        "risk_warnings": risk_warnings,
        "has_risks": len(risk_warnings) > 0,
    }


# ============================================================
# 报告生成层
# ============================================================

def generate_report(analysis: Dict) -> str:
    """
    生成格式化的IP概览报告
    """
    if analysis.get("error") or analysis.get("total", 0) == 0:
        company = analysis.get("company_name", "未知企业")
        return f"## 📋 IP快速筛查结果\n\n**企业名称**：{company}\n**专利总数**：0\n\n未查询到该企业相关专利，请确认企业名称是否正确。"

    company = analysis.get("company_name", "未知企业") or "未知企业"
    total = analysis["total"]
    today_str = date.today().strftime("%Y-%m-%d")

    lines = []
    lines.append(f"# 📋 IP快速筛查报告（尽调初筛）")
    lines.append(f"")
    lines.append(f"**生成日期**：{today_str}")
    lines.append(f"**筛查对象**：{company}")
    lines.append(f"**专利总数**：{total}件")
    lines.append(f"**数据源**：USPTO PatentsView API")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # 技术领域分布
    lines.append(f"## 🔬 技术领域分布")
    lines.append(f"")
    lines.append(f"| 技术领域 | 专利数 | 占比 |")
    lines.append(f"|---------|-------|------|")
    for tech_name, info in analysis["tech_distribution"]:
        pct = round(info["count"] / total * 100, 1)
        lines.append(f"| {tech_name} | {info['count']} | {pct}% |")

    # 按IPC大类汇总
    lines.append(f"")
    lines.append(f"### 技术领域分类概览（IPC大类）")
    lines.append(f"")
    section_dist = analysis["section_distribution"]
    lines.append(f"| 技术大类 | 专利数 | 占比 |")
    lines.append(f"|---------|-------|------|")
    for sec_name, count in sorted(section_dist.items(), key=lambda x: x[1], reverse=True):
        pct = round(count / total * 100, 1)
        lines.append(f"| {sec_name} | {count} | {pct}% |")

    lines.append(f"")

    # 法律状态分布
    lines.append(f"## ⚖️ 法律状态分布")
    lines.append(f"")
    ls = analysis["legal_status"]
    lines.append(f"| 状态 | 数量 | 占比 |")
    lines.append(f"|------|------|------|")
    for status_name in ["授权有效", "审查中", "已失效", "未知"]:
        count = ls.get(status_name, 0)
        if count > 0:
            pct = round(count / total * 100, 1)
            lines.append(f"| {status_name} | {count} | {pct}% |")

    lines.append(f"")

    # 专利质量初筛参考
    lines.append(f"## 🏆 专利质量初筛参考")
    lines.append(f"")
    lines.append(f"> ⚠️ 本表为基于公开指标的参考标记，不构成具体估值或评分数字")
    lines.append(f"")
    lines.append(f"| 专利号 | 被引次数 | 剩余保护期 | 综合标记 | 关键指标 |")
    lines.append(f"|--------|---------|-----------|---------|---------|")

    for qs in analysis["quality_scores"][:15]:
        pn = qs.get("patent_number", "")
        citedby = qs.get("citedby_count", 0)
        remaining = qs.get("remaining_years")
        remaining_str = f"{remaining}年" if remaining is not None else "未知"
        level = qs.get("score_level", "一般")
        indicators = "; ".join(qs.get("indicators", []))[:40]
        lines.append(f"| {pn} | {citedby} | {remaining_str} | {level} | {indicators} |")

    if len(analysis["quality_scores"]) > 15:
        lines.append(f"| ... | 还有{len(analysis['quality_scores']) - 15}件专利 | ... | ... | ... |")

    lines.append(f"")

    # 风险预警
    lines.append(f"## ⚠️ 风险预警清单")
    lines.append(f"")

    if not analysis["risk_warnings"]:
        lines.append(f"✅ **未发现明显风险信号**")
    else:
        for risk in analysis["risk_warnings"]:
            level_icon = {"高危": "🚩", "中危": "⚠️", "提示": "💡"}.get(risk["level"], "📌")
            lines.append(f"### {level_icon} {risk['type']}（{risk['level']}）")
            lines.append(f"")
            lines.append(f"涉及 {risk['count']} 件专利")
            lines.append(f"")
            lines.append(f">{risk['detail']}")
            if risk.get("patents"):
                lines.append(f"")
                for pn in risk["patents"]:
                    lines.append(f"- {pn}")
            lines.append(f"")

    # 结论与建议
    lines.append(f"---")
    lines.append(f"## 📌 初筛结论")
    lines.append(f"")

    has_risks = analysis.get("has_risks", False)
    risk_count = len(analysis.get("risk_warnings", []))

    if not has_risks:
        lines.append(f"✅ **IP组合基本健康**，未发现显著风险信号。")
    else:
        lines.append(f"⚠️ **发现 {risk_count} 类风险信号**，建议关注以下方面：")
        lines.append(f"")
        for risk in analysis["risk_warnings"]:
            lines.append(f"- {'🚩' if risk['level'] == '高危' else '⚠️'} **{risk['type']}**：{risk['detail']}")
    lines.append(f"")
    lines.append(f"> **建议**：如需深度P2I评估和专利价值量化分析，建议联系专业机构（如中知慧鉴）进行深度评估。")
    lines.append(f"> 本报告仅作为快速筛查参考，不构成法律意见。")

    return "\n".join(lines)


# ============================================================
# 入口
# ============================================================

def main():
    """
    主入口：解析输入参数，执行筛查流程
    """
    input_text = os.environ.get("QUERY_INPUT", "")
    if not input_text:
        # 尝试从命令行参数获取
        input_text = " ".join(sys.argv[1:])

    if not input_text:
        # 交互模式
        print("IP快速筛查（尽调初筛）")
        print("=" * 40)
        print("请输入企业名称或专利号列表（用逗号/空格分隔）：")
        input_text = sys.stdin.readline().strip()

    if not input_text:
        print("请提供企业名称或专利号")
        return json.dumps({"error": "请提供企业名称或专利号"}, ensure_ascii=False)

    # 判断输入类型
    input_text = input_text.strip()

    # 检测是否为专利号模式
    patent_pattern = re.compile(r'[A-Za-z]{0,2}[\d,]{4,}', re.IGNORECASE)
    has_patent_numbers = False
    patent_numbers = []

    # 按逗号/空格/分号分割
    parts = re.split(r'[,;，；\s]+', input_text)

    for part in parts:
        part = part.strip().upper()
        # 去除可能的US前缀
        clean = re.sub(r'^US', '', part) if part.startswith('US') else part
        if clean.isdigit() and len(clean) >= 6:
            has_patent_numbers = True
            patent_numbers.append(part)
        elif re.match(r'^[A-Z]{2}\d+', part):
            has_patent_numbers = True
            patent_numbers.append(part)

    try:
        if has_patent_numbers and len(patent_numbers) >= 1:
            company_name = "自定义专利列表"
            print(f"📡 正在查询 {len(patent_numbers)} 件专利...")
            patents = search_patents_by_numbers(patent_numbers)
        else:
            company_name = input_text
            print(f"📡 正在查询 {company_name} 的专利组合...")
            patents = search_patents_by_assignee(company_name)

        print(f"✅ 获取到 {len(patents)} 件专利数据")

        if not patents:
            result = {
                "company_name": company_name,
                "total": 0,
                "message": "未查询到该企业相关专利"
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return json.dumps(result, ensure_ascii=False)

        # 数据清洗
        for p in patents:
            if "cited_patent_count" in p and p["cited_patent_count"] is None:
                p["cited_patent_count"] = 0
            if "citedby_patent_count" in p and p["citedby_patent_count"] is None:
                p["citedby_patent_count"] = 0

        # 分析处理
        print("🔍 正在分析专利数据...")
        analysis = analyze_patent_portfolio(patents, company_name)

        # 生成报告
        print("📝 生成报告...")
        report = generate_report(analysis)

        # 输出报告
        print("\n" + "=" * 60 + "\n")
        print(report)
        print("\n" + "=" * 60)

        # 也输出JSON格式的结构化数据（给LLM后续处理用）
        result_json = {
            "report_markdown": report,
            "structured_data": {
                "company_name": company_name,
                "total_patents": analysis["total"],
                "tech_distribution": {k: v["count"] for k, v in analysis["tech_distribution"]},
                "legal_status": analysis["legal_status"],
                "risk_count": len(analysis.get("risk_warnings", [])),
                "has_risks": analysis.get("has_risks", False),
            }
        }
        print("\n---JSON_OUTPUT---")
        print(json.dumps(result_json, ensure_ascii=False, indent=2))

        return report

    except Exception as e:
        error_msg = f"查询处理失败: {str(e)}"
        print(f"❌ {error_msg}")
        return json.dumps({"error": error_msg}, ensure_ascii=False)


if __name__ == "__main__":
    main()