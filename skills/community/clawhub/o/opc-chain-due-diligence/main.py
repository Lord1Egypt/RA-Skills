#!/usr/bin/env python3
"""
OPC链式尽调增强版 - 核心脚本
面向技术尽调和投资评估场景，对目标企业进行全链条快速扫描

链式流程：
  模块A (企业基本信息) → 模块B (IP资产扫描) → 模块C (技术风险评估)
  模块A (企业基本信息) → 模块D (资金合规检查)
  模块A+B+C+D → 模块E (综合风险评估报告)

数据源：Wikidata API / USPTO PatentsView / WIPO / OpenCorporates（均为免费公开API）
"""

import os
import sys
import json
import re
import math
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from coze_workload_identity import requests


# ============================================================
# 常量定义
# ============================================================

WIKIDATA_SEARCH_URL = "https://www.wikidata.org/w/api.php"
WIKIDATA_ENTITY_URL = "https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
USPTO_API_URL = "https://api.patentsview.org/patents/query"
WIPO_SEARCH_URL = "https://www.wipo.int/edocs/"

# IPC大类 - 技术领域映射
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
    "A01": "农业/林业/畜牧业", "A23": "食品/烟草", "A61": "医学/卫生学",
    "B01": "物理/化学工艺设备", "B23": "机床/金属加工", "B60": "一般车辆",
    "B65": "输送/包装/存储", "C02": "水/废水处理", "C07": "有机化学",
    "C08": "有机高分子化合物", "C12": "生物化学/微生物学",
    "E04": "建筑物", "E21": "钻进/采矿", "F16": "工程元件",
    "F24": "供热/制冷/通风", "G01": "测量/测试", "G06": "计算/推算/计数",
    "G08": "信号装置", "G16": "专门适用ICT的", "H01": "基本电气元件",
    "H02": "发电/变电/配电", "H03": "基本电子电路", "H04": "电通信技术",
}

# 行业注册资本参考（万元人民币）
INDUSTRY_CAPITAL_REF = {
    "软件/信息技术": 100,
    "互联网": 100,
    "人工智能": 200,
    "生物医药": 500,
    "新材料": 500,
    "先进制造": 1000,
    "半导体": 1000,
    "环保": 300,
    "金融": 5000,
    "房地产": 3000,
    "贸易": 200,
    "咨询服务": 100,
    "教育": 100,
    "文化传媒": 100,
    "农业": 100,
    "能源": 2000,
}


# ============================================================
# 模块A：企业基本信息扫描
# ============================================================

class EnterpriseInfoScanner:
    """模块A：通过Wikidata等公开API扫描企业基本信息"""

    def __init__(self, company_name: str):
        self.company_name = company_name.strip()
        self.raw_data = {}
        self.parsed = {}

    def search_wikidata(self) -> Optional[str]:
        """搜索Wikidata获取企业实体QID"""
        params = {
            "action": "wbsearchentities",
            "search": self.company_name,
            "language": "zh",
            "format": "json",
            "limit": 5,
        }
        try:
            resp = requests.get(WIKIDATA_SEARCH_URL, params=params, timeout=15)
            if resp.status_code != 200:
                return None
            data = resp.json()
            results = data.get("search", [])
            if not results:
                # 用英文再试一次
                params["language"] = "en"
                resp = requests.get(WIKIDATA_SEARCH_URL, params=params, timeout=15)
                if resp.status_code != 200:
                    return None
                data = resp.json()
                results = data.get("search", [])
            if results:
                return results[0].get("id")
            return None
        except Exception:
            return None

    def fetch_entity_data(self, qid: str) -> Optional[Dict]:
        """获取Wikidata实体详细信息"""
        try:
            url = WIKIDATA_ENTITY_URL.format(qid=qid)
            resp = requests.get(url, timeout=15)
            if resp.status_code != 200:
                return None
            data = resp.json()
            entities = data.get("entities", {})
            return entities.get(qid)
        except Exception:
            return None

    def extract_enterprise_info(self, entity: Dict) -> Dict:
        """从Wikidata实体中提取企业信息"""
        result = {
            "name_zh": "",
            "name_en": "",
            "established": "",
            "industry": "",
            "headquarters": "",
            "founder": "",
            "capital": "",
            "employees": "",
            "website": "",
            "wikipedia_url": "",
        }

        claims = entity.get("claims", {})

        # 中文名称
        labels = entity.get("labels", {})
        result["name_zh"] = labels.get("zh", {}).get("value", "")
        result["name_en"] = labels.get("en", {}).get("value", "")

        # 成立时间 (P571)
        if "P571" in claims:
            for claim in claims["P571"]:
                mainsnak = claim.get("mainsnak", {})
                if mainsnak.get("datatype") == "time":
                    result["established"] = mainsnak.get("datavalue", {}).get("value", {}).get("time", "")

        # 行业 (P452)
        if "P452" in claims:
            industries = []
            for claim in claims["P452"]:
                mainsnak = claim.get("mainsnak", {})
                if mainsnak.get("datatype") == "wikibase-item":
                    item_id = mainsnak.get("datavalue", {}).get("value", {}).get("id", "")
                    industries.append(item_id)
            result["industry"] = "; ".join(industries)

        # 总部位置 (P159)
        if "P159" in claims:
            locations = []
            for claim in claims["P159"]:
                mainsnak = claim.get("mainsnak", {})
                if mainsnak.get("datatype") == "wikibase-item":
                    item_id = mainsnak.get("datavalue", {}).get("value", {}).get("id", "")
                    locations.append(item_id)
            result["headquarters"] = "; ".join(locations)

        # 创始人 (P488)
        if "P488" in claims:
            founders = []
            for claim in claims["P488"]:
                mainsnak = claim.get("mainsnak", {})
                if mainsnak.get("datatype") == "wikibase-item":
                    item_id = mainsnak.get("datavalue", {}).get("value", {}).get("id", "")
                    founders.append(item_id)
            result["founder"] = "; ".join(founders)

        # 实控人/CEO (P169)
        if "P169" in claims:
            ceo_items = []
            for claim in claims["P169"]:
                mainsnak = claim.get("mainsnak", {})
                if mainsnak.get("datatype") == "wikibase-item":
                    item_id = mainsnak.get("datavalue", {}).get("value", {}).get("id", "")
                    ceo_items.append(item_id)
            if ceo_items:
                result["founder"] = result["founder"] or "; ".join(ceo_items)

        # 员工数 (P1128)
        if "P1128" in claims:
            for claim in claims["P1128"]:
                mainsnak = claim.get("mainsnak", {})
                if mainsnak.get("datatype") == "quantity":
                    result["employees"] = str(mainsnak.get("datavalue", {}).get("value", {}).get("amount", ""))

        # 官方网站 (P856)
        if "P856" in claims:
            for claim in claims["P856"]:
                mainsnak = claim.get("mainsnak", {})
                if mainsnak.get("datatype") == "url":
                    result["website"] = mainsnak.get("datavalue", {}).get("value", "")

        # Wikipedia链接
        sitelinks = entity.get("sitelinks", {})
        zh_wiki = sitelinks.get("zhwiki", {})
        if zh_wiki:
            result["wikipedia_url"] = f"https://zh.wikipedia.org/wiki/{zh_wiki.get('title', '')}"

        return result

    def enrich_industry_name(self, industry_ids: str) -> str:
        """将Wikidata行业ID映射为中文行业名称（简化处理）"""
        if not industry_ids:
            return "未知"
        # 常用行业QID映射
        industry_map = {
            "Q4830453": "商业",
            "Q6881511": "信息技术",
            "Q11033": "制造业",
            "Q483247": "金融",
            "Q200538": "医疗",
            "Q380775": "教育",
            "Q3677511": "互联网",
            "Q8087": "半导体",
            "Q11158": "生物技术",
            "Q907288": "人工智能",
            "Q7747": "能源",
            "Q39614": "房地产",
        }
        names = []
        for iid in industry_ids.split("; "):
            name = industry_map.get(iid, iid)
            names.append(name)
        return "、".join(names)

    def enrich_location_name(self, loc_ids: str) -> str:
        """将Wikidata位置ID映射为中文城市名（简化）"""
        if not loc_ids:
            return "未知"
        location_map = {
            "Q8686": "北京",
            "Q8687": "上海",
            "Q8652": "深圳",
            "Q8773": "广州",
            "Q4970": "杭州",
            "Q8646": "成都",
            "Q8688": "南京",
            "Q3300": "武汉",
            "Q4766": "西安",
            "Q6514": "天津",
            "Q16585": "苏州",
            "Q5830": "合肥",
            "Q92": "伦敦",
            "Q30": "美国",
            "Q1490": "东京",
            "Q61": "中国",
        }
        names = []
        for lid in loc_ids.split("; "):
            name = location_map.get(lid, lid)
            names.append(name)
        return "、".join(names)

    def run(self) -> Dict:
        """执行企业基本信息扫描"""
        result = {
            "company_name": self.company_name,
            "found": False,
            "info": {},
            "risk_markers": {},
            "risk_level": "🟡",  # 默认关注（可能查不到完整信息）
        }

        # Step 1: 搜索Wikidata
        qid = self.search_wikidata()
        if not qid:
            result["risk_markers"]["info_completeness"] = "⚠️ 在公开数据源中未找到该企业的完整信息，以下分析基于有限数据"
            result["risk_level"] = "🟡"
            return result

        # Step 2: 获取实体数据
        entity = self.fetch_entity_data(qid)
        if not entity:
            result["risk_markers"]["info_completeness"] = "⚠️ 数据获取异常，信息可能不完整"
            result["risk_level"] = "🟡"
            return result

        # Step 3: 提取信息
        info = self.extract_enterprise_info(entity)
        result["found"] = True
        result["info"] = info
        result["qid"] = qid

        # Step 4: 风险标记
        risk_markers = {}
        today = date.today()

        # 4.1 存续时长检查
        established = info.get("established", "")
        if established:
            try:
                # Wikidata时间格式如 +2010-01-01T00:00:00Z
                year_str = established.strip("+")[:4]
                est_year = int(year_str)
                age = today.year - est_year
                if age <= 1:
                    risk_markers["establishment"] = ("🔴 成立不足1年，存在空壳风险", "🔴")
                elif age < 3:
                    risk_markers["establishment"] = ("🟡 成立不足3年，企业尚在成长期", "🟡")
                elif age < 5:
                    risk_markers["establishment"] = ("🟢 成立3-5年，已度过初创期", "🟢")
                else:
                    risk_markers["establishment"] = (f"🟢 成立{age}年，经营历史较长", "🟢")
                result["info"]["age_years"] = age
            except (ValueError, IndexError):
                risk_markers["establishment"] = ("🟡 成立时间信息不完整", "🟡")
        else:
            risk_markers["establishment"] = ("🟡 未获取到成立时间信息", "🟡")

        # 4.2 信息完整度
        info_fields_filled = sum(1 for v in info.values() if v)
        if info_fields_filled >= 5:
            risk_markers["info_completeness"] = ("🟢 企业公开信息较为完整", "🟢")
        elif info_fields_filled >= 3:
            risk_markers["info_completeness"] = ("🟡 企业公开信息部分缺失", "🟡")
        else:
            risk_markers["info_completeness"] = ("🔴 企业公开信息严重缺失", "🔴")

        # 4.3 行业判定
        industry_name = self.enrich_industry_name(info.get("industry", ""))
        result["info"]["industry_name"] = industry_name

        # 4.4 总部
        location_name = self.enrich_location_name(info.get("headquarters", ""))
        result["info"]["headquarters_name"] = location_name

        result["risk_markers"] = risk_markers

        # 综合风险等级
        levels = [v[1] for v in risk_markers.values()]
        if "🔴" in levels:
            result["risk_level"] = "🔴"
        elif "🟡" in levels:
            result["risk_level"] = "🟡"
        else:
            result["risk_level"] = "🟢"

        return result


# ============================================================
# 模块B：IP资产扫描
# ============================================================

class IPScanner:
    """模块B：通过USPTO PatentsView API扫描目标企业的IP资产"""

    def __init__(self, company_name: str):
        self.company_name = company_name

    def search_patents_by_assignee(self, limit: int = 100) -> List[Dict]:
        """按专利权人（公司名）搜索专利"""
        query = {
            "q": {
                "_and": [
                    {"assignee_organization": {"_like": self.company_name}}
                ]
            },
            "f": [
                "patent_number", "patent_title", "patent_abstract",
                "patent_date", "patent_issue_date",
                "patent_kind", "patent_type",
                "cpc_subsection_id",
                "cited_patent_count",
                "citedby_patent_count",
                "patent_year"
            ],
            "o": {"per_page": limit, "page": 1}
        }
        try:
            resp = requests.post(USPTO_API_URL, json=query, timeout=30,
                                 headers={"Content-Type": "application/json"})
            if resp.status_code != 200:
                return []
            data = resp.json()
            return data.get("patents", [])
        except Exception:
            return []

    def analyze_patent_distribution(self, patents: List[Dict]) -> Dict:
        """分析专利技术领域分布"""
        if not patents:
            return {"total": 0}

        total = len(patents)
        today = date.today()

        # 技术领域分布
        tech_dist = {}
        section_dist = {}
        for p in patents:
            cpc = p.get("cpc_subsection_id") or ""
            section = cpc[0:1] if cpc and len(cpc) >= 1 else "X"
            section_name = IPC_SECTION_MAP.get(section, "其他")
            section_dist[section_name] = section_dist.get(section_name, 0) + 1

            ipc_class = cpc[0:3] if cpc and len(cpc) >= 3 else "X00"
            tech_name = IPC_CLASS_MAP.get(ipc_class, section_name)
            tech_dist[tech_name] = tech_dist.get(tech_name, 0) + 1

        # 法律状态（基于kind code和年份）
        legal_status = {"授权有效": 0, "审查中": 0, "已失效": 0, "未知": 0}
        year_distribution = {}
        citedby_list = []

        for p in patents:
            kind = p.get("patent_kind", "")
            year = p.get("patent_year")
            issue_date = p.get("patent_issue_date") or p.get("patent_date", "")

            if not year and issue_date:
                try:
                    year = int(issue_date[:4])
                except (ValueError, IndexError):
                    year = None

            # 年份分布
            if year:
                year_distribution[year] = year_distribution.get(year, 0) + 1

            # 被引次数
            citedby = p.get("citedby_patent_count", 0) or 0
            citedby_list.append(citedby)

            # 法律状态推断
            if year:
                expiry_year = year + 20
                if kind in ("B1", "B2", "B"):
                    if expiry_year < today.year:
                        legal_status["已失效"] += 1
                    else:
                        legal_status["授权有效"] += 1
                elif kind in ("A", "A1", "A2"):
                    legal_status["审查中"] += 1
                elif kind in ("E", "P", "S"):
                    legal_status["已失效"] += 1
                else:
                    # 有年份但无kind code，用年份推断
                    if expiry_year < today.year:
                        legal_status["已失效"] += 1
                    else:
                        legal_status["授权有效"] += 1
            else:
                legal_status["未知"] += 1

        # 计算引用统计数据
        effective_ratio = legal_status.get("授权有效", 0) / total if total > 0 else 0
        citedby_mean = sum(citedby_list) / len(citedby_list) if citedby_list else 0
        zero_citation = sum(1 for c in citedby_list if c == 0)
        zero_citation_ratio = zero_citation / len(citedby_list) if citedby_list else 0

        # 近3年申请趋势
        sorted_years = sorted(year_distribution.keys())
        recent_years = [y for y in sorted_years if y >= today.year - 4]
        recent_trend = {}
        for y in recent_years:
            recent_trend[y] = year_distribution[y]

        # 技术集中度 (HHI简化版)
        sorted_tech = sorted(tech_dist.items(), key=lambda x: x[1], reverse=True)
        top_tech_ratio = sorted_tech[0][1] / total if sorted_tech and total > 0 else 0

        return {
            "total": total,
            "tech_distribution": dict(sorted_tech[:10]),
            "section_distribution": section_dist,
            "legal_status": legal_status,
            "effective_ratio": effective_ratio,
            "year_distribution": year_distribution,
            "recent_trend": recent_trend,
            "citedby_mean": round(citedby_mean, 1),
            "zero_citation_ratio": round(zero_citation_ratio, 2),
            "top_tech_ratio": round(top_tech_ratio, 2),
            "top_tech_name": sorted_tech[0][0] if sorted_tech else "",
            "citedby_list": citedby_list,
        }

    def run(self) -> Dict:
        """执行IP资产扫描"""
        result = {
            "company_name": self.company_name,
            "patents_found": False,
            "summary": {},
            "risk_markers": {},
            "risk_level": "🟡",
        }

        patents = self.search_patents_by_assignee()
        if not patents:
            result["risk_markers"]["patent_count"] = ("🔴 未查询到该企业名下专利", "🔴")
            result["risk_level"] = "🔴"
            return result

        result["patents_found"] = True
        analysis = self.analyze_patent_distribution(patents)
        result["summary"] = analysis

        total = analysis["total"]
        risk_markers = {}

        # 专利数量
        if total >= 20:
            risk_markers["patent_count"] = (f"🟢 专利数量充足（{total}件），具备一定技术积累", "🟢")
        elif total >= 5:
            risk_markers["patent_count"] = (f"🟡 专利数量一般（{total}件），技术积累有限", "🟡")
        elif total >= 1:
            risk_markers["patent_count"] = (f"🟡 专利数量偏少（{total}件），技术壁垒较弱", "🟡")
        else:
            risk_markers["patent_count"] = (f"🔴 无有效专利", "🔴")

        # 技术领域集中度
        top_ratio = analysis["top_tech_ratio"]
        if top_ratio > 0.8:
            risk_markers["tech_concentration"] = (
                f"🔴 技术领域高度集中（{analysis['top_tech_name']}占{top_ratio:.0%}），存在单一技术依赖风险", "🔴")
        elif top_ratio > 0.5:
            risk_markers["tech_concentration"] = (
                f"🟡 技术领域相对集中（{analysis['top_tech_name']}占{top_ratio:.0%}）", "🟡")
        else:
            risk_markers["tech_concentration"] = (
                f"🟢 技术领域分布较为分散，无明显集中风险", "🟢")

        # 法律状态（有效率）
        effective = analysis["effective_ratio"]
        if effective >= 0.7:
            risk_markers["effective_ratio"] = (f"🟢 专利有效率较高（{effective:.0%}）", "🟢")
        elif effective >= 0.4:
            risk_markers["effective_ratio"] = (f"🟡 专利有效率一般（{effective:.0%}），可能存在维护不足", "🟡")
        else:
            risk_markers["effective_ratio"] = (f"🔴 专利有效率偏低（{effective:.0%}），大量专利已失效", "🔴")

        # 引用影响力
        zero_ratio = analysis["zero_citation_ratio"]
        citedby_mean = analysis["citedby_mean"]
        if zero_ratio > 0.5 and total >= 5:
            risk_markers["citation_impact"] = (
                f"🔴 引用影响力偏低（{zero_ratio:.0%}专利零引用），技术影响力有限", "🔴")
        elif zero_ratio > 0.3:
            risk_markers["citation_impact"] = (
                f"🟡 部分专利（{zero_ratio:.0%}）零引用", "🟡")
        else:
            risk_markers["citation_impact"] = (f"🟢 引用分布正常", "🟢")

        # 近3年申请趋势
        recent = analysis["recent_trend"]
        if len(recent) >= 2:
            years = sorted(recent.keys())
            # 检查是否呈下降趋势
            mid = len(years) // 2
            first_half = sum(recent[y] for y in years[:mid])
            second_half = sum(recent[y] for y in years[mid:])
            if second_half < first_half * 0.5 and first_half > 0:
                risk_markers["trend"] = ("🔴 近3年专利申请量呈明显下降趋势，需关注研发持续性", "🔴")
            elif second_half < first_half:
                risk_markers["trend"] = ("🟡 近3年专利申请量略有下降", "🟡")
            else:
                risk_markers["trend"] = ("🟢 专利申请趋势稳定或上升", "🟢")
        elif len(recent) == 1:
            risk_markers["trend"] = ("🟡 仅有1年数据，无法判断趋势", "🟡")
        else:
            risk_markers["trend"] = ("🟡 无近3年申请数据", "🟡")

        result["risk_markers"] = risk_markers

        # 综合风险等级
        levels = [v[1] for v in risk_markers.values()]
        if "🔴" in levels:
            result["risk_level"] = "🔴"
        elif "🟡" in levels:
            result["risk_level"] = "🟡"
        else:
            result["risk_level"] = "🟢"

        return result


# ============================================================
# 模块C：技术风险评估
# ============================================================

class TechRiskAssessor:
    """模块C：基于IP扫描结果做技术风险评估"""

    def __init__(self, ip_result: Dict):
        self.ip_result = ip_result

    def detect_concept_swapping(self) -> Optional[str]:
        """
        检测"概念偷换"信号：
        - 专利涉及多个不相关的技术领域 -> 可能用热门概念包装
        - 专利标题/摘要中核心概念跳跃 -> 可能追热点
        """
        summary = self.ip_result.get("summary", {})
        tech_dist = summary.get("tech_distribution", {})
        section_dist = summary.get("section_distribution", {})

        # 如果跨多个IPC大类但每个大类专利数都很少
        if len(tech_dist) >= 4:
            values = list(tech_dist.values())
            # 检查是否大量专利集中在少数类别
            top_n = sum(sorted(values, reverse=True)[:2])
            total = sum(values)
            if top_n / total < 0.3 and total > 0:
                return '🟡 专利涉及多个非相关技术领域，需关注是否存在「追热点」或「概念包装」情况'

        # 如果专利分布在多个互不相关的IPC大类
        if len(section_dist) >= 4:
            return "🟡 专利覆盖多个不相关技术大类，可能存在技术方向分散或概念包装"

        return None

    def detect_tech_exaggeration(self) -> Optional[str]:
        """检测技术夸大信号"""
        summary = self.ip_result.get("summary", {})

        # 专利数量极少但领域描述宏大
        total = summary.get("total", 0)

        # 大量低质量专利（零引用）
        zero_ratio = summary.get("zero_citation_ratio", 0)
        if total >= 10 and zero_ratio > 0.6:
            return '🔴 超过60%的专利零引用，可能存在「专利泡沫」——数量多但技术影响力有限'

        # 近2年突然大量申请（突击凑数）
        recent = summary.get("recent_trend", {})
        years = sorted(recent.keys())
        if len(years) >= 2:
            last_year = years[-1]
            first_year = years[0]
            if recent.get(last_year, 0) > recent.get(first_year, 0) * 3 and recent.get(first_year, 0) > 0:
                return "🟡 近2年专利申请量激增，需关注是否突击申请以抬高估值"

        return None

    def analyze_rd_investment_signal(self) -> Optional[str]:
        """分析研发投入信号（基于专利数据推断）"""
        summary = self.ip_result.get("summary", {})
        year_dist = summary.get("year_distribution", {})

        if not year_dist:
            return None

        years = sorted(year_dist.keys())
        if len(years) < 3:
            return None

        # 检查是否有持续稳定的专利产出
        recent_3 = sum(year_dist.get(y, 0) for y in years[-3:])
        older = sum(year_dist.get(y, 0) for y in years[:-3])

        if recent_3 == 0 and older > 0:
            return "🔴 近3年无新增专利申请，研发活动可能已停滞"

        if recent_3 < older * 0.3 and older > 0:
            return "🟡 近年专利产出较历史峰值明显下降，需关注研发投入持续性"

        return None

    def assess_patent_quality(self) -> Optional[str]:
        """专利质量综合评估"""
        summary = self.ip_result.get("summary", {})
        total = summary.get("total", 0)

        if total == 0:
            return "🔴 无专利数据，无法评估技术实力"

        # 有效率
        effective = summary.get("effective_ratio", 0)
        # 引用均值
        citedby_mean = summary.get("citedby_mean", 0)

        if effective >= 0.7 and citedby_mean >= 5:
            return "🟢 专利质量较高：有效率高且被引活跃"
        elif effective >= 0.5 and citedby_mean >= 1:
            return "🟡 专利质量中等：基本正常但有改善空间"
        else:
            return "🔴 专利质量偏低：有效率低或引用不足"

    def run(self) -> Dict:
        """执行技术风险评估"""
        result = {
            "risk_markers": {},
            "risk_level": "🟡",
            "signals": [],
        }

        if not self.ip_result.get("patents_found"):
            result["risk_markers"]["no_patents"] = ("🔴 无专利数据，无法评估技术实力", "🔴")
            result["risk_level"] = "🔴"
            result["conclusion"] = "该企业无专利数据，技术实力无法通过公开数据验证"
            return result

        # 1. 概念偷换检测
        concept_signal = self.detect_concept_swapping()
        if concept_signal:
            level = "🔴" if "追热点" in concept_signal else "🟡"
            result["risk_markers"]["concept_swapping"] = (concept_signal, level)
            result["signals"].append(concept_signal)

        # 2. 技术夸大检测
        exaggerate_signal = self.detect_tech_exaggeration()
        if exaggerate_signal:
            level = "🔴" if "专利泡沫" in exaggerate_signal else "🟡"
            result["risk_markers"]["tech_exaggeration"] = (exaggerate_signal, level)
            result["signals"].append(exaggerate_signal)

        # 3. 研发投入信号
        rd_signal = self.analyze_rd_investment_signal()
        if rd_signal:
            level = "🔴" if "已停滞" in rd_signal else "🟡"
            result["risk_markers"]["rd_investment"] = (rd_signal, level)
            result["signals"].append(rd_signal)

        # 4. 专利质量综合
        quality_signal = self.assess_patent_quality()
        if quality_signal:
            level = "🔴" if "偏低" in quality_signal or "无法" in quality_signal else (
                     "🟡" if "中等" in quality_signal else "🟢")
            result["risk_markers"]["patent_quality"] = (quality_signal, level)

        # 综合等级
        levels = [v[1] for v in result["risk_markers"].values()]
        if "🔴" in levels:
            result["risk_level"] = "🔴"
        elif "🟡" in levels:
            result["risk_level"] = "🟡"
        else:
            result["risk_level"] = "🟢"

        # 总结
        signal_count = len(result["signals"])
        if signal_count == 0:
            result["conclusion"] = "未检测到明显技术风险信号，技术实力表现正常"
        elif signal_count <= 2:
            result["conclusion"] = f"检测到{signal_count}个技术风险信号，建议进一步核实"
        else:
            result["conclusion"] = f"检测到{signal_count}个技术风险信号，技术实力存疑，建议启动深度尽调"

        return result


# ============================================================
# 模块D：资金合规检查
# ============================================================

class FundComplianceChecker:
    """模块D：基于企业基本信息做资金合规检查"""

    def __init__(self, enterprise_result: Dict):
        self.enterprise_result = enterprise_result

    def check_capital_reasonableness(self, industry_name: str, age_years: Optional[int]) -> Optional[str]:
        """检查注册资本与行业、存续年限的合理性"""
        # 基于行业推测注册资本合理性
        # 由于Wikidata不直接提供注册资本，我们基于逻辑推断
        info = self.enterprise_result.get("info", {})
        employees = info.get("employees", "")
        website = info.get("website", "")

        signals = []
        if not website and not employees:
            signals.append("无官方网站和员工信息")
        if age_years is not None and age_years >= 3 and not employees:
            signals.append(f"成立{age_years}年但无员工数据")

        # 使用INDUSTRY_CAPITAL_REF进行行业资本合理性判断
        expected_capital = None
        for industry_keyword, ref_capital in INDUSTRY_CAPITAL_REF.items():
            if industry_keyword in industry_name:
                expected_capital = ref_capital
                break

        if expected_capital is not None:
            # 如果有员工数但较少，可能资本规模不大
            if employees:
                try:
                    emp_count = int(employees)
                    if emp_count < 10 and expected_capital > 500:
                        signals.append(f"行业（{industry_name}）通常注册资本需{expected_capital}万以上，但员工数仅{emp_count}人，规模与行业不匹配")
                except (ValueError, TypeError):
                    pass

        if signals:
            return f"🟡 资金合理性存疑：{'；'.join(signals)}"
        return None

    def check_establishment_risk(self, age_years: Optional[int]) -> Optional[str]:
        """检查成立时间相关风险"""
        if age_years is not None and age_years < 1:
            return "🔴 成立不足1年即有大额标的情况需高度警惕"
        if age_years is not None and age_years < 3:
            return "🟡 成立不足3年，需关注企业历史沿革"
        return None

    def check_industry_suitability(self, industry_name: str) -> Optional[str]:
        """检查行业是否需要特定资质"""
        # 需要特定资质的行业
        licensed_industries = {
            "金融": "金融牌照",
            "医疗": "医疗机构执业许可",
            "教育": "办学许可证",
            "半导体": "相关行业许可",
            "能源": "能源业务许可",
        }
        for keyword, license_needed in licensed_industries.items():
            if keyword in industry_name:
                return f"🟡 行业（{industry_name}）通常需要{license_needed}，请确认企业是否具备"
        return None

    def run(self) -> Dict:
        """执行资金合规检查"""
        result = {
            "risk_markers": {},
            "risk_level": "🟢",
            "found": self.enterprise_result.get("found", False),
        }

        if not result["found"]:
            result["risk_markers"]["no_data"] = ("🔴 未找到企业公开信息，无法进行资金合规检查", "🔴")
            result["risk_level"] = "🔴"
            return result

        info = self.enterprise_result.get("info", {})
        industry_name = info.get("industry_name", "未知")
        age_years = info.get("age_years")

        # 1. 资本合理性
        capital_signal = self.check_capital_reasonableness(industry_name, age_years)
        if capital_signal:
            level = "🔴" if "高度警惕" in capital_signal else "🟡"
            result["risk_markers"]["capital"] = (capital_signal, level)

        # 2. 成立时间风险
        est_signal = self.check_establishment_risk(age_years)
        if est_signal:
            level = "🔴" if "高度警惕" in est_signal else "🟡"
            result["risk_markers"]["establishment"] = (est_signal, level)

        # 3. 行业资质检查
        license_signal = self.check_industry_suitability(industry_name)
        if license_signal:
            result["risk_markers"]["license"] = (license_signal, "🟡")

        # 如果没有发现任何标记，添加默认
        if not result["risk_markers"]:
            result["risk_markers"]["normal"] = ("🟢 资金面未发现明显异常信号", "🟢")

        # 综合等级
        levels = [v[1] for v in result["risk_markers"].values()]
        if "🔴" in levels:
            result["risk_level"] = "🔴"
        elif "🟡" in levels:
            result["risk_level"] = "🟡"
        else:
            result["risk_level"] = "🟢"

        return result


# ============================================================
# 模块E：综合风险评估报告
# ============================================================

class ComprehensiveReport:
    """模块E：汇总ABCD四维结果，生成综合风险评估报告"""

    def __init__(self, result_a: Dict, result_b: Dict, result_c: Dict, result_d: Dict):
        self.results = {
            "A": result_a,
            "B": result_b,
            "C": result_c,
            "D": result_d,
        }

    def determine_overall_level(self) -> Tuple[str, str]:
        """综合判定风险等级"""
        levels = {
            "A": self.results["A"].get("risk_level", "🟡"),
            "B": self.results["B"].get("risk_level", "🟡"),
            "C": self.results["C"].get("risk_level", "🟡"),
            "D": self.results["D"].get("risk_level", "🟡"),
        }

        red_count = sum(1 for v in levels.values() if v == "🔴")
        yellow_count = sum(1 for v in levels.values() if v == "🟡")

        if red_count >= 2:
            return "🔴", "高风险 — 建议暂停并启动深度尽调"
        elif red_count == 1 or yellow_count >= 2:
            return "🟡", "关注 — 存在需关注事项，建议谨慎推进"
        else:
            return "🟢", "低风险 — 可正常推进，建议关注标记项"

    def generate(self) -> str:
        """生成综合报告"""
        company_name = self.results["A"].get("company_name", "未知企业")
        today_str = date.today().strftime("%Y-%m-%d")
        overall_level, overall_desc = self.determine_overall_level()

        lines = []
        lines.append("# 🛡️ OPC链式尽调综合风险评估报告")
        lines.append("")
        lines.append(f"**生成日期**：{today_str}")
        lines.append(f"**尽调对象**：{company_name}")
        lines.append(f"**数据来源**：Wikidata / USPTO PatentsView / 公开数据")
        lines.append(f"")
        lines.append("---")
        lines.append("")

        # ====== 综合结论 ======
        lines.append("## 📊 综合结论")
        lines.append("")
        lines.append(f"| 维度 | 标记 | 说明 |")
        lines.append(f"|------|------|------|")

        a_level = self.results["A"].get("risk_level", "🟡")
        b_level = self.results["B"].get("risk_level", "🟡")
        c_level = self.results["C"].get("risk_level", "🟡")
        d_level = self.results["D"].get("risk_level", "🟡")

        a_desc = "企业背景" + (" — 信息完整" if self.results["A"].get("found") else " — 信息缺失")
        b_desc = "IP资产" + (
            f" — {self.results['B'].get('summary', {}).get('total', 0)}件专利" if self.results["B"].get("patents_found") else " — 无专利")
        c_desc = "技术实力" + (
            f" — {len(self.results['C'].get('signals', []))}个风险信号" if self.results["C"].get("signals") else " — 未检测到明显风险")
        d_desc = "资金合规" + (" — 正常" if self.results["D"].get("risk_level") == "🟢" else " — 存在关注点")

        lines.append(f"| 模块A 企业背景 | {a_level} | {a_desc} |")
        lines.append(f"| 模块B IP资产 | {b_level} | {b_desc} |")
        lines.append(f"| 模块C 技术实力 | {c_level} | {c_desc} |")
        lines.append(f"| 模块D 资金合规 | {d_level} | {d_desc} |")
        lines.append(f"| **综合结论** | **{overall_level}** | **{overall_desc}** |")
        lines.append("")

        # ====== 模块A详情 ======
        lines.append("---")
        lines.append("## 🏢 模块A：企业基本信息")
        lines.append("")

        if self.results["A"].get("found"):
            info = self.results["A"].get("info", {})
            lines.append("| 项目 | 内容 |")
            lines.append("|------|------|")
            lines.append(f"| 企业名称 | {info.get('name_zh', '未获取')} |")
            lines.append(f"| 英文名称 | {info.get('name_en', '未获取')} |")
            lines.append(f"| 成立时间 | {info.get('established', '未获取')} |")
            lines.append(f"| 行业 | {info.get('industry_name', '未获取')} |")
            lines.append(f"| 总部 | {info.get('headquarters_name', '未获取')} |")
            lines.append(f"| 创始人/CEO | {info.get('founder', '未获取')} |")
            lines.append(f"| 员工数 | {info.get('employees', '未获取')} |")
            lines.append(f"| 官网 | {info.get('website', '未获取')} |")
            lines.append(f"| Wikipedia | {info.get('wikipedia_url', '未获取')} |")
        else:
            lines.append(f"⚠️ **未能在公开数据源中找到该企业的完整信息**")
            lines.append("")
            lines.append("可能原因：")
            lines.append("- 企业为中小型非上市企业，公开信息有限")
            lines.append("- 企业名称可能存在翻译差异")
            lines.append("- 企业为未注册实体")
        lines.append("")

        # 风险标记
        risk_markers_a = self.results["A"].get("risk_markers", {})
        if risk_markers_a:
            lines.append("### 风险标记")
            lines.append("")
            for key, (desc, _) in risk_markers_a.items():
                lines.append(f"- {desc}")
            lines.append("")

        # ====== 模块B详情 ======
        lines.append("---")
        lines.append("## 📜 模块B：IP资产扫描")
        lines.append("")

        if self.results["B"].get("patents_found"):
            summary = self.results["B"].get("summary", {})
            lines.append(f"**专利总数**：{summary.get('total', 0)}件")
            lines.append("")
            lines.append("### 法律状态分布")
            lines.append("")
            ls = summary.get("legal_status", {})
            lines.append("| 状态 | 数量 |")
            lines.append("|------|------|")
            for sname in ["授权有效", "审查中", "已失效", "未知"]:
                count = ls.get(sname, 0)
                if count > 0:
                    lines.append(f"| {sname} | {count} |")
            lines.append("")
            lines.append(f"**有效率**：{summary.get('effective_ratio', 0):.0%}")
            lines.append("")

            lines.append("### 技术领域分布")
            lines.append("")
            tech_dist = summary.get("tech_distribution", {})
            if tech_dist:
                total = summary.get("total", 1)
                lines.append("| 技术领域 | 专利数 | 占比 |")
                lines.append("|---------|-------|------|")
                for tech_name, count in sorted(tech_dist.items(), key=lambda x: x[1], reverse=True):
                    pct = count / total * 100
                    lines.append(f"| {tech_name} | {count} | {pct:.1f}% |")
            lines.append("")

            lines.append("### 专利申请趋势")
            lines.append("")
            year_dist = summary.get("year_distribution", {})
            if year_dist:
                lines.append("| 年份 | 专利数 |")
                lines.append("|------|-------|")
                for year in sorted(year_dist.keys()):
                    lines.append(f"| {year} | {year_dist[year]} |")
        else:
            lines.append("⚠️ **未查询到该企业名下专利**")
        lines.append("")

        # B风险标记
        risk_markers_b = self.results["B"].get("risk_markers", {})
        if risk_markers_b:
            lines.append("### 风险标记")
            lines.append("")
            for key, (desc, _) in risk_markers_b.items():
                lines.append(f"- {desc}")
            lines.append("")

        # ====== 模块C详情 ======
        lines.append("---")
        lines.append("## 🔬 模块C：技术风险评估")
        lines.append("")

        risk_markers_c = self.results["C"].get("risk_markers", {})
        if risk_markers_c:
            for key, (desc, _) in risk_markers_c.items():
                lines.append(f"- {desc}")
        else:
            lines.append("✅ **未检测到明显技术风险信号**")
        lines.append("")

        # 结论
        c_conclusion = self.results["C"].get("conclusion", "")
        if c_conclusion:
            lines.append(f"> **技术评估结论**：{c_conclusion}")
            lines.append("")

        # ====== 模块D详情 ======
        lines.append("---")
        lines.append("## 💰 模块D：资金合规检查")
        lines.append("")

        risk_markers_d = self.results["D"].get("risk_markers", {})
        if risk_markers_d:
            for key, (desc, _) in risk_markers_d.items():
                lines.append(f"- {desc}")
        else:
            lines.append("✅ **资金面未发现明显异常信号**")
        lines.append("")

        # ====== 综合建议 ======
        lines.append("---")
        lines.append("## 📌 综合建议")
        lines.append("")

        if overall_level == "🔴":
            lines.append(f"**{overall_desc}**")
            lines.append("")
            lines.append("**建议措施**：")
            lines.append("1. 🛑 暂停当前推进流程")
            lines.append("2. 🔍 针对🔴标记维度启动深度尽调")
            lines.append("3. 👥 建议联系专业尽调机构进行现场核查")
            lines.append("4. 📋 需要进一步验证的信息：")
            red_items = []
            for mod, res in [("A", self.results["A"]), ("B", self.results["B"]),
                              ("C", self.results["C"]), ("D", self.results["D"])]:
                if res.get("risk_level") == "🔴":
                    red_items.append(f"  - 模块{mod}：需深度核查")
            lines.extend(red_items)
        elif overall_level == "🟡":
            lines.append(f"**{overall_desc}**")
            lines.append("")
            lines.append("**建议措施**：")
            lines.append("1. 🔍 针对🟡标记维度进行针对性核实")
            lines.append("2. 📞 建议与目标企业进行技术/业务沟通")
            lines.append("3. 📋 如需更深度信息，建议发起正式尽调")
        else:
            lines.append(f"**{overall_desc}**")
            lines.append("")
            lines.append("**建议措施**：")
            lines.append("1. ✅ 可正常推进后续流程")
            lines.append("2. 👀 关注标记项的动态变化")
            lines.append("3. 📊 建议定期（季度/半年）更新扫描结果")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("> ⚠️ **免责声明**")
        lines.append("> 本报告基于公开数据源生成，仅供快速筛查参考，不构成投资建议或法律意见。")
        lines.append("> 数据可能存在延迟（最长1-2周），部分中国企业信息在公开API中可能不完整。")
        lines.append(f"> 生成时间：{today_str}")

        return "\n".join(lines)


# ============================================================
# 主入口
# ============================================================

def main():
    """主入口：解析输入，执行链式扫描"""
    input_text = os.environ.get("QUERY_INPUT", "")
    if not input_text:
        input_text = " ".join(sys.argv[1:])

    if not input_text:
        print("OPC链式尽调增强版")
        print("=" * 40)
        print("请输入目标企业名称：")
        input_text = sys.stdin.readline().strip()

    if not input_text:
        print("请提供企业名称")
        return json.dumps({"error": "请提供企业名称"}, ensure_ascii=False)

    company_name = input_text.strip()
    print(f"🔍 启动OPC链式尽调扫描：{company_name}")
    print("=" * 60)

    try:
        # 模块A：企业基本信息
        print("\n📡 [模块A] 扫描企业基本信息...")
        scanner_a = EnterpriseInfoScanner(company_name)
        result_a = scanner_a.run()
        print(f"   {'✅' if result_a['found'] else '⚠️'} 企业信息{'已获取' if result_a['found'] else '未找到'}")
        print(f"   风险等级：{result_a['risk_level']}")

        # 模块B：IP资产扫描
        print("\n📡 [模块B] 扫描IP资产...")
        scanner_b = IPScanner(company_name)
        result_b = scanner_b.run()
        p_count = result_b.get("summary", {}).get("total", 0)
        print(f"   {'✅' if result_b['patents_found'] else '⚠️'} 专利数据：{p_count}件")
        print(f"   风险等级：{result_b['risk_level']}")

        # 模块C：技术风险评估
        print("\n📡 [模块C] 技术风险评估...")
        assessor_c = TechRiskAssessor(result_b)
        result_c = assessor_c.run()
        print(f"   风险等级：{result_c['risk_level']}")
        for sig in result_c.get("signals", []):
            print(f"   📌 {sig[:60]}...")

        # 模块D：资金合规检查
        print("\n📡 [模块D] 资金合规检查...")
        checker_d = FundComplianceChecker(result_a)
        result_d = checker_d.run()
        print(f"   风险等级：{result_d['risk_level']}")

        # 模块E：综合报告
        print("\n📝 [模块E] 生成综合评估报告...")
        reporter = ComprehensiveReport(result_a, result_b, result_c, result_d)
        report = reporter.generate()

        # 输出报告
        print("\n" + "=" * 60)
        print(report)
        print("\n" + "=" * 60)

        # 输出结构化JSON（供后续处理）
        result_json = {
            "report_markdown": report,
            "structured_data": {
                "company_name": company_name,
                "risk_levels": {
                    "A_enterprise": result_a["risk_level"],
                    "B_ip": result_b["risk_level"],
                    "C_tech": result_c["risk_level"],
                    "D_fund": result_d["risk_level"],
                },
                "overall_risk_level": reporter.determine_overall_level()[0],
                "patent_count": result_b.get("summary", {}).get("total", 0),
                "has_risks": any(
                    r.get("risk_level") in ("🔴", "🟡")
                    for r in [result_a, result_b, result_c, result_d]
                ),
            }
        }

        print("\n---JSON_OUTPUT---")
        print(json.dumps(result_json, ensure_ascii=False, indent=2))

        return report

    except Exception as e:
        error_msg = f"链式扫描处理失败: {str(e)}"
        print(f"❌ {error_msg}")
        return json.dumps({"error": error_msg}, ensure_ascii=False)


if __name__ == "__main__":
    main()