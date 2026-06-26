#!/usr/bin/env python3
"""
GhostShield CLI
命令行工具
"""

import argparse
import sys
from pathlib import Path

from .core import GhostShield


def main():
    """CLI 主入口"""
    parser = argparse.ArgumentParser(
        description="🛡️ GhostShield - 反同事蒸馏防护盾",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析风格风险
  ghostshield analyze ./my-repo
  
  # Level 1 基础防护
  ghostshield process --level=1 --input=./my-repo --output=./protected
  
  # Level 2 深度混淆
  ghostshield process --level=2 --input=./my-repo --output=./protected
  
  # Level 3 极致隐匿（含水印）
  ghostshield process --level=3 --watermark --input=./my-repo --output=./protected
  
  # 评估混淆效果
  ghostshield evaluate --original=./my-repo --obfuscated=./protected
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="分析风格特征和蒸馏风险")
    analyze_parser.add_argument("input", help="输入路径（Git 仓库或文件目录）")
    
    # process 命令
    process_parser = subparsers.add_parser("process", help="执行混淆处理")
    process_parser.add_argument("--level", type=int, choices=[1, 2, 3], default=1,
                                help="混淆级别: 1=基础防护, 2=深度混淆, 3=极致隐匿")
    process_parser.add_argument("--input", required=True, help="输入路径")
    process_parser.add_argument("--output", required=True, help="输出路径")
    process_parser.add_argument("--watermark", action="store_true", help="启用水印（仅 Level 3）")
    process_parser.add_argument("--watermark-id", help="水印标识符")
    
    # evaluate 命令
    eval_parser = subparsers.add_parser("evaluate", help="评估混淆效果")
    eval_parser.add_argument("--original", required=True, help="原始路径")
    eval_parser.add_argument("--obfuscated", required=True, help="混淆后路径")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 执行命令
    gs = GhostShield()
    
    if args.command == "analyze":
        cmd_analyze(gs, args)
    elif args.command == "process":
        cmd_process(gs, args)
    elif args.command == "evaluate":
        cmd_evaluate(gs, args)


def cmd_analyze(gs: GhostShield, args):
    """执行 analyze 命令"""
    print("🔍 正在分析...")
    
    result = gs.analyze(args.input)
    
    print("\n" + "="*60)
    print("📊 风格分析报告")
    print("="*60)
    
    print(f"\n🎨 风格独特性: {result['uniqueness_score']:.2%}")
    print(f"⚠️  蒸馏风险: {result['distillation_risk']:.2%}")
    
    # PII 风险
    pii_count = len(result['pii_risks'])
    print(f"\n🔒 敏感信息: {pii_count} 处")
    
    if pii_count > 0:
        pii_types = {}
        for pii in result['pii_risks']:
            pii_type = pii.get('pii_type', 'unknown')
            pii_types[pii_type] = pii_types.get(pii_type, 0) + 1
        
        print("   类型分布:")
        for pii_type, count in pii_types.items():
            print(f"   - {pii_type}: {count} 处")
    
    # 建议
    print("\n💡 保护建议:")
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"   {i}. {rec}")
    
    print("\n" + "="*60)


def cmd_process(gs: GhostShield, args):
    """执行 process 命令"""
    level_names = {1: "基础防护", 2: "深度混淆", 3: "极致隐匿"}
    
    print(f"🛡️ GhostShield - {level_names[args.level]}")
    print(f"\n📂 输入: {args.input}")
    print(f"📂 输出: {args.output}")
    print(f"⚙️  级别: Level {args.level}")
    
    if args.watermark and args.level == 3:
        print("🔖 水印: 已启用")
    
    print("\n⏳ 处理中...")
    
    result = gs.process(
        input_path=args.input,
        output_path=args.output,
        level=args.level,
        enable_watermark=args.watermark and args.level == 3,
        watermark_id=args.watermark_id,
    )
    
    if result.success:
        print("\n✅ 防护完成！\n")
        
        report = result.report
        
        print("📊 防护效果评估:")
        print(f"   - PII 检测: {report['pii_detected']} 处")
        print(f"   - PII 脱敏: {report['pii_sanitized']} 处")
        print(f"   - 风格距离: {report['style_distance']:.2%}")
        print(f"   - 能力保留: {report['capability_retention']:.2%}")
        print(f"   - 蒸馏风险: {report['distillation_risk_before']:.2%} → {report['distillation_risk_after']:.2%}")
        
        if report['watermark_enabled']:
            print("   - 水印: ✅ 已注入")
        
        print(f"\n💾 输出位置: {result.output_path}")
    
    else:
        print("\n❌ 处理失败:")
        for error in result.errors:
            print(f"   - {error}")
        sys.exit(1)


def cmd_evaluate(gs: GhostShield, args):
    """执行 evaluate 命令"""
    print("📈 正在评估混淆效果...")
    
    result = gs.evaluate(
        original_path=args.original,
        obfuscated_path=args.obfuscated,
    )
    
    print("\n" + "="*60)
    print("📊 效果评估报告")
    print("="*60)
    
    print(f"\n📏 风格距离: {result['style_distance']:.2%}")
    print(f"💪 能力保留: {result['capability_retention']:.2%}")
    print(f"📉 风险降低: {result['risk_reduction']:.2%}")
    print(f"   - 原始风险: {result['risk_before']:.2%}")
    print(f"   - 混淆后风险: {result['risk_after']:.2%}")
    
    print(f"\n🎯 综合评分: {result['overall_score']:.2%}")
    
    # 评级
    score = result['overall_score']
    if score >= 0.8:
        grade = "优秀 ⭐⭐⭐"
    elif score >= 0.6:
        grade = "良好 ⭐⭐"
    elif score >= 0.4:
        grade = "一般 ⭐"
    else:
        grade = "较差"
    
    print(f"   评级: {grade}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
