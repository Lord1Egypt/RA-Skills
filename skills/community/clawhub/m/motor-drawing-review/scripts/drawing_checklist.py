#!/usr/bin/env python3
"""
电机图纸审图清单工具
生成标准审图检查表，支持逐项确认和PDF输出

用法：
  python drawing_checklist.py --type electromagnetic
  python drawing_checklist.py --type structural
  python drawing_checklist.py --type full --output review_checklist.txt
  python drawing_checklist.py --interactive
"""

import argparse
import sys
from datetime import datetime

CHECKLISTS = {
    "electromagnetic": {
        "title": "电磁设计图纸审图清单",
        "sections": [
            {
                "name": "极槽配合",
                "items": [
                    ("极数 2p", "极数合理（常见8/10/12/14极）"),
                    ("槽数 Q", "与极数配合：常见36/48/60槽"),
                    ("每极每相槽数 q=Q/(2pm)", "q≥1（整数槽）或分数槽合理"),
                    ("极槽比关系", "避免分数槽LCM过大导致振动"),
                    ("绕组排布", "60°相带/120°相带，分布合理"),
                ]
            },
            {
                "name": "磁路设计",
                "items": [
                    ("极距 τ", "τ=πDi/2p，计算值合理"),
                    ("气隙长度 δ", "通常0.3~1.0mm，有依据"),
                    ("气隙磁密 Bg", "目标值0.7~1.0T，有设计依据"),
                    ("磁密分布", "定子轭部≤1.5T，转子轭部≤1.4T"),
                    ("永磁体厚度 hm", "与 Br 和 Hc 匹配"),
                    ("漏磁系数 σ", "σ=1.1~1.4，有估算依据"),
                ]
            },
            {
                "name": "绕组设计",
                "items": [
                    ("每相串联匝数 Nph", "与反电动势设计匹配"),
                    ("绕组系数 Kw", "Kd×Kp，通常>0.85"),
                    ("分布系数 Kd", "与 q 值匹配"),
                    ("短距系数 Kp", "通常0.95~0.98（5/6节距）"),
                    ("槽满率", "45%~55%，有说明"),
                    ("并联支路数 a", "与极数配合，整数"),
                ]
            },
            {
                "name": "材料规格",
                "items": [
                    ("硅钢片牌号", "如35YT310，有规格书"),
                    ("永磁体牌号", "如N42SH，Br和Hc标注"),
                    ("电磁线规格", "AWG或线径，有依据"),
                    ("绝缘等级", "E/B/F/H级，对应温度"),
                ]
            }
        ]
    },
    "structural": {
        "title": "结构设计图纸审图清单",
        "sections": [
            {
                "name": "定子结构",
                "items": [
                    ("定子外径 Dso", "与机座配合，有公差"),
                    ("定子内径 Dsi", "与气隙+转子外径配合"),
                    ("铁心长度 L", "与设计长度一致"),
                    ("槽形尺寸", "槽宽、槽高有标注"),
                    ("定子轭部高度", "满足磁密要求"),
                ]
            },
            {
                "name": "转子结构",
                "items": [
                    ("转子外径 Dro", "Dsi - 2δ"),
                    ("转子内径 Dri", "与轴配合，有公差"),
                    ("转轴材料", "45#钢/40Cr，调质处理"),
                    ("轴承位尺寸", "与轴承内径配合h6/k6"),
                    ("磁钢安装位", "尺寸和公差标注清楚"),
                ]
            },
            {
                "name": "公差配合",
                "items": [
                    ("轴承位公差", "h6/k6/m6，视配合选择"),
                    ("机座止口", "H7，与端盖配合"),
                    ("轴承室", "H7，与轴承外径配合"),
                    ("转轴轴承位", "h6(IT6级)", "光滑圆柱配合表"),
                    ("键槽", "N9/js9，符合GB/T"),
                    ("同轴度", "≤0.03mm（端盖配合面）"),
                ]
            },
            {
                "name": "形位公差",
                "items": [
                    ("定子内圆跳动", "≤0.03mm"),
                    ("转子外圆跳动", "≤0.03mm"),
                    ("轴伸跳动", "≤0.03mm"),
                    ("端面跳动", "≤0.02mm（轴向）"),
                ]
            }
        ]
    },
    "full": {
        "title": "电机图纸完整审图清单",
        "sections": [
            {
                "name": "图纸基本信息",
                "items": [
                    ("图纸编号", "编号唯一，与BOM一致"),
                    ("图纸名称", "与产品型号匹配"),
                    ("版本号", "升版记录完整"),
                    ("比例尺", "正确，1:1或标注清楚"),
                    ("签字栏", "设计/审核/批准签字完整"),
                    ("日期", "最新日期"),
                ]
            },
            {
                "name": "电磁设计",
                "items": [
                    ("极槽配合", "极数、槽数合理"),
                    ("极距", "计算正确"),
                    ("气隙长度", "有设计依据（通常0.3~1.0mm）"),
                    ("气隙磁密", "目标值合理（0.7~1.0T）"),
                    ("绕组参数", "Nph、Kw、q 标注清楚"),
                    ("材料牌号", "硅钢片、磁钢、绝缘等级标注"),
                ]
            },
            {
                "name": "结构尺寸",
                "items": [
                    ("定子尺寸", "外径、内径、铁心长度"),
                    ("转子尺寸", "外径、内径、轴径"),
                    ("气隙", "尺寸+公差"),
                    ("键槽", "尺寸+公差+位置度"),
                    ("倒角/圆角", "标注清楚（防应力集中）"),
                ]
            },
            {
                "name": "公差配合",
                "items": [
                    ("轴承位", "h6/k6/m6 配合正确"),
                    ("止口/轴承室", "H7 配合合理"),
                    ("键槽配合", "N9/js9"),
                    ("形位公差", "跳动度、同轴度标注"),
                ]
            },
            {
                "name": "技术要求",
                "items": [
                    ("材料规格", "牌号、标准号完整"),
                    ("表面处理", "防锈、涂覆要求"),
                    ("热处理", "调质/渗碳等标注"),
                    ("动平衡等级", "G2.5/G6.3等"),
                    ("绝缘等级", "E/B/F/H"),
                    ("温升限值", "有具体数值"),
                ]
            },
            {
                "name": "表面质量",
                "items": [
                    ("粗糙度", "各表面 Ra 值标注"),
                    ("形位公差", "GD&T 规范"),
                    ("未注公差", "符合 GB/T 1804"),
                ]
            }
        ]
    }
}


def generate_checklist(drawing_type, output_file=None):
    """生成审图清单"""
    data = CHECKLISTS.get(drawing_type, CHECKLISTS["full"])
    date = datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append(f"{'='*70}")
    lines.append(f"  {data['title']}")
    lines.append(f"{'='*70}")
    lines.append(f"审图日期：{date}")
    lines.append(f"图纸编号：_______________  版本：_______________")
    lines.append(f"审图人：_______________  复核人：_______________")
    lines.append("")

    for section in data["sections"]:
        lines.append(f"【{section['name']}】")
        lines.append(f"{'#':>4} {'检查项':<30} {'检查内容/要求':<25} {'结果'}")
        lines.append("-" * 75)
        for i, item in enumerate(section["items"], 1):
            if isinstance(item, tuple):
                name, requirement = item
            else:
                name, requirement = item, ""
            lines.append(f"{i:>4}  {name:<30} {requirement:<25} □合格 □不合格")
        lines.append("")

    lines.append(f"{'='*70}")
    lines.append("问题汇总（不合格项）：")
    for i in range(5):
        lines.append(f"  {i+1}. ___________________________________________________________________")
    lines.append("")
    lines.append("审核结论：□ 通过   □ 修改后通过   □ 不通过")
    lines.append(f"{'='*70}")
    lines.append("签字：审图____________  复核____________  日期____________")

    content = "\n".join(lines)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] 已生成：{output_file}")
    else:
        print(content)

    return content


def main():
    parser = argparse.ArgumentParser(description="电机图纸审图清单工具")
    parser.add_argument("--type", "-t", default="full",
                       choices=list(CHECKLISTS.keys()),
                       help="审图类型")
    parser.add_argument("--output", "-o", help="输出文件")

    args = parser.parse_args()
    generate_checklist(args.type, output_file=args.output)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        generate_checklist("full")
    else:
        main()
