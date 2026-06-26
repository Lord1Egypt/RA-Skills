#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
酒店竞争分析 - 基础版（兜底方案）
无需 API Key，手动输入或 Excel 导入
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime

class BasicHotelAnalysis:
    def __init__(self, hotel_name, competitors=None):
        self.hotel_name = hotel_name
        self.competitors = competitors or []
        self.results = {}
    
    def add_competitor(self, name, distance=None, rating=None, price=None):
        """添加竞争对手"""
        self.competitors.append({
            'name': name,
            'distance': distance,
            'rating': rating,
            'price': price
        })
    
    def analyze(self):
        """基础分析"""
        self.results = {
            'hotel_name': self.hotel_name,
            'competitor_count': len(self.competitors),
            'avg_rating': None,
            'price_range': None,
            'close_competitors': 0
        }
        
        if self.competitors:
            # 计算平均评分
            ratings = [c['rating'] for c in self.competitors if c.get('rating')]
            if ratings:
                self.results['avg_rating'] = sum(ratings) / len(ratings)
            
            # 计算价格区间
            prices = []
            for c in self.competitors:
                if c.get('price'):
                    if '-' in str(c['price']):
                        parts = str(c['price']).split('-')
                        prices.extend([int(p) for p in parts if p.isdigit()])
                    elif str(c['price']).isdigit():
                        prices.append(int(c['price']))
            
            if prices:
                self.results['price_range'] = f"{min(prices)}-{max(prices)}元"
            
            # 统计近距离竞争
            self.results['close_competitors'] = sum(
                1 for c in self.competitors 
                if c.get('distance') and int(str(c['distance']).replace('米', '')) < 500
            )
        
        return self.results
    
    def generate_report(self, output_path):
        """生成 Markdown 报告"""
        if not self.results:
            self.analyze()
        
        report = []
        report.append(f"# 酒店竞争分析报告（兜底版）")
        report.append("")
        report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**数据来源**: 手动输入/Excel 导入")
        report.append("")
        
        # 目标酒店
        report.append("## 目标酒店")
        report.append("")
        report.append(f"- **名称**: {self.hotel_name}")
        report.append("")
        
        # 竞争对手列表
        report.append("## 竞争对手（手动录入）")
        report.append("")
        
        if self.competitors:
            report.append("| 酒店名称 | 距离 | 评分 | 价格 |")
            report.append("|---------|------|------|------|")
            
            for comp in self.competitors:
                name = comp.get('name', '-')
                distance = comp.get('distance', '-')
                rating = comp.get('rating', '-')
                price = comp.get('price', '-')
                report.append(f"| {name} | {distance} | {rating} | {price} |")
        else:
            report.append("*暂无竞争对手数据*")
        
        report.append("")
        
        # 基础分析
        report.append("## 基础分析")
        report.append("")
        report.append(f"- **竞争对手数量**: {self.results.get('competitor_count', 0)} 家")
        
        if self.results.get('avg_rating'):
            report.append(f"- **平均评分**: {self.results['avg_rating']:.1f} 分")
        
        if self.results.get('price_range'):
            report.append(f"- **价格区间**: {self.results['price_range']}")
        
        if self.results.get('close_competitors', 0) > 0:
            report.append(f"- **近距离竞争**: {self.results['close_competitors']} 家（500 米内）")
        
        report.append("")
        
        # 建议
        report.append("## 建议")
        report.append("")
        report.append("1. 关注近距离竞争对手")
        report.append("2. 保持服务品质优势")
        report.append("3. 考虑价格策略调整")
        report.append("")
        
        # 升级提示
        report.append("---")
        report.append("")
        report.append("💡 **提示**: 您当前使用的是兜底版")
        report.append("")
        report.append("升级标准版可获得：")
        report.append("  ✅ 自动搜索周边酒店（无需手动录入）")
        report.append("  ✅ 精准距离计算")
        report.append("  ✅ 地图可视化链接")
        report.append("  ✅ 更多数据维度")
        report.append("")
        report.append("一键升级：")
        report.append("  ```bash")
        report.append("  ./scripts/setup_wizard.sh")
        report.append("  ```")
        report.append("")
        report.append("或访问：https://lbs.amap.com/ 获取免费 API Key")
        report.append("")
        report.append("*报告由酒店竞争分析 SKILL 生成（兜底版）*")
        
        # 保存报告
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        return output_path

def main():
    parser = argparse.ArgumentParser(description='酒店竞争分析 - 兜底版')
    parser.add_argument('--hotel', required=True, help='目标酒店名称')
    parser.add_argument('--competitors', help='竞争对手列表，逗号分隔')
    parser.add_argument('--input', help='Excel 输入文件')
    parser.add_argument('--output', default='reports/basic_analysis.md', help='输出文件路径')
    parser.add_argument('--auto-fetch', action='store_true', help='自动抓取公开数据')
    
    args = parser.parse_args()
    
    print(f"🏨 酒店竞争分析 - 兜底版")
    print(f"目标酒店：{args.hotel}")
    print()
    
    # 创建分析对象
    analysis = BasicHotelAnalysis(args.hotel)
    
    # 从命令行添加竞争对手
    if args.competitors:
        # 支持多种分隔符：逗号、顿号、分号
        separators = [',', '，', ';', '；', '、']
        comps = args.competitors
        for sep in separators:
            comps = comps.replace(sep, ',')
        comp_list = [c.strip() for c in comps.split(',') if c.strip()]
        for comp in comp_list:
            analysis.add_competitor(comp)
        print(f"✅ 已添加 {len(comp_list)} 个竞争对手")
    
    # 从 Excel 导入
    if args.input:
        try:
            import pandas as pd
            df = pd.read_excel(args.input)
            for _, row in df.iterrows():
                analysis.add_competitor(
                    name=row.get('酒店名称'),
                    distance=row.get('距离'),
                    rating=row.get('评分'),
                    price=row.get('价格区间')
                )
            print(f"✅ 已从 Excel 导入 {len(df)} 个竞争对手")
        except Exception as e:
            print(f"⚠️  Excel 导入失败：{e}")
    
    # 自动抓取（模拟）
    if args.auto_fetch:
        print("⚠️  自动抓取功能需要配置 API，跳过...")
    
    print()
    print("📊 执行分析...")
    analysis.analyze()
    
    print(f"📝 生成报告...")
    output = analysis.generate_report(args.output)
    
    print()
    print("======================================")
    print("✅ 分析完成！")
    print("======================================")
    print(f"报告已保存：{output}")
    print()
    print("查看报告:")
    print(f"  cat {output}")
    print()

if __name__ == "__main__":
    main()
