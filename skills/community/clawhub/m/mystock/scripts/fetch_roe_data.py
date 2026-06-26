#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取所有A股股票的近10年ROE数据并存储到roe_data.json
参考：https://cnb.cool/codebuddy/cbteamsmarketplace/-/blob/main/plugins/finance-data/skills/finance-data-retrieval/SKILL.md
"""

import json
import os
import asyncio
import httpx
from datetime import datetime

# 数据文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOCK_CODES_FILE = os.path.join(BASE_DIR, "stock_codes.json")
ROE_DATA_FILE = os.path.join(BASE_DIR, "roe_data.json")

# 加载股票代码
def load_stock_codes():
    """加载股票代码信息"""
    try:
        if os.path.exists(STOCK_CODES_FILE):
            with open(STOCK_CODES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"加载 stock_codes 失败: {e}")
    return {}

# 加载ROE数据
def load_roe_data():
    """加载ROE数据"""
    try:
        if os.path.exists(ROE_DATA_FILE):
            with open(ROE_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"加载 ROE 数据失败: {e}")
    return {}

# 保存ROE数据
def save_roe_data(data):
    """保存ROE数据"""
    with open(ROE_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 转换股票代码格式
def convert_code_format(code):
    """转换股票代码格式为Tushare格式"""
    if code.startswith('sz'):
        return f"{code[2:]}.SZ"
    elif code.startswith('sh'):
        return f"{code[2:]}.SH"
    return None

# 获取单只股票的ROE数据
async def fetch_stock_roe(code, name):
    """获取单只股票的ROE数据"""
    tushare_code = convert_code_format(code)
    if not tushare_code:
        return None
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://www.codebuddy.cn/v2/tool/financedata",
                headers={"Content-Type": "application/json"},
                json={
                    "api_name": "fina_indicator",
                    "params": {
                        "ts_code": tushare_code,
                        "start_date": "20150101",
                        "end_date": "20241231"
                    },
                    "fields": "ts_code,end_date,roe"
                },
                timeout=30.0
            )
        
        result = response.json()
        if result.get('code') == 0 and result.get('data'):
            data = result['data']
            items = data.get('items', [])
            
            roe_data = []
            for item in items:
                if len(item) >= 3:
                    roe_data.append({
                        "date": item[1],
                        "roe": item[2]
                    })
            
            return {
                "code": code,
                "name": name,
                "roe_data": roe_data
            }
    except Exception as e:
        print(f"获取 {code} ROE 数据失败: {e}")
    return None

# 批量获取所有A股股票的ROE数据
async def main():
    """批量获取所有A股股票的ROE数据"""
    print(f"[{datetime.now()}] 开始获取ROE数据...")
    
    # 加载数据
    print(f"[{datetime.now()}] 加载股票代码数据...")
    stock_codes = load_stock_codes()
    print(f"[{datetime.now()}] 加载现有ROE数据...")
    roe_data = load_roe_data()
    
    # 过滤A股股票
    print(f"[{datetime.now()}] 过滤A股股票...")
    a_stocks = {k: v for k, v in stock_codes.items() if k.startswith('sz') or k.startswith('sh')}
    total = len(a_stocks)
    processed = 0
    success = 0
    failed = 0
    
    print(f"[{datetime.now()}] 发现 {total} 只A股股票")
    print(f"[{datetime.now()}] 已有 {len(roe_data)} 只股票的ROE数据")
    
    # 批量处理
    batch_size = 10
    stock_list = list(a_stocks.items())
    total_batches = (total + batch_size - 1) // batch_size
    
    print(f"[{datetime.now()}] 总共需要处理 {total_batches} 批次")
    
    for i in range(0, total, batch_size):
        batch = stock_list[i:i+batch_size]
        batch_num = i // batch_size + 1
        print(f"[{datetime.now()}] 开始处理第 {batch_num}/{total_batches} 批次")
        print(f"[{datetime.now()}] 批次股票: {[code for code, _ in batch]}")
        
        tasks = []
        batch_stocks = []
        
        for code, info in batch:
            if code not in roe_data:
                name = info.get('name', code)
                tasks.append(fetch_stock_roe(code, name))
                batch_stocks.append(f"{code}({name})")
            else:
                processed += 1
                print(f"[{datetime.now()}] 股票 {code} 已有数据，跳过")
        
        if tasks:
            print(f"[{datetime.now()}] 开始获取 {len(tasks)} 只股票的ROE数据")
            print(f"[{datetime.now()}] 获取中: {batch_stocks}")
            
            # 并行执行
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            print(f"[{datetime.now()}] 批次处理完成，开始处理结果")
            
            for j, result in enumerate(results):
                code = batch[j][0]
                if result and not isinstance(result, Exception):
                    roe_data[result['code']] = result
                    success += 1
                    print(f"[{datetime.now()}] 成功获取 {code} 的ROE数据")
                else:
                    failed += 1
                    print(f"[{datetime.now()}] 获取 {code} 的ROE数据失败")
                processed += 1
            
            # 每批次保存
            print(f"[{datetime.now()}] 保存当前批次数据...")
            save_roe_data(roe_data)
            print(f"[{datetime.now()}] 批次 {batch_num} 处理完成")
            print(f"[{datetime.now()}] 累计进度: {processed}/{total}, 成功: {success}, 失败: {failed}")
        else:
            print(f"[{datetime.now()}] 批次 {batch_num} 所有股票已有数据，跳过")
            print(f"[{datetime.now()}] 累计进度: {processed}/{total}")
    
    # 最终保存
    print(f"[{datetime.now()}] 最终保存所有数据...")
    save_roe_data(roe_data)
    
    print(f"\n[{datetime.now()}] ROE数据获取完成")
    print(f"[{datetime.now()}] 总股票数: {total}")
    print(f"[{datetime.now()}] 成功获取: {success}")
    print(f"[{datetime.now()}] 失败: {failed}")
    print(f"[{datetime.now()}] 已存储: {len(roe_data)}")
    print(f"[{datetime.now()}] 数据已保存到: {ROE_DATA_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
