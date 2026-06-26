#!/usr/bin/env python3
"""
ControlMemory 智能检索模块（带质量评分）
成功借鉴 - 2×失败次数 = 质量评分
评分高的优先
"""

import os
import re
from pathlib import Path
from difflib import SequenceMatcher

# 颜色输出
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_color(color, text):
    print(f"{color}{text}{Colors.NC}")

class OperationSearcher:
    def __init__(self):
        """初始化检索器"""
        self.script_dir = Path(__file__).parent
        # controlmemory.md 在 scripts 的上级目录
        self.memory_file = self.script_dir.parent / "controlmemory.md"
    
    def search_similar(self, user_command, threshold=0.5):
        """
        搜索相似操作（带质量评分排序）
        
        评分规则：质量评分 = 借鉴次数 - 2×失败次数
        """
        if not self.memory_file.exists():
            return []
        
        content = self.memory_file.read_text()
        operations = self.parse_operations(content)
        
        similar_ops = []
        for op in operations:
            # 计算命令相似度
            similarity = self.calculate_similarity(user_command, op['command'])
            
            if similarity >= threshold:
                op['similarity'] = similarity
                
                # 🎯 关键改进：计算质量评分
                usage = op.get('usage_count', 0)
                fails = op.get('fail_count', 0)
                op['quality_score'] = usage - 2 * fails
                
                similar_ops.append(op)
        
        # 🎯 按质量评分排序（高的优先）
        similar_ops.sort(key=lambda x: (x.get('quality_score', 0), x['similarity']), reverse=True)
        
        return similar_ops
    
    def calculate_similarity(self, text1, text2):
        """计算文本相似度"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def parse_operations(self, content):
        """解析操作记录（包含借鉴次数和失败次数）"""
        operations = []
        
        current_app = None
        current_op = None
        
        lines = content.split('\n')
        for line in lines:
            # 应用标题
            if line.startswith('### '):
                current_app = line.replace('### ', '').strip()
            
            # 操作标题
            elif line.startswith('#### '):
                if current_op:
                    operations.append(current_op)
                current_op = {
                    'app': current_app,
                    'name': line.replace('#### ', '').strip(),
                    'command': '',
                    'script': '',
                    'success_rate': '',
                    'usage_count': 0,
                    'fail_count': 0,
                    'quality_score': 0,
                    'notes': ''
                }
            
            # 属性
            elif current_op:
                if '**命令**:' in line:
                    match = re.search(r'\*\*命令\*\*: "(.+?)"', line)
                    if match:
                        commands = match.group(1).split('"、"')
                        current_op['command'] = commands[0].strip('"')
                elif '**执行**:' in line:
                    match = re.search(r'\*\*执行\*\*: `(.+?)`', line)
                    if match:
                        current_op['script'] = match.group(1)
                elif '**成功率**:' in line:
                    current_op['success_rate'] = line.split('**成功率**:')[1].strip()
                elif '**备注**:' in line:
                    current_op['notes'] = line.split('**备注**:')[1].strip()
                elif '**借鉴次数**:' in line:
                    match = re.search(r'👁️ (\d+)', line)
                    if match:
                        current_op['usage_count'] = int(match.group(1))
                elif '**失败次数**:' in line:
                    match = re.search(r'❌ (\d+)', line)
                    if match:
                        current_op['fail_count'] = int(match.group(1))
        
        # 添加最后一个
        if current_op:
            operations.append(current_op)
        
        return operations
    
    def find_best_match(self, user_command, threshold=0.5):
        """
        查找最佳匹配（质量评分优先）
        """
        similar_ops = self.search_similar(user_command, threshold)
        
        if similar_ops:
            return similar_ops[0]  # 返回质量评分最高的
        return None
    
    def find_all_for_app(self, app_name):
        """
        查找某个应用的所有操作（按质量评分排序）
        """
        if not self.memory_file.exists():
            return []
        
        content = self.memory_file.read_text()
        operations = self.parse_operations(content)
        
        # 过滤出指定应用
        app_ops = [op for op in operations if op['app'] == app_name]
        
        # 计算质量评分并排序
        for op in app_ops:
            op['quality_score'] = op.get('usage_count', 0) - 2 * op.get('fail_count', 0)
        
        app_ops.sort(key=lambda x: x['quality_score'], reverse=True)
        
        return app_ops
    
    def can_complete_task(self, operation, user_command):
        """分析操作是否能完成用户任务"""
        if not operation:
            return False, "未找到相似操作"
        
        usage = operation.get('usage_count', 0)
        fails = operation.get('fail_count', 0)
        quality = usage - 2 * fails
        success_rate = operation.get('success_rate', '0%')
        
        # 计算实际成功率
        if usage + fails > 0:
            actual_rate = usage / (usage + fails) * 100
        else:
            actual_rate = 100
        
        if quality > 100:
            return True, f"🔥 热门优质操作（评分{quality}），成功率{actual_rate:.0f}%"
        elif quality > 50:
            return True, f"⭐ 高质量操作（评分{quality}），成功率{actual_rate:.0f}%"
        elif quality > 0:
            return True, f"✅ 可靠操作（评分{quality}），成功率{actual_rate:.0f}%"
        elif quality > -20:
            return True, f"⚠️ 一般操作（评分{quality}），成功率{actual_rate:.0f}%"
        else:
            return True, f"❗ 低质量操作（评分{quality}），成功率{actual_rate:.0f}%（失败较多）"
    
    def increment_usage(self, operation_name, app_name):
        """增加借鉴次数"""
        if not self.memory_file.exists():
            return False
        
        content = self.memory_file.read_text()
        
        # 找到并更新借鉴次数
        pattern = rf'(#### {re.escape(operation_name)}\n.*?- \*\*借鉴次数\*\*: 👁️ )(\d+)'
        
        def replace_count(match):
            prefix = match.group(1)
            count = int(match.group(2))
            return f"{prefix}{count + 1}"
        
        new_content = re.sub(pattern, replace_count, content, flags=re.DOTALL)
        
        if new_content != content:
            self.memory_file.write_text(new_content)
            print_color(Colors.GREEN, f"📊 借鉴次数 +1")
            return True
        
        return False
    
    def increment_failure(self, operation_name, app_name):
        """
        增加失败次数
        
        Args:
            operation_name: 操作名称
            app_name: 应用名称
        """
        if not self.memory_file.exists():
            return False
        
        content = self.memory_file.read_text()
        
        # 找到并更新失败次数
        pattern = rf'(#### {re.escape(operation_name)}\n.*?- \*\*失败次数\*\*: ❌ )(\d+)'
        
        def replace_count(match):
            prefix = match.group(1)
            count = int(match.group(2))
            return f"{prefix}{count + 1}"
        
        new_content = re.sub(pattern, replace_count, content, flags=re.DOTALL)
        
        if new_content != content:
            self.memory_file.write_text(new_content)
            print_color(Colors.YELLOW, f"❌ 失败次数 +1")
            return True
        
        return False
    
    def execute_operation(self, operation):
        """执行操作"""
        script = operation.get('script', '')
        if not script:
            print_color(Colors.RED, "❌ 操作无执行脚本")
            return False
        
        print_color(Colors.BLUE, f"🚀 执行操作：{script}")
        
        import subprocess
        try:
            result = subprocess.run(script, shell=True, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print_color(Colors.GREEN, "✅ 操作成功！")
                return True
            else:
                print_color(Colors.RED, f"❌ 操作失败：{result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print_color(Colors.RED, "❌ 操作超时")
            return False
        except Exception as e:
            print_color(Colors.RED, f"❌ 执行错误：{e}")
            return False


def main():
    """命令行测试"""
    searcher = OperationSearcher()
    
    # 测试搜索
    test_commands = [
        "打开 Safari",
        "截个屏",
        "用 QQ 发消息",
        "显示电脑配置"
    ]
    
    for cmd in test_commands:
        print_color(Colors.BLUE, f"\n🔍 搜索：{cmd}")
        best_match = searcher.find_best_match(cmd)
        
        if best_match:
            print_color(Colors.GREEN, f"✅ 找到匹配：{best_match['app']} - {best_match['name']}")
            print(f"   借鉴次数：👁️ {best_match.get('usage_count', 0)}")
            print(f"   失败次数：❌ {best_match.get('fail_count', 0)}")
            print(f"   质量评分：{best_match.get('quality_score', 0)}")
            print(f"   命令：{best_match['command']}")
            print(f"   脚本：{best_match['script']}")
            print(f"   成功率：{best_match['success_rate']}")
            
            can_do, reason = searcher.can_complete_task(best_match, cmd)
            print(f"   📊 分析：{reason}")
        else:
            print_color(Colors.YELLOW, "⚠️  未找到匹配操作")


if __name__ == "__main__":
    main()
