# -*- coding: utf-8 -*-
"""
Description: LOF基金溢价监控程序
Author: kafrocyang@gmail.com
Version: 1.0.1
Date: 2026-03-12
"""


import pandas as pd
import akshare as ak
import requests
from bs4 import BeautifulSoup
import time


# 当场内价格高于场外净值时，高出的百分比溢价率超过10%时，视为溢价过高，需要告警。按需调整阈值，默认为10%。
premium_threshold = 10.0
# 当场内价格低于场外净值时，低出的百分比折价率超过10%时，视为折价过高，需要告警。按需调整阈值，默认为10%。
discount_threshold = 10.0


# 获取LOF基金列表及最新场内价格（实时数据）
def get_lof_fund_list_with_price():
    try:
        result = []
        raw_df = ak.fund_etf_category_sina(symbol="LOF基金")
        for _, row in raw_df.iterrows():
            code_with_prefix = row['代码']
            if code_with_prefix.startswith('sz'):
                market = 'sz'
                code = code_with_prefix[2:]
            elif code_with_prefix.startswith('sh'):
                market = 'sh'
                code = code_with_prefix[2:]
            else:
                market = ''
                code = code_with_prefix

            try:
                market_price = float(row['最新价']) if pd.notna(row['最新价']) else None
            except (ValueError, TypeError):
                market_price = None
            
            result.append({
                'market': market,
                'code': code,
                'name': row['名称'],
                'market_price': market_price
            })
        
        df = pd.DataFrame(result)
        return df
    except Exception as e:
        print(f"获取LOF基金列表失败: {e}")
        return None


# 解析基金状态（交易状态、封闭期等）
def parse_fund_state(code):
    url = "https://fund.eastmoney.com/" + code +".html"
    ret = ""
    
    try:
        response = requests.get(url, timeout=10)
        response.encoding = response.apparent_encoding 
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            target_div = None
            items = soup.find_all("div", class_="staticItem")
            for item in items:
                if "交易状态" in item.text:
                    target_div = item
                    break 
            if target_div:
                raw_text = target_div.get_text(strip=True)
                clean_text = raw_text.replace('\xa0', ' ')
                
                ret = clean_text.replace("交易状态：", "")
    except Exception as e:
        pass
    
    return ret


# 获取单个LOF基金的场外净值及日期
def get_nav_price(code):
    try:
        df = ak.fund_open_fund_info_em(symbol=code, indicator="单位净值走势")
        
        if df is not None and not df.empty:
            nav_date = df.iloc[-1, 0]
            nav_val = df.iloc[-1, 1]
            if hasattr(nav_date, 'strftime'):
                nav_date_str = nav_date.strftime('%Y-%m-%d')
            else:
                nav_date_str = str(nav_date)
                
            return float(nav_val), nav_date_str
        return None, None
    except Exception as e:
        return None, None


# 获取指定基金最近的一个有效单位净值
def get_latest_nav_value(fund_code, nav_df):
    row = nav_df[nav_df['基金代码'] == fund_code]

    if row.empty:
        return None,None
    
    row_data = row.iloc[0]
    nav_cols = [col for col in nav_df.columns if '单位净值' in col]
    nav_cols.sort(reverse=True)
    for col in nav_cols:
        val = row_data[col]
        if pd.notnull(val) and str(val).strip() != '' and val != '-':
            try:
                return float(val), col.split('-单位净值')[0]
            except ValueError:
                continue
 
    return None,None


# 获取所有LOF基金的完整数据（场内价格和场外净值）
def get_all_lof_fund_data():
    fund_df = get_lof_fund_list_with_price()
    if fund_df is not None:
        fund_df = fund_df[fund_df['market_price'] != 0]
    nav_df = None
    
    try:
        nav_df = ak.fund_open_fund_daily_em()
    except Exception as e:
        print(f"获取基金净值数据失败: {e}")
        return []
    
    if fund_df is None or nav_df is None or nav_df.empty:
        return []
    
    # 过滤nav_df，只保留fund_df中存在的基金代码，提高运行效率
    valid_codes = set(fund_df['code'].astype(str))
    nav_df = nav_df[nav_df['基金代码'].astype(str).isin(valid_codes)]
    
    result = []
    for idx, row in fund_df.iterrows():
        code = row['code']
        name = row['name']
        market_price = row['market_price']
        nav_price, nav_date = get_latest_nav_value(code, nav_df)
        if nav_price is None:
            nav_price, nav_date = get_nav_price(code)
        if nav_price is None:
            continue

        fund_data = {
            'code': code,
            'name': name,
            'market': row['market'],
            'market_price': market_price,
            'nav_price': nav_price,
            'nav_date': nav_date,
            'fund_state': None
        }

        result.append(fund_data)
    
    return result


# 主函数，获取基金数据，计算溢价率和折价率，并输出结果
if __name__ == "__main__":
    all_fund_data = get_all_lof_fund_data()
    with open('LOFMonitor_output.txt', 'w', encoding='utf-8') as f:
        for fund in all_fund_data:
            if fund['market_price'] is None or fund['nav_price'] is None:
                continue
            premium_rate = (fund['market_price'] - fund['nav_price']) / fund['nav_price'] * 100
            discount_rate = (fund['nav_price'] - fund['market_price']) / fund['nav_price'] * 100
            
            if premium_rate >= premium_threshold:
                fund_state = parse_fund_state(fund['code'])
                output_line = f"基金代码: {fund['code']}, 名称: {fund['name']}, 场内价格: {fund['market_price']:<8.4f}, 场外净值: {fund['nav_price']:<8.4f}, 溢价率: {premium_rate:.2f}%, 状态: {fund_state}\n"
                print(output_line.strip())
                f.write(output_line)
            elif discount_rate >= discount_threshold:
                fund_state = parse_fund_state(fund['code'])
                output_line = f"基金代码: {fund['code']}, 名称: {fund['name']}, 场内价格: {fund['market_price']:<8.4f}, 场外净值: {fund['nav_price']:>8.4f}, 折价率: {discount_rate:.2f}%, 状态: {fund_state}\n"
                print(output_line.strip())
                f.write(output_line)
