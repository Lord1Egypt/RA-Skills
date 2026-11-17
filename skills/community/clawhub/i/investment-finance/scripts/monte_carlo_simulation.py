#!/usr/bin/env python3
"""
Monte Carlo 模拟 - 产业项目投资回报概率分析
🐴 本工具为用户开发，2026年5月

功能：
1. 多变量概率分布模拟（营收增长/毛利率/Capex/WACC/退出倍数）
2. 10,000次模拟迭代
3. 输出IRR/MOIC概率分布
4. 计算P(IRR > 门槛)的成功概率
5. 生成敏感性分析排名

用法：python3 monte_carlo_simulation.py
"""

import numpy as np
import pandas as pd
import json
import os
from datetime import datetime

class MonteCarloProjectSimulator:
    """
    产业项目Monte Carlo模拟器
    支持正态分布/三角分布/均匀分布
    """
    
    def __init__(self, project_name="未命名项目"):
        self.project_name = project_name
        self.simulation_results = {}
        
    def revenue_model(self, base_revenue, growth_rate_annual, years=5):
        """
        营收模型
        base_revenue: 初始营收（万元）
        growth_rate_annual: 年增长率
        years: 预测年数
        """
        revenues = [base_revenue]
        for y in range(1, years + 1):
            revenues.append(revenues[-1] * (1 + growth_rate_annual))
        return revenues
    
    def three_statement_model(self, revenues, gross_margin, opex_rate, 
                               capex_pct, tax_rate, depreciation_rate=0.05,
                               debt_ratio=0.3, interest_rate=0.05,
                               exit_ebitda_multiple=12):
        """
        简化的三表联动模型
        返回: 净利润表、自由现金流、关键财务指标
        """
        years = len(revenues) - 1  # Year 0 是基期
        results = []
        
        initial_investment = revenues[0] * 2  # 初始投资假设为2倍营收
        cum_debt = initial_investment * debt_ratio
        cum_equity = initial_investment * (1 - debt_ratio) if (1 - debt_ratio) > 0 else initial_investment * 0.7
        fixed_assets = initial_investment * 0.6
        
        for y in range(1, years + 1):
            rev = revenues[y]
            
            # P&L
            cogs = rev * (1 - gross_margin)
            gross_profit = rev - cogs
            opex = rev * opex_rate
            depreciation = fixed_assets * depreciation_rate
            ebit = gross_profit - opex - depreciation
            interest = cum_debt * interest_rate
            ebt = ebit - interest
            tax = max(ebt * tax_rate, 0)
            net_income = ebt - tax
            
            # BS更新
            fixed_assets = fixed_assets - depreciation + (rev * capex_pct)
            cum_debt = cum_debt * (1 - 0.10 * min(y, 8))  # 递减还债
            
            # CF
            fcfe = net_income + depreciation - (rev * capex_pct)
            
            results.append({
                'year': y,
                'revenue': rev,
                'gross_profit': gross_profit,
                'ebit': ebit,
                'net_income': net_income,
                'free_cash_flow': fcfe,
                'fixed_assets': fixed_assets,
                'total_debt': cum_debt,
                'ebitda': ebit + depreciation
            })
        
        # 退出时股权价值 = 退出EBITDA × 退出倍数 - 剩余债务
        final_ebitda = results[-1]['ebitda']
        exit_enterprise_value = final_ebitda * exit_ebitda_multiple
        final_debt = results[-1]['total_debt']
        exit_equity_value = max(exit_enterprise_value - final_debt, 0)
        
        for r in results:
            r['exit_equity_value'] = exit_equity_value
        
        return results, initial_investment
    
    def calculate_irr(self, cash_flows, initial_inv):
        """
        计算IRR（含退出价值的完整现金流）
        产业项目IRR = 持有期现金流 + 最终退出回收
        """
        # 构建完整现金流序列：Year 0投入 → 每年运营现金流 → Year N退出回收
        all_cash_flows = [-initial_inv]
        for cf in cash_flows:
            all_cash_flows.append(cf['free_cash_flow'])
        # 最后一年加上退出回收（股权价值）
        final_equity = cash_flows[-1]['exit_equity_value']
        all_cash_flows[-1] += final_equity
        
        # numpy >= 2.0 移除了 np.irr，直接使用手动Newton法
        return self._manual_irr(all_cash_flows, initial_inv)
    
    def _manual_irr(self, cash_flows, initial_inv, guess=0.20):
        """手动计算IRR（Newton法）"""
        rate = guess
        max_iter = 1000
        tol = 1e-7
        
        for _ in range(max_iter):
            npv = 0.0
            dnpv = 0.0
            for i, cf in enumerate(cash_flows):
                try:
                    denom = (1 + rate) ** i
                    npv += cf / denom
                    dnpv += -i * cf / (1 + rate) ** (i + 1)
                except (OverflowError, ZeroDivisionError):
                    return -0.50
            
            if abs(dnpv) < 1e-12:
                break
            rate_new = rate - npv / dnpv
            
            if abs(rate_new - rate) < tol:
                break
            rate = rate_new
            
            if rate < -0.999 or rate > 10.0:  # 超出合理范围
                return -0.50
        
        # 验证npv接近0
        final_npv = 0.0
        for i, cf in enumerate(cash_flows):
            try:
                final_npv += cf / (1 + rate) ** i
            except:
                return -0.50
        
        if abs(final_npv) > initial_inv * 0.2:  # NPV偏离太大（放宽到20%）
            return -0.50
        
        return min(max(rate, -0.99), 5.0)  # -99% 到 500% 之间
    
    def calculate_moic(self, final_equity_value, initial_investment):
        """计算MOIC"""
        return final_equity_value / initial_investment if initial_investment > 0 else 0
    
    def setup_variable_distributions(self):
        """
        设置变量概率分布
        返回: 变量列表，每个变量包含: name, distribution_type, params
        """
        self.variables = {
            'revenue_growth': {
                'name': '营收增长率',
                'distribution': 'triangular',
                'params': {'low': -0.10, 'mode': 0.15, 'high': 0.40},
                'description': '年营收增长率'
            },
            'gross_margin': {
                'name': '毛利率',
                'distribution': 'triangular',
                'params': {'low': 0.15, 'mode': 0.35, 'high': 0.55},
                'description': '毛利率水平'
            },
            'opex_rate': {
                'name': '运营费用率',
                'distribution': 'triangular',
                'params': {'low': 0.10, 'mode': 0.20, 'high': 0.35},
                'description': '运营费用占营收比例'
            },
            'exit_multiple': {
                'name': '退出倍数',
                'distribution': 'normal',
                'params': {'mean': 12.0, 'std': 3.0},
                'description': '退出时EBITDA倍数'
            },
            'wacc': {
                'name': '折现率(WACC)',
                'distribution': 'normal',
                'params': {'mean': 0.10, 'std': 0.02},
                'description': '加权平均资本成本'
            }
        }
        return self
    
    def _sample_from_distribution(self, var_name):
        """从概率分布中采样一个值"""
        var = self.variables[var_name]
        dist = var['distribution']
        params = var['params']
        
        if dist == 'normal':
            return max(0.01, np.random.normal(params['mean'], params['std']))
        elif dist == 'triangular':
            return np.random.triangular(params['low'], params['mode'], params['high'])
        elif dist == 'uniform':
            return np.random.uniform(params['low'], params['high'])
        else:
            return params.get('mode', 0.15)
    
    def run_simulation(self, num_iterations=10000, initial_revenue=10000, 
                       exit_ebitda_multiple=12, irr_threshold=0.20):
        """
        运行Monte Carlo模拟
        num_iterations: 模拟次数（默认10,000次）
        initial_revenue: 初始营收（万元）
        exit_ebitda_multiple: 退出时EBITDA倍数
        irr_threshold: IRR门槛（默认20%）
        """
        print(f"🐴 开始 Monte Carlo 模拟: {self.project_name}")
        print(f"   总模拟次数: {num_iterations:,}")
        print(f"   初始营收: {initial_revenue:,} 万元")
        print(f"   IRR 门槛: {irr_threshold*100:.0f}%")
        print(f"{'='*60}")
        
        results = []
        
        for i in range(num_iterations):
            # 从每个变量分布中采样一个值
            growth_rate = self._sample_from_distribution('revenue_growth')
            gross_margin = self._sample_from_distribution('gross_margin')
            opex_rate = self._sample_from_distribution('opex_rate')
            exit_multiple = self._sample_from_distribution('exit_multiple')
            wacc = self._sample_from_distribution('wacc')
            
            # 营收预测
            revenues = self.revenue_model(initial_revenue, growth_rate)
            
            # 三表模型
            cash_flows, initial_equity = self.three_statement_model(
                revenues=revenues,
                gross_margin=gross_margin,
                opex_rate=opex_rate,
                capex_pct=0.05,
                tax_rate=0.25,
                exit_ebitda_multiple=exit_multiple
            )
            
            # IRR计算（含退出价值，在calculate_irr内处理）
            irr = self.calculate_irr(cash_flows, initial_equity)
            
            # MOIC计算
            final_equity = cash_flows[-1]['exit_equity_value']
            moic = self.calculate_moic(final_equity, initial_equity)
            
            results.append({
                'irr': irr,
                'moic': moic,
                'growth_rate': growth_rate,
                'gross_margin': gross_margin,
                'opex_rate': opex_rate,
                'exit_multiple': exit_multiple,
                'exit_value': final_equity,
                'initial_equity': initial_equity
            })
        
        df = pd.DataFrame(results)
        
        # 统计分析
        irr_values = df['irr'].values
        moic_values = df['moic'].values
        
        success_prob = np.mean(irr_values > irr_threshold)
        
        self.simulation_results = {
            'iterations': num_iterations,
            'irr_threshold': irr_threshold,
            'irr': {
                'mean': float(np.mean(irr_values)),
                'median': float(np.median(irr_values)),
                'p10': float(np.percentile(irr_values, 10)),
                'p25': float(np.percentile(irr_values, 25)),
                'p75': float(np.percentile(irr_values, 75)),
                'p90': float(np.percentile(irr_values, 90)),
                'std': float(np.std(irr_values)),
                'min': float(np.min(irr_values)),
                'max': float(np.max(irr_values))
            },
            'moic': {
                'mean': float(np.mean(moic_values)),
                'median': float(np.median(moic_values)),
                'p10': float(np.percentile(moic_values, 10)),
                'p90': float(np.percentile(moic_values, 90))
            },
            'success_probability': float(success_prob),
            'mean_growth_rate': float(np.mean(df['growth_rate'])),
            'mean_gross_margin': float(np.mean(df['gross_margin']))
        }
        
        # 敏感性分析：计算每个变量与IRR的相关系数
        correlations = {}
        for var in ['growth_rate', 'gross_margin', 'opex_rate', 'exit_multiple']:
            # 过滤掉IRR为 -50%（手动计算失败）或 -99% 的数据
            valid_mask = (df['irr'] > -0.50) & (df['irr'] < 2.0)
            valid_df = df[valid_mask]
            if len(valid_df) > 100:  # 至少100个有效数据点
                corr = float(valid_df[var].corr(valid_df['irr']))
                correlations[var] = corr if not np.isnan(corr) else 0.0
            else:
                correlations[var] = 0.0
        
        self.simulation_results['sensitivity'] = dict(
            sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
        )
        
        self.df = df
        return self
    
    def print_summary(self):
        """打印模拟结果摘要"""
        import locale
        r = self.simulation_results
        
        print(f"\n{'='*60}")
        print(f"📊 Monte Carlo 模拟结果: {self.project_name}")
        print(f"{'='*60}")
        print(f"模拟次数: {r['iterations']:,}")
        print(f"IRR门槛:  {r['irr_threshold']*100:.0f}%")
        print(f"\n--- IRR 分布 ---")
        print(f"  均值:     {r['irr']['mean']*100:.1f}%")
        print(f"  中位数:   {r['irr']['median']*100:.1f}%")
        print(f"  标准差:   {r['irr']['std']*100:.1f}%")
        print(f"  P10:      {r['irr']['p10']*100:.1f}%")
        print(f"  P25:      {r['irr']['p25']*100:.1f}%")
        print(f"  P75:      {r['irr']['p75']*100:.1f}%")
        print(f"  P90:      {r['irr']['p90']*100:.1f}%")
        print(f"  最小值:   {r['irr']['min']*100:.1f}%")
        print(f"  最大值:   {r['irr']['max']*100:.1f}%")
        print(f"\n--- MOIC 分布 ---")
        print(f"  均值:     {r['moic']['mean']:.2f}x")
        print(f"  中位数:   {r['moic']['median']:.2f}x")
        print(f"  P10:      {r['moic']['p10']:.2f}x")
        print(f"  P90:      {r['moic']['p90']:.2f}x")
        print(f"\n--- 关键指标 ---")
        print(f"  P(IRR > {r['irr_threshold']*100:.0f}%): {r['success_probability']*100:.1f}%")
        print(f"  均值营收增长率: {r['mean_growth_rate']*100:.1f}%")
        print(f"  均值毛利率:     {r['mean_gross_margin']*100:.1f}%")
        print(f"\n--- 敏感性分析（变量对IRR影响排名）---")
        for var, corr in r['sensitivity'].items():
            bar = "█" * int(abs(corr) * 20)
            print(f"  {var:20s} {bar} {corr:+.3f}")
        print(f"{'='*60}\n")
        
        # 结论
        if r['success_probability'] >= 0.70:
            rating = "⭐⭐⭐⭐⭐ 优秀 - 确定性高，强烈推荐"
        elif r['success_probability'] >= 0.50:
            rating = "⭐⭐⭐⭐ 良好 - 有一定确定性，推荐"
        elif r['success_probability'] >= 0.30:
            rating = "⭐⭐⭐ 一般 - 不确定性高，需深度尽调"
        elif r['success_probability'] >= 0.15:
            rating = "⭐⭐ 谨慎 - 风险较高"
        else:
            rating = "⭐ 不推荐 - 风险极高"
        print(f"项目评级: {rating}")
        print()
        
        return self
    
    def save_to_excel(self, filename=None):
        """保存为Excel"""
        if filename is None:
            filename = f").strftime('%Y%m%d')}.xlsx"
        filename = os.path.expanduser(filename)
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # 原始模拟数据（抽样1000条）
            sample_df = self.df.sample(min(1000, len(self.df)))
            sample_df.to_excel(writer, sheet_name='Simulation_Data', index=False)
            
            # 统计汇总
            summary = pd.DataFrame([self.simulation_results])
            summary.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"✓ 模拟数据已保存到: {filename}")
        return self


# ========== 使用示例 ==========
if __name__ == "__main__":
    print("🐴 Monte Carlo 模拟 - 产业项目投资回报概率分析")
    print("="*60)
    
    simulator = MonteCarloProjectSimulator("示例: 新能源电池回收项目")
    
    # 设置变量分布
    simulator.setup_variable_distributions()
    
    # 可以自定义每个变量的分布
    simulator.variables['revenue_growth'] = {
        'name': '营收增长率',
        'distribution': 'triangular',
        'params': {'low': 0.05, 'mode': 0.20, 'high': 0.50},
        'description': '考虑到新能源赛道高增长'
    }
    simulator.variables['gross_margin'] = {
        'name': '毛利率',
        'distribution': 'triangular',
        'params': {'low': 0.18, 'mode': 0.30, 'high': 0.45},
        'description': '回收行业毛利率区间'
    }
    simulator.variables['exit_multiple'] = {
        'name': '退出倍数',
        'distribution': 'normal',
        'params': {'mean': 10.0, 'std': 2.5},
        'description': '新能源行业退出倍数'
    }
    
    # 运行模拟（10,000次）
    simulator.run_simulation(
        num_iterations=10000,
        initial_revenue=5000,  # 初始营收5000万
        irr_threshold=0.20     # IRR门槛20%
    )
    
    # 打印结果
    simulator.print_summary()
    simulator.save_to_excel()
