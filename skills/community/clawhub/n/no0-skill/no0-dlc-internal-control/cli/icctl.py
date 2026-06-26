#!/usr/bin/env python3
"""
内控 Skills CLI - 数据分级命令行工具
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import argparse
import json
from pathlib import Path
from typing import List

from core.classification_engine import ClassificationEngine, DataLevel


def cmd_classify(args):
    """分级单个路径"""
    engine = ClassificationEngine()
    result = engine.classify(args.path)
    
    if result.source == 'excluded':
        print(f"📁 {result.path}")
        print(f"   状态: 已排除 ({result.exclusion_reason})")
    elif result.level:
        print(f"📁 {result.path}")
        print(f"   级别: {result.level}")
        print(f"   来源: {result.source}")
        print(f"   置信: {result.confidence:.2f}")
        print(f"   规则: {result.rule_id}")
        print(f"   原因: {result.reason}")
    else:
        print(f"📁 {result.path}")
        print(f"   级别: 未匹配")
        print(f"   默认建议: PRIVATE-R (保守处理)")


def cmd_classify_dir(args):
    """分级整个目录"""
    engine = ClassificationEngine()
    path = Path(args.path)
    
    if not path.exists():
        print(f"错误: 路径不存在: {args.path}")
        return 1
    
    if not path.is_dir():
        print(f"错误: 不是目录: {args.path}")
        return 1
    
    files = []
    for root, dirs, filenames in os.walk(path):
        # 排除常见缓存目录
        dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__', '.git', '.cache']]
        
        for filename in filenames:
            files.append(os.path.join(root, filename))
        
        if len(files) >= args.limit:
            break
    
    print(f"正在分级 {len(files)} 个文件...")
    print()
    
    results = engine.classify_batch(files[:args.limit])
    
    # 统计
    stats = {}
    for r in results:
        level = r.level or '未分级'
        stats[level] = stats.get(level, 0) + 1
    
    # 按级别分组显示
    level_order = ['PRIVATE-C', 'PRIVATE-B', 'PRIVATE-W', 'PRIVATE-R', 'INTERNAL', 'PUBLIC', '未分级']
    
    print("📊 分级统计:")
    print()
    for level in level_order:
        if level in stats:
            count = stats[level]
            emoji = {
                'PRIVATE-C': '🔴',
                'PRIVATE-B': '🟠', 
                'PRIVATE-W': '🟡',
                'PRIVATE-R': '🔵',
                'INTERNAL': '⚪',
                'PUBLIC': '🟢',
                '未分级': '⚫'
            }.get(level, '⚪')
            print(f"   {emoji} {level:12s}: {count:4d} 个文件")
    
    print()
    print("📋 详细结果:")
    print()
    
    # 显示前20个
    display_count = min(len(results), 20)
    for r in results[:display_count]:
        level_str = r.level or '未分级'
        if r.source == 'excluded':
            print(f"  [排除] {r.path[:60]}...")
        else:
            print(f"  [{level_str:10s}] {r.path[:50]}...")
    
    if len(results) > display_count:
        print(f"  ... 还有 {len(results) - display_count} 个文件")


def cmd_stats(args):
    """显示规则统计"""
    engine = ClassificationEngine()
    stats = engine.get_rule_stats()
    
    print("📊 规则引擎统计")
    print()
    print(f"  总规则数:    {stats['total_rules']}")
    print(f"  精确匹配:    {stats['exact_rules']}")
    print(f"  Glob规则:    {stats['glob_rules']}")
    print(f"  前缀匹配:    {stats['prefix_rules']}")
    print(f"  排除规则:    {stats['exclusion_rules']}")
    print()
    print(f"  规则文件:    {engine.rule_loader.system_rules_path}")


def cmd_reload(args):
    """重新加载规则"""
    engine = ClassificationEngine()
    engine.reload_rules()
    print("✅ 规则已重新加载")


def main():
    parser = argparse.ArgumentParser(
        prog='icctl',
        description='内控 Skills 命令行工具'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # classify 命令
    classify_parser = subparsers.add_parser('classify', help='分级文件或目录')
    classify_parser.add_argument('path', help='文件或目录路径')
    classify_parser.set_defaults(func=cmd_classify)
    
    # classify-dir 命令
    dir_parser = subparsers.add_parser('classify-dir', help='分级整个目录')
    dir_parser.add_argument('path', help='目录路径')
    dir_parser.add_argument('-l', '--limit', type=int, default=1000,
                           help='最大处理文件数 (默认: 1000)')
    dir_parser.set_defaults(func=cmd_classify_dir)
    
    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='显示规则统计')
    stats_parser.set_defaults(func=cmd_stats)
    
    # reload 命令
    reload_parser = subparsers.add_parser('reload', help='重新加载规则')
    reload_parser.set_defaults(func=cmd_reload)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main() or 0)
