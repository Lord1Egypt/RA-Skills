#!/usr/bin/env python3
"""
Dechow F-Score 实现（应计质量模型）
补充 Beneish M-Score 的不足
"""

import json
from typing import Dict

def safe_divide(a, b, default=0):
    """安全除法"""
    try:
        if b == 0 or b is None or a is None:
            return default
        return float(a) / float(b)
    except:
        return default

def calculate_dechow_fscore(data_curr: Dict, data_prev: Dict) -> Dict:
    """
    计算 Dechow F-Score
    
    F-Score = -4.255 + 1.191*RSST_Accruals + 0.057*ΔCash_Sales 
              + 0.691*ΔReceivables + 0.179*ΔInventory + 0.124*%Soft_Assets 
              + 0.303*ΔCash_Margin + 0.116*ΔROE
    
    简化版（基于可用数据）:
    F-Score ≈ -4.255 + 1.191*Accruals + 0.691*ΔAR + 0.179*ΔInv
    """
    
    # 提取数据
    revenue_t = data_curr.get('revenue', 0)
    revenue_t1 = data_prev.get('revenue', 0)
    
    ar_t = data_curr.get('accounts_receivable', 0)
    ar_t1 = data_prev.get('accounts_receivable', 0)
    
    inv_t = data_curr.get('inventory', 0)
    inv_t1 = data_prev.get('inventory', 0)
    
    ta_t = data_curr.get('total_assets', 0)
    ta_t1 = data_prev.get('total_assets', 0)
    
    ni_t = data_curr.get('net_profit', 0)
    cfo_t = data_curr.get('operating_cash_flow', 0)
    
    equity_t = data_curr.get('total_equity', 0)
    equity_t1 = data_prev.get('total_equity', 0)
    
    # 1. RSST Accruals (Richardson et al. 2005)
    # Accruals = (NI - CFO) / Average_TA
    avg_ta = (ta_t + ta_t1) / 2
    rsst_accruals = safe_divide(ni_t - cfo_t, avg_ta)
    
    # 2. ΔCash_Sales (变化率)
    # 简化：用营收增长率代替
    delta_cash_sales = safe_divide(revenue_t - revenue_t1, revenue_t1)
    
    # 3. ΔReceivables (应收账款变化率)
    delta_receivables = safe_divide(ar_t - ar_t1, ta_t1)
    
    # 4. ΔInventory (存货变化率)
    delta_inventory = safe_divide(inv_t - inv_t1, ta_t1)
    
    # 5. %Soft_Assets (软资产占比)
    # 软资产 = 总资产 - 现金 - 固定资产
    # 简化：无法准确计算，使用估计值
    soft_assets_pct = 0.3  # 估计值
    
    # 6. ΔCash_Margin (现金毛利率变化)
    cash_margin_t = safe_divide(cfo_t, revenue_t)
    cash_margin_t1 = safe_divide(data_prev.get('operating_cash_flow', 0), revenue_t1)
    delta_cash_margin = cash_margin_t - cash_margin_t1
    
    # 7. ΔROE (ROE变化)
    roe_t = safe_divide(ni_t, equity_t)
    roe_t1 = safe_divide(data_prev.get('net_profit', 0), equity_t1)
    delta_roe = roe_t - roe_t1
    
    # 计算 F-Score（简化版）
    f_score = (-4.255 + 
               1.191 * rsst_accruals + 
               0.057 * delta_cash_sales + 
               0.691 * delta_receivables + 
               0.179 * delta_inventory + 
               0.124 * soft_assets_pct + 
               0.303 * delta_cash_margin + 
               0.116 * delta_roe)
    
    return {
        'f_score': f_score,
        'rsst_accruals': rsst_accruals,
        'delta_cash_sales': delta_cash_sales,
        'delta_receivables': delta_receivables,
        'delta_inventory': delta_inventory,
        'soft_assets_pct': soft_assets_pct,
        'delta_cash_margin': delta_cash_margin,
        'delta_roe': delta_roe,
        'roe_t': roe_t * 100,
        'roe_t1': roe_t1 * 100,
    }

def analyze_company(code: str, company_data: Dict) -> None:
    """分析单个公司"""
    print(f"\n{'='*60}")
    print(f"{company_data['name']} ({code})")
    print(f"{'='*60}")
    
    years = sorted(company_data['data'].keys())
    
    for i in range(1, len(years)):
        year_prev = years[i-1]
        year_curr = years[i]
        
        data_prev = company_data['data'][year_prev]
        data_curr = company_data['data'][year_curr]
        
        result = calculate_dechow_fscore(data_curr, data_prev)
        
        print(f"\n{year_prev} -> {year_curr}:")
        print(f"  F-Score: {result['f_score']:.3f} {'[HIGH RISK]' if result['f_score'] > 1.0 else '[LOW RISK]'}")
        print(f"  RSST Accruals: {result['rsst_accruals']:.3f}")
        print(f"  ΔCash Sales: {result['delta_cash_sales']:.3f}")
        print(f"  ΔReceivables: {result['delta_receivables']:.3f}")
        print(f"  ΔInventory: {result['delta_inventory']:.3f}")
        print(f"  ΔCash Margin: {result['delta_cash_margin']:.3f}")
        print(f"  ΔROE: {result['delta_roe']:.3f}")
        print(f"  ROE: {result['roe_t1']:.1f}% -> {result['roe_t']:.1f}%")

def main():
    """主函数"""
    # 读取数据
    with open('eastmoney_semiconductor_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("="*60)
    print("Dechow F-Score 分析（应计质量模型）")
    print("="*60)
    print("\n注意:")
    print("  - F-Score > 1.0: 高应计质量风险")
    print("  - F-Score <= 1.0: 应计质量可接受")
    print("  - 补充 Beneish M-Score 的不足")
    
    for code, company_data in data.items():
        analyze_company(code, company_data)
    
    # 2024年汇总
    print(f"\n{'='*60}")
    print("2024年 F-Score 排名")
    print(f"{'='*60}")
    
    summary = []
    for code, company_data in data.items():
        if '2024' in company_data['data'] and '2023' in company_data['data']:
            result = calculate_dechow_fscore(
                company_data['data']['2024'],
                company_data['data']['2023']
            )
            summary.append({
                'code': code,
                'name': company_data['name'],
                'f_score': result['f_score'],
                'rsst_accruals': result['rsst_accruals'],
            })
    
    summary.sort(key=lambda x: x['f_score'])
    
    print(f"\n{'公司':<12} {'F-Score':<10} {'Accruals':<10} {'风险评级'}")
    print("-" * 50)
    for item in summary:
        risk = "[HIGH RISK]" if item['f_score'] > 1.0 else "[LOW RISK]"
        print(f"{item['name']:<10} {item['f_score']:<10.3f} {item['rsst_accruals']:<10.3f} {risk}")

if __name__ == "__main__":
    main()
