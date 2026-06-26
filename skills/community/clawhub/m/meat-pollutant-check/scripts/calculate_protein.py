#!/usr/bin/env python3
"""
畜禽肉蛋白质凯氏定氮法计算工具

依据 GB 5009.5-2025 第一法 凯氏定氮法
计算公式：X = (V1 - V2) * c * 0.0140 / (m * V3 / V4) * F * 100

功能：
1. 单次测定蛋白质含量计算
2. 干基蛋白质含量折算
3. 两次平行测定精密度验证
"""

import argparse
import math
import sys


def significant_figures(value, n_sig):
    """将数值格式化为指定有效数字位数"""
    if value == 0:
        return 0.0
    return round(value, n_sig - 1 - int(math.floor(math.log10(abs(value)))))


def format_result(value):
    """
    根据 GB 5009.5-2025 要求格式化结果：
    - 蛋白质含量 >= 1 g/100g：保留三位有效数字
    - 蛋白质含量 < 1 g/100g：保留两位有效数字
    """
    if value == 0:
        return "0.00"
    if abs(value) >= 1:
        formatted = significant_figures(value, 3)
    else:
        formatted = significant_figures(value, 2)
    # 格式化输出，去除不必要的末尾零但保留至少两位小数
    result_str = f"{formatted:.6f}".rstrip("0")
    parts = result_str.split(".")
    if len(parts) == 2:
        if len(parts[1]) < 2:
            parts[1] = parts[1].ljust(2, "0")
        result_str = parts[0] + "." + parts[1]
    return result_str


def calculate_protein(v1, v2, c, m, v3, v4, F):
    """
    计算蛋白质含量

    参数:
        v1: 试液消耗标准滴定液体积 (mL)
        v2: 试剂空白消耗标准滴定液体积 (mL)
        c: 标准滴定溶液浓度 (mol/L)
        m: 试样质量 (g 或 mL)
        v3: 吸取消化液体积 (mL)
        v4: 消解溶液定容体积 (mL)
        F: 蛋白质折算系数

    返回:
        蛋白质含量 (g/100g 或 g/100mL)
    """
    if m <= 0:
        raise ValueError("试样质量 m 必须大于 0")
    if v4 <= 0:
        raise ValueError("消解溶液定容体积 V4 必须大于 0")
    if v3 <= 0:
        raise ValueError("吸取消化液体积 V3 必须大于 0")
    if c <= 0:
        raise ValueError("标准滴定溶液浓度 c 必须大于 0")
    if F <= 0:
        raise ValueError("蛋白质折算系数 F 必须大于 0")

    # 公式(1): X = (V1 - V2) * c * 0.0140 / (m * V3 / V4) * F * 100
    X = (v1 - v2) * c * 0.0140 / (m * v3 / v4) * F * 100
    return X


def calculate_dry_basis(protein_content, moisture_percent):
    """
    干基蛋白质含量计算

    参数:
        protein_content: 湿基蛋白质含量 (g/100g)
        moisture_percent: 水分含量 (%)

    返回:
        干基蛋白质含量 (g/100g)
    """
    if moisture_percent < 0 or moisture_percent >= 100:
        raise ValueError("水分含量必须在 0~100 之间（不含100）")
    return protein_content / (1 - moisture_percent / 100)


def check_precision(result1, result2):
    """
    精密度验证

    依据 GB 5009.5-2025 第7章：
    - 蛋白质含量 <= 10 g/100g：绝对差值不超过算术平均值的 10%
    - 蛋白质含量 > 10 g/100g：绝对差值不超过算术平均值的 5%

    参数:
        result1: 第一次测定结果 (g/100g)
        result2: 第二次测定结果 (g/100g)

    返回:
        dict: 包含判定结果和详细信息
    """
    avg = (result1 + result2) / 2
    abs_diff = abs(result1 - result2)
    relative_diff = abs_diff / avg * 100 if avg != 0 else 0

    if avg <= 10:
        threshold = 10  # 百分比
        limit = avg * threshold / 100
        passed = abs_diff <= limit
        category = "蛋白质含量 <= 10 g/100g"
    else:
        threshold = 5  # 百分比
        limit = avg * threshold / 100
        passed = abs_diff <= limit
        category = "蛋白质含量 > 10 g/100g"

    return {
        "result1": result1,
        "result2": result2,
        "average": avg,
        "absolute_diff": abs_diff,
        "relative_diff_percent": relative_diff,
        "threshold_percent": threshold,
        "limit_value": limit,
        "category": category,
        "passed": passed,
    }


def main():
    parser = argparse.ArgumentParser(
        description="畜禽肉蛋白质凯氏定氮法计算工具 (GB 5009.5-2025 第一法)"
    )
    parser.add_argument("--v1", type=float, required=True, help="试液消耗标准滴定液体积 (mL)")
    parser.add_argument("--v2", type=float, required=True, help="试剂空白消耗标准滴定液体积 (mL)")
    parser.add_argument("--c", type=float, required=True, help="标准滴定溶液浓度 (mol/L)")
    parser.add_argument("--m", type=float, required=True, help="试样质量 (g)")
    parser.add_argument("--v3", type=float, required=True, help="吸取消化液体积 (mL)")
    parser.add_argument("--v4", type=float, required=True, help="消解溶液定容体积 (mL)")
    parser.add_argument("--F", type=float, default=6.25, help="蛋白质折算系数，默认6.25（畜禽肉）")
    parser.add_argument("--moisture", type=float, default=None, help="水分含量百分比（可选，用于干基计算）")

    # 精密度验证参数
    parser.add_argument("--precision", action="store_true", help="启用精密度验证（需提供第二次测定参数）")
    parser.add_argument("--v1_2", type=float, default=None, help="第二次测定：试液消耗标准滴定液体积 (mL)")
    parser.add_argument("--v2_2", type=float, default=None, help="第二次测定：试剂空白消耗标准滴定液体积 (mL)")
    parser.add_argument("--c2", type=float, default=None, help="第二次测定：标准滴定溶液浓度 (mol/L)")
    parser.add_argument("--m2", type=float, default=None, help="第二次测定：试样质量 (g)")
    parser.add_argument("--v3_2", type=float, default=None, help="第二次测定：吸取消化液体积 (mL)")
    parser.add_argument("--v4_2", type=float, default=None, help="第二次测定：消解溶液定容体积 (mL)")

    args = parser.parse_args()

    # 第一次测定计算
    try:
        result1 = calculate_protein(args.v1, args.v2, args.c, args.m, args.v3, args.v4, args.F)
    except ValueError as e:
        print(f"计算错误: {e}", file=sys.stderr)
        sys.exit(1)

    print("=" * 50)
    print("畜禽肉蛋白质凯氏定氮法计算结果")
    print("依据: GB 5009.5-2025 第一法")
    print("=" * 50)

    # 计算详情
    nitrogen_content = (args.v1 - args.v2) * args.c * 0.0140 / (args.m * args.v3 / args.v4) * 100
    print(f"\n--- 第一次测定 ---")
    print(f"试液消耗体积 V1: {args.v1} mL")
    print(f"空白消耗体积 V2: {args.v2} mL")
    print(f"标准溶液浓度 c: {args.c} mol/L")
    print(f"试样质量 m: {args.m} g")
    print(f"吸取消化液体积 V3: {args.v3} mL")
    print(f"定容体积 V4: {args.v4} mL")
    print(f"折算系数 F: {args.F}")
    print(f"氮含量: {format_result(nitrogen_content)} g/100g")
    print(f"蛋白质含量: {format_result(result1)} g/100g")

    # 干基计算
    if args.moisture is not None:
        try:
            dry_result = calculate_dry_basis(result1, args.moisture)
            print(f"水分含量: {args.moisture}%")
            print(f"干基蛋白质含量: {format_result(dry_result)} g/100g")
        except ValueError as e:
            print(f"干基计算错误: {e}", file=sys.stderr)

    # 精密度验证
    if args.precision:
        if any(v is None for v in [args.v1_2, args.v2_2, args.c2, args.m2, args.v3_2, args.v4_2]):
            print("\n错误: 启用精密度验证需要提供第二次测定的全部参数 (--v1_2, --v2_2, --c2, --m2, --v3_2, --v4_2)", file=sys.stderr)
            sys.exit(1)

        try:
            result2 = calculate_protein(
                args.v1_2, args.v2_2, args.c2, args.m2, args.v3_2, args.v4_2, args.F
            )
        except ValueError as e:
            print(f"第二次测定计算错误: {e}", file=sys.stderr)
            sys.exit(1)

        nitrogen2 = (args.v1_2 - args.v2_2) * args.c2 * 0.0140 / (args.m2 * args.v3_2 / args.v4_2) * 100

        print(f"\n--- 第二次测定 ---")
        print(f"试液消耗体积 V1: {args.v1_2} mL")
        print(f"空白消耗体积 V2: {args.v2_2} mL")
        print(f"标准溶液浓度 c: {args.c2} mol/L")
        print(f"试样质量 m: {args.m2} g")
        print(f"吸取消化液体积 V3: {args.v3_2} mL")
        print(f"定容体积 V4: {args.v4_2} mL")
        print(f"氮含量: {format_result(nitrogen2)} g/100g")
        print(f"蛋白质含量: {format_result(result2)} g/100g")

        precision = check_precision(result1, result2)

        print(f"\n--- 精密度验证 ---")
        print(f"判定类别: {precision['category']}")
        print(f"两次结果: {format_result(result1)}, {format_result(result2)} g/100g")
        print(f"算术平均值: {format_result(precision['average'])} g/100g")
        print(f"绝对差值: {precision['absolute_diff']:.4f} g/100g")
        print(f"相对差值: {precision['relative_diff_percent']:.2f}%")
        print(f"允许阈值: {precision['threshold_percent']}% (限值: {precision['limit_value']:.4f} g/100g)")
        if precision["passed"]:
            print("精密度判定: 通过")
        else:
            print("精密度判定: 不通过 - 两次结果偏差超出允许范围")

    # 检出限提示
    print(f"\n--- 方法检出限 ---")
    if args.c <= 0.05:
        print("使用 0.05 mol/L 标准滴定液时，检出限为 0.008 g/100g")
    else:
        print("使用 0.10 mol/L 标准滴定液时，检出限为 0.008 g/100g（称样量5.0g时）")

    print("=" * 50)


if __name__ == "__main__":
    main()
