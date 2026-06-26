"""
智能优化引擎
ROI优化、预算重分配、出价建议
"""
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from loguru import logger
from api_client import OceanEngineClient


@dataclass
class OptimizationSuggestion:
    """优化建议"""
    type: str  # budget, bid, targeting, creative
    priority: str  # high, medium, low
    reason: str
    expected_improvement: float  # 预期改善百分比
    action_items: List[str]


@dataclass
class BudgetAllocation:
    """预算分配"""
    campaign_id: str
    current_budget: int
    suggested_budget: int
    reason: str


@dataclass
class BidSuggestion:
    """出价建议"""
    campaign_id: str
    current_bid: float
    suggested_bid: float
    suggested_bid_strategy: str


class OceanEngineOptimizer:
    """巨量广告智能优化引擎"""
    
    def __init__(self):
        self.client = OceanEngineClient()
        self.optimization_history: List[Dict] = []
    
    def analyze_campaign_performance(self, account_id: str, days: int = 7) -> Dict:
        """分析广告表现"""
        logger.info(f"分析广告表现: 账户{account_id}, 近{days}天")
        
        # 获取报表数据
        report_data = self.client.get_campaign_report(
            account_id=account_id,
            start_date=(datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
            end_date=datetime.now().strftime("%Y-%m-%d"),
            metrics=["cost", "impressions", "clicks", "ctr", "cpc", "conversion", "cpa"]
        )
        
        if not report_data or report_data.get("code") != 0:
            return {"status": "error", "message": "无法获取报表数据"}
        
        campaigns = report_data.get("data", {}).get("campaign_list", [])
        
        analysis_result = {
            "total_campaigns": len(campaigns),
            "total_spend": sum(c.get("cost", 0) for c in campaigns),
            "total_impressions": sum(c.get("impressions", 0) for c in campaigns),
            "total_clicks": sum(c.get("clicks", 0) for c in campaigns),
            "avg_ctr": np.mean([c.get("ctr", 0) for c in campaigns]),
            "avg_cpa": np.mean([c.get("cpa", 0) for c in campaigns]),
            "campaign_analysis": []
        }
        
        # 分析每个广告计划
        for campaign in campaigns:
            analysis = self._analyze_single_campaign(campaign)
            analysis_result["campaign_analysis"].append(analysis)
        
        # 生成优化建议
        suggestions = self._generate_optimization_suggestions(analysis_result)
        analysis_result["suggestions"] = suggestions
        
        # 保存历史
        self.optimization_history.append({
            "analysis_time": datetime.now().isoformat(),
            "result": analysis_result
        })
        
        return analysis_result
    
    def _analyze_single_campaign(self, campaign: Dict) -> Dict:
        """分析单个广告计划"""
        campaign_id = campaign.get("campaign_id", "")
        name = campaign.get("name", "")
        
        cost = campaign.get("cost", 0)
        impressions = campaign.get("impressions", 0)
        clicks = campaign.get("clicks", 0)
        ctr = campaign.get("ctr", 0)
        cpa = campaign.get("cpa", 0)
        conversions = campaign.get("conversion", 0)
        
        # 计算关键指标
        cpm = (cost / impressions * 1000) if impressions > 0 else 0
        cpc = cost / clicks if clicks > 0 else 0
        roi = (conversions * 100) / cost if cost > 0 else 0
        
        # 评估表现
        performance = "unknown"
        if ctr > 2.0 and cpa < 50:
            performance = "excellent"
        elif ctr > 1.0 and cpa < 100:
            performance = "good"
        elif ctr > 0.5 and cpa < 200:
            performance = "average"
        elif ctr > 0.3:
            performance = "below_average"
        else:
            performance = "poor"  # 默认值
        
        # 识别问题
        issues = []
        if cpm > 500:
            issues.append("CPM过高，建议优化定向")
        if ctr < 0.5:
            issues.append("CTR过低，建议优化创意")
        if cpa > 200:
            issues.append("CPA过高，建议优化落地页")
        if impressions == 0:
            issues.append("无曝光，检查预算和定向")
        
        return {
            "campaign_id": campaign_id,
            "name": name,
            "performance": performance,
            "metrics": {
                "cost": cost,
                "impressions": impressions,
                "clicks": clicks,
                "ctr": ctr,
                "cpm": cpm,
                "cpc": cpc,
                "cpa": cpa,
                "conversions": conversions,
                "roi": roi
            },
            "issues": issues
        }
    
    def _generate_optimization_suggestions(self, analysis_result: Dict) -> List[OptimizationSuggestion]:
        """生成优化建议"""
        suggestions = []
        campaigns = analysis_result.get("campaign_analysis", [])
        
        # 整体分析
        avg_ctr = analysis_result.get("avg_ctr", 0)
        avg_cpa = analysis_result.get("avg_cpa", 0)
        
        # 建议优先级排序
        high_priority = []
        medium_priority = []
        low_priority = []
        
        # 预算优化建议
        if analysis_result.get("total_spend", 0) > 0:
            for campaign in campaigns:
                if campaign["metrics"]["cpa"] > avg_cpa * 1.5:
                    high_priority.append(OptimizationSuggestion(
                        type="budget",
                        priority="high",
                        reason=f"广告 {campaign['name']} CPA过高({campaign['metrics']['cpa']:.2f}元)",
                        expected_improvement=20.0,
                        action_items=["减少预算", "优化定向", "更换创意"]
                    ))
                elif campaign["metrics"]["ctr"] < avg_ctr * 0.7:
                    medium_priority.append(OptimizationSuggestion(
                        type="bid",
                        priority="medium",
                        reason=f"广告 {campaign['name']} CTR偏低({campaign['metrics']['ctr']:.2f}%)",
                        expected_improvement=15.0,
                        action_items=["提高出价", "测试新创意", "优化定向"]
                    ))
        
        # 出价建议
        if avg_ctr < 1.0:
            high_priority.append(OptimizationSuggestion(
                type="bid",
                priority="high",
                reason=f"整体CTR偏低({avg_ctr:.2f}%)，建议提高出价",
                expected_improvement=25.0,
                action_items=["整体提高出价5-10%", "测试自动出价", "考虑使用智能出价"]
            ))
        
        # 创意建议
        for campaign in campaigns:
            if len(campaign["metrics"].get("issues", [])) > 2:
                medium_priority.append(OptimizationSuggestion(
                    type="creative",
                    priority="medium",
                    reason=f"广告 {campaign['name']} 多个指标异常",
                    expected_improvement=15.0,
                    action_items=["更换主图", "优化文案", "A/B测试"]
                ))
        
        suggestions = high_priority + medium_priority + low_priority
        return suggestions
    
    def optimize_budget_allocation(self, account_id: str) -> List[BudgetAllocation]:
        """优化预算分配"""
        logger.info(f"优化预算分配: 账户{account_id}")
        
        # 获取广告数据
        report_data = self.client.get_campaign_report(
            account_id=account_id,
            start_date=(datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d"),
            end_date=datetime.now().strftime("%Y-%m-%d"),
            metrics=["cost", "impressions", "clicks", "ctr", "conversion", "cpa"]
        )
        
        campaigns = report_data.get("data", {}).get("campaign_list", [])
        
        allocations = []
        
        # 分析每个广告的ROI
        for campaign in campaigns:
            campaign_id = campaign.get("campaign_id", "")
            current_budget = campaign.get("budget", 0)
            cost = campaign.get("cost", 0)
            cpa = campaign.get("cpa", 0)
            ctr = campaign.get("ctr", 0)
            
            # 计算ROI和效率
            roi = (campaign.get("conversion", 0) * 100) / cost if cost > 0 else 0
            
            # 预算优化策略
            if roi > 200:  # 高ROI，增加预算
                suggested_budget = int(current_budget * 1.3)
                reason = f"高ROI({roi:.1f}%)，建议增加30%预算"
            elif roi > 100:  # 中等ROI
                suggested_budget = int(current_budget * 1.15)
                reason = f"良好ROI({roi:.1f}%)，建议增加15%预算"
            elif roi < 50:  # 低ROI，减少预算
                suggested_budget = int(current_budget * 0.7)
                reason = f"低ROI({roi:.1f}%)，建议减少30%预算"
            else:
                suggested_budget = current_budget
                reason = "ROI正常，保持当前预算"
            
            if ctr > 0.5:  # CTR高，可以考虑增加
                suggested_budget = int(suggested_budget * 1.1)
                reason = f"CTR高({ctr:.1f}%)，建议增加10%预算"
            
            allocations.append(BudgetAllocation(
                campaign_id=campaign_id,
                current_budget=current_budget,
                suggested_budget=suggested_budget,
                reason=reason
            ))
        
        logger.info(f"预算优化建议: {len(allocations)} 个广告")
        return allocations
    
    def suggest_bid_strategy(self, campaign_id: str, current_bid: float, 
                           performance_metrics: Dict) -> BidSuggestion:
        """出价策略建议"""
        ctr = performance_metrics.get("ctr", 0)
        cpa = performance_metrics.get("cpa", 0)
        conversions = performance_metrics.get("conversions", 0)
        
        suggested_bid = current_bid
        suggested_strategy = "MANUAL"
        
        # 基于CTR和CPA调整
        if ctr < 1.0 and cpa < 50:
            # CTR低但CPA好，可以提高出价
            suggested_bid = current_bid * 1.15
            suggested_strategy = "AUTO_BID"
            reason = "CTR低但CPA优秀，建议提高出价15%"
        elif ctr > 2.0 and cpa > 100:
            # CTR高但CPA差，降低出价
            suggested_bid = current_bid * 0.85
            suggested_strategy = "MANUAL"
            reason = "CTR高但CPA偏高，建议降低出价15%"
        elif conversions < 10 and cpa < 50:
            # 转化少但CPA好，可以测试更高出价
            suggested_bid = current_bid * 1.2
            suggested_strategy = "AUTO_BID"
            reason = "转化数据少，建议提高出价20%测试"
        else:
            reason = "表现正常，保持当前出价策略"
        
        return BidSuggestion(
            campaign_id=campaign_id,
            current_bid=current_bid,
            suggested_bid=suggested_bid,
            suggested_bid_strategy=suggested_strategy
        )
    
    def generate_optimization_report(self, account_id: str, period: str = "last_7d") -> str:
        """生成优化报告"""
        logger.info(f"生成优化报告: 账户{account_id}, 周期{period}")
        
        # 分析广告表现
        analysis_result = self.analyze_campaign_performance(account_id, 
                                                          days=7 if "7d" in period else 30)
        
        # 预算优化
        budget_allocations = self.optimize_budget_allocation(account_id)
        
        # 生成报告
        report = f"""
# 巨量广告优化报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
账户ID: {account_id}
报告周期: {period}

## 📊 整体表现
- 总广告数: {analysis_result['total_campaigns']}
- 总消耗: {analysis_result['total_spend']:.2f}元
- 总曝光: {analysis_result['total_impressions']:,}
- 总点击: {analysis_result['total_clicks']:,}
- 平均CTR: {analysis_result['avg_ctr']:.2f}%
- 平均CPA: {analysis_result['avg_cpa']:.2f}元

## 🎯 优化建议
"""
        
        # 高优先级建议
        high_suggestions = [s for s in analysis_result['suggestions'] if s.priority == 'high']
        if high_suggestions:
            report += "\n### 🔴 高优先级\n"
            for i, sugg in enumerate(high_suggestions[:5], 1):
                report += f"{i+1}. {sugg.type}: {sugg.reason}\n"
                report += f"   预期改善: {sugg.expected_improvement:.1f}%\n"
                report += f"   行动建议: {'; '.join(sugg.action_items[:2])}\n\n"
        
        # 预算优化
        report += "\n### 💰 预算优化建议\n"
        for alloc in budget_allocations[:5]:
            report += f"- {alloc.campaign_id}:\n"
            report += f"  当前预算: {alloc.current_budget}元\n"
            report += f"  建议预算: {alloc.suggested_budget}元\n"
            report += f"  原因: {alloc.reason}\n\n"
        
        # 详细分析
        report += "## 📈 广告详情\n"
        for campaign in analysis_result['campaign_analysis'][:5]:
            report += f"\n### {campaign['name']}\n"
            report += f"表现等级: {campaign['performance']}\n"
            report += f"消耗: {campaign['metrics']['cost']:.2f}元\n"
            report += f"曝光: {campaign['metrics']['impressions']:,}\n"
            report += f"点击: {campaign['metrics']['clicks']:,}\n"
            report += f"CTR: {campaign['metrics']['ctr']:.2f}%\n"
            report += f"CPA: {campaign['metrics']['cpa']:.2f}元\n"
            if campaign['issues']:
                report += f"问题: {', '.join(campaign['issues'])}\n"
        
        # 免责声明
        report += """
---
**报告由 LemClaw 智能优化引擎自动生成**
建议仅供参考，请结合实际情况调整
按月付费使用请联系：business@lemclaw.com
"""
        
        return report


# 示例使用
if __name__ == "__main__":
    optimizer = OceanEngineOptimizer()
    
    # 示例：分析广告表现
    result = optimizer.analyze_campaign_performance(account_id="act_test_001", days=7)
    print("分析结果:", result)
    
    # 示例：生成优化报告
    report = optimizer.generate_optimization_report(account_id="act_test_001", period="last_7d")
    print(report)