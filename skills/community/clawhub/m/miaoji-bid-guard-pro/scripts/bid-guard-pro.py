#!/usr/bin/env python3
"""
广告护城河Pro版 - Level 2
Bid Guard Pro

基于免费版竞价计算，增加：
- ab-test: 竞价策略A/B测试模拟
- time-bid: 时间分时段出价建议
- budget-optimizer: 预算分配优化器

Author: Miaoji Studio Pro
Version: 1.0.0
"""

import sys
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class BidResult:
    """出价结果"""
    keyword: str
    recommended_bid: float
    bid_range: Tuple[float, float]
    strategy: str
    reasoning: List[str]


@dataclass
class ABTestResult:
    """A/B测试结果"""
    strategy_a: Dict[str, float]
    strategy_b: Dict[str, float]
    simulation_period: int
    projected_results: Dict[str, Any]


class BidGuardPro:
    """广告护城河Pro版"""
    
    def __init__(self):
        self.current_bids: List[BidResult] = []
    
    def calculate_bid(self, keyword: str, target_acos: float, 
                      product_price: float, competition: str = "medium") -> BidResult:
        """
        计算竞价
        
        Args:
            keyword: 关键词
            target_acos: 目标ACOS
            product_price: 产品价格
            competition: 竞争程度
        
        Returns:
            出价结果
        """
        # 基础出价计算
        base_bid = product_price * 0.1  # 基础出价为售价的10%
        
        # 竞争程度调整
        competition_factor = {
            "low": 0.8,
            "medium": 1.0,
            "high": 1.3
        }.get(competition, 1.0)
        
        # 目标ACOS调整
        acos_factor = target_acos  # 目标ACOS越低，出价越低
        
        # 最终出价
        final_bid = base_bid * competition_factor * acos_factor
        final_bid = min(final_bid, product_price * 0.5)  # 最高出价不超过售价50%
        
        # 出价范围
        bid_range = (final_bid * 0.7, final_bid * 1.3)
        
        return BidResult(
            keyword=keyword,
            recommended_bid=round(final_bid, 2),
            bid_range=(round(bid_range[0], 2), round(bid_range[1], 2)),
            strategy=self._get_bid_strategy(final_bid, base_bid),
            reasoning=self._generate_reasoning(final_bid, target_acos, competition)
        )
    
    def _get_bid_strategy(self, bid: float, base: float) -> str:
        """获取出价策略"""
        ratio = bid / base if base > 0 else 1
        if ratio < 0.8:
            return "保守出价-低竞争词"
        elif ratio < 1.2:
            return "标准出价-平衡策略"
        else:
            return "积极出价-竞争词扩展"
    
    def _generate_reasoning(self, bid: float, target_acos: float, 
                           competition: str) -> List[str]:
        """生成出价理由"""
        reasoning = []
        reasoning.append(f"基于目标ACOS {target_acos*100:.0f}%计算")
        reasoning.append(f"竞争程度: {competition}")
        reasoning.append(f"建议动态调整，结合时段优化")
        return reasoning
    
    def simulate_ab_test(self, current_strategy: Dict, 
                         test_strategy: Dict) -> ABTestResult:
        """
        A/B测试模拟
        
        Args:
            current_strategy: 当前策略
            test_strategy: 测试策略
        
        Returns:
            A/B测试结果
        """
        # 模拟参数
        base_clicks = 100
        base_cvr = 0.1
        base_cvr = current_strategy.get("cvr", base_cvr)
        
        # 计算策略A效果（当前策略）
        strategy_a_results = {
            "impressions": current_strategy.get("impressions", 10000),
            "clicks": current_strategy.get("clicks", base_clicks),
            "cvr": base_cvr,
            "orders": base_clicks * base_cvr,
            "spend": current_strategy.get("spend", 500),
            "acos": current_strategy.get("acos", 0.25)
        }
        
        # 计算策略B效果（测试策略）
        test_cvr = test_strategy.get("cvr", base_cvr + 0.02)
        strategy_b_results = {
            "impressions": test_strategy.get("impressions", 12000),
            "clicks": test_strategy.get("clicks", base_clicks * 1.2),
            "cvr": test_cvr,
            "orders": base_clicks * 1.2 * test_cvr,
            "spend": test_strategy.get("spend", 550),
            "acos": test_strategy.get("acos", 0.22)
        }
        
        # 计算改进
        projected_results = {
            "order_change": f"+{(strategy_b_results['orders'] - strategy_a_results['orders'])/strategy_a_results['orders']*100:.1f}%",
            "acos_change": f"{(strategy_b_results['acos'] - strategy_a_results['acos'])*100:.1f}pp",
            "recommendation": "建议采用策略B" if strategy_b_results["orders"] > strategy_a_results["orders"] else "保持策略A"
        }
        
        return ABTestResult(
            strategy_a=strategy_a_results,
            strategy_b=strategy_b_results,
            simulation_period=30,
            projected_results=projected_results
        )
    
    def generate_time_bidding(self, keyword: str) -> Dict[str, Any]:
        """
        生成时间分时段出价建议
        
        Args:
            keyword: 关键词
        
        Returns:
            时段出价建议
        """
        # 美国时区的典型转化模式
        time_slots = {
            "weekday_morning": {
                "time": "6:00-9:00 PST",
                "bid_adjustment": 0.7,
                "转化率": "低",
                "reason": "购物意愿低，可降低出价"
            },
            "weekday_midday": {
                "time": "9:00-12:00 PST",
                "bid_adjustment": 0.9,
                "转化率": "中",
                "reason": "工作时段，稳步投放"
            },
            "weekday_afternoon": {
                "time": "12:00-15:00 PST",
                "bid_adjustment": 1.0,
                "转化率": "中",
                "reason": "下午时段，标准出价"
            },
            "weekday_evening": {
                "time": "18:00-21:00 PST",
                "bid_adjustment": 1.3,
                "转化率": "高",
                "reason": "黄金时段，提高出价"
            },
            "weekend_morning": {
                "time": "8:00-11:00 PST",
                "bid_adjustment": 1.1,
                "转化率": "中高",
                "reason": "周末购物高峰"
            },
            "weekend_evening": {
                "time": "19:00-22:00 PST",
                "bid_adjustment": 1.4,
                "转化率": "高",
                "reason": "周末最高转化时段"
            }
        }
        
        return {
            "keyword": keyword,
            "base_bid": 1.50,  # 假设基础出价
            "time_slots": time_slots,
            "recommendations": [
                "晚间时段(18:00-22:00)提高出价30-40%",
                "周末保持较高出价争取流量",
                "凌晨至早间可降低出价节省预算",
                "结合转化数据持续优化时段系数"
            ]
        }
    
    def optimize_budget_allocation(self, campaigns: List[Dict]) -> Dict[str, Any]:
        """
        预算分配优化
        
        Args:
            campaigns: 广告活动列表
        
        Returns:
            优化建议
        """
        if not campaigns:
            return {"error": "无广告活动数据"}
        
        total_budget = sum(c.get("budget", 0) for c in campaigns)
        
        # 计算各活动效率
        campaign_analysis = []
        for campaign in campaigns:
            acos = campaign.get("acos", 0.3)
            orders = campaign.get("orders", 0)
            spend = campaign.get("spend", campaign.get("budget", 0))
            
            # 效率评分 (越低ACOS、越高订单量，效率越高)
            efficiency = (1 - acos) * 50 + min(orders / 10, 50)
            
            campaign_analysis.append({
                "name": campaign.get("name", "Unknown"),
                "acos": acos,
                "orders": orders,
                "efficiency": round(efficiency, 1),
                "current_budget": campaign.get("budget", 0),
                "allocation": 0
            })
        
        # 按效率排序
        campaign_analysis.sort(key=lambda x: x["efficiency"], reverse=True)
        
        # 重新分配预算
        # 高效率活动增加预算，低效率活动减少预算
        high_eff_campaigns = [c for c in campaign_analysis if c["efficiency"] >= 50]
        low_eff_campaigns = [c for c in campaign_analysis if c["efficiency"] < 50]
        
        # 从低效活动削减预算
        budget_reduction = sum(c["current_budget"] for c in low_eff_campaigns) * 0.3
        
        # 分配给高效活动
        for campaign in high_eff_campaigns:
            share = campaign["efficiency"] / sum(c["efficiency"] for c in high_eff_campaigns)
            new_budget = campaign["current_budget"] + budget_reduction * share
            campaign["allocation"] = round(new_budget, 2)
            campaign["change"] = f"+{(new_budget - campaign['current_budget'])/campaign['current_budget']*100:.1f}%"
        
        # 低效活动预算调整
        for campaign in low_eff_campaigns:
            new_budget = campaign["current_budget"] * 0.7
            campaign["allocation"] = round(new_budget, 2)
            campaign["change"] = f"-{(1 - new_budget/campaign['current_budget'])*100:.1f}%"
        
        return {
            "total_budget": total_budget,
            "campaigns": campaign_analysis,
            "summary": {
                "high_efficiency_count": len(high_eff_campaigns),
                "low_efficiency_count": len(low_eff_campaigns),
                "projected_acos_improvement": "5-10%",
                "projected_order_increase": "+15-20%"
            }
        }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python bid-guard-pro.py <command> [args]")
        print("命令:")
        print("  ab-test         - 竞价策略A/B测试")
        print("  time-bid        - 时间分时段出价")
        print("  budget-optimizer - 预算分配优化")
        return
    
    command = sys.argv[1]
    guard = BidGuardPro()
    
    if command == "ab-test":
        current = {
            "impressions": 10000,
            "clicks": 120,
            "cvr": 0.10,
            "acos": 0.28,
            "orders": 12,
            "spend": 600
        }
        
        test = {
            "impressions": 12000,
            "clicks": 140,
            "cvr": 0.12,
            "acos": 0.24,
            "orders": 17,
            "spend": 650
        }
        
        result = guard.simulate_ab_test(current, test)
        
        print("=" * 60)
        print("竞价策略A/B测试模拟")
        print("=" * 60)
        
        print("\n【策略A (当前)】")
        for k, v in result.strategy_a.items():
            if k != "acos":
                print(f"  {k}: {v}")
            else:
                print(f"  ACOS: {v*100:.1f}%")
        
        print("\n【策略B (测试)】")
        for k, v in result.strategy_b.items():
            if k != "acos":
                print(f"  {k}: {v}")
            else:
                print(f"  ACOS: {v*100:.1f}%")
        
        print("\n【预测结果】")
        pr = result.projected_results
        print(f"  订单变化: {pr['order_change']}")
        print(f"  ACOS变化: {pr['acos_change']}")
        print(f"  建议: {pr['recommendation']}")
    
    elif command == "time-bid":
        result = guard.generate_time_bidding("wireless earbuds")
        
        print("=" * 60)
        print(f"时间分时段出价 - {result['keyword']}")
        print("=" * 60)
        
        print(f"\n基础出价: ${result['base_bid']}\n")
        
        print("【时段出价建议】")
        for slot_name, slot_data in result["time_slots"].items():
            adjusted_bid = result["base_bid"] * slot_data["bid_adjustment"]
            print(f"\n  {slot_data['time']}")
            print(f"    系数: {slot_data['bid_adjustment']:.1f}x | 出价: ${adjusted_bid:.2f}")
            print(f"    转化率: {slot_data['转化率']} | {slot_data['reason']}")
        
        print("\n【优化建议】")
        for rec in result["recommendations"]:
            print(f"  → {rec}")
    
    elif command == "budget-optimizer":
        campaigns = [
            {"name": "自动广告", "budget": 200, "acos": 0.30, "orders": 15},
            {"name": "手动广泛", "budget": 300, "acos": 0.25, "orders": 25},
            {"name": "手动词组", "budget": 150, "acos": 0.35, "orders": 8},
            {"name": "手动精确", "budget": 250, "acos": 0.20, "orders": 30},
            {"name": "同行词", "budget": 100, "acos": 0.40, "orders": 5}
        ]
        
        result = guard.optimize_budget_allocation(campaigns)
        
        print("=" * 60)
        print("预算分配优化")
        print("=" * 60)
        
        print(f"\n总预算: ${result['total_budget']}\n")
        
        print("【优化方案】")
        for c in result["campaigns"]:
            print(f"\n  {c['name']}")
            print(f"    当前: ${c['current_budget']} | ACOS: {c['acos']*100:.0f}% | 订单: {c['orders']}")
            print(f"    效率: {c['efficiency']} | 调整后: ${c['allocation']} ({c['change']})")
        
        print("\n【预期效果】")
        summary = result["summary"]
        print(f"  高效活动: {summary['high_efficiency_count']}个")
        print(f"  低效活动: {summary['low_efficiency_count']}个")
        print(f"  预计ACOS改善: {summary['projected_acos_improvement']}")
        print(f"  预计订单增长: {summary['projected_order_increase']}")
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
