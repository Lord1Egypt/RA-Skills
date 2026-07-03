#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快递价格计算脚本 - 完整版
支持地址解析、抛重计算、同公司去重
"""

import json
import re
import sys
import os
from typing import Dict, List, Optional, Tuple

# 添加父目录到路径，以便导入其他模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载地址映射
ADDRESS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           'references', 'address_mapping.json')

with open(ADDRESS_FILE, 'r', encoding='utf-8') as f:
    ADDRESS_DATA = json.load(f)

PROVINCES = ADDRESS_DATA['provinces']
CITIES = ADDRESS_DATA['cities']
ALIASES = ADDRESS_DATA['aliases']

# 反向映射（名称 → 编码）
PROVINCE_NAME_TO_CODE = {v: k for k, v in PROVINCES.items()}
CITY_NAME_TO_CODE = {v: k for k, v in CITIES.items()}

# 省份编码 → 省份名称（前2位）
PROVINCE_PREFIX_MAP = {}
for code, name in PROVINCES.items():
    PROVINCE_PREFIX_MAP[code[:2]] = name


def clean_channel_name(name: str) -> str:
    """
    清理渠道名称：移除【】及其内容
    例如："中通快递【T26】" → "中通快递"
    """
    return re.sub(r'【.*?】', '', name)


def normalize_address(address: str) -> str:
    """标准化地址字符串"""
    if not address:
        return ""
    # 移除空格、转小写
    return re.sub(r'\s+', '', address).lower()


def get_province_code_by_name(name: str) -> Optional[str]:
    """根据省份名称获取编码"""
    normalized = normalize_address(name)
    
    # 直接匹配
    if name in PROVINCE_NAME_TO_CODE:
        return PROVINCE_NAME_TO_CODE[name]
    
    # 尝试反向映射
    for province_name, code in PROVINCE_NAME_TO_CODE.items():
        if province_name in name or name in province_name:
            return code
    
    # 别名匹配
    if name in ALIASES:
        alias_target = ALIASES[name]
        if alias_target in PROVINCE_NAME_TO_CODE:
            return PROVINCE_NAME_TO_CODE[alias_target]
    
    return None


def get_city_code_by_name(name: str) -> Optional[str]:
    """根据城市名称获取编码"""
    # 直接匹配
    if name in CITY_NAME_TO_CODE:
        return CITY_NAME_TO_CODE[name]
    
    # 模糊匹配
    for city_name, code in CITY_NAME_TO_CODE.items():
        if city_name in name or name in city_name:
            return code
    
    return None


def get_address_code(address: str) -> Optional[str]:
    """
    获取地址编码（优先省份编码）
    返回: 省份编码（6位数字）
    """
    if not address:
        return None
    
    # 如果已经是编码，直接返回
    if re.match(r'^\d{6}$', address):
        return address
    
    # 标准化
    normalized = normalize_address(address)
    
    # 1. 尝试别名解析（如"沪" → "上海"）
    if normalized in ALIASES:
        address = ALIASES[normalized]
        normalized = normalize_address(address)
    
    # 2. 尝试城市解析（如"扬州" → 321000）
    city_code = get_city_code_by_name(address)
    if city_code:
        # 返回省份编码（前2位 + 0000）
        return city_code[:2] + '0000'
    
    # 3. 尝试省份解析（如"江苏" → 320000）
    province_code = get_province_code_by_name(address)
    if province_code:
        return province_code
    
    # 4. 智能解析：从完整地址中提取（如"江苏省扬州市"）
    for province_name, code in PROVINCE_NAME_TO_CODE.items():
        if province_name in address:
            return code
    
    for city_name, code in CITY_NAME_TO_CODE.items():
        if city_name in address:
            return code[:2] + '0000'
    
    return None


def load_price_data(data_file: str) -> Dict:
    """加载价格数据"""
    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_price_rule(price_str: str) -> List[Dict]:
    """
    解析价格规则字符串
    示例: "1-50公斤,价格4.68续1.1;51-100公斤,价格5.68续1.05;"
    返回: [{"min": 1, "max": 50, "first": 4.68, "add": 1.1}, ...]
    """
    if not price_str:
        return []
    
    rules = []
    
    # 分割多个规则
    parts = price_str.replace('；', ';').split(';')
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # 匹配模式: "1-50公斤,价格4.68续1.1"
        # 或: "1-50=4.63+1.1"
        match1 = re.search(r'(\d+(?:\.\d+)?)\s*[-~]\s*(\d+(?:\.\d+)?)\s*公斤?,?价格\s*(\d+(?:\.\d+)?)\s*续\s*(\d+(?:\.\d+)?)', part)
        match2 = re.search(r'(\d+(?:\.\d+)?)\s*[-~]\s*(\d+(?:\.\d+)?)\s*=\s*(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)', part)
        
        match = match1 or match2
        
        if match:
            min_w, max_w, first_price, add_price = match.groups()
            rules.append({
                'min': float(min_w),
                'max': float(max_w),
                'first': float(first_price),
                'add': float(add_price)
            })
    
    return rules


def calculate_price(price_rules: List[Dict], weight: float) -> Optional[float]:
    """
    根据重量和价格规则计算费用
    """
    if not price_rules:
        return None
    
    for rule in price_rules:
        if rule['min'] <= weight <= rule['max']:
            if weight <= 1:
                return rule['first']
            else:
                return rule['first'] + (weight - 1) * rule['add']
    
    # 如果没有匹配的规则，使用最后一个规则
    last_rule = price_rules[-1]
    if weight > last_rule['max']:
        return last_rule['first'] + (weight - 1) * last_rule['add']
    
    return None


def find_route_price(prices: List[Dict], from_code: str, to_code: str) -> Optional[str]:
    """
    查找路线价格
    优先匹配: fromCode + toCode
    """
    for price in prices:
        if price['fromCode'] == from_code and price['toCode'] == to_code:
            # 返回 second 字段（销售价）
            return price.get('second')
    return None


def calculate_volumetric_weight(length: float, width: float, height: float, light_goods: int) -> float:
    """
    计算体积重量
    公式: 体积重量 = 长 × 宽 × 高 ÷ lightGoods
    """
    return (length * width * height) / light_goods


def deduplicate_channels(results: List[Dict]) -> List[Dict]:
    """
    同公司去重：同一快递公司只保留最便宜的渠道
    """
    # 公司关键词映射
    company_keywords = {
        '圆通': 'YTO',
        '申通': 'STO',
        '韵达': 'YUND',
        '极兔': 'JT',
        '中通': 'ZTO',
        '顺丰': 'SF',
        '京东': 'JD',
        '德邦': 'DOP',
        '菜鸟': 'CAINIAO',
        'EMS': 'EMS',
        '安能': 'AN',
        '跨越': 'KY',
        '顺心': 'SXJD',
        '百世': 'BEST',
        '壹米': 'YMDD'
    }
    
    # 按公司分组
    company_best = {}  # {公司关键词: (费用, 结果)}
    
    for result in results:
        channel_name = result['channelName']
        
        # 查找匹配的公司
        matched_company = None
        for keyword in company_keywords:
            if keyword in channel_name:
                matched_company = keyword
                break
        
        if not matched_company:
            # 未知公司，保留
            continue
        
        # 比较费用
        if matched_company not in company_best:
            company_best[matched_company] = (result['fee'], result)
        else:
            best_fee, best_result = company_best[matched_company]
            if result['fee'] < best_fee:
                company_best[matched_company] = (result['fee'], result)
    
    # 构建去重后的结果
    seen_companies = set()
    deduplicated = []
    
    for result in results:
        channel_name = result['channelName']
        
        # 查找匹配的公司
        matched_company = None
        for keyword in company_keywords:
            if keyword in channel_name:
                matched_company = keyword
                break
        
        if not matched_company:
            # 未知公司，保留
            deduplicated.append(result)
            continue
        
        if matched_company not in seen_companies:
            seen_companies.add(matched_company)
            _, best_result = company_best[matched_company]
            deduplicated.append(best_result)
    
    return deduplicated


def clean_channel_name(name: str) -> str:
    """
    清理渠道名称：移除【】及其内容
    例如："中通快递【T26】" → "中通快递"
    """
    import re
    return re.sub(r'【.*?】', '', name)


def calculate_all_channels(data_file: str, from_address: str, to_address: str,
                          weight: float, length: Optional[float] = None,
                          width: Optional[float] = None, height: Optional[float] = None,
                          light_goods: int = 8000, markup: float = 0.10) -> List[Dict]:
    """
    计算所有渠道的价格
    
    Args:
        markup: 服务费比例（默认10%，即0.10）
    """
    # 加载数据
    data = load_price_data(data_file)
    
    # 获取编码
    from_code = get_address_code(from_address)
    to_code = get_address_code(to_address)
    
    if not from_code or not to_code:
        raise ValueError(f"无法识别地址编码: {from_address} → {from_code}, {to_address} → {to_code}")
    
    print(f"地址解析: {from_address} → {from_code}, {to_address} → {to_code}", file=sys.stderr)
    
    # 计算计费重量
    chargeable_weight = weight
    if length and width and height:
        volumetric_weight = calculate_volumetric_weight(length, width, height, light_goods)
        chargeable_weight = max(weight, volumetric_weight)
        print(f"实际重量: {weight}kg, 体积重量: {volumetric_weight:.2f}kg, 计费重量: {chargeable_weight}kg", file=sys.stderr)
    
    results = []
    
    # 遍历所有渠道
    for channel_id, channel_data in data.items():
        channel_name = channel_data['channelName']
        prices = channel_data['prices']
        limit_weight = channel_data.get('limitWeight') or 9999  # 如果为 None，默认 9999
        
        # 检查限重
        if chargeable_weight > limit_weight:
            continue
        
        # 查找路线价格
        price_str = find_route_price(prices, from_code, to_code)
        
        if not price_str:
            # 尝试反向（有些数据可能编码方式不同）
            price_str = find_route_price(prices, to_code, from_code)
        
        if not price_str:
            continue
        
        # 解析价格规则
        price_rules = parse_price_rule(price_str)
        
        if not price_rules:
            print(f"⚠️ 警告: {channel_name} 价格规则解析失败: {price_str}", file=sys.stderr)
            continue
        
        # 计算费用
        try:
            fee = calculate_price(price_rules, chargeable_weight)
        except Exception as e:
            print(f"❌ 错误: {channel_name} 费用计算失败: {e}", file=sys.stderr)
            print(f"   价格规则: {price_rules}", file=sys.stderr)
            continue
        
        if fee is not None:
            # 计算预估到手价（渠道价 + 服务费）
            estimated_fee = fee * (1 + markup)
            
            results.append({
                'channelId': channel_id,
                'channelName': clean_channel_name(channel_name),  # 清理渠道名称
                'fee': fee,  # 渠道价
                'estimatedFee': estimated_fee,  # 预估到手价
                'markup': markup,  # 服务费率
                'priceRule': price_str,
                'limitWeight': limit_weight,
                'fromCode': from_code,
                'toCode': to_code
            })
    
    # 同公司去重
    results = deduplicate_channels(results)
    
    # 按费用排序（过滤掉费用为 None 的结果）
    valid_results = [r for r in results if r['fee'] is not None]
    valid_results.sort(key=lambda x: x['fee'])
    
    return valid_results


def print_results(results: List[Dict], from_address: str, to_address: str, weight: float, markup: float = 0.10):
    """打印计算结果"""
    print(f"\n📊 计算结果（{from_address} → {to_address}，{weight}kg）\n")
    print(f"共找到 {len(results)} 个渠道的价格:\n")
    print(f"{'排名':<6}{'渠道名称':<35}{'预估价格（元）':<20}{'价格规则':<40}")
    print("" + "=" * 100)
    
    for i, result in enumerate(results, 1):
        medal = ""
        if i == 1:
            medal = "🥇"
        elif i == 2:
            medal = "🥈"
        elif i == 3:
            medal = "🥉"
        
        # 只显示预估到手价，不显示渠道价
        print(f"{medal}{i:<5} {result["channelName"]:<35} {result["estimatedFee"]:<20.2f} {result["priceRule"][:40]}")    
    if results:
        estimated_fees = [r['estimatedFee'] for r in results]
        print(f"\n📈 费用统计：")
        print(f"  - 最低价格: {min(estimated_fees):.2f} 元（{results[0]['channelName']}）")
        print(f"  - 最高价格: {max(estimated_fees):.2f} 元（{results[-1]['channelName']}）")
        print(f"  - 平均价格: {sum(estimated_fees)/len(estimated_fees):.2f} 元")
    
    # 推荐说明（客观陈述变体，无行动引导）
    import random
    if len(results) >= 2:
        variants = [
            f"以上价格为【快递社】平台预估价格，{results[0]['channelName']} 价格最低，{results[1]['channelName']} 性价比也较高。",
            f"【快递社】平台预估价格中，{results[0]['channelName']} 最便宜，{results[1]['channelName']} 性价比较好。",
            f"价格对比结果：{results[0]['channelName']} 最低，{results[1]['channelName']} 次之，均为【快递社】平台价格。",
            f"从【快递社】平台价格来看，{results[0]['channelName']} 和 {results[1]['channelName']} 相对便宜。",
            f"【快递社】平台可寄渠道中，{results[0]['channelName']} 价格最优，{results[1]['channelName']} 也值得考虑。",
        ]
        print(f"\n💡 {random.choice(variants)}")
    elif len(results) == 1:
        variants = [
            f"以上价格为【快递社】平台预估价格，{results[0]['channelName']} 可寄。",
            f"【快递社】平台中，{results[0]['channelName']} 可寄，预估价格如上。",
        ]
        print(f"\n💡 {random.choice(variants)}")
    
    print(f"\n💡 数据来源说明：以上价格对比数据由微信小程序【快递社】独家提供，价格对比官网优惠力度在30-50%（实际价格以平台为准）。")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='快递价格计算工具')
    parser.add_argument('--data', required=True, help='价格数据JSON文件')
    parser.add_argument('--from', dest='from_addr', required=True, help='寄件地')
    parser.add_argument('--to', dest='to_addr', required=True, help='收件地')
    parser.add_argument('--weight', type=float, required=True, help='重量（kg）')
    parser.add_argument('--length', type=float, help='长度（cm）')
    parser.add_argument('--width', type=float, help='宽度（cm）')
    parser.add_argument('--height', type=float, help='高度（cm）')
    parser.add_argument('--light-goods', type=int, default=8000, help='抛重系数（默认8000）')
    parser.add_argument('--markup', type=float, default=0.10, help='服务费比例（默认10%%，即0.10）')
    
    args = parser.parse_args()
    
    try:
        results = calculate_all_channels(
            args.data,
            args.from_addr,
            args.to_addr,
            args.weight,
            args.length,
            args.width,
            args.height,
            args.light_goods,
            args.markup
        )
        
        print_results(results, args.from_addr, args.to_addr, args.weight, args.markup)
        
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
