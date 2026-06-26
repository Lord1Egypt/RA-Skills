#!/usr/bin/env python3
"""
电机装配检查清单生成工具
根据装配阶段生成检查清单，支持逐项确认和记录

用法：
  python assembly_checklist.py --stage rotor
  python assembly_checklist.py --stage stator
  python assembly_checklist.py --stage full --output checklist.txt
  python assembly_checklist.py --stage bearing --interactive
"""

import argparse
import sys
from datetime import datetime

STAGES = {
    "rotor": {
        "title": "转子装配检查清单",
        "checks": [
            {"id": "R01", "item": "转子铁心外观：无翘曲、无毛刺、无锈蚀", "method": "目测", "standard": "无可见缺陷"},
            {"id": "R02", "item": "转子外径测量", "method": "卡尺", "standard": "D±IT8"},
            {"id": "R03", "item": "转子内径测量", "method": "塞规", "standard": "d+H7"},
            {"id": "R04", "item": "叠压系数检验", "method": "测量计算", "standard": "≥0.95"},
            {"id": "R05", "item": "磁钢外观：无崩角、无裂纹", "method": "目测", "standard": "无崩角/裂纹"},
            {"id": "R06", "item": "磁钢极性标识", "method": "目测", "standard": "NS交替清晰"},
            {"id": "R07", "item": "磁钢高度测量", "method": "高度尺", "standard": "图样要求±0.05mm"},
            {"id": "R08", "item": "磁钢与铁心间隙", "method": "塞尺", "standard": "≤0.05mm"},
            {"id": "R09", "item": "转子动平衡（G2.5）", "method": "动平衡机", "standard": "<2.5mm/s @3000rpm"},
            {"id": "R10", "item": "配重固定确认", "method": "目测+手试", "standard": "点胶/螺钉紧固"},
            {"id": "R11", "item": "转子充磁后磁通", "method": "磁通计", "standard": "≥设计值90%"},
            {"id": "R12", "item": "转子表面清理", "method": "目测", "standard": "无铁屑/杂质"},
        ]
    },
    "stator": {
        "title": "定子装配检查清单",
        "checks": [
            {"id": "S01", "item": "定子铁心外观：无翘曲、无毛刺", "method": "目测", "standard": "无可见缺陷"},
            {"id": "S02", "item": "定子外径/内径", "method": "卡尺", "standard": "图样要求"},
            {"id": "S03", "item": "槽形样板检验", "method": "样板", "standard": "符合图样"},
            {"id": "S04", "item": "槽满率", "method": "计算", "standard": "45%~55%"},
            {"id": "S05", "item": "相电阻测量", "method": "电桥", "standard": "三相不平衡≤2%"},
            {"id": "S06", "item": "绝缘电阻（500V）", "method": "兆欧表", "standard": "≥100MΩ"},
            {"id": "S07", "item": "匝间绝缘", "method": "匝间冲击仪", "standard": "无击穿"},
            {"id": "S08", "item": "相间绝缘", "method": "万用表", "standard": "无短路"},
            {"id": "S09", "item": "浸漆外观", "method": "目测", "standard": "漆膜完整无气泡"},
            {"id": "S10", "item": "浸漆固化温度曲线", "method": "温度记录仪", "standard": "符合工艺文件"},
            {"id": "S11", "item": "定子端部尺寸", "method": "卡尺", "standard": "图样要求"},
        ]
    },
    "bearing": {
        "title": "轴承装配检查清单",
        "checks": [
            {"id": "B01", "item": "轴承型号确认", "method": "核对图样", "standard": "与图样一致"},
            {"id": "B02", "item": "轴承精度等级", "method": "核对标记", "standard": "P0/P6"},
            {"id": "B03", "item": "轴承游隙", "method": "塞尺", "standard": "C3（高温电机）"},
            {"id": "B04", "item": "轴承外观：滚动体无损伤", "method": "目测", "standard": "无划伤/缺陷"},
            {"id": "B05", "item": "轴承旋转灵活度", "method": "手动旋转", "standard": "无卡滞"},
            {"id": "B06", "item": "轴承加热温度", "method": "温度计", "standard": "80~100℃"},
            {"id": "B07", "item": "轴颈清洁度", "method": "目测", "standard": "无油污/杂质"},
            {"id": "B08", "item": "压装力沿内圈", "method": "观察", "standard": "禁止外圈受力"},
            {"id": "B09", "item": "压装后贴合度", "method": "塞尺", "standard": "无间隙"},
            {"id": "B10", "item": "轴承旋转检测", "method": "手动", "standard": "灵活无异响"},
            {"id": "B11", "item": "轴承润滑脂补充", "method": "目测", "standard": "适量（≤1/2腔）"},
        ]
    },
    "full": {
        "title": "整机装配终检清单",
        "checks": [
            {"id": "F01", "item": "外观检验", "method": "目测", "standard": "无磕碰/划伤"},
            {"id": "F02", "item": "铭牌信息", "method": "核对", "standard": "型号/编号正确"},
            {"id": "F03", "item": "出线盒密封", "method": "目测+手试", "standard": "密封胶完好"},
            {"id": "F04", "item": "螺栓力矩", "method": "力矩扳手", "standard": "符合力矩表"},
            {"id": "F05", "item": "绝缘电阻（500V）", "method": "兆欧表", "standard": "≥100MΩ"},
            {"id": "F06", "item": "耐压试验", "method": "耐压仪", "standard": "1500V/1mA/1min无击穿"},
            {"id": "F07", "item": "空载电流", "method": "功率分析仪", "standard": "≤额定电流30%"},
            {"id": "F08", "item": "空载转速", "method": "转速表", "standard": "额定±5%"},
            {"id": "F09", "item": "振动检测", "method": "振动仪", "standard": "≤2.8mm/s(G6.3)"},
            {"id": "F10", "item": "噪音检测", "method": "声级计", "standard": "≤65dB(A)"},
            {"id": "F11", "item": "转向确认", "method": "点动", "standard": "符合图样"},
            {"id": "F12", "item": "轴承温升（运行30min后）", "method": "点温仪", "standard": "≤40℃（环境25℃）"},
            {"id": "F13", "item": "接地标志", "method": "目测", "standard": "接地标志清晰"},
            {"id": "F14", "item": "包装防护", "method": "目测", "standard": "防潮/防震包装"},
        ]
    }
}


def generate_checklist(stage, show_method=True, output_file=None):
    """生成检查清单"""
    if stage == "full":
        checks = STAGES["full"]["checks"]
        title = STAGES["full"]["title"]
        header = f"{'='*60}\n  {title}（完整流程）\n{'='*60}"
    else:
        stage_data = STAGES.get(stage, {})
        checks = stage_data.get("checks", [])
        title = stage_data.get("title", f"{stage} 检查清单")
        header = f"{'='*60}\n  {title}\n{'='*60}"

    date = datetime.now().strftime("%Y-%m-%d")

    lines = []
    lines.append(header)
    lines.append(f"日期：{date}")
    lines.append(f"产品型号：_______________  产品编号：_______________")
    lines.append(f"操作者：_______________  检验员：_______________")
    lines.append("")
    lines.append(f"{'序号':>4} {'检查项':<30} {'方法':<12} {'标准':<15} {'结果'}")
    lines.append("-" * 90)

    for i, c in enumerate(checks, 1):
        method_str = f"[{c['method']}]" if show_method else ""
        lines.append(f"{i:>4}  {c['item']:<30} {method_str:<12} {c['standard']:<15} □合格  □不合格")

    lines.append("")
    lines.append("不合格项处理：")
    for i in range(3):
        lines.append(f"  {i+1}. _______________________________________________________")
    lines.append("")
    lines.append(f"{'='*60}")
    lines.append("签字：操作者____________  检验员____________  审核____________")

    output = "\n".join(lines)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[OK] 已生成：{output_file}")
    else:
        print(output)

    return output


def interactive_check(stage):
    """交互式检查确认"""
    stage_data = STAGES.get(stage, {})
    checks = stage_data.get("checks", [])
    title = stage_data.get("title", f"{stage} 检查")

    print(f"\n{'='*60}")
    print(f"  {title}（交互模式）")
    print(f"{'='*60}")

    results = []
    for c in checks:
        while True:
            print(f"\n[{c['id']}] {c['item']}")
        print(f"  方法：{c['method']}，标准：{c['standard']}")
            try:
                ans = input("  结果：[P]合格  [F]不合格  [N]不适用  → ").strip().upper()
                if ans in ("P", "F", "N"):
                    results.append({"id": c["id"], "item": c["item"], "result": ans})
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n已退出")
                sys.exit(0)

    # 统计
    passed = sum(1 for r in results if r["result"] == "P")
    failed = sum(1 for r in results if r["result"] == "F")
    na = sum(1 for r in results if r["result"] == "N")

    print(f"\n{'='*60}")
    print(f"检查完成：合格 {passed}，不合格 {failed}，不适用 {na}")
    if failed > 0:
        print("不合格项：")
        for r in results:
            if r["result"] == "F":
                print(f"  [{r['id']}] {r['item']}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="电机装配检查清单生成工具")
    parser.add_argument("--stage", "-s", required=True,
                       choices=["rotor", "stator", "bearing", "full"],
                       help="装配阶段")
    parser.add_argument("--output", "-o", help="输出文件")
    parser.add_argument("--no_method", action="store_true", help="不显示检验方法")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")

    args = parser.parse_args()

    if args.interactive:
        interactive_check(args.stage)
    else:
        generate_checklist(args.stage, show_method=not args.no_method,
                         output_file=args.output)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 默认显示完整清单
        generate_checklist("full")
    else:
        main()
