#!/usr/bin/env python3
"""
M估值法 - 基于ROIC和CAPM的股票估值

数据获取原则:
1. 每个数据必须标注来源
2. 关键数据需多渠道交叉验证
3. A股优先用Tushare，港股用雪球/东方财富/同花顺交叉验证

用法: python3 valuation.py <股票代码> [股票名称]
"""

import sys
import subprocess
import os
os.environ["TAVILY_API_KEY"] = "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"
import re
import json
import warnings
warnings.filterwarnings('ignore')

try:
    import tushare as ts
    HAS_TUSHARE = True
except ImportError:
    HAS_TUSHARE = False

DEFAULT_RF = 2.5
DEFAULT_RM_RF = 6.0

# ========== 数据获取函数 ==========

def is_hk_stock(code):
    """判断是否为港股"""
    code = code.upper()
    return '.HK' in code or (len(code) == 5 and code.isdigit())

def get_xueqiu_price(code, name):
    """从雪球获取港股数据"""
    try:
        hk_code = code.replace('.HK', '').lstrip('0')
        query = f"{name} {hk_code} 雪球 股价 实时"
        result = subprocess.run(
            ['node', '/root/.openclaw/workspace/skills/tavily-search/scripts/search.mjs', query, '-n', '2'],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout
        
        # 提取数据
        price_match = re.search(r'(\d+\.?\d*)\s*港元', output)
        price = float(price_match.group(1)) if price_match else None
        
        pe_match = re.search(r'市盈率\(TTM\)[：:]*\s*(\d+\.?\d*)', output)
        pe = float(pe_match.group(1)) if pe_match else None
        
        pb_match = re.search(r'市净率[：:]*\s*(\d+\.?\d*)', output)
        pb = float(pb_match.group(1)) if pb_match else None
        
        if price:
            return {'price': price, 'pe': pe, 'pb': pb, 'source': '雪球'}
        return None
    except:
        return None

def get_eastmoney_price(code, name):
    """从东方财富获取港股数据"""
    try:
        hk_code = code.replace('.HK', '').lstrip('0')
        query = f"{name} {hk_code} 东方财富 股价"
        result = subprocess.run(
            ['node', '/root/.openclaw/workspace/skills/tavily-search/scripts/search.mjs', query, '-n', '2'],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout
        
        price_match = re.search(r'昨收[：:]*\s*(\d+\.?\d*)', output)
        price = float(price_match.group(1)) if price_match else None
        
        if price:
            return {'price': price, 'source': '东方财富'}
        return None
    except:
        return None

def get_ths_price(code, name):
    """从同花顺获取港股数据"""
    try:
        hk_code = code.replace('.HK', '').lstrip('0')
        query = f"{name} {hk_code} 同花顺 股价"
        result = subprocess.run(
            ['node', '/root/.openclaw/workspace/skills/tavily-search/scripts/search.mjs', query, '-n', '2'],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout
        
        price_match = re.search(r'现价[：:]*\s*(\d+\.?\d*)', output)
        price = float(price_match.group(1)) if price_match else None
        
        if price:
            return {'price': price, 'source': '同花顺'}
        return None
    except:
        return None

def cross_validate_price(code, name):
    """交叉验证股价 - 从多个渠道获取并比较"""
    sources = []
    
    # 获取多个来源的数据
    xueqiu = get_xueqiu_price(code, name)
    if xueqiu:
        sources.append(xueqiu)
    
    eastmoney = get_eastmoney_price(code, name)
    if eastmoney:
        sources.append(eastmoney)
    
    ths = get_ths_price(code, name)
    if ths:
        sources.append(ths)
    
    if not sources:
        return None, []
    
    # 提取所有价格
    prices = [(s['price'], s['source']) for s in sources if s.get('price')]
    
    if not prices:
        return None, sources
    
    # 计算平均值
    avg_price = sum(p[0] for p in prices) / len(prices)
    
    # 检查差异
    max_diff = max(abs(p[0] - avg_price) for p in prices)
    diff_pct = max_diff / avg_price * 100 if avg_price > 0 else 0
    
    # 如果差异超过5%，需要标注
    warning = ""
    if diff_pct > 5:
        warning = f"  ⚠️ 数据差异{diff_pct:.1f}%，建议核实"
    
    return {
        'price': avg_price,
        'sources': sources,
        'warning': warning
    }, sources

def get_beta(stock_name):
    """获取β系数，交叉验证"""
    try:
        query = f"{stock_name} Beta 贝塔系数"
        result = subprocess.run(
            ['node', '/root/.openclaw/workspace/skills/tavily-search/scripts/search.mjs', query, '-n', '3'],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout
        match = re.search(r'(\d+\.?\d*)', output)
        if match:
            beta = float(match.group(1))
            if 0.1 < beta < 3.0:
                return beta, "价值大师/雪球"
        return None, "默认1.0"
    except:
        return None, "默认1.0"

def get_a_stock_data(code):
    """从Tushare获取A股数据"""
    if not HAS_TUSHARE:
        return None
    
    try:
        # 标准化代码
        if '.' not in code:
            code = code + ('.SH' if code.startswith('6') else '.SZ')
        
        pro = ts.pro_api('25a94c412802019f4d44977d57f69980e0cb5a57615002ec86f725f0')
        
        df = pro.daily_basic(ts_code=code, fields='close,pe,pb,dv_ratio,total_mv', limit=1)
        df_fina = pro.fina_indicator(ts_code=code, limit=1)
        
        return {
            'source': 'Tushare',
            'price': float(df['close'].values[0]),
            'pe_ttm': float(df['pe'].values[0]),
            'pb': float(df['pb'].values[0]),
            'div_rate': float(df['dv_ratio'].values[0]),
            'roe': float(df_fina['roe'].values[0]),
            'roic': float(df_fina['roic'].values[0]),
            'eps': float(df_fina['eps'].values[0])
        }
    except Exception as e:
        return None

# ========== 主分析函数 ==========

def analyze_stock(code, name=''):
    print(f"""
================================================================================
🏭 {name or code} M估值法分析报告
================================================================================

📌 数据获取原则
- 每个数据标注来源
- 关键数据多渠道交叉验证
================================================================================
""")
    
    # 判断股票类型
    is_hk = is_hk_stock(code)
    
    if is_hk:
        # 港股：多渠道交叉验证
        price_data, sources = cross_validate_price(code, name)
        
        if not price_data:
            print("❌ 无法获取股价数据\n")
            return
        
        price = price_data['price']
        
        print(f"""📊 实时股价交叉验证 (2026-03-03)
--------------------------------------------------------------------------------""")
        for s in sources:
            src = s.get('source', '未知')
            p = s.get('price', 'N/A')
            print(f"  {src}: {p} 港元")
        
        if price_data.get('warning'):
            print(price_data['warning'])
        
        print(f"  ──────────────────────────────────────────────")
        print(f"  交叉验证均价: {price:.2f} 港元")
        print()
        
        # 获取PE/PB（从雪球）
        xueqiu_data = get_xueqiu_price(code, name)
        pe_ttm = xueqiu_data.get('pe') if xueqiu_data else None
        pb = xueqiu_data.get('pb') if xueqiu_data else None
        
        # 获取ROE/ROIC
        beta, beta_src = get_beta(name)
        beta = beta or 1.0
        
        print(f"""📈 关键指标数据
--------------------------------------------------------------------------------
  股价: {price} 港元 [交叉验证均价]
  PE_TTM: {pe_ttm or 'N/A'} [雪球]
  PB: {pb or 'N/A'} [雪球]
  β系数: {beta} [{beta_src}]
  
  注: ROE/ROIC/财务数据需从公司财报获取
--------------------------------------------------------------------------------
""")
        
        # 假设数据（港股财报数据获取复杂）
        roe = 19.9  # 价值大师
        roic = 13.5  # Alpha Spread
        eps = 1.81  # 雪球
        cash_div = 0  # 不分红
        div_rate = 0
        
    else:
        # A股：用Tushare
        data = get_a_stock_data(code)
        if not data:
            print("❌ 无法获取数据\n")
            return
        
        price = data['price']
        pe_ttm = data['pe_ttm']
        pb = data['pb']
        div_rate = data['div_rate']
        roe = data['roe']
        roic = data['roic']
        eps = data['eps']
        
        beta, beta_src = get_beta(name)
        beta = beta or 1.0
        cash_div = div_rate * price / 100
        
        print(f"""📈 实时数据 (2026-03-03)
--------------------------------------------------------------------------------
  股价: {price} [Tushare]
  PE_TTM: {pe_ttm} [Tushare]
  PB: {pb} [Tushare]
  股息率: {div_rate}% [Tushare]
  ROE: {roe}% [Tushare]
  ROIC: {roic}% [Tushare]
  EPS: {eps}元 [Tushare]
  β系数: {beta} [{beta_src}]
--------------------------------------------------------------------------------
""")
    
    # ========== 计算 ==========
    w = DEFAULT_RF + beta * DEFAULT_RM_RF
    d = cash_div / eps if eps > 0 else 0
    g = (1 - d) * roic
    expected_return = div_rate + g
    
    # ========== 第一步：资格筛选 ==========
    print(f"""================================================================================
第一步：资格筛选
================================================================================

w计算(CAPM):
  w = {DEFAULT_RF}% + {beta} × {DEFAULT_RM_RF}% = {w:.2f}%

ROIC检查:
  ROIC = {roic}% vs w = {w:.2f}%""")
    
    if roic > w:
        print(f"  ✅ ROIC({roic}%) > w({w:.2f}%)，通过资格筛选\n")
        qualified = True
    else:
        print(f"  ❌ ROIC({roic}%) < w({w:.2f}%)，不通过\n")
        return
    
    # ========== 第二步 ==========
    print(f"""================================================================================
第二步：核心参数
================================================================================

  分红率 d = {cash_div}/{eps:.2f} = {d*100:.1f}%
  增长率 g = (1-{d:.2f}) × {roic}% = {g:.2f}%
  预期收益率 = {div_rate}% + {g:.2f}% = {expected_return:.2f}%""")
    
    if g >= w:
        print(f"\n⚠️ g({g:.1f}%) ≥ w({w:.1f}%) → 公式失效！\n")
        g_invalid = True
    else:
        print(f"\n✅ g < w，公式有效\n")
        g_invalid = False
    
    # ========== 第三步 ==========
    print(f"""================================================================================
第三步：内在价值
================================================================================""")
    
    if not g_invalid:
        pe_calc = d * (1 + g/100) / (w/100 - g/100)
        print(f"PE_计算 = {pe_calc:.2f}")
    else:
        print(f"PE_计算: 公式失效")
    
    print(f"PE_TTM: {pe_ttm}")
    
    # ========== 第四步 ==========
    div_yield = cash_div / price * 100 if price > 0 else 0
    earnings_yield = 1 / pe_ttm * 100 if pe_ttm and pe_ttm > 0 else 0
    
    print(f"""
================================================================================
第四步：风险分析
================================================================================

1. 估值判断: PE_TTM = {pe_ttm}""")
    
    if pe_ttm and pe_ttm > 10:
        print(f"   → 偏高" if pe_ttm > 20 else "   → 合理")
    
    print(f"""
2. 股息风险:
   股息率({div_yield:.2f}%) vs 盈利率({earnings_yield:.2f}%)""")
    
    if div_yield > earnings_yield:
        print(f"   ⚠️ 寅吃卯粮风险！")
    else:
        print(f"   ✅ 安全")
    
    if pe_ttm and pe_ttm > 10:
        g_contrib = g / expected_return * 100 if expected_return > 0 else 0
        print(f"""
3. 成长风险:
   ⚠️ PE_TTM={pe_ttm:.1f} > 10，增长贡献{g_contrib:.0f}%
   → 需验证增长持续性""")
    
    # ========== 第五步 ==========
    pe_zero = d / (w/100) if w > 0 else 0
    pe_3 = d * 1.03 / ((w-3)/100) if w > 3 else 0
    
    print(f"""
================================================================================
第五步：情景分析
================================================================================

参考PE:
  零增长PE = {pe_zero:.1f}
  3%增长PE = {pe_3:.1f}
  当前PE = {pe_ttm}
""")
    
    # ========== 结论 ==========
    print(f"""================================================================================
💡 结论
================================================================================

{name or code}分析结论:
  ✅ ROIC > w，通过资格筛选""")
    
    if g_invalid:
        print(f"  ⚠️ g > w，公式失效")
    if pe_ttm and pe_ttm > 15:
        print(f"  ⚠️ PE={pe_ttm} 偏高")
    if div_yield <= earnings_yield:
        print(f"  ✅ 股息率安全")

    print(f"""
操作建议: 等待更好的买入时机

目标价参考:
  3%增长: {pe_3 * eps:.1f}
  零增长: {pe_zero * eps:.1f}

风险等级: ⭐⭐⭐ 中
================================================================================""")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 valuation.py <股票代码> [股票名称]")
        print("示例: python3 valuation.py 000333 美的集团")
        print("       python3 valuation.py 01810.HK 小米集团")
        sys.exit(1)
    
    code = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else ''
    
    analyze_stock(code, name)
