#!/usr/bin/env python3
"""
审核机制模块
管理和验证操作记录
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 颜色输出
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_color(color, text):
    print(f"{color}{text}{Colors.NC}")

class ReviewSystem:
    def __init__(self):
        """初始化审核系统"""
        self.script_dir = Path(__file__).parent
        self.memory_file = self.script_dir / "controlmemory.md"
        self.review_file = self.script_dir / ".review_queue.json"
    
    def get_pending_reviews(self):
        """获取待审核操作"""
        if not self.memory_file.exists():
            return []
        
        content = self.memory_file.read_text()
        pending = []
        
        # 查找待验证操作
        pattern = r'#### (.+?)\n.*?\*\*验证状态\*\*: ⏳ 待验证'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            op_name = match.strip()
            pending.append(op_name)
        
        return pending
    
    def verify_operation(self, operation_name, verified=True):
        """
        验证操作
        
        Args:
            operation_name: 操作名称
            verified: 是否验证通过
        """
        if not self.memory_file.exists():
            print_color(Colors.RED, "❌ Memory 文件不存在")
            return False
        
        content = self.memory_file.read_text()
        
        # 更新验证状态
        if verified:
            old_status = "**验证状态**: ⏳ 待验证"
            new_status = "**验证状态**: ✅ 已验证"
        else:
            old_status = "**验证状态**: ⏳ 待验证"
            new_status = "**验证状态**: ❌ 未通过"
        
        # 查找并替换
        if operation_name in content:
            new_content = content.replace(old_status, new_status, 1)
            self.memory_file.write_text(new_content)
            
            status = "✅ 已验证" if verified else "❌ 未通过"
            print_color(Colors.GREEN, f"✅ 操作 '{operation_name}' 已标记为 {status}")
            return True
        else:
            print_color(Colors.RED, f"❌ 未找到操作：{operation_name}")
            return False
    
    def test_operation(self, operation_name):
        """
        测试操作
        
        Args:
            operation_name: 操作名称
        """
        print_color(Colors.BLUE, f"🧪 测试操作：{operation_name}")
        
        # 解析操作脚本
        script = self.extract_script(operation_name)
        
        if not script:
            print_color(Colors.RED, "❌ 未找到执行脚本")
            return False
        
        print_color(Colors.BLUE, f"🚀 执行：{script}")
        
        import subprocess
        try:
            result = subprocess.run(script, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print_color(Colors.GREEN, "✅ 测试通过！")
                self.verify_operation(operation_name, True)
                return True
            else:
                print_color(Colors.RED, f"❌ 测试失败：{result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print_color(Colors.RED, "❌ 测试超时")
            return False
        except Exception as e:
            print_color(Colors.RED, f"❌ 测试错误：{e}")
            return False
    
    def extract_script(self, operation_name):
        """提取操作的执行脚本"""
        if not self.memory_file.exists():
            return None
        
        content = self.memory_file.read_text()
        
        # 查找操作
        pattern = rf'#### {re.escape(operation_name)}\n.*?\*\*执行\*\*: `(.+?)`'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return None
    
    def list_pending(self):
        """列出待审核操作"""
        pending = self.get_pending_reviews()
        
        print_color(Colors.BLUE, "╔════════════════════════════════════════╗")
        print_color(Colors.BLUE, "║   📋 待审核操作                        ║")
        print_color(Colors.BLUE, "╚════════════════════════════════════════╝")
        print()
        
        if not pending:
            print_color(Colors.GREEN, "✅ 无待审核操作")
            return
        
        for i, op in enumerate(pending, 1):
            print(f"{i}. {op}")
        
        print()
        print(f"共 {len(pending)} 个待审核操作")
    
    def review_all(self):
        """审核所有待验证操作"""
        pending = self.get_pending_reviews()
        
        if not pending:
            print_color(Colors.GREEN, "✅ 无待审核操作")
            return
        
        print_color(Colors.BLUE, f"📋 开始审核 {len(pending)} 个操作...")
        print()
        
        passed = 0
        failed = 0
        
        for op in pending:
            print(f"审核：{op}")
            if self.test_operation(op):
                passed += 1
            else:
                failed += 1
            print()
        
        print_color(Colors.BLUE, "╔════════════════════════════════════════╗")
        print_color(Colors.BLUE, "║   审核完成                           ║")
        print_color(Colors.BLUE, "╚════════════════════════════════════════╝")
        print(f"通过：{passed}")
        print(f"失败：{failed}")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='审核系统')
    parser.add_argument('--list', action='store_true', help='列出待审核操作')
    parser.add_argument('--verify', metavar='操作名', help='验证操作')
    parser.add_argument('--reject', metavar='操作名', help='拒绝操作')
    parser.add_argument('--test', metavar='操作名', help='测试操作')
    parser.add_argument('--all', action='store_true', help='审核所有')
    
    args = parser.parse_args()
    
    review = ReviewSystem()
    
    if args.list:
        review.list_pending()
    elif args.verify:
        review.verify_operation(args.verify, True)
    elif args.reject:
        review.verify_operation(args.reject, False)
    elif args.test:
        review.test_operation(args.test)
    elif args.all:
        review.review_all()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
