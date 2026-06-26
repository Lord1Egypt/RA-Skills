#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金类型批量查询工具
使用说明：
1. 将基金代码放入 codes 列表
2. 运行脚本：python query_fund_type.py
3. 结果输出到 fund_types.csv
"""

import requests
import re
import time
import csv

def get_fund_type(code):
    """
    查询基金类型
    使用天天基金网 API
    """
    try:
        url = f"http://fund.eastmoney.com/pingzhongdata/{code}.js"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'http://fund.eastmoney.com/'
        }
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            # 解析返回的 JS，提取 fundType
            match = re.search(r'fundType\s*=\s*"([^"]+)"', response.text)
            if match:
                return match.group(1)
            
            # 尝试其他可能的字段
            match = re.search(r'fType\s*=\s*"([^"]+)"', response.text)
            if match:
                return match.group(1)
                
            return "未知类型"
        else:
            return f"查询失败 ({response.status_code})"
    except Exception as e:
        return f"错误：{str(e)}"

def batch_query(codes, delay=0.5):
    """
    批量查询基金类型
    codes: 基金代码列表
    delay: 每次请求间隔秒数（避免频率限制）
    """
    results = []
    total = len(codes)
    
    print(f"开始查询 {total} 只基金...")
    print("-" * 50)
    
    for i, code in enumerate(codes, 1):
        fund_type = get_fund_type(code)
        results.append({
            '基金代码': code,
            '基金类型': fund_type
        })
        print(f"[{i}/{total}] {code}: {fund_type}")
        time.sleep(delay)  # 避免频率限制
    
    print("-" * 50)
    print("查询完成！")
    
    return results

def save_to_csv(results, filename='fund_types.csv'):
    """保存结果到 CSV 文件"""
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['基金代码', '基金类型'])
        writer.writeheader()
        writer.writerows(results)
    print(f"结果已保存到 {filename}")

if __name__ == '__main__':
    # ====== 在这里填入你的基金代码 ======
    codes = [
        '003095',  # 中欧医疗健康混合 A
        '001938',  # 中欧时代先锋股票 A
        '110011',  # 易方达优质精选混合
        '005918',  # 天弘沪深 300ETF 联接 C
        '002963',  # 易方达黄金 ETF 联接 C
        '040046',  # 华安纳斯达克 100ETF 联接
        '006321',  # 中欧养老目标 2035FOF
        # ... 在这里添加更多基金代码
    ]
    # ===================================
    
    # 执行批量查询
    results = batch_query(codes, delay=0.5)
    
    # 保存结果
    save_to_csv(results)
    
    # 打印结果（方便复制到 Excel）
    print("\n===== 复制以下结果到 Excel D 列 =====")
    for r in results:
        print(f"{r['基金代码']}\t{r['基金类型']}")
