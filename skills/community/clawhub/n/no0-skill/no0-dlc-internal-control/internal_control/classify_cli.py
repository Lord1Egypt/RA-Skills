#!/usr/bin/env python3
"""
数据分级 CLI 工具

命令：
    openclaw-classify get <path>           - 查询单文件分级
    openclaw-classify dir <directory>      - 批量分级目录
    openclaw-classify stats                - 查看统计
    openclaw-classify exclusions           - 列出排除规则
    openclaw-classify reload               - 重新加载规则

示例：
    openclaw-classify get ~/.ssh/id_rsa
    openclaw-classify dir ~/Documents --recursive
"""

import sys
import argparse
import json
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from internal_control.rules import ClassificationEngine, DataLevel


def print_result(result):
    """打印分级结果"""
    if result.level:
        level_emoji = {
            'L1-PUBLIC': '🟢',
            'L2-INTERNAL': '🔵',
            'L3-RESTRICTED': '🟡',
            'L4-CONFIDENTIAL': '🟠',
            'L5-SECRET': '🔴',
            'L6-CRITICAL': '⚫',
        }.get(result.level, '⚪')
        
        print(f"{level_emoji} 路径: {result.path}")
        print(f"   级别: {result.level}")
        print(f"   来源: {result.source}")
        print(f"   置信度: {result.confidence:.1%}")
        if result.rule_id:
            print(f"   规则: {result.rule_id}")
        if result.reason:
            print(f"   原因: {result.reason}")
        if result.note:
            print(f"   备注: {result.note}")
    elif result.source == 'excluded':
        print(f"⏭️  路径: {result.path}")
        print(f"   状态: 已排除")
        if result.exclusion_reason:
            print(f"   原因: {result.exclusion_reason}")
    else:
        print(f"❓ 路径: {result.path}")
        print(f"   状态: 未匹配")
        if result.note:
            print(f"   备注: {result.note}")


def cmd_get(args):
    """查询单文件分级"""
    engine = ClassificationEngine()
    result = engine.classify_sync(args.path)
    print_result(result)


def cmd_dir(args):
    """批量分级目录"""
    engine = ClassificationEngine()
    
    print(f"正在分级目录: {args.directory}")
    print(f"递归: {'是' if args.recursive else '否'}")
    if args.recursive and args.max_depth:
        print(f"最大深度: {args.max_depth}")
    print()
    
    result = engine.classify_directory_sync(
        args.directory,
        recursive=args.recursive,
        max_depth=args.max_depth
    )
    
    # 打印统计
    print("=" * 50)
    print("分级统计:")
    print("=" * 50)
    
    level_order = ['L1-PUBLIC', 'L2-INTERNAL', 'L3-RESTRICTED', 
                   'L4-CONFIDENTIAL', 'L5-SECRET', 'L6-CRITICAL', 'excluded']
    
    for level in level_order:
        count = result.statistics.get(level, 0)
        if count > 0:
            emoji = {
                'L1-PUBLIC': '🟢',
                'L2-INTERNAL': '🔵',
                'L3-RESTRICTED': '🟡',
                'L4-CONFIDENTIAL': '🟠',
                'L5-SECRET': '🔴',
                'L6-CRITICAL': '⚫',
                'excluded': '⏭️',
            }.get(level, '⚪')
            print(f"  {emoji} {level}: {count} 个文件")
    
    print(f"\n总计: {result.total_files} 个文件")
    
    # 如果需要详细列表
    if args.verbose:
        print()
        print("=" * 50)
        print("详细列表:")
        print("=" * 50)
        for file_result in result.files:
            print_result(file_result)
            print()


def cmd_stats(args):
    """查看统计"""
    engine = ClassificationEngine()
    
    print("=" * 50)
    print("规则统计:")
    print("=" * 50)
    rule_stats = engine.get_rule_stats()
    print(f"  总规则数: {rule_stats.total_rules}")
    print(f"  精确规则: {rule_stats.exact_rules}")
    print(f"  Glob规则: {rule_stats.glob_rules}")
    print(f"  排除规则: {rule_stats.exclusion_rules}")
    
    print()
    print("=" * 50)
    print("缓存统计:")
    print("=" * 50)
    cache_stats = engine.get_cache_stats()
    print(f"  缓存大小: {cache_stats['size']}")
    print(f"  命中率: {cache_stats['hit_rate']}")
    print(f"  过期条目: {cache_stats['expired_count']}")
    
    print()
    print("=" * 50)
    print("排除规则统计:")
    print("=" * 50)
    exclusion_stats = engine.get_exclusion_stats()
    print(f"  总排除规则: {exclusion_stats['total']}")
    print(f"  自定义规则: {exclusion_stats['custom']}")
    print("  按类型:")
    for type_name, count in sorted(exclusion_stats['by_type'].items()):
        print(f"    - {type_name}: {count}")


def cmd_exclusions(args):
    """列出排除规则"""
    engine = ClassificationEngine()
    
    if args.list:
        print("=" * 50)
        print("所有排除规则:")
        print("=" * 50)
        
        rules = engine.exclusion_manager.list_all_exclusions()
        for i, rule in enumerate(rules, 1):
            print(f"{i}. [{rule.exclusion_type.value}] {rule.pattern}")
            print(f"   原因: {rule.reason}")
    
    if args.check:
        print()
        result = engine.classify_sync(args.check)
        if result.source == 'excluded':
            print(f"✅ 路径 '{args.check}' 被排除")
            print(f"   原因: {result.exclusion_reason}")
        else:
            print(f"❌ 路径 '{args.check}' 未被排除")


def cmd_reload(args):
    """重新加载规则"""
    engine = ClassificationEngine()
    engine.reload_rules()
    print("✅ 规则已重新加载")


def main():
    parser = argparse.ArgumentParser(
        prog='openclaw-classify',
        description='数据分级 CLI 工具'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # get 命令
    get_parser = subparsers.add_parser('get', help='查询单文件分级')
    get_parser.add_argument('path', help='文件路径')
    get_parser.set_defaults(func=cmd_get)
    
    # dir 命令
    dir_parser = subparsers.add_parser('dir', help='批量分级目录')
    dir_parser.add_argument('directory', help='目录路径')
    dir_parser.add_argument('-r', '--recursive', action='store_true', 
                           help='递归分级')
    dir_parser.add_argument('-d', '--max-depth', type=int, default=10,
                           help='最大递归深度')
    dir_parser.add_argument('-v', '--verbose', action='store_true',
                           help='显示详细列表')
    dir_parser.set_defaults(func=cmd_dir)
    
    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='查看统计')
    stats_parser.set_defaults(func=cmd_stats)
    
    # exclusions 命令
    exclusions_parser = subparsers.add_parser('exclusions', help='排除规则管理')
    exclusions_parser.add_argument('-l', '--list', action='store_true',
                                  help='列出所有排除规则')
    exclusions_parser.add_argument('-c', '--check', metavar='PATH',
                                  help='检查路径是否被排除')
    exclusions_parser.set_defaults(func=cmd_exclusions)
    
    # reload 命令
    reload_parser = subparsers.add_parser('reload', help='重新加载规则')
    reload_parser.set_defaults(func=cmd_reload)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()