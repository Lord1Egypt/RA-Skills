#!/usr/bin/env python3
"""
包装成本与尺寸计算工具
用于计算包装材料成本、尺寸规格等
"""

import json
import sys
from typing import Dict, List, Optional


def calculate_packaging_cost(
    material_type: str,
    material_cost_per_kg: float,
    material_density: float,
    packaging_volume_ml: float,
    fill_rate: float = 0.85,
    wall_thickness_mm: float = 0.5,
    packaging_count: int = 1
) -> Dict:
    """
    计算包装材料成本
    
    Args:
        material_type: 材料类型 (PP/PE/PET/Glass/Aluminum等)
        material_cost_per_kg: 材料单价(元/kg)
        material_density: 材料密度(g/cm³)
        packaging_volume_ml: 包装容量(ml)
        fill_rate: 填充率(容积效率)
        wall_thickness_mm: 壁厚(mm)
        packaging_count: 包装数量
    
    Returns:
        成本计算结果
    """
    # 根据包装类型估算材料用量
    volume_cm3 = packaging_volume_ml
    
    # 简化计算：假设包装为圆柱形或方形
    # 实际表面积估算(与体积的关系)
    surface_area_cm2 = (volume_cm3 ** (2/3)) * 5
    
    # 材料体积
    material_volume_cm3 = surface_area_cm2 * wall_thickness_mm
    
    # 材料重量(kg)
    material_weight_kg = (material_volume_cm3 * material_density) / 1000
    
    # 单个包装材料成本
    unit_cost = material_weight_kg * material_cost_per_kg
    
    # 总成本
    total_cost = unit_cost * packaging_count
    
    return {
        "material_type": material_type,
        "material_weight_per_unit_kg": round(material_weight_kg, 4),
        "unit_cost_yuan": round(unit_cost, 4),
        "total_cost_yuan": round(total_cost, 4),
        "packaging_count": packaging_count,
        "surface_area_cm2": round(surface_area_cm2, 2),
        "wall_thickness_mm": wall_thickness_mm
    }


def calculate_packaging_dimensions(
    volume_ml: float,
    shape: str = "cylinder",
    aspect_ratio: float = 1.5
) -> Dict:
    """
    根据目标容量计算包装尺寸
    
    Args:
        volume_ml: 目标容量(ml)
        shape: 包装形状 (cylinder/rectangle/bottle)
        aspect_ratio: 长宽比或高径比
    
    Returns:
        推荐尺寸规格
    """
    volume_cm3 = volume_ml
    
    if shape == "cylinder":
        # 圆柱形: 高 = aspect_ratio × 直径
        # V = π × (D/2)² × H
        # V = π × (D/2)² × (aspect_ratio × D)
        # V = π × D³ × aspect_ratio / 4
        # D³ = 4V / (π × aspect_ratio)
        diameter_cm = ((4 * volume_cm3) / (3.14159 * aspect_ratio)) ** (1/3)
        height_cm = diameter_cm * aspect_ratio
        
        return {
            "shape": "圆柱形",
            "diameter_cm": round(diameter_cm, 2),
            "height_cm": round(height_cm, 2),
            "estimated_diameter_mm": round(diameter_cm * 10, 0),
            "estimated_height_mm": round(height_cm * 10, 0),
            "volume_ml": volume_ml
        }
    
    elif shape == "rectangle":
        # 长方形: 长:宽:高 = aspect_ratio : 1 : (aspect_ratio/2)
        # 简化计算
        length_ratio = aspect_ratio
        width_ratio = 1
        height_ratio = aspect_ratio / 2
        
        total_ratio = length_ratio * width_ratio * height_ratio
        scale = (volume_cm3 / total_ratio) ** (1/3)
        
        length_cm = length_ratio * scale
        width_cm = width_ratio * scale
        height_cm = height_ratio * scale
        
        return {
            "shape": "长方形",
            "length_cm": round(length_cm, 2),
            "width_cm": round(width_cm, 2),
            "height_cm": round(height_cm, 2),
            "estimated_length_mm": round(length_cm * 10, 0),
            "estimated_width_mm": round(width_cm * 10, 0),
            "estimated_height_mm": round(height_cm * 10, 0),
            "volume_ml": volume_ml
        }
    
    elif shape == "bottle":
        # 瓶形: 考虑瓶口和瓶身
        # 简化: 瓶身直径, 瓶口直径, 总高度
        body_diameter_cm = ((volume_cm3) / (3.14159 * aspect_ratio * 0.7)) ** (1/3)
        body_height_cm = body_diameter_cm * aspect_ratio
        neck_diameter_cm = body_diameter_cm * 0.4
        neck_height_cm = body_height_cm * 0.15
        
        return {
            "shape": "瓶形",
            "body_diameter_cm": round(body_diameter_cm, 2),
            "body_height_cm": round(body_height_cm, 2),
            "neck_diameter_cm": round(neck_diameter_cm, 2),
            "neck_height_cm": round(neck_height_cm, 2),
            "total_height_cm": round(body_height_cm + neck_height_cm, 2),
            "estimated_body_diameter_mm": round(body_diameter_cm * 10, 0),
            "estimated_total_height_mm": round((body_height_cm + neck_height_cm) * 10, 0),
            "volume_ml": volume_ml
        }
    
    else:
        return {"error": f"不支持的形状: {shape}"}


def calculate_barrier_requirement(
    product_type: str,
    storage_condition: str = "ambient"
) -> Dict:
    """
    计算包装阻隔性能要求
    
    Args:
        product_type: 产品类型
        storage_condition: 存储条件 (ambient/refrigerated/frozen)
    
    Returns:
        阻隔性能要求
    """
    # 氧气透过率要求 (cm³/m²·day·atm)
    barrier_requirements = {
        "snack": {"otrv": 5-50, "description": "中等阻隔"},
        "coffee": {"otrv": 1-5, "description": "高阻隔"},
        "dairy": {"otrv": 0.5-5, "description": "高阻隔"},
        "meat": {"otrv": 0.5-3, "description": "超高阻隔"},
        "beverage": {"otrv": 0.1-2, "description": "超高阻隔"},
        "oil": {"otrv": 1-10, "description": "中高阻隔"},
        "powder": {"otrv": 1-10, "description": "中高阻隔"},
        "candy": {"otrv": 5-50, "description": "中等阻隔"},
    }
    
    # 存储条件系数
    storage_factor = {
        "ambient": 1.0,
        "refrigerated": 0.8,
        "frozen": 0.5
    }
    
    req = barrier_requirements.get(product_type.lower(), barrier_requirements["snack"])
    factor = storage_factor.get(storage_condition.lower(), 1.0)
    
    adjusted_otrv = req["otrv"] * factor if isinstance(req["otrv"], (int, float)) else req["otrv"]
    
    return {
        "product_type": product_type,
        "storage_condition": storage_condition,
        "otrv_requirement": adjusted_otrv,
        "barrier_level": req["description"],
        "recommendation": f"建议选择OTRV≤{adjusted_otrv}的阻隔材料"
    }


def calculate_shrinkage(
    material_type: str,
    temperature_change: float
) -> Dict:
    """
    计算材料收缩率
    
    Args:
        material_type: 材料类型
        temperature_change: 温度变化(℃)
    
    Returns:
        收缩率计算结果
    """
    # 材料热收缩系数 (mm/mm/℃)
    shrinkage_coefficients = {
        "PE": 0.0002,
        "PP": 0.00015,
        "PET": 0.00007,
        "PS": 0.00008,
        "PVC": 0.00008,
        "Glass": 0.000009,
        "Aluminum": 0.000024
    }
    
    coefficient = shrinkage_coefficients.get(material_type.upper(), 0.0001)
    shrinkage_rate = coefficient * abs(temperature_change) * 100
    
    return {
        "material_type": material_type,
        "temperature_change_c": temperature_change,
        "shrinkage_coefficient": coefficient,
        "shrinkage_rate_percent": round(shrinkage_rate, 4),
        "dimension_change_mm_per_m": round(shrinkage_rate * 10, 2)
    }


def compare_packaging_cost(
    materials: List[Dict],
    volume_ml: float
) -> List[Dict]:
    """
    比较不同包装材料的成本
    
    Args:
        materials: 材料列表 [{"type": "PET", "cost_per_kg": 12, "density": 1.38}]
        volume_ml: 包装容量
    
    Returns:
        成本比较结果
    """
    results = []
    
    for mat in materials:
        cost_result = calculate_packaging_cost(
            material_type=mat["type"],
            material_cost_per_kg=mat["cost_per_kg"],
            material_density=mat["density"],
            packaging_volume_ml=volume_ml
        )
        results.append(cost_result)
    
    # 按成本排序
    results.sort(key=lambda x: x["unit_cost_yuan"])
    
    # 添加排名
    for i, r in enumerate(results):
        r["rank"] = i + 1
        if i == 0:
            r["saving_percent"] = 0
        else:
            saving = (results[i]["unit_cost_yuan"] - results[0]["unit_cost_yuan"]) / results[i]["unit_cost_yuan"] * 100
            r["saving_percent"] = round(saving, 2)
    
    return results


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("包装计算工具")
        print("=" * 50)
        print("用法: python3 package_calculator.py <command> [args]")
        print("")
        print("命令:")
        print("  cost <material> <cost_per_kg> <density> <volume_ml> [thickness]")
        print("  dimension <volume_ml> [shape] [aspect_ratio]")
        print("  barrier <product_type> [storage_condition]")
        print("  shrinkage <material> <temp_change>")
        print("  compare <materials_json> <volume_ml>")
        print("")
        print("示例:")
        print("  python3 package_calculator.py cost PET 12 1.38 500 0.5")
        print("  python3 package_calculator.py dimension 500 bottle 2.0")
        print("  python3 package_calculator.py barrier coffee ambient")
        return
    
    command = sys.argv[1]
    
    try:
        if command == "cost":
            material = sys.argv[2]
            cost_per_kg = float(sys.argv[3])
            density = float(sys.argv[4])
            volume = float(sys.argv[5])
            thickness = float(sys.argv[6]) if len(sys.argv) > 6 else 0.5
            
            result = calculate_packaging_cost(
                material, cost_per_kg, density, volume,
                wall_thickness_mm=thickness
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == "dimension":
            volume = float(sys.argv[2])
            shape = sys.argv[3] if len(sys.argv) > 3 else "cylinder"
            ratio = float(sys.argv[4]) if len(sys.argv) > 4 else 1.5
            
            result = calculate_packaging_dimensions(volume, shape, ratio)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == "barrier":
            product = sys.argv[2]
            condition = sys.argv[3] if len(sys.argv) > 3 else "ambient"
            
            result = calculate_barrier_requirement(product, condition)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == "shrinkage":
            material = sys.argv[2]
            temp_change = float(sys.argv[3])
            
            result = calculate_shrinkage(material, temp_change)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif command == "compare":
            materials = json.loads(sys.argv[2])
            volume = float(sys.argv[3])
            
            results = compare_packaging_cost(materials, volume)
            print(json.dumps(results, ensure_ascii=False, indent=2))
        
        else:
            print(f"未知命令: {command}")
    
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
