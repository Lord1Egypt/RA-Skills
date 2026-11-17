#!/usr/bin/env python3
"""
2026年投融资估值标准验证脚本
用于验证项目估值是否符合2026年最新标准

使用方法：
python validate_2026_valuation.py --industry AI --revenue 10000000 --ev_revenue_multiple 8
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple

class ValuationValidator2026:
    """2026年估值标准验证器"""
    
    def __init__(self):
        # 2026年最新行业估值倍数标准
        self.industry_multiples = {
            "人工智能": {"ev_revenue": [5, 10], "ev_ebitda": [15, 25], "pe": [25, 40], "ps": [3, 8]},
            "生物科技": {"ev_revenue": [3, 8], "ev_ebitda": [20, 30], "pe": [30, 50], "ps": [2, 6]},
            "新能源": {"ev_revenue": [2, 5], "ev_ebitda": [12, 18], "pe": [15, 25], "ps": [1, 4]},
            "SaaS": {"ev_revenue": [8, 15], "ev_ebitda": [20, 30], "pe": [25, 40], "ps": [3, 8]},
            "电商": {"ev_revenue": [0.3, 0.8], "ev_ebitda": [12, 18], "pe": [18, 30], "ps": [0.2, 0.6]},
            "医疗健康": {"ev_revenue": [4, 7], "ev_ebitda": [18, 25], "pe": [20, 35], "ps": [2, 5]},
            "消费品": {"ev_revenue": [1, 3], "ev_ebitda": [15, 22], "pe": [18, 30], "ps": [1, 3]},
            "金融科技": {"ev_revenue": [3, 6], "ev_ebitda": [18, 28], "pe": [20, 35], "ps": [2, 5]},
            "教育科技": {"ev_revenue": [2, 4], "ev_ebitda": [15, 25], "pe": [15, 28], "ps": [1, 4]},
            "硬科技": {"ev_revenue": [4, 8], "ev_ebitda": [18, 28], "pe": [22, 38], "ps": [2, 6]}
        }
        
        # 2026年同比变化趋势
        self.trends = {
            "人工智能": "下降15-20%",
            "生物科技": "上升5-10%",
            "新能源": "稳定",
            "SaaS": "下降10-15%",
            "电商": "稳定",
            "医疗健康": "上升3-8%",
            "消费品": "稳定",
            "金融科技": "下降5-10%",
            "教育科技": "下降8-12%",
            "硬科技": "稳定"
        }
        
        # 风险调整因子
        self.risk_adjustments = {
            "市场情绪": 0.10,
            "流动性": 0.15,
            "控制权": 0.10,
            "特殊条款": 0.08
        }
    
    def validate_multiple(self, industry: str, multiple_type: str, value: float) -> Dict:
        """验证估值倍数是否符合2026年标准"""
        if industry not in self.industry_multiples:
            return {"valid": False, "error": f"行业 {industry} 不在2026年标准中"}
        
        if multiple_type not in self.industry_multiples[industry]:
            return {"valid": False, "error": f"倍数类型 {multiple_type} 不支持"}
        
        min_val, max_val = self.industry_multiples[industry][multiple_type]
        
        if min_val <= value <= max_val:
            return {
                "valid": True,
                "within_range": True,
                "range": [min_val, max_val],
                "trend": self.trends.get(industry, "未知"),
                "adjustment": 0
            }
        else:
            # 计算偏差百分比
            if value < min_val:
                deviation = (min_val - value) / min_val
            else:
                deviation = (value - max_val) / max_val
            
            return {
                "valid": False,
                "within_range": False,
                "range": [min_val, max_val],
                "deviation": deviation,
                "trend": self.trends.get(industry, "未知"),
                "adjustment": deviation
            }
    
    def calculate_valuation_range(self, industry: str, revenue: float, ebitda: float = None) -> Dict:
        """计算估值区间"""
        if industry not in self.industry_multiples:
            return {"error": f"行业 {industry} 不在2026年标准中"}
        
        multiples = self.industry_multiples[industry]
        results = {}
        
        # EV/Revenue 估值
        ev_revenue_min = revenue * multiples["ev_revenue"][0]
        ev_revenue_max = revenue * multiples["ev_revenue"][1]
        results["ev_revenue"] = {
            "min": ev_revenue_min,
            "max": ev_revenue_max,
            "range": [ev_revenue_min, ev_revenue_max]
        }
        
        # PE 估值（需要净利润）
        if ebitda:
            pe_min = ebitda * multiples["pe"][0] * 0.7  # 假设EBITDA到净利润的转换率
            pe_max = ebitda * multiples["pe"][1] * 0.7
            results["pe"] = {
                "min": pe_min,
                "max": pe_max,
                "range": [pe_min, pe_max]
            }
        
        # EV/EBITDA 估值
        if ebitda:
            ev_ebitda_min = ebitda * multiples["ev_ebitda"][0]
            ev_ebitda_max = ebitda * multiples["ev_ebitda"][1]
            results["ev_ebitda"] = {
                "min": ev_ebitda_min,
                "max": ev_ebitda_max,
                "range": [ev_ebitda_min, ev_ebitda_max]
            }
        
        return results
    
    def apply_risk_adjustment(self, base_valuation: float, risk_factors: Dict[str, float]) -> float:
        """应用风险调整"""
        total_adjustment = 0
        for factor, weight in self.risk_adjustments.items():
            if factor in risk_factors:
                total_adjustment += weight * risk_factors[factor]
        
        adjusted_valuation = base_valuation * (1 + total_adjustment)
        return adjusted_valuation
    
    def generate_report(self, industry: str, revenue: float, ebitda: float = None, 
                       custom_multiples: Dict = None) -> str:
        """生成验证报告"""
        report = []
        report.append(f"# 2026年估值标准验证报告")
        report.append(f"**验证日期：** {datetime.now().strftime('%Y-%m-%d')}")
        report.append(f"**行业：** {industry}")
        report.append(f"**营收：** ¥{revenue:,.0f}")
        if ebitda:
            report.append(f"**EBITDA：** ¥{ebitda:,.0f}")
        report.append("")
        
        # 1. 行业标准验证
        report.append("## 1. 估值倍数标准验证")
        report.append("")
        
        if custom_multiples:
            for mult_type, value in custom_multiples.items():
                validation = self.validate_multiple(industry, mult_type, value)
                if validation["valid"]:
                    report.append(f"- **{mult_type.upper()}: {value}** ✅ 符合2026年标准")
                    report.append(f"  - 范围：{validation['range']}")
                    report.append(f"  - 趋势：{validation['trend']}")
                else:
                    report.append(f"- **{mult_type.upper()}: {value}** ❌ 不符合2026年标准")
                    report.append(f"  - 标准范围：{validation['range']}")
                    report.append(f"  - 偏差：{validation['deviation']:.1%}")
                    report.append(f"  - 趋势：{validation['trend']}")
                report.append("")
        
        # 2. 估值区间计算
        report.append("## 2. 估值区间计算")
        report.append("")
        
        valuation_ranges = self.calculate_valuation_range(industry, revenue, ebitda)
        for method, range_data in valuation_ranges.items():
            report.append(f"- **{method.upper()}:**")
            report.append(f"  - 最小估值：¥{range_data['min']:,.0f}")
            report.append(f"  - 最大估值：¥{range_data['max']:,.0f}")
            report.append(f"  - 区间：¥{range_data['min']:,.0f} - ¥{range_data['max']:,.0f}")
            report.append("")
        
        # 3. 趋势分析
        report.append("## 3. 2026年趋势分析")
        report.append("")
        trend = self.trends.get(industry, "未知")
        report.append(f"- **行业趋势：** {trend}")
        
        if "下降" in trend:
            report.append("- **建议：** 估值倍数相对保守，需重点关注基本面验证")
        elif "上升" in trend:
            report.append("- **建议：** 估值倍数相对宽松，可适当提高估值预期")
        else:
            report.append("- **建议：** 估值倍数稳定，按标准范围执行即可")
        report.append("")
        
        # 4. 风险提示
        report.append("## 4. 2026年风险提示")
        report.append("")
        report.append("- **ESG风险：** 碳足迹追踪成为必查项")
        report.append("- **技术风险：** AI模型透明度和算法偏见检测要求提高")
        report.append("- **法律风险：** 数据合规性和跨境数据传输要求严格")
        report.append("- **市场风险：** 科技行业估值倍数普遍下降15-20%")
        report.append("")
        
        # 5. 建议措施
        report.append("## 5. 建议措施")
        report.append("")
        report.append("- **多方法交叉验证：** 使用≥2种估值方法，结果差异<15pp")
        report.append("- **ESG尽职调查：** 强化碳足迹和数据隐私合规评估")
        report.append("- **技术尽职调查：** 重点评估AI模型透明度和算法公平性")
        report.append("- **法律合规审查：** 确保数据合规性和知识产权保护")
        report.append("")
        
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="2026年估值标准验证工具")
    parser.add_argument("--industry", type=str, required=True, help="行业名称")
    parser.add_argument("--revenue", type=float, required=True, help="营收金额")
    parser.add_argument("--ebitda", type=float, help="EBITDA金额")
    parser.add_argument("--ev_revenue", type=float, help="EV/Revenue倍数")
    parser.add_argument("--ev_ebitda", type=float, help="EV/EBITDA倍数")
    parser.add_argument("--pe", type=float, help="PE倍数")
    parser.add_argument("--output", type=str, help="输出文件路径")
    
    args = parser.parse_args()
    
    validator = ValuationValidator2026()
    
    # 构建自定义倍数字典
    custom_multiples = {}
    if args.ev_revenue:
        custom_multiples["ev_revenue"] = args.ev_revenue
    if args.ev_ebitda:
        custom_multiples["ev_ebitda"] = args.ev_ebitda
    if args.pe:
        custom_multiples["pe"] = args.pe
    
    # 生成报告
    report = validator.generate_report(args.industry, args.revenue, args.ebitda, custom_multiples)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {args.output}")
    else:
        print(report)

if __name__ == "__main__":
    main()