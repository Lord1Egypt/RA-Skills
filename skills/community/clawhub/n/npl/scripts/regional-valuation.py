#!/usr/bin/env python3
"""
不良资产区域估值速算工具

基于城市能级调节系数（CRF）的不良资产快速估值模型
适用于收购前快速评估、多城市资产包拆分估值

用法：
    python3 regional-valuation.py --fair-value 100000000 --bad-debt 80000000 --tier 一线
    python3 regional-valuation.py --batch --file assets.csv

作者：助手 · 2026-05-18
"""

import argparse
import sys

# ============================================================
# 城市能级参数表 (City Tier Parameters)
# ============================================================

CITY_TIER_PARAMS = {
    '一线': {
        'crf': 0.72,
        'discount': 0.35,    # 不良折扣率
        'irr_min': 12,
        'irr_max': 22,
        'cycle': 18,          # 月
        '折现率范围': '10-18%',
        'alpha_司法效率': 0.90,
        'beta_流动性': 0.85,
        'gamma_透明度': 0.90,
        'delta_投资者密度': 1.05,
        '代表城市': '北京/上海/深圳/广州',
        '回收率基准': 0.70,
    },
    '新一线': {
        'crf': 0.36,
        'discount': 0.25,
        'irr_min': 10,
        'irr_max': 18,
        'cycle': 24,
        '折现率范围': '14-22%',
        'alpha_司法效率': 0.75,
        'beta_流动性': 0.70,
        'gamma_透明度': 0.80,
        'delta_投资者密度': 0.85,
        '代表城市': '杭州/成都/武汉/南京/重庆/苏州',
        '回收率基准': 0.60,
    },
    '二线': {
        'crf': 0.18,
        'discount': 0.20,
        'irr_min': 8,
        'irr_max': 15,
        'cycle': 30,
        '折现率范围': '18-28%',
        'alpha_司法效率': 0.62,
        'beta_流动性': 0.58,
        'gamma_透明度': 0.68,
        'delta_投资者密度': 0.70,
        '代表城市': '济南/福州/合肥/长沙/南昌',
        '回收率基准': 0.50,
    },
    '三线': {
        'crf': 0.06,
        'discount': 0.15,
        'irr_min': 5,
        'irr_max': 12,
        'cycle': 42,
        '折现率范围': '22-35%',
        'alpha_司法效率': 0.48,
        'beta_流动性': 0.42,
        'gamma_透明度': 0.52,
        'delta_投资者密度': 0.50,
        '代表城市': '芜湖/洛阳/遵义/赣州/绵阳',
        '回收率基准': 0.35,
    },
    '四线': {
        'crf': 0.015,
        'discount': 0.10,
        'irr_min': 3,
        'irr_max': 8,
        'cycle': 54,
        '折现率范围': '28-45%',
        'alpha_司法效率': 0.30,
        'beta_流动性': 0.20,
        'gamma_透明度': 0.35,
        'delta_投资者密度': 0.25,
        '代表城市': '县级市及以下',
        '回收率基准': 0.22,
    },
}

# ============================================================
# 资产类型调节因子
# ============================================================

ASSET_TYPE_FACTORS = {
    '住宅':       1.20,   # 流动性强
    '商办':       1.00,   # 基准
    '工业用地':   0.70,   # 流动性一般
    '产业园':     0.65,   # 专业买家有限
    '商业综合':   0.80,   # 体大难处置
    '酒店':       0.50,   # 运营难度大
    '制造业贷款': 0.60,   # 行业关联风险
    '个贷':       0.55,   # 分散处置成本高
    '城投债':     0.40,   # 政策风险
    '股权':       0.35,   # 信息不对称最大
}

# ============================================================
# 核心估值函数
# ============================================================

def estimate_npl(fair_value, bad_debt, tier, asset_type='商办', verbose=True):
    """
    评估不良资产价值
    
    参数:
        fair_value: 公允价值（元）
        bad_debt: 不良本金（元）
        tier: 城市能级
        asset_type: 资产类型
        verbose: 是否详细输出
    
    返回:
        dict: 评估结果
    """
    p = CITY_TIER_PARAMS.get(tier)
    if p is None:
        raise ValueError(f"不支持的城市能级: {tier}，可选: {list(CITY_TIER_PARAMS.keys())}")
    
    af = ASSET_TYPE_FACTORS.get(asset_type, 1.0)
    
    # 1. 基础估值
    base_valuation = fair_value * p['discount']
    
    # 2. CRF调整
    adjusted = base_valuation * p['crf'] * af
    
    # 3. 建议收购价范围
    buy_low = adjusted * 0.6
    buy_high = adjusted * 1.0
    
    # 4. 预期回收
    recovery = adjusted / bad_debt * 100 if bad_debt > 0 else 0
    
    # 5. 预期回收金额
    recovery_amount = bad_debt * (p['回收率基准'] * af)
    recovery_amount = min(recovery_amount, fair_value * 0.9)  # 上限
    
    # 6. 处置净收益
    net_return = recovery_amount - buy_high
    net_return_rate = net_return / buy_high * 100 if buy_high > 0 else 0
    
    result = {
        '城市能级': tier,
        '资产类型': asset_type,
        '公允价值': f"{fair_value/10000:,.0f}万",
        '不良本金': f"{bad_debt/10000:,.0f}万",
        '资产调节因子': f"{af:.2f}",
        '基础折扣率': f"{p['discount']*100:.0f}%",
        'CRF综合系数': f"{p['crf']:.3f}",
        'CRF调整估值': f"{base_valuation/10000:,.0f}万(基准)→{adjusted/10000:,.0f}万(调整)",
        '建议收购价': f"{buy_low/10000:,.0f}万 ~ {buy_high/10000:,.0f}万",
        '预期回收金额': f"{recovery_amount/10000:,.0f}万",
        '预期本金回收率': f"{recovery:.1f}%",
        '预期净收益': f"{net_return/10000:,.0f}万",
        '预期净收益率': f"{net_return_rate:.1f}%",
        '预期处置周期': f"{p['cycle']}个月",
        '目标IRR范围': f"{p['irr_min']}-{p['irr_max']}%",
        '折现率参考': p['折现率范围'],
        '代表城市': p['代表城市'],
        'CRF分项': f"α(司法)={p['alpha_司法效率']:.2f} | β(流动)={p['beta_流动性']:.2f} | γ(透明)={p['gamma_透明度']:.2f} | δ(投资)={p['delta_投资者密度']:.2f}",
    }
    
    if verbose:
        _print_valuation(result, p)
    
    return result


def _print_valuation(result, p):
    """打印估值报告"""
    print("=" * 60)
    print(f"  不良资产区域估值报告")
    print(f"  城市能级: {result['城市能级']} ({result['代表城市']})")
    print(f"  资产类型: {result['资产类型']} (因子: {result['资产调节因子']})")
    print("=" * 60)
    print(f"  公允价值:          {result['公允价值']}")
    print(f"  不良本金:          {result['不良本金']}")
    print(f"  ─────────────────────────────────────────")
    print(f"  ① 基础折扣估值:    {result['公允价值']} × {result['基础折扣率']}")
    print(f"  ② CRF调整估值:     {result['CRF调整估值']}")
    print(f"  ③ 建议收购价:      {result['建议收购价']}")
    print(f"  ─────────────────────────────────────────")
    print(f"  预期回收金额:      {result['预期回收金额']}")
    print(f"  预期本金回收率:    {result['预期本金回收率']}")
    print(f"  预期净收益:        {result['预期净收益']}")
    print(f"  预期净收益率:      {result['预期净收益率']}")
    print(f"  ─────────────────────────────────────────")
    print(f"  预期处置周期:      {result['预期处置周期']}")
    print(f"  目标IRR范围:       {result['目标IRR范围']}")
    print(f"  折现率参考:        {result['折现率参考']}")
    print(f"  CRF分项:           {result['CRF分项']}")
    print("=" * 60)


def batch_estimate(assets_list):
    """批量资产包估值"""
    print("=" * 70)
    print(f"  跨区域资产包批量估值")
    print(f"  资产数量: {len(assets_list)}")
    print("=" * 70)
    
    total_buy = 0
    total_recovery = 0
    results = []
    
    for i, asset in enumerate(assets_list, 1):
        r = estimate_npl(
            asset['fair_value'],
            asset['bad_debt'],
            asset['tier'],
            asset.get('asset_type', '商办'),
            verbose=False
        )
        results.append(r)
        
        # Parse numbers back
        buy_str = r['建议收购价']
        buy_high_str = buy_str.split('~')[1].strip().replace('万', '')
        recovery_str = r['预期回收金额'].replace('万', '')
        
        buy_val = float(buy_high_str) * 10000
        rec_val = float(recovery_str) * 10000
        total_buy += buy_val
        total_recovery += rec_val
        
        print(f"\n  资产{i}: {r['城市能级']} {r['资产类型']} | "
              f"本金{r['不良本金']} | 收购价{r['建议收购价']} | "
              f"回收{r['预期回收金额']} | 回收率{r['预期本金回收率']}")
    
    print("\n" + "=" * 70)
    print(f"  资产包合计:")
    print(f"  总收购成本:      {total_buy/10000:,.0f}万")
    print(f"  预期总回收:      {total_recovery/10000:,.0f}万")
    print(f"  预期总净收益:    {(total_recovery-total_buy)/10000:,.0f}万")
    print(f"  综合回收率:      {total_recovery/total_buy*100:.1f}%")
    
    if total_buy > 0:
        years = 2.0  # 假设平均处置周期2年
        irr = ((total_recovery / total_buy) ** (1/years) - 1) * 100
        print(f"  年化IRR(估算):   {irr:.1f}%")
    
    print("=" * 70)
    return results


# ============================================================
# 对比分析
# ============================================================

def compare_tiers(fair_value, bad_debt, asset_type='商办'):
    """对比同一资产在不同城市能级的估值差异"""
    print("=" * 65)
    print(f"  城市能级对比分析")
    print(f"  公允价值: {fair_value/10000:,.0f}万 | 不良本金: {bad_debt/10000:,.0f}万 | 资产类型: {asset_type}")
    print("=" * 65)
    print(f"  {'能级':<6} {'CRF':<6} {'调整估值':<10} {'建议收购价':<14} {'预期回收':<10} {'净收益':<10} {'IRR':<8} {'周期':<6}")
    print(f"  {'─'*5} {'─'*5} {'─'*8} {'─'*12} {'─'*8} {'─'*8} {'─'*6} {'─'*5}")
    
    for tier in ['一线', '新一线', '二线', '三线', '四线']:
        r = estimate_npl(fair_value, bad_debt, tier, asset_type, verbose=False)
        buy_str = r['建议收购价']  # e.g., "2,520万 ~ 4,200万"
        buy_high_str = buy_str.split('~')[1].strip().replace('万', '').replace(',', '')
        rec_str = r['预期回收金额'].replace('万', '').replace(',', '')
        
        try:
            buy_mid = float(buy_high_str) * 10000
            rec = float(rec_str) * 10000
            net = rec - buy_mid
        except ValueError:
            buy_mid = 0
            rec = 0
            net = 0
        
        p = CITY_TIER_PARAMS[tier]
        adj_parts = r['CRF调整估值'].split('→')
        adj_str = adj_parts[-1].strip() if len(adj_parts) > 1 else adj_parts[0]
        
        print(f"  {tier:<6} {p['crf']:<6.3f} {adj_str:<10} "
              f"{r['建议收购价']:<14} {r['预期回收金额']:<10} "
              f"{net/10000:,.0f}万{' ':<4} {p['irr_min']}-{p['irr_max']}%{' ':<3} {p['cycle']}月")
    
    print("=" * 65)


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='不良资产区域估值速算工具')
    parser.add_argument('--fair-value', type=float, help='公允价值（元）')
    parser.add_argument('--bad-debt', type=float, help='不良本金（元）')
    parser.add_argument('--tier', type=str, help='城市能级（一线/新一线/二线/三线/四线）')
    parser.add_argument('--asset-type', type=str, default='商办', help='资产类型')
    parser.add_argument('--compare', action='store_true', help='对比各城市能级差异')
    parser.add_argument('--batch', action='store_true', help='批量模式（暂未支持JSON输入）')
    
    args = parser.parse_args()
    
    if args.compare and args.fair_value and args.bad_debt:
        compare_tiers(args.fair_value, args.bad_debt, args.asset_type or '商办')
    elif args.fair_value and args.bad_debt and args.tier:
        estimate_npl(args.fair_value, args.bad_debt, args.tier, args.asset_type or '商办')
    else:
        # 示例模式
        print("=" * 60)
        print("  不良资产区域估值速算工具 v1.0")
        print("  作者: 助手 @ 使用方团队")
        print("=" * 60)
        print("\n📋 使用示例:")
        print("  python3 regional-valuation.py --fair-value 100000000 --bad-debt 80000000 --tier 一线")
        print("  python3 regional-valuation.py --fair-value 50000000 --bad-debt 30000000 --tier 成都  --compare")
        print("\n📊 演示: 同一1亿物业在不同城市的估值对比\n")
        compare_tiers(100_000_000, 80_000_000, '商办')


if __name__ == '__main__':
    main()
