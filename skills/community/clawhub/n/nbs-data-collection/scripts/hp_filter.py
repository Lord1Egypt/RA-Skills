#!/usr/bin/env python3
"""
HP滤波计算脚本
Hodrick-Prescott Filter for Output Gap Calculation

用法:
    python3 hp_filter.py --input checkpoint_gdp.csv --output checkpoint_hp_filter.csv
    python3 hp_filter.py --input data.csv --lambda 1600 --column gdp
"""

import argparse
import csv
import numpy as np
from pathlib import Path


def hp_filter(y: np.ndarray, lamb: int = 1600) -> tuple:
    """
    Hodrick-Prescott滤波
    
    将时间序列分解为趋势成分（潜在GDP）和周期成分（产出缺口）
    
    参数:
        y: 输入序列（如实际GDP）
        lamb: 平滑参数
            - 季度数据: λ=1600 (标准值)
            - 年度数据: λ=100
            - 月度数据: λ=14400
    
    返回:
        (trend, cycle): 趋势成分和周期成分
    """
    n = len(y)
    
    # 构建单位矩阵I和二阶差分矩阵D
    I = np.eye(n)
    D = np.diff(I, n=2)  # 二阶差分
    
    # 求解: (I + λ*D'D) * trend = y
    # trend = (I + λ*D'D)^(-1) * y
    try:
        trend = np.linalg.solve(I + lamb * D.T @ D, y)
    except np.linalg.LinAlgError:
        # 如果矩阵奇异，使用伪逆
        from numpy.linalg import pinv
        A = I + lamb * D.T @ D
        trend = pinv(A) @ y
    
    # 周期成分 = 实际值 - 趋势值
    cycle = y - trend
    
    return trend, cycle


def calculate_output_gap(gdp_series: np.ndarray, lamb: int = 1600) -> dict:
    """
    计算产出缺口
    
    参数:
        gdp_series: GDP时间序列
        lamb: HP滤波平滑参数（默认季度=1600）
    
    返回:
        dict: 包含潜在GDP、产出缺口(亿元)、产出缺口率(%)
    """
    y = np.array(gdp_series, dtype=float)
    
    # 执行HP滤波
    trend, cycle = hp_filter(y, lamb)
    
    # 计算产出缺口率 = (cycle / trend) * 100
    gap_rate = (cycle / trend) * 100
    
    return {
        "trend": trend.tolist(),      # 潜在GDP
        "cycle": cycle.tolist(),       # 产出缺口(亿元)
        "gap_rate": gap_rate.tolist()  # 产出缺口率(%)
    }


def main():
    parser = argparse.ArgumentParser(description="HP滤波计算产出缺口")
    parser.add_argument("--input", "-i", required=True, help="输入CSV文件路径")
    parser.add_argument("--output", "-o", help="输出CSV文件路径")
    parser.add_argument("--lambda", "-l", type=int, default=1600, 
                        help="平滑参数 (季度=1600, 年度=100, 月度=14400)")
    parser.add_argument("--column", "-c", default="gdp", 
                        help="GDP列名")
    parser.add_argument("--period-column", "-p", default="period",
                        help="期间列名")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"输入文件不存在: {args.input}")
        return 1
    
    # 读取数据
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        records = list(reader)
    
    if not records:
        print("输入文件为空")
        return 1
    
    # 提取GDP序列
    gdp_values = []
    periods = []
    years = []
    quarters = []
    
    for record in records:
        period = record.get(args.period_column, record.get('period', ''))
        gdp = record.get(args.column, record.get('gdp', ''))
        
        if gdp and gdp != 'None' and gdp != '':
            try:
                gdp_values.append(float(gdp))
                periods.append(period)
                
                # 提取年份和季度
                if 'Q' in period:
                    year, q = period.split('Q')
                    years.append(int(year))
                    quarters.append(int(q))
                elif 'q' in period:
                    year, q = period.split('q')
                    years.append(int(year))
                    quarters.append(int(q))
            except ValueError:
                continue
    
    if len(gdp_values) < 4:
        print(f"有效数据点不足: {len(gdp_values)}")
        return 1
    
    print(f"HP滤波计算")
    print(f"  数据点: {len(gdp_values)}")
    print(f"  平滑参数 λ: {args.lambda}")
    print(f"  时间范围: {periods[0]} - {periods[-1]}")
    
    # 计算产出缺口
    result = calculate_output_gap(gdp_values, args.lambda)
    
    # 构建输出数据
    output_records = []
    for i, period in enumerate(periods):
        output_records.append({
            "period": period,
            "year": years[i] if i < len(years) else '',
            "quarter": quarters[i] if i < len(quarters) else '',
            "actual_gdp": gdp_values[i],
            "potential_gdp": round(result["trend"][i], 2),
            "output_gap": round(result["cycle"][i], 2),
            "output_gap_rate": round(result["gap_rate"][i], 2)
        })
    
    # 保存结果
    output_path = Path(args.output) if args.output else input_path.parent / "checkpoint_hp_filter.csv"
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if output_records:
            writer = csv.DictWriter(f, fieldnames=output_records[0].keys())
            writer.writeheader()
            writer.writerows(output_records)
    
    print(f"\n输出文件: {output_path}")
    
    # 显示部分结果
    print(f"\n=== 部分结果验证 ===")
    for i in [0, len(output_records)//4, len(output_records)//2, 
              3*len(output_records)//4, len(output_records)-1]:
        if i < len(output_records):
            r = output_records[i]
            print(f"{r['period']}: GDP={r['actual_gdp']:.1f}, "
                  f"潜在GDP={r['potential_gdp']:.1f}, "
                  f"缺口率={r['output_gap_rate']:.2f}%")
    
    # 验证经济危机时期
    print(f"\n=== 经济危机时期验证 ===")
    crisis_periods = {
        "2009Q1": ("金融危机", -13.7),
        "2020Q1": ("COVID-19", -19.5)
    }
    
    for period, (event, expected_rate) in crisis_periods.items():
        for r in output_records:
            if r['period'] == period:
                actual_rate = r['output_gap_rate']
                status = "✅" if abs(actual_rate - expected_rate) < 5 else "⚠️"
                print(f"{period} ({event}): {actual_rate:.2f}% (预期约{expected_rate}%) {status}")
                break
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
