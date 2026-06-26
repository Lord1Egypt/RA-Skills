#!/usr/bin/env python3
"""
ControlMemory - 操作行为记录模块（带成功/失败双指标）
成功借鉴 - 2×失败次数 = 质量评分
"""

import os
import sys
import json
import hashlib
import uuid
import re
from datetime import datetime
from pathlib import Path

# 颜色输出
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_color(color, text):
    print(f"{color}{text}{Colors.NC}")

class ControlMemory:
    def __init__(self):
        """初始化 ControlMemory"""
        self.script_dir = Path(__file__).parent
        # controlmemory.md 在 scripts 的上级目录
        self.memory_file = self.script_dir.parent / "controlmemory.md"
        self.user_id = self.get_user_id()
        
        # 确保文件存在
        if not self.memory_file.exists():
            self.create_template()
    
    def get_user_id(self):
        """获取用户 ID（匿名化）"""
        import socket
        import getpass
        user_str = f"{socket.gethostname()}_{getpass.getuser()}"
        return hashlib.md5(user_str.encode()).hexdigest()[:8]
    
    def create_template(self):
        """创建模板文件"""
        print_color(Colors.YELLOW, "⚠️  ControlMemory 文件不存在，创建模板...")
        template_file = self.script_dir / "controlmemory.md"
        if template_file.exists():
            print_color(Colors.GREEN, "✅ 使用现有模板")
        else:
            print_color(Colors.RED, "❌ 模板文件不存在")
    
    def record_success(self, app_name, command, script, success_rate="100%", 
                      notes="", permissions="无"):
        """记录成功操作（新操作）"""
        print_color(Colors.BLUE, f"📝 记录成功操作：{app_name} - {command}")
        
        record = {
            'id': str(uuid.uuid4())[:8],
            'app': app_name,
            'command': command,
            'script': script,
            'success_rate': success_rate,
            'notes': notes,
            'permissions': permissions,
            'contributor': self.user_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d'),
            'verified': False,
            'usage_count': 0,
            'fail_count': 0
        }
        
        if self.is_duplicate(record):
            print_color(Colors.YELLOW, "⚠️  操作已存在")
            return False
        
        self.append_to_memory(record)
        print_color(Colors.GREEN, "✅ 记录成功")
        self.trigger_sync()
        return True
    
    def increment_usage(self, app_name, command):
        """增加借鉴次数（成功使用已有操作）"""
        print_color(Colors.BLUE, f"📊 增加借鉴次数：{app_name} - {command}")
        
        if not self.memory_file.exists():
            return False
        
        content = self.memory_file.read_text()
        
        # 找到操作并增加借鉴次数
        # 支持格式：👁️ 0 或 👁️150
        pattern = rf'(### {re.escape(app_name)}\n.*?#### .+?\n.*?- \*\*命令\*\*: ".+?{re.escape(command)}.+?".*?- \*\*借鉴次数\*\*: 👁️\s*)(\d+)'
        
        def replace_count(match):
            prefix = match.group(1)
            count = int(match.group(2))
            return f"{prefix}{count + 1}"
        
        new_content = re.sub(pattern, replace_count, content, flags=re.DOTALL)
        
        if new_content != content:
            self.memory_file.write_text(new_content)
            print_color(Colors.GREEN, f"✅ 借鉴次数 +1")
            self.update_statistics()
            return True
        else:
            print_color(Colors.YELLOW, "⚠️  未找到操作")
            return False
    
    def increment_failure(self, app_name, command):
        """
        增加失败次数（操作失败）
        
        Args:
            app_name: 应用名称
            command: 失败的命令
        """
        print_color(Colors.YELLOW, f"❌ 增加失败次数：{app_name} - {command}")
        
        if not self.memory_file.exists():
            return False
        
        content = self.memory_file.read_text()
        
        # 找到操作并增加失败次数
        # 支持格式：❌ 0 或 ❌5
        pattern = rf'(### {re.escape(app_name)}\n.*?#### .+?\n.*?- \*\*命令\*\*: ".+?{re.escape(command)}.+?".*?- \*\*失败次数\*\*: ❌\s*)(\d+)'
        
        def replace_count(match):
            prefix = match.group(1)
            count = int(match.group(2))
            return f"{prefix}{count + 1}"
        
        new_content = re.sub(pattern, replace_count, content, flags=re.DOTALL)
        
        if new_content != content:
            self.memory_file.write_text(new_content)
            print_color(Colors.YELLOW, f"❌ 失败次数 +1")
            self.update_statistics()
            return True
        else:
            print_color(Colors.YELLOW, "⚠️  未找到操作")
            return False
    
    def is_duplicate(self, new_record):
        """检查是否重复"""
        if not self.memory_file.exists():
            return False
        
        content = self.memory_file.read_text()
        app = new_record['app']
        command = new_record['command']
        script = new_record['script']
        
        if f"### {app}" in content:
            if f'**命令**: "{command}"' in content:
                return True
            if f'**执行**: `{script}`' in content:
                return True
        
        return False
    
    def append_to_memory(self, record):
        """添加到记忆文档"""
        content = self.memory_file.read_text()
        
        operations_marker = "## 🎯 操作记录"
        if operations_marker not in content:
            print_color(Colors.RED, "❌ 文档格式错误")
            return
        
        new_operation = f"""
### {record['app']}

#### {self.get_operation_name(record['command'])}
- **命令**: "{record['command']}"
- **执行**: `{record['script']}`
- **成功率**: {record['success_rate']}
- **耗时**: <5 秒
- **备注**: {record['notes']}
- **权限**: {record['permissions']}
- **贡献者**: {record['contributor']}
- **添加时间**: {record['timestamp']}
- **验证状态**: ⏳ 待验证
- **借鉴次数**: 👁️ 0
- **失败次数**: ❌ 0
- **质量评分**: 0 (成功 -2×失败)

---
"""
        parts = content.split(operations_marker, 1)
        if len(parts) == 2:
            new_content = parts[0] + operations_marker + "\n" + new_operation + parts[1]
        else:
            new_content = content + "\n" + new_operation
        
        new_content = self.update_statistics(new_content)
        self.memory_file.write_text(new_content)
    
    def get_operation_name(self, command):
        """从命令提取操作名称"""
        return command.replace('"', '').replace('打开', '').replace('关闭', '').strip()
    
    def update_statistics(self, content=None):
        """更新统计信息"""
        if content is None:
            if not self.memory_file.exists():
                return ""
            content = self.memory_file.read_text()
        
        # 解析所有操作
        app_stats = {}
        total_usage = 0
        total_fails = 0
        
        app_pattern = r'### (.+?)\n(.*?)(?=### |\Z)'
        for match in re.finditer(app_pattern, content, re.DOTALL):
            app_name = match.group(1).strip()
            app_content = match.group(2)
            
            op_count = len(re.findall(r'#### ', app_content))
            usage_matches = re.findall(r'\*\*借鉴次数\*\*: 👁️ (\d+)', app_content)
            fail_matches = re.findall(r'\*\*失败次数\*\*: ❌ (\d+)', app_content)
            
            app_usage = sum(int(x) for x in usage_matches)
            app_fails = sum(int(x) for x in fail_matches)
            
            # 计算平均成功率
            if app_usage + app_fails > 0:
                avg_rate = app_usage / (app_usage + app_fails) * 100
            else:
                avg_rate = 100
            
            app_stats[app_name] = {
                'ops': op_count,
                'usage': app_usage,
                'fails': app_fails,
                'rate': avg_rate
            }
            total_usage += app_usage
            total_fails += app_fails
        
        # 生成统计表格
        stats_table = "| 应用 | 成功操作数 | 总借鉴次数 | 总失败次数 | 平均成功率 | 最后更新 |\n"
        stats_table += "|------|-----------|-----------|-----------|-----------|---------|\n"
        
        for app, data in app_stats.items():
            stats_table += f"| {app} | {data['ops']} | {data['usage']} | {data['fails']} | {data['rate']:.0f}% | {datetime.now().strftime('%Y-%m-%d')} |\n"
        
        total_ops = sum(d['ops'] for d in app_stats.values())
        total_rate = total_usage / (total_usage + total_fails) * 100 if (total_usage + total_fails) > 0 else 100
        stats_table += f"| **总计** | **{total_ops}** | **{total_usage}** | **{total_fails}** | **{total_rate:.0f}%** | - |"
        
        # 替换统计部分
        stats_marker = "## 📊 统计信息"
        if stats_marker in content:
            start = content.find(stats_marker)
            end = content.find("\n\n##", start)
            if end == -1:
                end = content.find("\n---", start)
            if end != -1:
                content = content[:start] + f"## 📊 统计信息\n\n{stats_table}\n\n" + content[end:]
        
        return content
    
    def trigger_sync(self):
        """触发 ClawHub 同步"""
        print_color(Colors.BLUE, "🔄 触发 ClawHub 同步...")
        sync_script = self.script_dir / "clawhub_sync.py"
        
        if sync_script.exists():
            os.system(f"python3 {sync_script}")
        else:
            print_color(Colors.YELLOW, "⚠️  同步脚本不存在，跳过同步")


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ControlMemory - 操作记录工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 记录命令
    record_parser = subparsers.add_parser('record', help='记录成功操作')
    record_parser.add_argument('--app', required=True, help='应用名称')
    record_parser.add_argument('--command', required=True, help='自然语言命令')
    record_parser.add_argument('--script', required=True, help='执行脚本')
    record_parser.add_argument('--rate', default='100%', help='成功率')
    record_parser.add_argument('--notes', default='', help='备注')
    record_parser.add_argument('--perms', default='无', help='所需权限')
    
    # 增加借鉴
    usage_parser = subparsers.add_parser('usage', help='增加借鉴次数')
    usage_parser.add_argument('--app', required=True, help='应用名称')
    usage_parser.add_argument('--command', required=True, help='命令')
    
    # 增加失败
    fail_parser = subparsers.add_parser('fail', help='增加失败次数')
    fail_parser.add_argument('--app', required=True, help='应用名称')
    fail_parser.add_argument('--command', required=True, help='命令')
    
    args = parser.parse_args()
    
    memory = ControlMemory()
    
    if args.command == 'record':
        memory.record_success(
            app_name=args.app,
            command=args.command,
            script=args.script,
            success_rate=args.rate,
            notes=args.notes,
            permissions=args.perms
        )
    elif args.command == 'usage':
        memory.increment_usage(args.app, args.command)
    elif args.command == 'fail':
        memory.increment_failure(args.app, args.command)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
