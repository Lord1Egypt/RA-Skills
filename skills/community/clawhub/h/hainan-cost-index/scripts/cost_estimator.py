#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海南省建设工程造价估算工具
基于《2024年版海南省建设工程典型案例造价指标》
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class CostEstimateResult:
    """造价估算结果"""
    project_type: str
    building_area: float
    base_index: float
    adjusted_index: float
    total_cost_low: float
    total_cost_mid: float
    total_cost_high: float
    adjustments: Dict[str, float]
    breakdown: Dict[str, float]

class HainanCostEstimator:
    """海南省造价估算器"""
    
    def __init__(self, database_path: Optional[str] = None):
        """初始化估算器"""
        if database_path is None:
            # 默认路径
            skill_dir = Path(__file__).parent.parent
            database_path = skill_dir / "references" / "hainan-cost-database.json"
        
        with open(database_path, 'r', encoding='utf-8') as f:
            self.database = json.load(f)
    
    def estimate(
        self,
        project_type: str,
        building_area: float,
        region: str = "haikou",
        year: str = "2024",
        decoration: str = "standard",
        structure: str = "frame_shear",
        prefabrication_rate: float = 50,
        green_building: str = "none"
    ) -> CostEstimateResult:
        """
        进行投资估算
        
        Args:
            project_type: 项目类型代码 (如: affordable_housing, commercial_housing, office等)
            building_area: 建筑面积(㎡)
            region: 地区 (haikou, sanya, other_cities)
            year: 价格年份
            decoration: 装修标准 (rough, simple, standard, luxury)
            structure: 结构类型 (frame, frame_shear, shear, steel)
            prefabrication_rate: 装配率(%)
            green_building: 绿建标准 (none, basic, one_star, two_star, three_star)
        """
        
        # 获取基准造价指标
        base_index = self._get_base_index(project_type)
        
        # 获取调整系数
        adjustments = self._get_adjustments(
            region, year, decoration, structure, prefabrication_rate, green_building
        )
        
        # 计算综合调整系数
        total_coefficient = 1.0
        for name, coeff in adjustments.items():
            total_coefficient *= coeff
        
        # 计算调整后指标
        adjusted_index = base_index * total_coefficient
        
        # 计算投资估算区间 (±10%)
        total_cost_mid = adjusted_index * building_area / 10000  # 转换为万元
        total_cost_low = total_cost_mid * 0.90
        total_cost_high = total_cost_mid * 1.10
        
        # 计算造价构成
        breakdown = self._calculate_breakdown(total_cost_mid)
        
        return CostEstimateResult(
            project_type=project_type,
            building_area=building_area,
            base_index=base_index,
            adjusted_index=adjusted_index,
            total_cost_low=total_cost_low,
            total_cost_mid=total_cost_mid,
            total_cost_high=total_cost_high,
            adjustments=adjustments,
            breakdown=breakdown
        )
    
    def _get_base_index(self, project_type: str) -> float:
        """获取基准造价指标"""
        cost_reference = self.database.get("cost_index_reference", {})
        
        # 在各类建筑中查找
        for category in ["residential_buildings", "public_buildings", "industrial_buildings"]:
            if category in cost_reference:
                if project_type in cost_reference[category]:
                    return cost_reference[category][project_type]["unit_cost_range"]["mid"]
        
        # 默认返回安居房指标
        return 4337.0
    
    def _get_adjustments(
        self,
        region: str,
        year: str,
        decoration: str,
        structure: str,
        prefabrication_rate: float,
        green_building: str
    ) -> Dict[str, float]:
        """获取各项调整系数"""
        coeffs = self.database.get("adjustment_coefficients", {})
        adjustments = {}
        
        # 地区系数
        regional = coeffs.get("regional", {})
        adjustments["地区"] = regional.get(region, {}).get("coefficient", 1.0)
        
        # 时间系数
        temporal = coeffs.get("temporal", {})
        adjustments["时间"] = temporal.get(year, {}).get("coefficient", 1.0)
        
        # 装修系数
        decoration_coeffs = coeffs.get("decoration", {})
        adjustments["装修"] = decoration_coeffs.get(decoration, {}).get("coefficient", 1.0)
        
        # 结构系数
        structure_coeffs = coeffs.get("structure", {})
        adjustments["结构"] = structure_coeffs.get(structure, {}).get("coefficient", 1.0)
        
        # 装配率系数
        if prefabrication_rate >= 90:
            adjustments["装配率"] = 1.12
        elif prefabrication_rate >= 70:
            adjustments["装配率"] = 1.08
        elif prefabrication_rate >= 50:
            adjustments["装配率"] = 1.05
        elif prefabrication_rate >= 30:
            adjustments["装配率"] = 1.02
        else:
            adjustments["装配率"] = 1.00
        
        # 绿建系数
        green_coeffs = {
            "none": 1.0,
            "basic": 1.02,
            "one_star": 1.03,
            "two_star": 1.05,
            "three_star": 1.08
        }
        adjustments["绿建"] = green_coeffs.get(green_building, 1.0)
        
        return adjustments
    
    def _calculate_breakdown(self, total_cost: float) -> Dict[str, float]:
        """计算造价构成"""
        # 基于典型案例的比例
        return {
            "建筑工程": total_cost * 0.55,
            "装饰工程": total_cost * 0.15,
            "安装工程": total_cost * 0.18,
            "措施项目": total_cost * 0.08,
            "其他费用": total_cost * 0.04
        }
    
    def print_estimate_report(self, result: CostEstimateResult):
        """打印估算报告"""
        print("\n" + "=" * 60)
        print("海南省建设工程投资估算报告")
        print("=" * 60)
        
        print(f"\n【项目信息】")
        print(f"  项目类型: {result.project_type}")
        print(f"  建筑面积: {result.building_area:,.2f} ㎡")
        
        print(f"\n【造价指标】")
        print(f"  基准指标: {result.base_index:,.2f} 元/㎡")
        print(f"  调整后指标: {result.adjusted_index:,.2f} 元/㎡")
        
        print(f"\n【调整系数】")
        for name, coeff in result.adjustments.items():
            print(f"  {name}: {coeff:.2f}")
        print(f"  综合系数: {result.adjusted_index/result.base_index:.2f}")
        
        print(f"\n【投资估算】")
        print(f"  低限: {result.total_cost_low:,.2f} 万元")
        print(f"  中值: {result.total_cost_mid:,.2f} 万元")
        print(f"  高限: {result.total_cost_high:,.2f} 万元")
        
        print(f"\n【造价构成】")
        for item, cost in result.breakdown.items():
            proportion = cost / result.total_cost_mid * 100
            print(f"  {item}: {cost:,.2f} 万元 ({proportion:.1f}%)")
        
        print("\n" + "=" * 60)
        print("数据来源: 《2024年版海南省建设工程典型案例造价指标》")
        print("=" * 60)


def interactive_estimate():
    """交互式估算"""
    print("\n" + "=" * 60)
    print("海南省建设工程造价估算工具")
    print("=" * 60)
    
    # 项目类型选择
    print("\n请选择项目类型:")
    project_types = {
        "1": ("affordable_housing", "安居房"),
        "2": ("commercial_housing", "商品住宅"),
        "3": ("resettlement_housing", "安置房"),
        "4": ("student_dormitory", "学生公寓"),
        "5": ("office", "办公建筑"),
        "6": ("research", "科研建筑"),
        "7": ("education", "教育建筑"),
        "8": ("medical", "医疗建筑"),
        "9": ("manufacturing", "生产厂房"),
        "10": ("warehouse", "仓储物流")
    }
    
    for key, (code, name) in project_types.items():
        print(f"  {key}. {name}")
    
    choice = input("\n请输入选项编号: ").strip()
    project_type = project_types.get(choice, ("affordable_housing", "安居房"))[0]
    
    # 建筑面积
    building_area = float(input("请输入建筑面积(㎡): ").strip() or "10000")
    
    # 地区
    print("\n请选择地区:")
    print("  1. 海口市")
    print("  2. 三亚市")
    print("  3. 其他市县")
    region_choice = input("请输入选项编号: ").strip()
    regions = {"1": "haikou", "2": "sanya", "3": "other_cities"}
    region = regions.get(region_choice, "haikou")
    
    # 装修标准
    print("\n请选择装修标准:")
    print("  1. 毛坯")
    print("  2. 简装")
    print("  3. 精装")
    print("  4. 豪装")
    decoration_choice = input("请输入选项编号: ").strip()
    decorations = {"1": "rough", "2": "simple", "3": "standard", "4": "luxury"}
    decoration = decorations.get(decoration_choice, "standard")
    
    # 创建估算器并计算
    estimator = HainanCostEstimator()
    result = estimator.estimate(
        project_type=project_type,
        building_area=building_area,
        region=region,
        decoration=decoration
    )
    
    estimator.print_estimate_report(result)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_estimate()
    else:
        # 演示模式
        estimator = HainanCostEstimator()
        
        # 示例1: 三亚商品住宅
        print("\n【示例1: 三亚市商品住宅项目】")
        result1 = estimator.estimate(
            project_type="commercial_housing",
            building_area=20000,
            region="sanya",
            decoration="standard"
        )
        estimator.print_estimate_report(result1)
        
        # 示例2: 海口安居房
        print("\n【示例2: 海口市安居房项目】")
        result2 = estimator.estimate(
            project_type="affordable_housing",
            building_area=21528,
            region="haikou",
            decoration="standard",
            prefabrication_rate=50,
            green_building="two_star"
        )
        estimator.print_estimate_report(result2)
