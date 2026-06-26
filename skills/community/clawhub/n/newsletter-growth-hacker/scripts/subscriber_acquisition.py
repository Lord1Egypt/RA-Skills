#!/usr/bin/env python3
"""
Newsletter Growth Hacker - Subscriber Acquisition Strategies
Provides data-driven strategies for growing newsletter subscriber base
"""

import json
from typing import Dict, List
from datetime import datetime

class SubscriberAcquisition:
    """订阅者获取策略引擎"""
    
    def __init__(self):
        self.strategies = {
            "content_upgrade": {
                "name": "内容升级策略",
                "description": "通过高质量免费资源吸引订阅",
                "tactics": [
                    "创建行业报告/白皮书作为订阅诱饵",
                    "提供独家模板、清单或工具包",
                    "设置系列内容的付费墙前预览",
                    "创建交互式评估工具"
                ],
                "conversion_rate": "3-8%",
                "effort": "中等",
                "roi": "高"
            },
            "social_proof": {
                "name": "社会证明策略",
                "description": "利用现有订阅者影响力吸引新用户",
                "tactics": [
                    "展示订阅者数量和增长里程碑",
                    "分享读者成功案例和推荐",
                    "在社交媒体展示精选评论",
                    "创建'订阅者专属'社区感"
                ],
                "conversion_rate": "2-5%",
                "effort": "低",
                "roi": "中高"
            },
            "referral_program": {
                "name": "推荐计划",
                "description": "激励现有订阅者邀请他人",
                "tactics": [
                    "推荐 3 人获得独家内容",
                    "推荐排行榜 + 月度奖励",
                    "双向奖励（推荐人和被推荐人都获益）",
                    "创建病毒式传播循环"
                ],
                "conversion_rate": "15-25%",
                "effort": "高",
                "roi": "非常高"
            },
            "cross_promotion": {
                "name": "交叉推广",
                "description": "与其他创作者/品牌合作互换受众",
                "tactics": [
                    "Newsletter 互换推荐",
                    "播客嘉宾互换",
                    "联合网络研讨会",
                    "社交媒体互相背书"
                ],
                "conversion_rate": "5-12%",
                "effort": "中等",
                "roi": "高"
            },
            "seo_lead_magnet": {
                "name": "SEO 引流磁铁",
                "description": "通过搜索引擎优化吸引有机流量",
                "tactics": [
                    "创建 evergreen 内容枢纽",
                    "优化高意图关键词着陆页",
                    "制作可分享的 infographic",
                    "回答行业常见问题（建立权威）"
                ],
                "conversion_rate": "2-6%",
                "effort": "高（前期）",
                "roi": "长期非常高"
            },
            "paid_ads": {
                "name": "付费广告",
                "description": "精准投放广告获取订阅者",
                "tactics": [
                    "Facebook/Instagram 线索广告",
                    "Twitter 推广推文",
                    "LinkedIn 精准定向（B2B）",
                    "Google Search 广告（高意图）"
                ],
                "conversion_rate": "1-4%",
                "effort": "中等",
                "roi": "取决于 CPC"
            }
        }
    
    def get_strategies(self, budget: str = "any", effort: str = "any") -> List[Dict]:
        """
        获取适合的订阅者获取策略
        
        Args:
            budget: 预算级别 (low/medium/high/any)
            effort: 投入程度 (low/medium/high/any)
        
        Returns:
            策略列表
        """
        results = []
        for key, strategy in self.strategies.items():
            match = True
            if effort != "any" and strategy["effort"].lower() != effort:
                # 模糊匹配
                if effort == "low" and strategy["effort"] != "低":
                    match = False
                elif effort == "medium" and strategy["effort"] != "中等":
                    match = False
                elif effort == "high" and strategy["effort"] != "高":
                    match = False
            
            if match:
                results.append({
                    "id": key,
                    **strategy
                })
        
        return results
    
    def calculate_projection(self, current_subscribers: int, strategy: str, 
                           months: int, conversion_rate: float = None) -> Dict:
        """
        计算订阅者增长预测
        
        Args:
            current_subscribers: 当前订阅者数量
            strategy: 策略 ID
            months: 预测月数
            conversion_rate: 转化率（可选，使用默认值）
        
        Returns:
            增长预测数据
        """
        if strategy not in self.strategies:
            return {"error": "未知策略"}
        
        strat = self.strategies[strategy]
        
        # 解析转化率范围
        if not conversion_rate:
            rate_range = strat["conversion_rate"].replace("%", "").split("-")
            avg_rate = (float(rate_range[0]) + float(rate_range[1])) / 2 / 100
        else:
            avg_rate = conversion_rate
        
        # 简单增长模型（实际应更复杂）
        monthly_growth = avg_rate * 100  # 简化为月增长率
        projections = []
        
        for month in range(1, months + 1):
            new_subs = int(current_subscribers * (monthly_growth / 100))
            current_subscribers += new_subs
            projections.append({
                "month": month,
                "new_subscribers": new_subs,
                "total_subscribers": current_subscribers
            })
        
        return {
            "strategy": strat["name"],
            "initial_subscribers": projections[0]["total_subscribers"] - projections[0]["new_subscribers"],
            "final_subscribers": current_subscribers,
            "total_growth": current_subscribers - (projections[0]["total_subscribers"] - projections[0]["new_subscribers"]),
            "growth_rate": f"{monthly_growth:.1f}% 每月",
            "projections": projections
        }
    
    def generate_action_plan(self, strategy_ids: List[str], timeline: str = "30 天") -> Dict:
        """
        生成执行行动计划
        
        Args:
            strategy_ids: 选择的策略 ID 列表
            timeline: 时间线
        
        Returns:
            行动计划
        """
        plan = {
            "timeline": timeline,
            "selected_strategies": [],
            "action_items": [],
            "milestones": []
        }
        
        for sid in strategy_ids:
            if sid in self.strategies:
                plan["selected_strategies"].append(self.strategies[sid]["name"])
        
        # 生成通用行动项
        plan["action_items"] = [
            {
                "phase": "第 1 周：准备",
                "tasks": [
                    "审计现有内容和渠道",
                    "设置追踪和分析工具",
                    "创建基线指标文档",
                    "准备内容素材"
                ]
            },
            {
                "phase": "第 2-3 周：执行",
                "tasks": [
                    "启动首选获取策略",
                    "A/B 测试着陆页",
                    "开始交叉推广合作",
                    "监控每日指标"
                ]
            },
            {
                "phase": "第 4 周：优化",
                "tasks": [
                    "分析表现数据",
                    "优化低效渠道",
                    "扩大高效策略",
                    "准备下月计划"
                ]
            }
        ]
        
        plan["milestones"] = [
            {"day": 7, "target": "完成所有准备工作"},
            {"day": 14, "target": "启动至少 2 个获取渠道"},
            {"day": 21, "target": "获得初步数据，开始优化"},
            {"day": 30, "target": "实现月度增长目标"}
        ]
        
        return plan


def main():
    """CLI 入口"""
    acquisition = SubscriberAcquisition()
    
    print("=== Newsletter 订阅者获取策略 ===\n")
    
    # 显示所有策略
    strategies = acquisition.get_strategies()
    for i, strat in enumerate(strategies, 1):
        print(f"{i}. {strat['name']}")
        print(f"   {strat['description']}")
        print(f"   转化率：{strat['conversion_rate']} | 投入：{strat['effort']} | ROI: {strat['roi']}\n")
    
    # 示例：增长预测
    print("\n=== 增长预测示例 ===")
    projection = acquisition.calculate_projection(
        current_subscribers=1000,
        strategy="referral_program",
        months=6
    )
    print(f"策略：{projection['strategy']}")
    print(f"初始订阅者：{projection['initial_subscribers']}")
    print(f"6 个月后：{projection['final_subscribers']}")
    print(f"总增长：{projection['total_growth']}")


if __name__ == "__main__":
    main()
