#!/usr/bin/env python3
r"""剂量计算：体重/体表面积/肾功能校正（医学册工具）。
用法: python dose_calc.py --mg-per-kg 5 --weight 80 [--cap 500] [--height 170] [--scr 90 --age 65 --sex M]
依赖：Python 3 标准库，无第三方依赖；可独立执行。
输出: 剂量计算结果与封顶核对；计算基准须由使用者在报告标注（实际/理想/校正体重）。
"""
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mg-per-kg", type=float, required=True, help="单位体重剂量 mg/kg")
    ap.add_argument("--weight", type=float, required=True, help="体重 kg（基准由报告标注）")
    ap.add_argument("--cap", type=float, default=None, help="单次最大剂量 mg")
    ap.add_argument("--height", type=float, default=None, help="身高 cm（算 BSA 用）")
    ap.add_argument("--scr", type=float, default=None, help="血肌酐 μmol/L（肾功能校正用）")
    ap.add_argument("--age", type=float, default=None)
    ap.add_argument("--sex", choices=["M", "F"], default=None)
    a = ap.parse_args()
    dose = a.mg_per_kg * a.weight
    print(f"按体重剂量: {dose:.1f} mg（基准体重 {a.weight} kg，基准类型须报告标注）")
    if a.height:
        bsa = ((a.height * a.weight) / 3600) ** 0.5
        print(f"体表面积(BSA) ≈ {bsa:.3f} m²（Mosteller 公式）")
    if a.cap is not None:
        status = "未超限" if dose <= a.cap else "超限，须下调或分次"
        print(f"封顶核对: 上限 {a.cap} mg → {status}")
    if a.scr and a.age and a.sex:
        scr_mgdl = a.scr / 88.4
        crcl = ((140 - a.age) * a.weight) / (72 * scr_mgdl) * (1.0 if a.sex == "M" else 0.85)
        print(f"肌酐清除率(Cockcroft-Gault) ≈ {crcl:.1f} mL/min（体重/公式假设须标注）")
    print("注：本计算为参数换算，不构成用药建议；个体用药须处方医师决定")

if __name__ == "__main__":
    main()
