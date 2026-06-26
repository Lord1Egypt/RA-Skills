#!/usr/bin/env python3
"""
企业筛选评分脚本
胡田-OPC导师-招商引流工具包

功能：从候选企业池中筛选高潜力企业，计算综合评分
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class EnterpriseData:
    """企业数据"""
    name: str
    # 团队实力
    founder_background: str = ""  # 985/211/海归/上市公司背景
    team_stability: int = 0  # 0-6分
    team_completeness: int = 0  # 0-6分
    # 技术壁垒
    patents: int = 0  # 发明专利数量
    tech_leadership: str = ""  # 国际/国内领先/一般
    trl_level: int = 0  # 1-9
    # 商业模式
    market_size: float = 0  # 亿
    biz_model: str = ""  # 已验证/探索中
    growth_rate: float = 0  # %
    # 财务健康
    revenue: float = 0  # 万元
    funding_stage: str = ""  # 轮次
    cash_flow: str = ""  # 正向/平衡/紧张
    # 产业契合
    industry_position: str = ""  # 链主/关键配套/一般
    region_match: float = 0  # 0-1
    chain_effect: int = 0  # 带动上下游数量


class EnterpriseScreener:
    """企业筛选器"""
    
    def __init__(self):
        self.enterprises: List[EnterpriseData] = []
        self.scores: Dict[str, Dict] = {}
    
    def add_enterprise(self, name: str, data: Dict) -> None:
        """添加企业"""
        enterprise = EnterpriseData(name=name, **data)
        self.enterprises.append(enterprise)
        self._calculate_score(enterprise)
    
    def _calculate_score(self, enterprise: EnterpriseData) -> Dict:
        """计算企业评分"""
        score = {
            "name": enterprise.name,
            "total": 0,
            "dimensions": {}
        }
        
        # 1. 团队实力（20分）
        team_score = self._score_team(enterprise)
        score["dimensions"]["team"] = team_score
        
        # 2. 技术壁垒（20分）
        tech_score = self._score_tech(enterprise)
        score["dimensions"]["tech"] = tech_score
        
        # 3. 商业模式（20分）
        biz_score = self._score_biz(enterprise)
        score["dimensions"]["biz"] = biz_score
        
        # 4. 财务健康（20分）
        finance_score = self._score_finance(enterprise)
        score["dimensions"]["finance"] = finance_score
        
        # 5. 产业契合（20分）
        industry_score = self._score_industry(enterprise)
        score["dimensions"]["industry"] = industry_score
        
        # 总分
        score["total"] = sum([
            team_score["total"],
            tech_score["total"],
            biz_score["total"],
            finance_score["total"],
            industry_score["total"]
        ])
        
        # 评级
        score["rating"] = self._get_rating(score["total"])
        
        self.scores[enterprise.name] = score
        return score
    
    def _score_team(self, e: EnterpriseData) -> Dict:
        """评分：团队实力"""
        scores = {}
        
        # 创始人背景（0-8分）
        if "海归" in e.founder_background and ("985" in e.founder_background or "211" in e.founder_background):
            founder_score = 8
        elif "海归" in e.founder_background or "985" in e.founder_background or "上市公司" in e.founder_background:
            founder_score = 6
        elif "211" in e.founder_background:
            founder_score = 5
        elif e.founder_background:
            founder_score = 4
        else:
            founder_score = 2
        scores["founder"] = min(founder_score, 8)
        
        # 核心团队稳定性（0-6分）
        scores["stability"] = min(e.team_stability, 6)
        
        # 团队完整性（0-6分）
        scores["completeness"] = min(e.team_completeness, 6)
        
        scores["total"] = sum(scores.values())
        scores["max"] = 20
        return scores
    
    def _score_tech(self, e: EnterpriseData) -> Dict:
        """评分：技术壁垒"""
        scores = {}
        
        # 专利数量（0-8分）
        if e.patents >= 10:
            scores["patents"] = 8
        elif e.patents >= 5:
            scores["patents"] = 6
        elif e.patents >= 2:
            scores["patents"] = 4
        elif e.patents >= 1:
            scores["patents"] = 2
        else:
            scores["patents"] = 0
        
        # 技术领先性（0-6分）
        if "国际领先" in e.tech_leadership:
            scores["leadership"] = 6
        elif "国内领先" in e.tech_leadership:
            scores["leadership"] = 5
        elif "行业前" in e.tech_leadership:
            scores["leadership"] = 4
        else:
            scores["leadership"] = 2
        
        # TRL等级（0-6分）
        if e.trl_level >= 9:
            scores["trl"] = 6
        elif e.trl_level >= 7:
            scores["trl"] = 5
        elif e.trl_level >= 5:
            scores["trl"] = 4
        elif e.trl_level >= 3:
            scores["trl"] = 2
        else:
            scores["trl"] = 0
        
        scores["total"] = sum(scores.values())
        scores["max"] = 20
        return scores
    
    def _score_biz(self, e: EnterpriseData) -> Dict:
        """评分：商业模式"""
        scores = {}
        
        # 市场规模（0-6分）
        if e.market_size >= 100:
            scores["market"] = 6
        elif e.market_size >= 10:
            scores["market"] = 4
        elif e.market_size >= 1:
            scores["market"] = 2
        else:
            scores["market"] = 1
        
        # 商业模式清晰度（0-8分）
        if "已验证" in e.biz_model:
            scores["model"] = 8
        elif "清晰" in e.biz_model:
            scores["model"] = 6
        elif "基本" in e.biz_model:
            scores["model"] = 4
        elif "探索" in e.biz_model:
            scores["model"] = 2
        else:
            scores["model"] = 1
        
        # 增长潜力（0-6分）
        if e.growth_rate >= 50:
            scores["growth"] = 6
        elif e.growth_rate >= 30:
            scores["growth"] = 5
        elif e.growth_rate >= 10:
            scores["growth"] = 3
        else:
            scores["growth"] = 1
        
        scores["total"] = sum(scores.values())
        scores["max"] = 20
        return scores
    
    def _score_finance(self, e: EnterpriseData) -> Dict:
        """评分：财务健康"""
        scores = {}
        
        # 营收规模（0-8分）
        if e.revenue >= 10000:
            scores["revenue"] = 8
        elif e.revenue >= 3000:
            scores["revenue"] = 6
        elif e.revenue >= 1000:
            scores["revenue"] = 4
        elif e.revenue >= 500:
            scores["revenue"] = 3
        else:
            scores["revenue"] = 1
        
        # 融资阶段（0-6分）
        if "C轮" in e.funding_stage or "D轮" in e.funding_stage or "上市" in e.funding_stage:
            scores["funding"] = 6
        elif "B轮" in e.funding_stage:
            scores["funding"] = 5
        elif "A轮" in e.funding_stage:
            scores["funding"] = 4
        elif "天使" in e.funding_stage:
            scores["funding"] = 2
        else:
            scores["funding"] = 1
        
        # 现金流（0-6分）
        if "正向" in e.cash_flow:
            scores["cashflow"] = 6
        elif "平衡" in e.cash_flow:
            scores["cashflow"] = 4
        else:
            scores["cashflow"] = 2
        
        scores["total"] = sum(scores.values())
        scores["max"] = 20
        return scores
    
    def _score_industry(self, e: EnterpriseData) -> Dict:
        """评分：产业契合"""
        scores = {}
        
        # 产业链位置（0-8分）
        if "链主" in e.industry_position or "平台" in e.industry_position:
            scores["position"] = 8
        elif "关键" in e.industry_position or "核心" in e.industry_position:
            scores["position"] = 6
        elif "配套" in e.industry_position:
            scores["position"] = 4
        else:
            scores["position"] = 2
        
        # 区域产业匹配（0-6分）
        scores["match"] = min(int(e.region_match * 6), 6)
        
        # 带动效应（0-6分）
        if e.chain_effect >= 10:
            scores["effect"] = 6
        elif e.chain_effect >= 5:
            scores["effect"] = 4
        elif e.chain_effect >= 2:
            scores["effect"] = 2
        else:
            scores["effect"] = 1
        
        scores["total"] = sum(scores.values())
        scores["max"] = 20
        return scores
    
    def _get_rating(self, total: float) -> str:
        """获取评级"""
        if total >= 85:
            return "A级（最高优先级）"
        elif total >= 70:
            return "B级（高优先级）"
        elif total >= 55:
            return "C级（中优先级）"
        elif total >= 40:
            return "D级（低优先级）"
        else:
            return "E级（暂不考虑）"
    
    def get_ranking(self) -> List[Dict]:
        """获取企业排名"""
        results = list(self.scores.values())
        results.sort(key=lambda x: x["total"], reverse=True)
        return results
    
    def get_report(self) -> str:
        """生成筛选报告"""
        ranking = self.get_ranking()
        
        report = "=" * 60 + "\n"
        report += "企业筛选评分报告\n"
        report += "=" * 60 + "\n\n"
        
        for i, item in enumerate(ranking, 1):
            report += f"{i}. {item['name']} - {item['total']:.0f}/100分\n"
            report += f"   评级：{item['rating']}\n"
            report += f"   团队：{item['dimensions']['team']['total']}/20 | "
            report += f"技术：{item['dimensions']['tech']['total']}/20 | "
            report += f"商业：{item['dimensions']['biz']['total']}/20\n"
            report += f"   财务：{item['dimensions']['finance']['total']}/20 | "
            report += f"产业：{item['dimensions']['industry']['total']}/20\n"
            report += "\n"
        
        return report


# 示例用法
if __name__ == "__main__":
    screener = EnterpriseScreener()
    
    # 添加企业案例
    screener.add_enterprise("深圳智链科技有限公司", {
        "founder_background": "海归+行业经验",
        "team_stability": 5,
        "team_completeness": 5,
        "patents": 3,
        "tech_leadership": "国内领先",
        "trl_level": 7,
        "market_size": 120,
        "biz_model": "已验证",
        "growth_rate": 40,
        "revenue": 800,
        "funding_stage": "A轮后",
        "cash_flow": "基本平衡",
        "industry_position": "关键配套",
        "region_match": 0.9,
        "chain_effect": 6
    })
    
    screener.add_enterprise("杭州云图设计工作室", {
        "founder_background": "211+知名企业背景",
        "team_stability": 3,
        "team_completeness": 2,
        "patents": 0,
        "tech_leadership": "行业有一定优势",
        "trl_level": 6,
        "market_size": 50,
        "biz_model": "已验证",
        "growth_rate": 20,
        "revenue": 150,
        "funding_stage": "未融资",
        "cash_flow": "基本平衡",
        "industry_position": "一般配套",
        "region_match": 0.8,
        "chain_effect": 3
    })
    
    screener.add_enterprise("苏州蓝鲸智能科技有限公司", {
        "founder_background": "985+上市公司高管",
        "team_stability": 6,
        "team_completeness": 6,
        "patents": 12,
        "tech_leadership": "行业领先",
        "trl_level": 8,
        "market_size": 500,
        "biz_model": "已验证",
        "growth_rate": 60,
        "revenue": 5000,
        "funding_stage": "B轮",
        "cash_flow": "正向",
        "industry_position": "链主企业",
        "region_match": 0.95,
        "chain_effect": 15
    })
    
    # 输出报告
    print(screener.get_report())
    
    # 输出JSON格式
    print("\nJSON格式：")
    print(json.dumps(screener.get_ranking(), indent=2, ensure_ascii=False))
