#!/usr/bin/env python3
"""
电机质量检验报告生成工具
根据检验类型和标准生成检验记录表和报告

用法：
  python inspection_report.py --type oqc --model "BLDC-200W" --sn "20240001"
  python inspection_report.py --type iqc --output iqc_report.txt
  python inspection_report.py --type pqc --model "PMSM-1kW" --sn "20240015"
  python inspection_report.py --list
"""

import argparse
import sys
from datetime import datetime

INSPECTION_TYPES = {
    "iqc": {
        "title": "来料检验报告 (IQC)",
        "sections": [
            {
                "name": "磁性材料",
                "items": [
                    ("硅钢片厚度", "0.35±0.02mm", "千分尺", "II级"),
                    ("硅钢片涂层", "均匀无脱落", "目测", "I级"),
                    ("磁通密度", "≥1.5T @ 5000A/m", "爱泼斯坦仪", "S-4"),
                    ("磁钢牌号 Br", "符合图样", "退磁曲线测试", "S-3"),
                    ("磁钢尺寸", "±0.05mm", "卡尺", "II级"),
                ]
            },
            {
                "name": "绝缘材料",
                "items": [
                    ("槽绝缘厚度", "0.25±0.02mm", "千分尺", "II级"),
                    ("耐温等级", "F级(155℃)", "热老化试验", "S-3"),
                    ("击穿电压", "≥6kV/mm", "耐压仪", "S-4"),
                ]
            },
            {
                "name": "轴承",
                "items": [
                    ("外观", "无划伤、无锈蚀", "目测", "I级"),
                    ("游隙", "符合C3组", "塞规", "S-3"),
                    ("旋转灵活性", "无异响", "手动旋转", "S-3"),
                ]
            },
            {
                "name": "电磁线",
                "items": [
                    ("线径", "±0.01mm", "微千分尺", "II级"),
                    ("绝缘厚度", "符合QZ-2标准", "剥除外被测量", "II级"),
                    ("耐电压", "2000V/1min不击穿", "耐压仪", "S-3"),
                ]
            }
        ]
    },
    "pqc": {
        "title": "过程检验报告 (PQC)",
        "sections": [
            {
                "name": "定子检验",
                "items": [
                    ("槽满率", "45%~55%", "计算+目测", "II级"),
                    ("直流电阻", "三相不平衡≤2%", "电桥", "S-4"),
                    ("绝缘电阻（浸漆前）", "≥100MΩ", "兆欧表500V", "S-3"),
                    ("匝间绝缘", "无击穿", "匝间冲击仪", "S-3"),
                    ("相间绝缘", "无短路", "万用表", "S-3"),
                    ("绝缘电阻（浸漆后）", "≥100MΩ", "兆欧表500V", "S-3"),
                ]
            },
            {
                "name": "转子检验",
                "items": [
                    ("动平衡", "G2.5级", "动平衡机", "S-3"),
                    ("轴向跳动", "≤0.02mm", "百分表", "S-4"),
                    ("径向跳动", "≤0.03mm", "百分表", "S-4"),
                    ("磁钢极性", "NS交替", "指南针法", "S-3"),
                ]
            },
            {
                "name": "整机装配",
                "items": [
                    ("气隙均匀性", "偏差≤10%均值", "气隙规", "S-3"),
                    ("端盖同轴度", "≤0.03mm", "同轴度仪", "S-3"),
                    ("螺栓力矩", "符合工艺文件", "力矩扳手", "S-4"),
                    ("轴承游隙", "转动灵活无卡滞", "手动", "S-3"),
                ]
            }
        ]
    },
    "fqc": {
        "title": "成品检验报告 (FQC)",
        "sections": [
            {
                "name": "电气性能",
                "items": [
                    ("空载电流", "≤额定电流30%", "功率分析仪", "S-3"),
                    ("空载转速", "额定转速±5%", "光电转速仪", "S-3"),
                    ("绝缘电阻", "≥100MΩ", "兆欧表500V", "S-3"),
                    ("耐电压", "1500V/1mA/1min", "耐压仪", "S-3"),
                    ("接地电阻", "≤0.1Ω", "接地电阻仪", "S-3"),
                ]
            },
            {
                "name": "机械性能",
                "items": [
                    ("振动", "≤2.8mm/s", "振动仪", "S-3"),
                    ("噪音", "≤65dB(A)", "声级计", "S-3"),
                    ("轴承温升", "≤40℃（环境25℃）", "点温仪", "S-4"),
                ]
            },
            {
                "name": "外观",
                "items": [
                    ("外观检查", "无损伤、无锈蚀", "目测", "I级"),
                    ("铭牌标识", "清晰正确", "目测", "I级"),
                    ("出线盒密封", "密封完好", "目测+手试", "I级"),
                ]
            }
        ]
    },
    "oqc": {
        "title": "出厂检验报告 (OQC)",
        "sections": [
            {
                "name": "出货检查",
                "items": [
                    ("外观检查", "无损伤、无锈蚀、标识清晰", "目测", "I级"),
                    ("型号规格核对", "与合同/技术协议一致", "核对", "S-3"),
                    ("绝缘电阻", "≥100MΩ", "兆欧表500V", "S-3"),
                    ("耐电压", "1500V/1mA/1min无击穿", "耐压仪", "S-3"),
                ]
            },
            {
                "name": "运行测试",
                "items": [
                    ("空载运行", "30min无异响无振动", "听诊+目测", "S-3"),
                    ("负载运行", "额定负载30min温升正常", "温度监测", "S-4"),
                    ("噪声", "≤65dB(A)", "声级计", "S-3"),
                    ("振动", "≤2.8mm/s", "振动仪", "S-3"),
                ]
            },
            {
                "name": "文件检查",
                "items": [
                    ("检验报告", "齐全", "目测", "I级"),
                    ("合格证", "有", "目测", "I级"),
                    ("说明书", "齐全", "目测", "I级"),
                    ("出厂编号", "与机身一致", "核对", "S-3"),
                ]
            }
        ]
    }
}


def generate_report(insp_type, model=None, sn=None, supplier=None,
                   batch=None, output_file=None):
    """生成检验报告"""

    if insp_type not in INSPECTION_TYPES:
        print(f"错误：未知检验类型 '{insp_type}'")
        print("可用类型：", list(INSPECTION_TYPES.keys()))
        sys.exit(1)

    data = INSPECTION_TYPES[insp_type]
    date = datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append(f"{'='*70}")
    lines.append(f"          {data['title']}")
    lines.append(f"{'='*70}")
    lines.append(f"报告日期：{date}")
    lines.append(f"产品型号：{model or '_______________'}")
    lines.append(f"产品编号：{sn or '_______________'}")
    if supplier:
        lines.append(f"供应商：{supplier}")
    if batch:
        lines.append(f"生产批号：{batch}")
    lines.append("")

    for section in data["sections"]:
        lines.append(f"【{section['name']}】")
        lines.append(f"{'检验项':<22} {'技术要求':<18} {'检验方法':<12} {'AQL':<6} {'实测值':<10} {'判定'}")
        lines.append("-" * 80)
        for item in section["items"]:
            name, standard, method, aql = item
            lines.append(f"  {name:<20} {standard:<18} {method:<12} {aql:<6} ________  □")
        lines.append("")

    # 判定结果
    lines.append(f"{'='*70}")
    lines.append("检验结论：□ 合格   □ 不合格（备注：___________________）")
    lines.append("")
    lines.append("不合格项记录：")
    for i in range(3):
        lines.append(f"  {i+1}. _____________________________________________________________")
    lines.append("")
    lines.append(f"{'='*70}")
    lines.append("检验员：____________  审核：____________  批准：____________")
    lines.append(f"{'='*70}")

    content = "\n".join(lines)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] 已生成：{output_file}")
    else:
        print(content)

    return content


def list_types():
    print("\n===== 检验类型 =====")
    for key, val in INSPECTION_TYPES.items():
        print(f"  {key}: {val['title']}")


def main():
    parser = argparse.ArgumentParser(description="电机质量检验报告生成工具")
    parser.add_argument("--type", "-t", required=True,
                       choices=list(INSPECTION_TYPES.keys()),
                       help="检验类型")
    parser.add_argument("--model", "-m", help="产品型号")
    parser.add_argument("--sn", help="产品编号")
    parser.add_argument("--supplier", "-s", help="供应商（仅IQC）")
    parser.add_argument("--batch", "-b", help="生产批号")
    parser.add_argument("--output", "-o", help="输出文件")
    parser.add_argument("--list", "-l", action="store_true", help="列出检验类型")

    args = parser.parse_args()

    if args.list:
        list_types()
    else:
        generate_report(
            insp_type=args.type,
            model=args.model,
            sn=args.sn,
            supplier=args.supplier,
            batch=args.batch,
            output_file=args.output,
        )


if __name__ == "__main__":
    if len(sys.argv) == 1:
        list_types()
    else:
        main()
