#!/usr/bin/env python3
"""德育-Katherine助手 - CLI入口"""
import sys

def cmd_help():
    print("📋 德育-Katherine 助手")
    print("="*50)
    print("  overview    查看核心能力概览")
    print("  er-t        查看E-R-T三环判断模型")
    print("  risk        查看四级风险分级")
    print("  scenarios   查看36个场景卡索引")
    print("  help        帮助")
    print()

def cmd_overview():
    print("Katherine v2.0 - 高中德育管理")
    print("="*40)
    print("核心能力:")
    print("  • E-R-T 三环判断模型")
    print("  • 十二工作原则")
    print("  • 四级风险分级")
    print("  • 36个场景卡（含6个新增实操场景）")
    print()
    print("新增:")
    print("  • 警告信闭环实操指南")
    print("  • 手机突击检查流程")
    print("  • 正向积分制")
    print("  • 目标感重建")
    print("  • 家庭教育指导")

def cmd_ert():
    print("E-R-T 三环判断模型")
    print("="*40)
    print("E | Environment 环境")
    print("   判断: 手机/睡眠/同伴/学业反馈")
    print("   新增前置预防层")
    print()
    print("R | Relationship 关系")
    print("   判断: 师生关系/同伴关系/家校关系")
    print()
    print("T | Transformation 转变")
    print("   路径: 关系建立信任→信任让惩罚变成教育")
    print("         →教育需要成功支点→成功支点来自阳性事件")

def cmd_risk():
    print("四级风险分级")
    print("="*40)
    print("🔴 Level 1: 立即上报")
    print("   自伤/自杀/暴力/性侵/严重心理危机")
    print()
    print("🟡 Level 2: 需协同处理")
    print("   长期厌学/网络成瘾/严重违纪/家庭暴力")
    print()
    print("🟢 Level 3: 班主任可处理")
    print("   普通违纪/情绪波动/同伴矛盾/学业困难")
    print()
    print("⚪ Level 4: 常规关注")
    print("   一般性行为习惯问题")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("help","--help","-h"):
        cmd_help()
        return
    cmd = sys.argv[1]
    if cmd == "overview":
        cmd_overview()
    elif cmd in ("ert","er-t"):
        cmd_ert()
    elif cmd == "risk":
        cmd_risk()
    elif cmd == "scenarios":
        print("36个场景卡索引: 包含6个新增实操场景")
        print("详细内容请参考 SKILL.md 正文")
    else:
        cmd_help()

if __name__ == "__main__":
    main()
