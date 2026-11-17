#!/usr/bin/env python3
"""
每日知识库同步脚本 v1.0
功能：从腾讯文档读取最新数据，保存到本地JSON文件
调度：每日早上8:00自动执行（通过WorkBuddy自动化）

使用方式：
  python3 sync_knowledge_base.py --project meilan-center --all
  python3 sync_knowledge_base.py --project meilan-center --sheet 房源销控表
"""

import os
import sys
import json
import argparse
from datetime import datetime

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.knowledge_base import KnowledgeBase

def sync_sheet(project_id, sheet_name, kb):
    """
    同步单个数据表
    """
    print(f"📡 同步 {sheet_name} ...")
    
    # 从腾讯文档读取（强制刷新，不使用缓存）
    data, error = kb.load(sheet_name, use_cache=False)
    
    if error:
        print(f"   ❌ 同步失败：{error}")
        return False
    
    # 保存到本地
    save_path = kb.save(sheet_name, data)
    
    if save_path:
        print(f"   ✅ 同步成功：{len(data.get('records', []))} 条记录")
        print(f"      保存位置：{save_path}")
        return True
    else:
        print(f"   ❌ 保存失败")
        return False

def main():
    parser = argparse.ArgumentParser(description='每日知识库同步脚本')
    parser.add_argument('--project', type=str, default='meilan-center',
                        help='项目ID（默认：meilan-center）')
    parser.add_argument('--sheet', type=str, default=None,
                        help='指定同步的数据表（默认：全部）')
    parser.add_argument('--all', action='store_true',
                        help='同步所有数据表')
    
    args = parser.parse_args()
    
    print(f"🚀 开始同步知识库")
    print(f"   项目：{args.project}")
    print(f"   时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 初始化知识库
    kb = KnowledgeBase(project_id=args.project)
    
    # 定义需要同步的数据表
    sheets_to_sync = [
        "房源销控表",
        "租金报价表",
        "配套资源表",
        "客户跟进记录",  # 可选：客户记录变化频繁，也可不同步
    ]
    
    # 如果指定了单个sheet，只同步该sheet
    if args.sheet:
        sheets_to_sync = [args.sheet]
    
    # 执行同步
    success_count = 0
    total_count = len(sheets_to_sync)
    
    for sheet_name in sheets_to_sync:
        print(f"[{sheets_to_sync.index(sheet_name) + 1}/{total_count}] ", end='')
        result = sync_sheet(args.project, sheet_name, kb)
        if result:
            success_count += 1
        print()
    
    # 输出同步报告
    print("=" * 50)
    print(f"✅ 同步完成：{success_count}/{total_count} 个数据表")
    print(f"   项目目录：{kb.project_dir}")
    print(f"   同步时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_count == total_count:
        print(f"\n🎉 所有数据表同步成功！AI现在可以极速读取本地数据。")
        return 0
    else:
        print(f"\n⚠️ 部分数据表同步失败，请检查配置。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
