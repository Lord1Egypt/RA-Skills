#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共享文件夹记忆同步系统 - 命令行接口

使用方法：
python shared_memory_cli.py [command] [options]

命令：
  sync-hermes-to-openclaw    Hermes → OpenClaw 同步
  sync-openclaw-to-hermes    OpenClaw → Hermes 同步
  sync-bidirectional         双向同步
  cleanup                    清理记忆文件
  full-workflow              完整工作流（清理 + 同步）
  status                     系统状态
  help                       显示帮助

选项：
  --min-importance N        最小重要性阈值 (默认: 7)
  --limit N                 导出限制数量 (默认: 20)
  --clean-hermes            清理 Hermes 记忆
  --clean-openclaw          清理 OpenClaw 记忆
"""

import argparse
import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from shared_folder_sync import SharedFolderSync
from hermes_exporter import HermesMemoryExporter
from openclaw_importer import OpenClawMemoryImporter
from openclaw_exporter import OpenClawMemoryExporter
from hermes_importer import HermesMemoryImporter
from memory_cleaner import MemoryCleaner
from shared_memory_controller import SharedMemoryController

import json
from datetime import datetime

def print_result(result: dict, indent: int = 2):
    """打印结果"""
    print(json.dumps(result, ensure_ascii=False, indent=indent))

def main():
    parser = argparse.ArgumentParser(
        description='共享文件夹记忆同步系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'command',
        choices=[
            'sync-hermes-to-openclaw',
            'sync-openclaw-to-hermes', 
            'sync-bidirectional',
            'cleanup',
            'full-workflow',
            'status',
            'help'
        ],
        help='要执行的命令'
    )
    
    parser.add_argument(
        '--min-importance',
        type=int,
        default=7,
        help='最小重要性阈值 (默认: 7)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=20,
        help='导出限制数量 (默认: 20)'
    )
    
    parser.add_argument(
        '--clean-hermes',
        action='store_true',
        help='清理 Hermes 记忆'
    )
    
    parser.add_argument(
        '--clean-openclaw',
        action='store_true',
        help='清理 OpenClaw 记忆'
    )
    
    args = parser.parse_args()
    
    # 初始化控制器
    controller = SharedMemoryController()
    
    # 执行命令
    if args.command == 'sync-hermes-to-openclaw':
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行 Hermes → OpenClaw 同步")
        result = controller.run_hermes_to_openclaw_sync()
        print_result(result)
        
    elif args.command == 'sync-openclaw-to-hermes':
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行 OpenClaw → Hermes 同步")
        result = controller.run_openclaw_to_hermes_sync()
        print_result(result)
        
    elif args.command == 'sync-bidirectional':
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行双向同步")
        result = controller.run_bidirectional_sync()
        print_result(result)
        
    elif args.command == 'cleanup':
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行记忆清理")
        clean_hermes = args.clean_hermes or True  # 默认清理 Hermes
        clean_openclaw = args.clean_openclaw or True  # 默认清理 OpenClaw
        result = controller.run_memory_cleanup(
            clean_hermes=clean_hermes,
            clean_openclaw=clean_openclaw
        )
        print_result(result)
        
    elif args.command == 'full-workflow':
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 执行完整工作流")
        result = controller.run_full_workflow()
        print_result(result)
        
    elif args.command == 'status':
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 系统状态")
        result = controller.get_status()
        print_result(result)
        
    elif args.command == 'help':
        parser.print_help()
        
    else:
        print(f"未知命令: {args.command}")
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()