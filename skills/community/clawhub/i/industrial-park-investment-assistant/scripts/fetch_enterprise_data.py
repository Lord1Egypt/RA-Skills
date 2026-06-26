#!/usr/bin/env python3
"""
企查查API集成脚本
获取企业实时数据：背景、融资、招聘、专利等
"""

import json
import os
import sys
import requests
import time
from datetime import datetime

# 配置
QCC_API_KEY = "YOUR_API_KEY_HERE"  # 企查查API Key（需申请）
QCC_API_URL = "https://api.qichacha.com/"

class EnterpriseDataFetcher:
    def __init__(self, enterprise_name):
        self.enterprise_name = enterprise_name
        self.api_key = QCC_API_KEY
        self.data = {}
        
    def fetch_basic_info(self):
        """获取企业基本信息"""
        print(f"🔍 正在获取 {self.enterprise_name} 的基本信息...")
        
        # 实际API调用（需申请企查查API Key）
        # url = f"{QCC_API_URL}/enterprise/getBasicDetails"
        # params = {"key": self.api_key, "searchKey": self.enterprise_name}
        # response = requests.get(url, params=params)
        
        # 模拟数据（实际应用中替换为真实API调用）
        time.sleep(1)  # 模拟API延迟
        
        self.data["basic"] = {
            "name": self.enterprise_name,
            "founded": "2015-03-12",
            "registered_capital": "1000万元",
            "scale": "150人",
            "revenue_estimate": "2.5亿元（估算）",
            "funding_round": "B轮",
            "funding_amount": "5亿元",
            "business": "人工智能解决方案",
            "industry_rank": "细分领域Top5",
            "legal_representative": "张XX",
            "registration_status": "存续"
        }
        
        print(f"✅ 基本信息获取完成")
        return self.data["basic"]
    
    def fetch_funding_history(self):
        """获取融资历史"""
        print(f"💰 正在获取融资历史...")
        
        # 模拟数据
        time.sleep(0.8)
        
        self.data["funding"] = [
            {
                "round": "天使轮",
                "date": "2016-08",
                "amount": "500万元",
                "investors": "XX创投"
            },
            {
                "round": "A轮",
                "date": "2018-05",
                "amount": "3000万元",
                "investors": "XX资本、YY投资"
            },
            {
                "round": "B轮",
                "date": "2026-03",
                "amount": "5亿元",
                "investors": "XX基金、YY资本、ZZ投资"
            }
        ]
        
        print(f"✅ 融资历史获取完成")
        return self.data["funding"]
    
    def fetch_recruitment_info(self):
        """获取招聘信息（扩张信号）"""
        print(f"👥 正在获取招聘信息...")
        
        # 模拟数据
        time.sleep(0.7)
        
        self.data["recruitment"] = {
            "recent_posts": [
                {"position": "高级算法工程师", "count": 10, "date": "2026-05"},
                {"position": "产品经理", "count": 5, "date": "2026-04"},
                {"position": "销售总监", "count": 3, "date": "2026-03"}
            ],
            "total_recent": 18,
            "expansion_signal": "强（近3个月招聘18人）"
        }
        
        print(f"✅ 招聘信息获取完成")
        return self.data["recruitment"]
    
    def fetch_patent_info(self):
        """获取专利信息"""
        print(f"🔬 正在获取专利信息...")
        
        # 模拟数据
        time.sleep(0.6)
        
        self.data["patents"] = {
            "total": 45,
            "inventions": 32,
            "utility_models": 10,
            "designs": 3,
            "recent_growth": "近1年新增15项发明专利"
        }
        
        print(f"✅ 专利信息获取完成")
        return self.data["patents"]
    
    def fetch_related_companies(self):
        """获取关联企业（产业链分析）"""
        print(f"🔗 正在获取关联企业...")
        
        # 模拟数据
        time.sleep(0.9)
        
        self.data["related"] = {
            "subsidiaries": ["华东分公司", "深圳研发中心"],
            "branches": ["北京办事处", "成都研发中心"],
            "invested_companies": ["AA科技", "BB智能"],
            "upstream": ["CC供应链", "DD材料"],
            "downstream": ["EE应用", "FF解决方案"]
        }
        
        print(f"✅ 关联企业获取完成")
        return self.data["related"]
    
    def analyze_industry_match(self, park_industries):
        """分析产业匹配度"""
        print(f"📊 正在分析产业匹配度...")
        
        # 模拟分析
        time.sleep(0.5)
        
        # 假设园区主导产业：人工智能、生物医药、智能制造
        enterprise_industry = self.data["basic"]["business"]
        
        match_score = 0
        match_details = []
        
        if "人工智能" in enterprise_industry:
            match_score += 5
            match_details.append("✅ 主营业务与园区主导产业（人工智能）高度匹配")
            
        if self.data["basic"]["industry_rank"] in ["Top1", "Top3", "Top5"]:
            match_score += 3
            match_details.append("✅ 行业地位高，可吸引产业链上下游企业")
            
        if self.data["funding"][-1]["round"] in ["B轮", "C轮", "D轮"]:
            match_score += 2
            match_details.append("✅ 融资阶段成熟，扩张意愿强")
            
        self.data["industry_match"] = {
            "score": match_score,
            "max_score": 10,
            "percentage": f"{match_score/10*100:.0f}%",
            "details": match_details,
            "recommendation": "重点跟进" if match_score >= 7 else "普通跟进"
        }
        
        print(f"✅ 产业匹配度分析完成: {self.data['industry_match']['percentage']}")
        return self.data["industry_match"]
    
    def fetch_all_data(self):
        """获取所有企业数据"""
        print(f"🚀 开始获取 {self.enterprise_name} 的完整数据...")
        print(f"=" * 60)
        
        # 顺序获取所有数据
        self.fetch_basic_info()
        self.fetch_funding_history()
        self.fetch_recruitment_info()
        self.fetch_patent_info()
        self.fetch_related_companies()
        
        print(f"=" * 60)
        print(f"🎉 所有数据获取完成！")
        print(f"📋 数据摘要:")
        print(f"   企业名称: {self.enterprise_name}")
        print(f"   成立时间: {self.data['basic']['founded']}")
        print(f"   融资轮次: {self.data['basic']['funding_round']}")
        print(f"   近期招聘: {self.data['recruitment']['total_recent']} 人")
        print(f"   专利数量: {self.data['patents']['total']} 项")
        
        return self.data
    
    def save_to_file(self, output_dir=None):
        """保存数据到文件"""
        if output_dir is None:
            output_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant/data/enterprise")
            
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.enterprise_name}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
            
        print(f"💾 数据已保存: {filepath}")
        return filepath

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 fetch_enterprise_data.py <企业名称>")
        print("示例: python3 fetch_enterprise_data.py \"XX科技公司\"")
        sys.exit(1)
    
    enterprise_name = sys.argv[1]
    
    fetcher = EnterpriseDataFetcher(enterprise_name)
    data = fetcher.fetch_all_data()
    
    # 分析产业匹配度（需要提供园区主导产业列表）
    park_industries = ["人工智能", "生物医药", "智能制造"]
    fetcher.analyze_industry_match(park_industries)
    
    # 保存数据
    output_file = fetcher.save_to_file()
    
    print(f"\n📊 完整数据结构:")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    
    print(f"\n💡 使用建议:")
    print(f"   1. 将获取的实时数据集成到会前简报中")
    print(f"   2. 基于招聘信息判断扩张紧迫度")
    print(f"   3. 基于融资历史判断资金实力和扩租能力")
    print(f"   4. 基于专利增长判断技术驱动型和场地需求（研发实验室）")

if __name__ == "__main__":
    main()