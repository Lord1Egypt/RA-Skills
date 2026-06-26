#!/usr/bin/env python3
"""
Newsletter Analytics & Reporting
分析和报告生成引擎
"""

import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


@dataclass
class NewsletterMetrics:
    """邮件核心指标"""
    sent: int = 0
    delivered: int = 0
    opened: int = 0
    clicked: int = 0
    unsubscribed: int = 0
    bounced: int = 0
    spam_complaints: int = 0


class AnalyticsEngine:
    """邮件营销分析引擎"""
    
    def __init__(self):
        self.benchmarks = {
            "open_rate": {"poor": 15, "average": 21, "good": 25, "excellent": 30},
            "click_rate": {"poor": 2, "average": 3.5, "good": 5, "excellent": 7},
            "click_to_open": {"poor": 10, "average": 15, "good": 20, "excellent": 25},
            "unsubscribe_rate": {"excellent": 0.1, "good": 0.3, "average": 0.5, "poor": 1.0},
            "bounce_rate": {"excellent": 0.5, "good": 1.0, "average": 2.0, "poor": 5.0}
        }
    
    def calculate_metrics(self, data: NewsletterMetrics) -> Dict:
        """
        计算关键指标
        
        Args:
            data: 原始数据
        
        Returns:
            计算后的指标字典
        """
        if data.sent == 0:
            return {"error": "无发送数据"}
        
        metrics = {
            "delivery_rate": (data.delivered / data.sent * 100) if data.sent > 0 else 0,
            "open_rate": (data.opened / data.delivered * 100) if data.delivered > 0 else 0,
            "click_rate": (data.clicked / data.delivered * 100) if data.delivered > 0 else 0,
            "click_to_open_rate": (data.clicked / data.opened * 100) if data.opened > 0 else 0,
            "unsubscribe_rate": (data.unsubscribed / data.delivered * 100) if data.delivered > 0 else 0,
            "bounce_rate": (data.bounced / data.sent * 100) if data.sent > 0 else 0,
            "spam_rate": (data.spam_complaints / data.delivered * 100) if data.delivered > 0 else 0
        }
        
        # 添加评级
        metrics["ratings"] = {
            "open_rate": self._rate_metric("open_rate", metrics["open_rate"]),
            "click_rate": self._rate_metric("click_rate", metrics["click_rate"]),
            "click_to_open_rate": self._rate_metric("click_to_open", metrics["click_to_open_rate"]),
            "unsubscribe_rate": self._rate_metric("unsubscribe_rate", metrics["unsubscribe_rate"], reverse=True),
            "bounce_rate": self._rate_metric("bounce_rate", metrics["bounce_rate"], reverse=True)
        }
        
        return metrics
    
    def _rate_metric(self, metric: str, value: float, reverse: bool = False) -> str:
        """评级指标表现"""
        if metric not in self.benchmarks:
            return "unknown"
        
        bench = self.benchmarks[metric]
        
        if reverse:
            # 越低越好（如退订率）
            if value <= bench["excellent"]:
                return "excellent"
            elif value <= bench["good"]:
                return "good"
            elif value <= bench["average"]:
                return "average"
            else:
                return "poor"
        else:
            # 越高越好（如打开率）
            if value >= bench["excellent"]:
                return "excellent"
            elif value >= bench["good"]:
                return "good"
            elif value >= bench["average"]:
                return "average"
            else:
                return "poor"
    
    def generate_insights(self, metrics: Dict, historical: List[Dict] = None) -> List[Dict]:
        """
        生成数据洞察和建议
        
        Args:
            metrics: 当前指标
            historical: 历史数据（可选）
        
        Returns:
            洞察列表
        """
        insights = []
        ratings = metrics.get("ratings", {})
        
        # 打开率洞察
        if ratings.get("open_rate") == "poor":
            insights.append({
                "category": "打开率",
                "severity": "high",
                "finding": f"打开率 {metrics['open_rate']:.1f}% 低于行业平均",
                "recommendation": "优化主题行，测试发送时间，清理不活跃订阅者",
                "potential_impact": "高"
            })
        elif ratings.get("open_rate") == "excellent":
            insights.append({
                "category": "打开率",
                "severity": "positive",
                "finding": f"打开率 {metrics['open_rate']:.1f}% 表现优秀！",
                "recommendation": "保持当前策略，分析成功因素复制到其他方面",
                "potential_impact": "维持优势"
            })
        
        # 点击率洞察
        if ratings.get("click_rate") == "poor":
            insights.append({
                "category": "点击率",
                "severity": "high",
                "finding": f"点击率 {metrics['click_rate']:.1f}% 需要改善",
                "recommendation": "优化内容相关性，强化 CTA，增加个性化",
                "potential_impact": "高"
            })
        
        # 退订率洞察
        if ratings.get("unsubscribe_rate") == "poor":
            insights.append({
                "category": "退订率",
                "severity": "critical",
                "finding": f"退订率 {metrics['unsubscribe_rate']:.2f}% 过高",
                "recommendation": "检查发送频率，确保内容价值，重新确认订阅偏好",
                "potential_impact": "紧急"
            })
        
        # 送达率洞察
        if metrics.get("delivery_rate", 100) < 95:
            insights.append({
                "category": "送达率",
                "severity": "high",
                "finding": f"送达率 {metrics['delivery_rate']:.1f}% 偏低",
                "recommendation": "清理无效邮箱，验证列表质量，检查发件人声誉",
                "potential_impact": "高"
            })
        
        # 历史对比（如果有数据）
        if historical and len(historical) > 0:
            avg_open = sum(h.get("open_rate", 0) for h in historical) / len(historical)
            current_open = metrics.get("open_rate", 0)
            
            if current_open > avg_open * 1.1:
                insights.append({
                    "category": "趋势",
                    "severity": "positive",
                    "finding": f"打开率比历史平均提升 {((current_open - avg_open) / avg_open * 100):.1f}%",
                    "recommendation": "分析本期成功因素并持续应用",
                    "potential_impact": "积极"
                })
            elif current_open < avg_open * 0.9:
                insights.append({
                    "category": "趋势",
                    "severity": "medium",
                    "finding": f"打开率比历史平均下降 {((avg_open - current_open) / avg_open * 100):.1f}%",
                    "recommendation": "检查内容质量、发送时间、主题行策略",
                    "potential_impact": "关注"
                })
        
        return insights
    
    def create_report(self, campaign_name: str, metrics: NewsletterMetrics,
                     period: str = "单次活动", insights: List[Dict] = None) -> Dict:
        """
        创建完整报告
        
        Args:
            campaign_name: 活动名称
            metrics: 原始指标
            period: 时间段
            insights: 洞察列表
        
        Returns:
            完整报告
        """
        calculated = self.calculate_metrics(metrics)
        
        if not insights:
            insights = self.generate_insights(calculated)
        
        report = {
            "report_title": f"{campaign_name} - 表现报告",
            "period": period,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "sent": metrics.sent,
                "delivered": metrics.delivered,
                "opened": metrics.opened,
                "clicked": metrics.clicked,
                "unsubscribed": metrics.unsubscribed
            },
            "key_metrics": calculated,
            "performance_ratings": calculated.get("ratings", {}),
            "insights": insights,
            "action_items": self._generate_action_items(insights)
        }
        
        return report
    
    def _generate_action_items(self, insights: List[Dict]) -> List[Dict]:
        """从洞察生成行动项"""
        actions = []
        
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "positive": 4}
        
        sorted_insights = sorted(
            insights,
            key=lambda x: priority_order.get(x.get("severity", "low"), 2)
        )
        
        for i, insight in enumerate(sorted_insights[:5], 1):  # 最多 5 个行动项
            if insight["severity"] != "positive":
                actions.append({
                    "priority": i,
                    "category": insight["category"],
                    "action": insight["recommendation"],
                    "expected_impact": insight["potential_impact"]
                })
        
        return actions


class GrowthTracker:
    """订阅者增长追踪器"""
    
    def __init__(self):
        self.growth_data = []
    
    def add_period(self, date: str, subscribers: int, new: int, 
                   lost: int, source: Dict = None):
        """添加周期数据"""
        self.growth_data.append({
            "date": date,
            "subscribers": subscribers,
            "new_subscribers": new,
            "lost_subscribers": lost,
            "net_growth": new - lost,
            "growth_rate": ((new - lost) / (subscribers - new + lost) * 100) if (subscribers - new + lost) > 0 else 0,
            "sources": source or {}
        })
    
    def get_growth_summary(self) -> Dict:
        """获取增长摘要"""
        if not self.growth_data:
            return {"error": "无数据"}
        
        total_new = sum(d["new_subscribers"] for d in self.growth_data)
        total_lost = sum(d["lost_subscribers"] for d in self.growth_data)
        
        # 计算平均增长率
        avg_growth_rate = sum(d["growth_rate"] for d in self.growth_data) / len(self.growth_data)
        
        # 找出最佳和最差周期
        best_period = max(self.growth_data, key=lambda x: x["net_growth"])
        worst_period = min(self.growth_data, key=lambda x: x["net_growth"])
        
        # 来源分析
        source_totals = {}
        for period in self.growth_data:
            for source, count in period.get("sources", {}).items():
                source_totals[source] = source_totals.get(source, 0) + count
        
        return {
            "periods_tracked": len(self.growth_data),
            "total_new_subscribers": total_new,
            "total_lost_subscribers": total_lost,
            "net_growth": total_new - total_lost,
            "average_growth_rate": f"{avg_growth_rate:.2f}%",
            "best_period": {
                "date": best_period["date"],
                "growth": best_period["net_growth"]
            },
            "worst_period": {
                "date": worst_period["date"],
                "growth": worst_period["net_growth"]
            },
            "top_sources": sorted(
                [{"source": k, "subscribers": v} for k, v in source_totals.items()],
                key=lambda x: x["subscribers"],
                reverse=True
            )[:5]
        }
    
    def project_growth(self, months: int = 6) -> List[Dict]:
        """基于历史数据预测未来增长"""
        if not self.growth_data:
            return []
        
        # 计算平均月增长
        recent_data = self.growth_data[-3:]  # 最近 3 期
        avg_monthly_growth = sum(d["net_growth"] for d in recent_data) / len(recent_data)
        avg_growth_rate = sum(d["growth_rate"] for d in recent_data) / len(recent_data)
        
        current_subs = self.growth_data[-1]["subscribers"]
        projections = []
        
        for month in range(1, months + 1):
            new_subs = int(current_subs * (avg_growth_rate / 100))
            current_subs += new_subs
            projections.append({
                "month": month,
                "projected_subscribers": current_subs,
                "new_subscribers": new_subs,
                "cumulative_growth": current_subs - self.growth_data[-1]["subscribers"]
            })
        
        return projections


def main():
    """CLI 入口"""
    print("=== Newsletter 分析与报告工具 ===\n")
    
    # 示例指标
    metrics = NewsletterMetrics(
        sent=10000,
        delivered=9850,
        opened=2462,
        clicked=493,
        unsubscribed=15,
        bounced=150,
        spam_complaints=5
    )
    
    # 计算指标
    engine = AnalyticsEngine()
    calculated = engine.calculate_metrics(metrics)
    
    print("核心指标:")
    print(f"  送达率：{calculated['delivery_rate']:.1f}%")
    print(f"  打开率：{calculated['open_rate']:.1f}% ({calculated['ratings']['open_rate']})")
    print(f"  点击率：{calculated['click_rate']:.1f}% ({calculated['ratings']['click_rate']})")
    print(f"  点开比：{calculated['click_to_open_rate']:.1f}%")
    print(f"  退订率：{calculated['unsubscribe_rate']:.2f}%")
    
    # 生成洞察
    print("\n数据洞察:")
    insights = engine.generate_insights(calculated)
    for insight in insights:
        print(f"  [{insight['severity'].upper()}] {insight['category']}: {insight['finding']}")
        print(f"    → {insight['recommendation']}")
    
    # 增长追踪
    print("\n\n=== 增长追踪 ===")
    tracker = GrowthTracker()
    
    # 添加示例数据
    tracker.add_period("2026-01", 5000, 320, 45, {"organic": 150, "referral": 100, "paid": 70})
    tracker.add_period("2026-02", 5275, 380, 52, {"organic": 180, "referral": 120, "paid": 80})
    tracker.add_period("2026-03", 5603, 410, 48, {"organic": 200, "referral": 130, "paid": 80})
    
    summary = tracker.get_growth_summary()
    print(f"追踪周期：{summary['periods_tracked']} 个月")
    print(f"净增长：{summary['net_growth']} 订阅者")
    print(f"平均增长率：{summary['average_growth_rate']}")
    print(f"最佳月份：{summary['best_period']['date']} (+{summary['best_period']['growth']})")
    print(f"主要来源：{summary['top_sources']}")
    
    # 增长预测
    print("\n6 个月增长预测:")
    projections = tracker.project_growth(6)
    for proj in projections:
        print(f"  第{proj['month']}月：{proj['projected_subscribers']} 订阅者 (+{proj['new_subscribers']})")


if __name__ == "__main__":
    main()
