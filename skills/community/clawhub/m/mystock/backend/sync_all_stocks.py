#!/usr/bin/env python3
"""
股票数据统一同步脚本
自动同步 A股、港股、ETF 到 stock_codes.json

使用方法：
    python sync_all_stocks.py              # 同步所有
    python sync_all_stocks.py --a-share    # 只同步A股
    python sync_all_stocks.py --hk         # 只同步港股
    python sync_all_stocks.py --etf       # 只同步ETF
"""

import json
import os
import time
import requests
import argparse

def load_portfolio_data():
    """加载portfolio_data.json"""
    data_file = os.path.join(os.path.dirname(__file__), '..', 'portfolio_data.json')
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_portfolio_data(data):
    """保存portfolio_data.json"""
    data_file = os.path.join(os.path.dirname(__file__), '..', 'portfolio_data.json')
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def sync_a_stocks():
    """同步A股（使用AKShare）"""
    print("\n" + "="*60)
    print("📥 同步 A股（沪深京）...")
    print("="*60)

    try:
        import akshare_proxy_patch
        import akshare as ak

        stock_info = ak.stock_info_a_code_name()
        print(f"   获取到 {len(stock_info)} 只A股")

        stock_codes = {}
        for _, row in stock_info.iterrows():
            code = row['code']
            name = row['name']

            # 判断交易所
            if code.startswith('6'):
                market = 'sh'
            elif code.startswith('8') or code.startswith('4'):
                market = 'bj'
            else:
                market = 'sz'

            full_code = f"{market}{code}"

            # 如果code已存在，添加别名
            if full_code in stock_codes:
                if name and name != stock_codes[full_code]['name']:
                    stock_codes[full_code]['aliases'].append(name)
                if ' ' in name:
                    stock_codes[full_code]['aliases'].append(name.replace(' ', ''))
            else:
                stock_codes[full_code] = {
                    'name': name,
                    'aliases': []
                }
                if ' ' in name:
                    stock_codes[full_code]['aliases'].append(name.replace(' ', ''))

        print(f"   ✓ A股同步完成: {len(stock_codes)} 条")
        return stock_codes

    except Exception as e:
        print(f"   ✗ A股同步失败: {e}")
        return {}

def sync_hk_stocks():
    """同步港股（使用腾讯API轮询）"""
    print("\n" + "="*60)
    print("📥 同步 港股...")
    print("="*60)

    stock_codes = {}
    url_template = "https://qt.gtimg.cn/q=hk{}"

    # 港股代码范围
    start, end = 1, 10000
    total = 0

    print(f"   开始扫描港股代码 hk00001 - hk09999...")

    for i in range(start, end + 1):
        code = f"{i:05d}"
        full_code = f"hk{code}"
        full_url = url_template.format(code)

        try:
            response = requests.get(full_url, timeout=2)
            response.encoding = 'gbk'
            text = response.text

            if '="";' not in text and len(text) > 50:
                parts = text.split('="')[1].rstrip('";')
                fields = parts.split('~')

                if len(fields) > 3 and fields[3] and fields[3] != '0':
                    name = fields[1]
                    if name and len(name) > 0:
                        aliases = []
                        if not name.endswith('-W'):
                            aliases.append(f"{name}-W")

                        if full_code in stock_codes:
                            if name not in stock_codes[full_code]['aliases']:
                                stock_codes[full_code]['aliases'].append(name)
                            stock_codes[full_code]['aliases'].extend(aliases)
                        else:
                            stock_codes[full_code] = {
                                'name': name,
                                'aliases': aliases
                            }
                        total += 1

                        if total % 500 == 0:
                            print(f"   已找到 {total} 只港股...")

        except:
            pass

        if i % 100 == 0:
            time.sleep(0.05)

    print(f"   ✓ 港股同步完成: {total} 只")
    return stock_codes

def sync_etf():
    """同步ETF基金"""
    print("\n" + "="*60)
    print("📥 同步 ETF基金...")
    print("="*60)

    try:
        import akshare as ak

        df = ak.fund_etf_category_sina(symbol='ETF基金')
        print(f"   获取到 {len(df)} 只ETF基金")

        etf_codes = {}
        for _, row in df.iterrows():
            code = str(row['代码'])

            # 转换代码格式: sz159998 -> sz159998, sh518660 -> sh518660
            if code.startswith(('sz', 'sh')):
                full_code = code.lower()
            else:
                # 处理纯数字代码
                if code.startswith('5') or code.startswith('15'):
                    full_code = f"sh{code}"
                else:
                    full_code = f"sz{code}"

            name = row['名称']

            if full_code in etf_codes:
                if name not in etf_codes[full_code]['aliases']:
                    etf_codes[full_code]['aliases'].append(name)
            else:
                etf_codes[full_code] = {
                    'name': name,
                    'aliases': []
                }

        print(f"   ✓ ETF同步完成: {len(etf_codes)} 条")
        return etf_codes

    except Exception as e:
        print(f"   ✗ ETF同步失败: {e}")
        return {}

def sync_all(a_share=True, hk=True, etf=False):
    """同步股票数据"""
    print("="*60)
    print("股票数据统一同步工具")
    print("="*60)

    # 读取现有数据
    stock_codes_file = os.path.join(os.path.dirname(__file__), '..', 'stock_codes.json')
    if os.path.exists(stock_codes_file):
        with open(stock_codes_file, 'r', encoding='utf-8') as f:
            all_codes = json.load(f)
        print(f"   现有股票: {len(all_codes)} 条")
    else:
        all_codes = {}

    result_count = {'a': 0, 'hk': 0, 'etf': 0}

    # 1. 同步A股
    if a_share:
        a_codes = sync_a_stocks()
        all_codes.update(a_codes)
        result_count['a'] = len(a_codes)
        time.sleep(1)

    # 2. 同步港股
    if hk:
        hk_codes = sync_hk_stocks()
        all_codes.update(hk_codes)
        result_count['hk'] = len(hk_codes)
        time.sleep(1)

    # 3. 同步ETF
    if etf:
        etf_codes = sync_etf()
        all_codes.update(etf_codes)
        result_count['etf'] = len(etf_codes)

    # 保存
    print("\n" + "="*60)
    print("📊 同步完成！")
    print("="*60)
    if a_share:
        print(f"   A股: +{result_count['a']} 条")
    if hk:
        print(f"   港股: +{result_count['hk']} 条")
    if etf:
        print(f"   ETF: +{result_count['etf']} 条")
    print(f"   总计: {len(all_codes)} 条")
    print("="*60)

    with open(stock_codes_file, 'w', encoding='utf-8') as f:
        json.dump(all_codes, f, ensure_ascii=False, indent=4)

    print(f"\n✅ 已保存到 stock_codes.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='股票数据同步工具')
    parser.add_argument('--a-share', action='store_true', help='只同步A股')
    parser.add_argument('--hk', action='store_true', help='只同步港股')
    parser.add_argument('--etf', action='store_true', help='只同步ETF')
    parser.add_argument('--all', action='store_true', default=True, help='同步所有(默认)')

    args = parser.parse_args()

    # 根据参数决定同步哪些
    a_share = args.a_share or (not args.hk and not args.etf)
    hk = args.hk or (not args.a_share and not args.etf)
    etf = args.etf

    sync_all(a_share=a_share, hk=hk, etf=etf)
