#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宠物用品分析辅助脚本
用于整理和分析收集到的产品评测数据
"""

import json
from datetime import datetime
from typing import List, Dict, Any

class ProductAnalyzer:
    """产品分析器"""
    
    def __init__(self, product_name: str, product_type: str):
        self.product_name = product_name
        self.product_type = product_type
        self.reviews = []
        self.videos = []
        self.competitors = []
        
    def add_review(self, platform: str, username: str, content: str, 
                   is_positive: bool, credibility: str, link: str = ""):
        """添加用户评测"""
        self.reviews.append({
            "platform": platform,
            "username": username,
            "content": content,
            "is_positive": is_positive,
            "credibility": credibility,  # A/B/C/D
            "link": link,
            "added_at": datetime.now().isoformat()
        })
    
    def add_video(self, title: str, uploader: str, platform: str,
                  views: str, key_points: str, link: str):
        """添加评测视频"""
        self.videos.append({
            "title": title,
            "uploader": uploader,
            "platform": platform,
            "views": views,
            "key_points": key_points,
            "link": link,
            "added_at": datetime.now().isoformat()
        })
    
    def add_competitor(self, name: str, price: str, features: str, 
                       pros: str, cons: str):
        """添加竞品信息"""
        self.competitors.append({
            "name": name,
            "price": price,
            "features": features,
            "pros": pros,
            "cons": cons
        })
    
    def get_summary(self) -> Dict[str, Any]:
        """获取评测摘要"""
        positive_reviews = [r for r in self.reviews if r["is_positive"]]
        negative_reviews = [r for r in self.reviews if not r["is_positive"]]
        
        # 按可信度统计
        credibility_count = {"A": 0, "B": 0, "C": 0, "D": 0}
        for r in self.reviews:
            if r["credibility"] in credibility_count:
                credibility_count[r["credibility"]] += 1
        
        return {
            "product_name": self.product_name,
            "product_type": self.product_type,
            "total_reviews": len(self.reviews),
            "positive_count": len(positive_reviews),
            "negative_count": len(negative_reviews),
            "credibility_distribution": credibility_count,
            "video_count": len(self.videos),
            "competitor_count": len(self.competitors)
        }
    
    def export_to_json(self, filepath: str):
        """导出数据到JSON文件"""
        data = {
            "product_name": self.product_name,
            "product_type": self.product_type,
            "reviews": self.reviews,
            "videos": self.videos,
            "competitors": self.competitors,
            "summary": self.get_summary(),
            "exported_at": datetime.now().isoformat()
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已导出到: {filepath}")


class ReviewFilter:
    """评测内容筛选器"""
    
    # 软广关键词库
    SPONSORED_KEYWORDS = [
        "绝绝子", "YYDS", "闭眼入", "挖到宝", "种草",
        "不会还有人", "后悔没早点", "所有养猫人",
        "一定要试试", "姐妹们快冲", "马住"
    ]
    
    # 真实评测关键词
    AUTHENTIC_KEYWORDS = [
        "用了", "体验", "感受", "问题", "缺点",
        "避雷", "踩坑", "真实", "长期", "三个月",
        "半年", "一年"
    ]
    
    @classmethod
    def check_sponsored_signals(cls, content: str) -> Dict[str, Any]:
        """检查软广信号"""
        content_lower = content.lower()
        
        sponsored_count = sum(1 for kw in cls.SPONSORED_KEYWORDS if kw in content)
        authentic_count = sum(1 for kw in cls.AUTHENTIC_KEYWORDS if kw in content)
        
        # 计算软广风险分数
        risk_score = sponsored_count * 2 - authentic_count
        
        if risk_score >= 3:
            risk_level = "高"
        elif risk_score >= 1:
            risk_level = "中"
        else:
            risk_level = "低"
        
        return {
            "sponsored_keywords_found": sponsored_count,
            "authentic_keywords_found": authentic_count,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "is_likely_sponsored": risk_level == "高"
        }
    
    @classmethod
    def assess_credibility(cls, platform: str, username: str, 
                          content: str, fan_count: str = "unknown") -> str:
        """评估内容可信度等级"""
        signals = cls.check_sponsored_signals(content)
        
        # 基础评分
        score = 5
        
        # 根据软广信号扣分
        if signals["risk_level"] == "高":
            score -= 3
        elif signals["_level"] == "中":
            score -= 1
        
        # 根据粉丝数调整
        if fan_count != "unknown":
            try:
                fan_num = int(fan_count.replace("万", "0000").replace("千", "000"))
                if fan_num > 100000:
                    score -= 1  # 大V可能有商业合作
            except:
                pass
        
        # 根据关键词加分
        score += signals["authentic_keywords_found"] * 0.5
        
        # 内容长度加分（真实评测通常更长）
        if len(content) > 200:
            score += 1
        
        # 确定等级
        if score >= 7:
            return "A"
        elif score >= 5:
            return "B"
        elif score >= 3:
            return "C"
        else:
            return "D"


class ScoreCalculator:
    """评分计算器"""
    
    # 产品类型权重配置
    WEIGHTS = {
        "智能猫砂盆": {
            "清洁效果": 0.25,
            "噪音控制": 0.20,
            "安全性": 0.20,
            "容量适配": 0.15,
            "耗材成本": 0.10,
            "APP体验": 0.05,
            "清洁维护": 0.05
        },
        "自动喂食器": {
            "出粮精准度": 0.25,
            "密封保鲜": 0.20,
            "摄像头功能": 0.15,
            "APP体验": 0.15,
            "供电安全": 0.15,
            "清洁维护": 0.10
        },
        "智能饮水机": {
            "过滤效果": 0.25,
            "水流设计": 0.20,
            "安全性": 0.20,
            "续航容量": 0.15,
            "清洁维护": 0.10,
            "噪音控制": 0.10
        }
    }
    
    @classmethod
    def calculate_score(cls, product_type: str, dimension_scores: Dict[str, float]) -> Dict[str, Any]:
        """计算综合评分"""
        if product_type not in cls.WEIGHTS:
            return {"error": f"未知产品类型: {product_type}"}
        
        weights = cls.WEIGHTS[product_type]
        
        # 计算加权总分
        total_score = 0
        details = []
        
        for dimension, score in dimension_scores.items():
            weight = weights.get(dimension, 0)
            weighted_score = score * weight
            total_score += weighted_score
            details.append({
                "dimension": dimension,
                "score": score,
                "weight": weight,
                "weighted_score": weighted_score
            })
        
        # 确定等级
        if total_score >= 9:
            grade = "S"
        elif total_score >= 8:
            grade = "A"
        elif total_score >= 7:
            grade = "B"
        elif total_score >= 6:
            grade = "C"
        else:
            grade = "D"
        
        return {
            "total_score": round(total_score, 2),
            "grade": grade,
            "details": details
        }


def generate_report_summary(analyzer: ProductAnalyzer) -> str:
    """生成报告摘要文本"""
    summary = analyzer.get_summary()
    
    text = f"""
{'='*60}
产品分析报告摘要
{'='*60}

产品名称: {summary['product_name']}
产品类型: {summary['product_type']}

【数据收集情况】
- 用户评测: {summary['total_reviews']}条
  - 正面评价: {summary['positive_count']}条
  - 负面评价: {summary['negative_count']}条
- 评测视频: {summary['video_count']}个
- 竞品信息: {summary['competitor_count']}个

【可信度分布】
- A级(高可信): {summary['credibility_distribution']['A']}条
- B级(较可信): {summary['credibility_distribution']['B']}条
- C级(需谨慎): {summary['credibility_distribution']['C']}条
- D级(可能软广): {summary['credibility_distribution']['D']}条

{'='*60}
"""
    return text


# 使用示例
if __name__ == "__main__":
    # 创建分析器实例
    analyzer = ProductAnalyzer("小佩智能猫砂盆MAX", "智能猫砂盆")
    
    # 添加评测数据示例
    analyzer.add_review(
        platform="小红书",
        username="养猫的普通人",
        content="用了三个月，整体还不错，但是除臭效果一般，夏天有点味道",
        is_positive=True,
        credibility="A",
        link="https://xiaohongshu.com/xxx"
    )
    
    analyzer.add_review(
        platform="小红书",
        username="某品牌合作达人",
        content="这个猫砂盆绝绝子！YYDS！所有养猫人都需要！闭眼入！",
        is_positive=True,
        credibility="D",
        link="https://xiaohongshu.com/yyy"
    )
    
    # 添加视频
    analyzer.add_video(
        title="小佩MAX三个月使用体验",
        uploader="猫奴日常",
        platform="B站",
        views="5.2万",
        key_points="优点：清理方便；缺点：噪音略大、耗材贵",
        link="https://bilibili.com/xxx"
    )
    
    # 添加竞品
    analyzer.add_competitor(
        name="Catlink智能猫砂盆",
        price="¥1899",
        features="自动清理、APP控制、多猫识别",
        pros="识别准确、噪音小",
        cons="价格较高"
    )
    
    # 打印摘要
    print(generate_report_summary(analyzer))
    
    # 导出数据
    analyzer.export_to_json("analysis_data.json")
    
    # 评分计算示例
    dimension_scores = {
        "清洁效果": 8.5,
        "噪音控制": 7.0,
        "安全性": 9.0,
        "容量适配": 8.0,
        "耗材成本": 6.5,
        "APP体验": 7.5,
        "清洁维护": 8.0
    }
    
    result = ScoreCalculator.calculate_score("智能猫砂盆", dimension_scores)
    print(f"\n综合评分: {result['total_score']}/10")
    print(f"评级: {result['grade']}级")
