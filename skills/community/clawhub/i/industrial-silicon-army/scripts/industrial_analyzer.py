#!/usr/bin/env python3
"""
Industrial Silicon Army - 塑化行业运营分析工具
用途：分析客户询盘、生成报价建议、库存提醒
"""

import argparse
import json
from datetime import datetime

def analyze_inquiry(inquiry_text: str) -> dict:
    """分析询盘内容，提取关键信息"""
    keywords = {
        'product': ['PVC', 'PE', 'PP', 'ABS', 'PS', 'PC', 'PA', 'POM', 'PMMA', 'PBT'],
        'quantity': ['吨', 'kg', '公斤', '吨位', '数量'],
        'urgency': ['急', '紧急', '尽快', '马上', 'urgent']
    }
    
    result = {
        'timestamp': datetime.now().isoformat(),
        'products_mentioned': [],
        'urgency_level': 'normal',
        'suggested_actions': []
    }
    
    # 检测产品类型
    for product in keywords['product']:
        if product.lower() in inquiry_text.lower():
            result['products_mentioned'].append(product)
    
    # 检测紧急程度
    for word in keywords['urgency']:
        if word in inquiry_text:
            result['urgency_level'] = 'high'
            break
    
    # 生成建议
    if result['products_mentioned']:
        result['suggested_actions'].append('检查库存: ' + ', '.join(result['products_mentioned']))
    if result['urgency_level'] == 'high':
        result['suggested_actions'].append('优先处理: 标记为紧急询盘')
    
    return result

def main():
    parser = argparse.ArgumentParser(description='Industrial Silicon Army Analysis Tool')
    parser.add_argument('--inquiry', '-i', type=str, help='询盘内容')
    parser.add_argument('--output', '-o', type=str, default='json', choices=['json', 'text'])
    args = parser.parse_args()
    
    if args.inquiry:
        result = analyze_inquiry(args.inquiry)
        if args.output == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"分析结果:")
            print(f"  时间: {result['timestamp']}")
            print(f"  产品: {', '.join(result['products_mentioned']) or '未识别'}")
            print(f"  紧急程度: {result['urgency_level']}")
            print(f"  建议操作: {', '.join(result['suggested_actions']) or '无'}")
    else:
        print("Industrial Silicon Army v1.2.3")
        print("使用方法: python industrial_analyzer.py --inquiry '您的询盘内容'")

if __name__ == '__main__':
    main()
