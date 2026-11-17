#!/usr/bin/env python3
"""
产业项目投资敏感性与情景分析工具
🐴 本工具为用户开发，2026年5月

功能：
1. 单变量敏感性分析（Tornado Chart数据）
2. 双变量敏感性矩阵（Heat Map数据）
3. 三情景分析（Base/Bull/Bear）
4. 盈亏平衡点计算
5. 输出可读的关键发现

用法：python3 sensitivity_analysis.py
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

class SensitivityAnalysis:
    """
    敏感性分析与情景构建工具
    """
    
    def __init__(self, project_name="未命名项目"):
        self.project_name = project_name
        self.base_case = {}
        self.variables = {}
        self.results = {}
        
    def setup_base_case(self, revenue, ebitda_margin, exit_multiple, 
                         initial_investment, holding_years=5, wacc=0.10):
        """
        设置Base Case参数
        """
        self.base_case = {
            'revenue': revenue,
            'ebitda_margin': ebitda_margin,
            'ebitda': revenue * ebitda_margin,
            'exit_multiple': exit_multiple,
            'exit_value': revenue * ebitda_margin * exit_multiple,
            'initial_investment': initial_investment,
            'holding_years': holding_years,
            'wacc': wacc
        }
        
        # 计算基准IRR和MOIC
        exit_val = self.base_case['exit_value']
        inv = self.base_case['initial_investment']
        self.base_case['moic'] = exit_val / inv if inv > 0 else 0
        self.base_case['irr'] = (exit_val / inv) ** (1 / holding_years) - 1 if holding_years > 0 and inv > 0 else 0
        
        return self
    
    def add_variable(self, name, base_value, low_pct, high_pct, display_name=None):
        """
        添加一个敏感性分析变量
        name: 变量名
        base_value: 基准值
        low_pct: 下降百分比（如 0.20 = -20%）
        high_pct: 上升百分比（如 0.20 = +20%）
        display_name: 显示名称
        """
        self.variables[name] = {
            'base_value': base_value,
            'low_value': base_value * (1 - low_pct),
            'high_value': base_value * (1 + high_pct),
            'low_pct': low_pct,
            'high_pct': high_pct,
            'display_name': display_name or name
        }
        return self
    
    def _calculate_irr(self, revenue, ebitda_margin, exit_multiple, 
                        initial_investment, holding_years):
        """内部IRR计算"""
        ebitda = revenue * ebitda_margin
        exit_value = ebitda * exit_multiple
        moic = exit_value / initial_investment if initial_investment > 0 else 0
        irr = moic ** (1 / holding_years) - 1 if holding_years > 0 and initial_investment > 0 else -0.99
        return irr, moic
    
    def run_single_variable_analysis(self):
        """
        运行单变量敏感性分析
        输出 Tornado Chart 数据
        """
        bc = self.base_case
        base_irr = bc['irr']
        
        tornado_data = {}
        
        for var_name, var_data in self.variables.items():
            # 低值情景
            if var_name == 'revenue':
                low_irr, low_moic = self._calculate_irr(
                    var_data['low_value'], bc['ebitda_margin'], bc['exit_multiple'],
                    bc['initial_investment'], bc['holding_years'])
                high_irr, high_moic = self._calculate_irr(
                    var_data['high_value'], bc['ebitda_margin'], bc['exit_multiple'],
                    bc['initial_investment'], bc['holding_years'])
            elif var_name == 'ebitda_margin':
                low_irr, low_moic = self._calculate_irr(
                    bc['revenue'], var_data['low_value'], bc['exit_multiple'],
                    bc['initial_investment'], bc['holding_years'])
                high_irr, high_moic = self._calculate_irr(
                    bc['revenue'], var_data['high_value'], bc['exit_multiple'],
                    bc['initial_investment'], bc['holding_years'])
            elif var_name == 'exit_multiple':
                low_irr, low_moic = self._calculate_irr(
                    bc['revenue'], bc['ebitda_margin'], var_data['low_value'],
                    bc['initial_investment'], bc['holding_years'])
                high_irr, high_moic = self._calculate_irr(
                    bc['revenue'], bc['ebitda_margin'], var_data['high_value'],
                    bc['initial_investment'], bc['holding_years'])
            elif var_name == 'initial_investment':
                low_irr, low_moic = self._calculate_irr(
                    bc['revenue'], bc['ebitda_margin'], bc['exit_multiple'],
                    var_data['high_value'], bc['holding_years'])  # 投资多=IRR低
                high_irr, high_moic = self._calculate_irr(
                    bc['revenue'], bc['ebitda_margin'], bc['exit_multiple'],
                    var_data['low_value'], bc['holding_years'])  # 投资少=IRR高
            elif var_name == 'holding_years':
                low_irr, low_moic = self._calculate_irr(
                    bc['revenue'], bc['ebitda_margin'], bc['exit_multiple'],
                    bc['initial_investment'], int(var_data['low_value']))
                high_irr, high_moic = self._calculate_irr(
                    bc['revenue'], bc['ebitda_margin'], bc['exit_multiple'],
                    bc['initial_investment'], int(var_data['high_value']))
            else:
                continue
            
            # 入参变化范围
            pct_range = var_data['low_pct'] + var_data['high_pct']
            irr_impact_low = low_irr - base_irr
            irr_impact_high = high_irr - base_irr
            total_irr_swing = abs(irr_impact_low) + abs(irr_impact_high)
            
            tornado_data[var_name] = {
                'display_name': var_data['display_name'],
                'base_value': var_data['base_value'],
                'low_value': var_data['low_value'],
                'high_value': var_data['high_value'],
                'low_irr': low_irr,
                'high_irr': high_irr,
                'irr_impact_low': irr_impact_low,
                'irr_impact_high': irr_impact_high,
                'total_irr_swing': total_irr_swing,
                'low_moic': low_moic,
                'high_moic': high_moic
            }
        
        # 按影响程度排序
        self.tornado_data = dict(
            sorted(tornado_data.items(), key=lambda x: x[1]['total_irr_swing'], reverse=True)
        )
        
        return self
    
    def run_dual_variable_matrix(self, var_x_name='revenue', var_y_name='ebitda_margin'):
        """
        运行双变量敏感性矩阵（Heat Map数据）
        """
        bc = self.base_case
        var_x = self.variables[var_x_name]
        var_y = self.variables[var_y_name]
        
        # 生成5x5矩阵
        x_values = np.linspace(var_x['low_value'], var_x['high_value'], 5)
        y_values = np.linspace(var_y['low_value'], var_y['high_value'], 5)
        
        matrix = []
        for y_val in y_values:
            row = []
            for x_val in x_values:
                if var_x_name == 'revenue' and var_y_name == 'ebitda_margin':
                    irr, moic = self._calculate_irr(
                        x_val, y_val, bc['exit_multiple'],
                        bc['initial_investment'], bc['holding_years'])
                else:
                    irr, moic = 0, 0
                row.append({
                    'irr': irr,
                    'moic': moic
                })
            matrix.append({
                'y_value': y_val,
                'row': row
            })
        
        self.heatmap_data = {
            'var_x': var_x_name,
            'var_y': var_y_name,
            'x_values': x_values.tolist(),
            'y_values': y_values.tolist(),
            'matrix': matrix,
            'threshold': 0.20  # IRR 20%门槛
        }
        
        return self
    
    def run_scenario_analysis(self):
        """
        运行三情景分析（Base/Bull/Bear）
        """
        bc = self.base_case
        
        # Base Case（已设定）
        base_irr, base_moic = bc['irr'], bc['moic']
        
        # Bull Case（乐观 - 所有有利因素同时发生）
        bull_multiple = bc['exit_multiple'] * 1.30
        bull_margin = bc['ebitda_margin'] * 1.25
        bull_revenue = bc['revenue'] * 1.20
        bull_ebitda = bull_revenue * bull_margin
        bull_exit = bull_ebitda * bull_multiple
        bull_irr = (bull_exit / bc['initial_investment']) ** (1 / bc['holding_years']) - 1
        bull_moic = bull_exit / bc['initial_investment']
        
        # Bear Case（悲观 - 所有不利因素同时发生）
        bear_multiple = bc['exit_multiple'] * 0.70
        bear_margin = bc['ebitda_margin'] * 0.75
        bear_revenue = bc['revenue'] * 0.80
        bear_ebitda = bear_revenue * bear_margin
        bear_exit = bear_ebitda * bear_multiple
        bear_irr = (bear_exit / bc['initial_investment']) ** (1 / bc['holding_years']) - 1 if bear_exit > 0 else -0.50
        bear_moic = bear_exit / bc['initial_investment']
        
        self.scenarios = {
            'bull': {
                'name': 'Bull Case（乐观）',
                'weight': 0.225,
                'assumptions': {
                    '营收增长率提升': '+20%',
                    'EBITDA Margin提升': '+25%',
                    '退出倍数提升': '+30%',
                },
                'results': {
                    'exit_value': bull_exit,
                    'irr': bull_irr,
                    'moic': bull_moic
                }
            },
            'base': {
                'name': 'Base Case（基准）',
                'weight': 0.55,
                'assumptions': {
                    '营收': f'¥{bc["revenue"]:,.0f}万',
                    'EBITDA Margin': f'{bc["ebitda_margin"]*100:.1f}%',
                    '退出倍数': f'{bc["exit_multiple"]:.0f}x',
                },
                'results': {
                    'exit_value': bc['exit_value'],
                    'irr': base_irr,
                    'moic': base_moic
                }
            },
            'bear': {
                'name': 'Bear Case（悲观）',
                'weight': 0.225,
                'assumptions': {
                    '营收下降': '-20%',
                    'EBITDA Margin下降': '-25%',
                    '退出倍数下降': '-30%',
                },
                'results': {
                    'exit_value': bear_exit,
                    'irr': bear_irr,
                    'moic': bear_moic
                }
            }
        }
        
        # 加权估值
        self.scenarios['weighted_valuation'] = (
            self.scenarios['bull']['results']['exit_value'] * self.scenarios['bull']['weight'] +
            self.scenarios['base']['results']['exit_value'] * self.scenarios['base']['weight'] +
            self.scenarios['bear']['results']['exit_value'] * self.scenarios['bear']['weight']
        )
        
        return self
    
    def run_breakeven_analysis(self):
        """
        运行盈亏平衡分析
        计算: 需要多高的退出倍数才能达到IRR门槛？
        """
        bc = self.base_case
        irr_targets = [0.15, 0.20, 0.25, 0.30]
        
        breakeven = {}
        for target in irr_targets:
            # 目标退出价值 = 投资 × (1+IRR)^n
            target_exit = bc['initial_investment'] * (1 + target) ** bc['holding_years']
            # 需要的EBITDA = 退出价值 / 退出倍数
            target_ebitda = target_exit / bc['exit_multiple']
            # 需要的营收 = EBITDA / 利润率
            target_revenue = target_ebitda / bc['ebitda_margin']
            
            # 需要的增长率
            rev_growth = (target_revenue / bc['revenue']) ** (1 / bc['holding_years']) - 1
            
            breakeven[f'IRR_{target*100:.0f}%'] = {
                'target_irr': target,
                'target_exit_value': target_exit,
                'target_revenue': target_revenue,
                'required_revenue_growth_cagr': rev_growth,
                'target_ebitda': target_ebitda,
                'moic': target_exit / bc['initial_investment']
            }
        
        self.breakeven = breakeven
        return self
    
    def run_all(self):
        """运行所有分析"""
        self.run_single_variable_analysis()
        self.run_dual_variable_matrix()
        self.run_scenario_analysis()
        self.run_breakeven_analysis()
        return self
    
    def print_summary(self):
        """打印完整分析报告"""
        bc = self.base_case
        irr_threshold = 0.20
        
        print(f"\n{'='*60}")
        print(f"📊 敏感性分析报告: {self.project_name}")
        print(f"{'='*60}")
        
        # === Base Case ===
        print(f"\n--- 基准情景 (Base Case) ---")
        print(f"  营收:           ¥{bc['revenue']:,.0f} 万")
        print(f"  EBITDA Margin:  {bc['ebitda_margin']*100:.1f}%")
        print(f"  EBITDA:         ¥{bc['ebitda']:,.0f} 万")
        print(f"  退出倍数:       {bc['exit_multiple']:.0f}x")
        print(f"  退出价值:       ¥{bc['exit_value']:,.0f} 万")
        print(f"  初始投资:       ¥{bc['initial_investment']:,.0f} 万")
        print(f"  持有期:         {bc['holding_years']} 年")
        print(f"  ───────────────────────────────")
        print(f"  Base IRR:       {bc['irr']*100:.1f}%")
        print(f"  Base MOIC:      {bc['moic']:.2f}x")
        
        # === Tornado Chart（单变量） ===
        print(f"\n--- 单变量敏感性分析 (Tornado Chart) ---")
        print(f"  基准 IRR: {bc['irr']*100:.1f}%")
        print(f"{'='*50}")
        print(f"{'变量':20s} {'低值IRR':10s} {'高值IRR':10s} {'波动幅度':10s}")
        print(f"{'-'*50}")
        
        for var_name, data in self.tornado_data.items():
            low_irr_str = f"{data['low_irr']*100:.1f}%"
            high_irr_str = f"{data['high_irr']*100:.1f}%"
            swing = abs(data['total_irr_swing'] * 100)
            bar = "█" * int(min(swing, 30))
            print(f"{data['display_name']:20s} {low_irr_str:>8s} {high_irr_str:>8s} {swing:6.1f}% {bar}")
        
        print(f"\n  🔑 关键发现: 最敏感变量是 {list(self.tornado_data.keys())[0]}")
        print(f"     对IRR影响幅度: {list(self.tornado_data.values())[0]['total_irr_swing']*100:.1f}%")
        
        # === 三情景分析 ===
        print(f"\n--- 三情景分析 (Base/Bull/Bear) ---")
        print(f"{'='*50}")
        print(f"{'情景':20s} {'退出价值':15s} {'IRR':10s} {'MOIC':8s} {'权重':8s}")
        print(f"{'-'*50}")
        
        for key in ['bull', 'base', 'bear']:
            s = self.scenarios[key]
            r = s['results']
            irr_str = f"{r['irr']*100:.1f}%" if r['irr'] > -0.49 else "N/A"
            moic_str = f"{r['moic']:.2f}x" if r['moic'] > 0 else "亏损"
            print(f"{s['name']:20s} ¥{r['exit_value']:>10,.0f}万 {irr_str:>8s} {moic_str:>8s} {s['weight']*100:5.0f}%")
        
        print(f"\n  加权估值: ¥{self.scenarios['weighted_valuation']:,.0f} 万")
        print(f"  安全边际: {(self.scenarios['weighted_valuation'] / bc['exit_value'] - 1)*100:.1f}%")
        
        # === 盈亏平衡分析 ===
        print(f"\n--- 盈亏平衡分析（达到特定IRR所需条件）---")
        print(f"{'='*55}")
        print(f"{'目标IRR':10s} {'目标退出价值':15s} {'需要营收CAGR':15s} {'MOIC':8s}")
        print(f"{'-'*55}")
        
        for irr_key, data in self.breakeven.items():
            print(f"{irr_key:10s} ¥{data['target_exit_value']:>8,.0f}万 {data['required_revenue_growth_cagr']*100:>8.1f}% {data['moic']:>6.2f}x")
        
        # === 综合结论 ===
        print(f"\n--- 综合结论 ---")
        bear_irr = self.scenarios['bear']['results']['irr']
        base_irr = self.scenarios['base']['results']['irr']
        
        if base_irr >= irr_threshold and bear_irr > 0:
            print(f"  ✅ Base IRR ({base_irr*100:.1f}%) 超出 {irr_threshold*100:.0f}% 门槛")
            print(f"  ✅ Bear Case 仍为正回报（下行保护良好）")
            print(f"  ⭐⭐⭐⭐⭐ 强烈推荐：确定性高，风险可控")
        elif base_irr >= irr_threshold and bear_irr <= 0:
            print(f"  ✅ Base IRR ({base_irr*100:.1f}%) 超出 {irr_threshold*100:.0f}% 门槛")
            print(f"  ⚠️ Bear Case 可能亏损（需注意下行保护）")
            print(f"  ⭐⭐⭐⭐ 推荐：回报可观，但需设计保护条款")
        elif base_irr < irr_threshold and bear_irr > 0.10:
            print(f"  ⚠️ Base IRR ({base_irr*100:.1f}%) 低于 {irr_threshold*100:.0f}% 门槛")
            print(f"  ⚠️ 下行保护尚可，但回报不够吸引")
            print(f"  ⭐⭐⭐ 有条件推荐：需要更好的价格或条款")
        else:
            print(f"  ❌ Base IRR ({base_irr*100:.1f}%) 大幅低于 {irr_threshold*100:.0f}% 门槛")
            print(f"  ❌ Bear Case 可能造成重大亏损")
            print(f"  ⭐ 不推荐：回报风险比不理想")
        
        print(f"{'='*60}\n")
        
        return self
    
    def save_to_excel(self, filename=None):
        """保存为Excel"""
        if filename is None:
            filename = f").strftime('%Y%m%d')}.xlsx"
        filename = os.path.expanduser(filename)
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Tornado数据
            tornado_rows = []
            for var_name, data in self.tornado_data.items():
                tornado_rows.append({
                    'Variable': data['display_name'],
                    'Base Value': data['base_value'],
                    'Low Value': data['low_value'],
                    'High Value': data['high_value'],
                    'Low IRR': data['low_irr'],
                    'High IRR': data['high_irr'],
                    'IRR Impact Low': data['irr_impact_low'],
                    'IRR Impact High': data['irr_impact_high'],
                    'Total Swing': data['total_irr_swing']
                })
            pd.DataFrame(tornado_rows).to_excel(writer, sheet_name='Tornado', index=False)
            
            # 情景分析
            scenario_rows = []
            for key in ['bull', 'base', 'bear']:
                s = self.scenarios[key]
                row = {'Scenario': s['name'], 'Weight': s['weight']}
                row.update({f"{k}_assumption": v for k, v in s['assumptions'].items()})
                row.update({f"result_{k}": v for k, v in s['results'].items()})
                scenario_rows.append(row)
            pd.DataFrame(scenario_rows).to_excel(writer, sheet_name='Scenarios', index=False)
            
            # 盈亏平衡
            breakeven_rows = []
            for irr_key, data in self.breakeven.items():
                breakeven_rows.append(data)
            pd.DataFrame(breakeven_rows).to_excel(writer, sheet_name='Breakeven', index=False)
        
        print(f"✓ 分析报告已保存到: {filename}")
        return self


# ========== 使用示例 ==========
if __name__ == "__main__":
    print("🐴 产业项目敏感性分析工具")
    print("="*60)
    
    analysis = SensitivityAnalysis("示例: 动力电池回收项目")
    
    # 设置Base Case
    analysis.setup_base_case(
        revenue=50000,           # 营收5亿
        ebitda_margin=0.25,      # EBITDA利润率25%
        exit_multiple=10,        # 退出倍数10x
        initial_investment=30000, # 初始投资3亿
        holding_years=5,         # 持有期5年
        wacc=0.10                # WACC 10%
    )
    
    # 添加敏感性变量
    analysis.add_variable('revenue', 50000, 0.20, 0.20, '营收')
    analysis.add_variable('ebitda_margin', 0.25, 0.20, 0.20, 'EBITDA Margin')
    analysis.add_variable('exit_multiple', 10, 0.20, 0.20, '退出倍数')
    analysis.add_variable('initial_investment', 30000, 0.15, 0.15, '初始投资')
    analysis.add_variable('holding_years', 5, 0.20, 0.20, '持有期')
    
    # 运行所有分析
    analysis.run_all()
    
    # 打印报告
    analysis.print_summary()
    analysis.save_to_excel()
