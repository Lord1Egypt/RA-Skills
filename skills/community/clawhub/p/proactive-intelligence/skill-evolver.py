# -*- coding: utf-8 -*-
"""Proactive Intelligence - 技能进化器

自动分析、编辑和升级其他技能的代码。
"""

import os
import sys
import json
import shutil
import re
from pathlib import Path
from datetime import datetime
import ast
import difflib

# 设置标准输出编码
sys.stdout.reconfigure(encoding='utf-8')

class SkillEvolver:
    def __init__(self):
        self.skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
        self.memory_dir = Path.home() / "proactive-intelligence"
        self.backup_dir = self.memory_dir / "skill-backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def log(self, message, level="INFO"):
        """记录日志"""
        print(f"[{level}] {message}")
    
    def backup_skill(self, skill_name):
        """备份技能"""
        skill_path = self.skills_dir / skill_name
        if not skill_path.exists():
            self.log(f"技能不存在: {skill_name}", "ERROR")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"{skill_name}_{timestamp}"
        
        try:
            shutil.copytree(skill_path, backup_path)
            self.log(f"已备份技能到: {backup_path}")
            return backup_path
        except Exception as e:
            self.log(f"备份失败: {e}", "ERROR")
            return None
    
    def analyze_skill(self, skill_name):
        """分析技能代码"""
        skill_path = self.skills_dir / skill_name
        if not skill_path.exists():
            self.log(f"技能不存在: {skill_name}", "ERROR")
            return None
        
        analysis = {
            'name': skill_name,
            'path': str(skill_path),
            'files': [],
            'issues': [],
            'suggestions': [],
            'complexity': {},
            'dependencies': []
        }
        
        # 分析所有文件
        for file_path in skill_path.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                file_analysis = self.analyze_file(file_path)
                analysis['files'].append(file_analysis)
                
                # 收集问题
                if file_analysis['issues']:
                    analysis['issues'].extend(file_analysis['issues'])
                
                # 收集建议
                if file_analysis['suggestions']:
                    analysis['suggestions'].extend(file_analysis['suggestions'])
        
        # 统计复杂度
        analysis['complexity'] = self.calculate_complexity(analysis['files'])
        
        # 检查依赖
        analysis['dependencies'] = self.check_dependencies(skill_path)
        
        return analysis
    
    def analyze_file(self, file_path):
        """分析单个文件"""
        analysis = {
            'path': str(file_path.relative_to(self.skills_dir)),
            'type': file_path.suffix,
            'size': file_path.stat().st_size,
            'issues': [],
            'suggestions': []
        }
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # 检查常见问题
            analysis['issues'] = self.detect_issues(content, lines, file_path)
            analysis['suggestions'] = self.detect_improvements(content, lines, file_path)
            
        except Exception as e:
            analysis['issues'].append(f"读取失败: {e}")
        
        return analysis
    
    def detect_issues(self, content, lines, file_path):
        """检测代码问题"""
        issues = []
        
        # Python 文件检查
        if file_path.suffix == '.py':
            try:
                ast.parse(content)
            except SyntaxError as e:
                issues.append(f"语法错误: {e}")
            
            # 检查常见问题
            for i, line in enumerate(lines, 1):
                # 硬编码路径
                if 'C:\\' in line or '/Users/' in line:
                    issues.append(f"行 {i}: 硬编码路径")
                
                # 缺少编码声明
                if i == 1 and not line.startswith('# -*- coding'):
                    issues.append("缺少编码声明")
                
                # 未使用的导入
                if line.startswith('import ') or line.startswith('from '):
                    if 'as _' not in line:  # 忽略有意忽略的导入
                        # 简单检查是否在代码中使用
                        module = line.split()[-1]
                        if module not in content[len(line):]:
                            issues.append(f"行 {i}: 可能未使用的导入")
        
        # Markdown 文件检查
        elif file_path.suffix == '.md':
            # 检查链接格式
            for i, line in enumerate(lines, 1):
                if '[' in line and ']' in line and '(' not in line:
                    if ']]' not in line:  # 忽略 wikilink
                        issues.append(f"行 {i}: 可能的损坏链接")
        
        # JavaScript 文件检查
        elif file_path.suffix == '.js':
            # 检查 console.log
            for i, line in enumerate(lines, 1):
                if 'console.log' in line:
                    issues.append(f"行 {i}: 包含 console.log")
        
        return issues
    
    def detect_improvements(self, content, lines, file_path):
        """检测改进建议"""
        suggestions = []
        
        if file_path.suffix == '.py':
            # 检查函数长度
            in_function = False
            function_start = 0
            function_name = ""
            
            for i, line in enumerate(lines, 1):
                if line.startswith('def '):
                    if in_function and i - function_start > 50:
                        suggestions.append(f"函数 {function_name} 过长 ({i - function_start} 行)")
                    in_function = True
                    function_start = i
                    function_name = line.split('(')[0].replace('def ', '')
                
                if line.startswith('class '):
                    if in_function and i - function_start > 50:
                        suggestions.append(f"函数 {function_name} 过长 ({i - function_start} 行)")
                    in_function = False
            
            # 检查重复代码
            unique_lines = set()
            duplicate_lines = []
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    if stripped in unique_lines:
                        duplicate_lines.append(i)
                    unique_lines.add(stripped)
            
            if len(duplicate_lines) > 5:
                suggestions.append(f"发现 {len(duplicate_lines)} 行重复代码")
            
            # 检查魔法数字
            for i, line in enumerate(lines, 1):
                if re.search(r'\b\d{3,}\b', line) and not line.strip().startswith('#'):
                    suggestions.append(f"行 {i}: 可能的魔法数字")
        
        return suggestions
    
    def calculate_complexity(self, files):
        """计算代码复杂度"""
        total_lines = 0
        total_files = len(files)
        total_issues = 0
        total_suggestions = 0
        
        for file in files:
            if 'lines' in file:
                total_lines += file['lines']
            total_issues += len(file.get('issues', []))
            total_suggestions += len(file.get('suggestions', []))
        
        return {
            'total_files': total_files,
            'total_lines': total_lines,
            'total_issues': total_issues,
            'total_suggestions': total_suggestions,
            'health_score': max(0, 100 - (total_issues * 10) - (total_suggestions * 5))
        }
    
    def check_dependencies(self, skill_path):
        """检查依赖"""
        dependencies = []
        
        # 检查 package.json
        package_json = skill_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'dependencies' in data:
                        dependencies.extend(data['dependencies'].keys())
                    if 'devDependencies' in data:
                        dependencies.extend(data['devDependencies'].keys())
            except:
                pass
        
        # 检查 requirements.txt
        requirements = skill_path / "requirements.txt"
        if requirements.exists():
            try:
                with open(requirements, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            dependencies.append(line.split('==')[0].split('>=')[0])
            except:
                pass
        
        return dependencies
    
    def fix_issues(self, skill_name, auto_fix=False):
        """修复问题"""
        analysis = self.analyze_skill(skill_name)
        if not analysis:
            return False
        
        if not analysis['issues']:
            self.log("没有发现问题", "INFO")
            return True
        
        self.log(f"发现 {len(analysis['issues'])} 个问题:", "INFO")
        for issue in analysis['issues']:
            self.log(f"  - {issue}", "INFO")
        
        if not auto_fix:
            response = input("\n是否自动修复这些问题? (y/N): ")
            if response.lower() != 'y':
                self.log("跳过修复", "INFO")
                return False
        
        # 备份
        backup_path = self.backup_skill(skill_name)
        if not backup_path:
            return False
        
        # 修复逻辑
        fixed_count = 0
        skill_path = self.skills_dir / skill_name
        
        for file_path in skill_path.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    content = file_path.read_text(encoding='utf-8')
                    original = content
                    
                    # 修复 Python 文件
                    if file_path.suffix == '.py':
                        # 添加编码声明
                        if not content.startswith('# -*- coding: utf-8 -*-'):
                            content = '# -*- coding: utf-8 -*-\n' + content
                            fixed_count += 1
                        
                        # 移除 console.log (如果有的话)
                        if 'console.log' in content:
                            content = content.replace('console.log(', '# console.log(')
                            fixed_count += 1
                    
                    # 如果有更改，写入文件
                    if content != original:
                        file_path.write_text(content, encoding='utf-8')
                        self.log(f"已修复: {file_path.relative_to(skill_path)}")
                
                except Exception as e:
                    self.log(f"修复失败 {file_path}: {e}", "ERROR")
        
        self.log(f"修复完成: {fixed_count} 个问题", "INFO")
        return True
    
    def enhance_skill(self, skill_name, enhancement_type="auto"):
        """增强技能"""
        analysis = self.analyze_skill(skill_name)
        if not analysis:
            return False
        
        if not analysis['suggestions']:
            self.log("没有发现可增强的点", "INFO")
            return True
        
        self.log(f"发现 {len(analysis['suggestions'])} 个增强建议:", "INFO")
        for suggestion in analysis['suggestions']:
            self.log(f"  - {suggestion}", "INFO")
        
        response = input("\n是否应用这些建议? (y/N): ")
        if response.lower() != 'y':
            self.log("跳过增强", "INFO")
            return False
        
        # 备份
        backup_path = self.backup_skill(skill_name)
        if not backup_path:
            return False
        
        # 增强逻辑
        self.log("增强功能开发中...", "INFO")
        return True
    
    def optimize_skill(self, skill_name):
        """优化技能"""
        analysis = self.analyze_skill(skill_name)
        if not analysis:
            return False
        
        self.log(f"技能健康分数: {analysis['complexity']['health_score']}/100", "INFO")
        
        if analysis['complexity']['health_score'] >= 80:
            self.log("技能状态良好，无需优化", "INFO")
            return True
        
        self.log("优化建议:", "INFO")
        if analysis['complexity']['total_issues'] > 0:
            self.log(f"  - 修复 {analysis['complexity']['total_issues']} 个问题", "INFO")
        if analysis['complexity']['total_suggestions'] > 0:
            self.log(f"  - 应用 {analysis['complexity']['total_suggestions']} 个改进建议", "INFO")
        
        return True
    
    def generate_report(self, skill_name):
        """生成详细报告"""
        analysis = self.analyze_skill(skill_name)
        if not analysis:
            return None
        
        report_file = self.memory_dir / f"skill-report-{skill_name}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        self.log(f"报告已生成: {report_file}", "INFO")
        return report_file


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("""
Proactive Intelligence - 技能进化器

用法:
  python skill-evolver.py <command> <skill-name>

命令:
  analyze   分析技能代码
  fix       修复问题
  enhance   增强功能
  optimize  优化性能
  report    生成详细报告

示例:
  python skill-evolver.py analyze file-reader
  python skill-evolver.py fix tavily-web-search-for-openclaw
""")
        sys.exit(1)
    
    command = sys.argv[1]
    skill_name = sys.argv[2]
    
    evolver = SkillEvolver()
    
    if command == "analyze":
        analysis = evolver.analyze_skill(skill_name)
        if analysis:
            print(f"\n[ANALYSIS] {skill_name}")
            print("=" * 50)
            print(f"文件数: {len(analysis['files'])}")
            print(f"问题数: {len(analysis['issues'])}")
            print(f"建议数: {len(analysis['suggestions'])}")
            print(f"健康分数: {analysis['complexity']['health_score']}/100")
            
            if analysis['issues']:
                print(f"\n[ISSUES] 问题:")
                for issue in analysis['issues']:
                    print(f"  - {issue}")
            
            if analysis['suggestions']:
                print(f"\n[SUGGESTIONS] 建议:")
                for suggestion in analysis['suggestions']:
                    print(f"  - {suggestion}")
    
    elif command == "fix":
        evolver.fix_issues(skill_name, auto_fix=False)
    
    elif command == "enhance":
        evolver.enhance_skill(skill_name)
    
    elif command == "optimize":
        evolver.optimize_skill(skill_name)
    
    elif command == "report":
        evolver.generate_report(skill_name)
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
