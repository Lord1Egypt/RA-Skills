#!/usr/bin/env python3
"""
双引擎估值模型 - 运营提升 + 估值修复
团队AI · 投资研究能力包，2026年7月
用法: python3 fosun_dual_engine_model.py
适用场景: 产业并购、战略投资、运营提升型投资
核心逻辑: 运营提升 + 估值修复 = 双重收益
"""

class FosunDualEngineModel:
    """双引擎估值模型: 运营提升 + 估值修复"""
    
    def __init__(self, project_name="未命名项目"):
        self.project_name = project_name
        self.results = {}
        
    def setup_acquisition(self, purchase_price, control_premium=0.25, transaction_fees=0):
        self.base_valuation = purchase_price / (1 + control_premium)
        self.control_premium = control_premium
        self.purchase_price = purchase_price
        self.transaction_fees = transaction_fees
        self.total_investment = purchase_price + transaction_fees
        return self
    
    def setup_benchmarks(self, base_pe=10, base_ev_ebitda=8):
        self.base_pe = base_pe
        self.base_ev_ebitda = base_ev_ebitda
        return self
    
    def setup_operating_improvement(self, years=5, historical_growth=0.08,
                                     fosun_boost=0.08, margin_improvement=0.04,
                                     fee_reduction=0.02):
        self.improve_years = years
        self.historical_growth = historical_growth
        self.fosun_boost = fosun_boost
        self.margin_improvement = margin_improvement
        self.fee_reduction = fee_reduction
        return self
    
    def setup_valuation_recovery(self, target_pe=18, target_ev_ebitda=14, recovery_year=5):
        self.target_pe = target_pe
        self.target_ev_ebitda = target_ev_ebitda
        self.recovery_year = recovery_year
        return self
    
    def setup_exit(self, exit_year=5, exit_pe=None, dividend_yield=0.02):
        self.exit_year = exit_year
        self.exit_pe = exit_pe or self.target_pe
        self.dividend_yield = dividend_yield
        return self
    
    def run_model(self, initial_revenue=10000, initial_margin=0.30, initial_fees=0.20):
        """运行双引擎模型"""
        results = []
        ebitda = initial_revenue * initial_margin
        
        for year in range(1, self.improve_years + 1):
            revenue = initial_revenue * (1 + self.historical_growth + self.fosun_boost) ** year
            margin = initial_margin + self.margin_improvement * min(year, 3)
            fees_pct = max(initial_fees - self.fee_reduction * min(year, 3), 0.10)
            ebitda = revenue * margin
            net_income = ebitda * (1 - fees_pct)
            
            pe_value = net_income * self.target_pe
            ev_ebitda_value = ebitda * self.target_ev_ebitda
            exit_value = max(pe_value, ev_ebitda_value)
            
            cumulative_return = exit_value / self.total_investment
            irr = cumulative_return ** (1 / year) - 1
            
            results.append({
                'year': year,
                'revenue': revenue,
                'ebitda': ebitda,
                'net_income': net_income,
                'pe_value': pe_value,
                'ev_ebitda_value': ev_ebitda_value,
                'exit_value': exit_value,
                'moic': round(cumulative_return, 2),
                'irr': round(irr, 4)
            })
        
        self.results = results
        return results
    
    def print_report(self):
        """打印评估报告"""
        print(f"\n{'='*60}")
        print(f"项目: {self.project_name}")
        print(f"总投资: ¥{self.total_investment:,.0f}")
        print(f"{'='*60}")
        print(f"{'年份':>4} {'收入':>10} {'EBITDA':>10} {'退出价值':>12} {'MOIC':>6} {'IRR':>8}")
        print(f"{'-'*50}")
        for r in self.results:
            print(f"{r['year']:>4} {r['revenue']:>10,.0f} {r['ebitda']:>10,.0f} "
                  f"{r['exit_value']:>12,.0f} {r['moic']:>5.1f}x {r['irr']:>7.1%}")
        print(f"{'='*60}")
        print(f"退出年份: 第{self.exit_year}年 | 目标PE: {self.target_pe}x | 目标EV/EBITDA: {self.target_ev_ebitda}x")

if __name__ == "__main__":
    model = FosunDualEngineModel("示例项目")
    model.setup_acquisition(purchase_price=50000, control_premium=0.25)
    model.setup_benchmarks(base_pe=10, base_ev_ebitda=8)
    model.setup_operating_improvement(years=5, historical_growth=0.08, fosun_boost=0.08)
    model.setup_valuation_recovery(target_pe=18, target_ev_ebitda=14)
    model.setup_exit(exit_year=5)
    model.run_model(initial_revenue=10000, initial_margin=0.30)
    model.print_report()
