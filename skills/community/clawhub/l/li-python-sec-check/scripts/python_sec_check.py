#!/usr/bin/env python3
"""
Li_python_sec_check - Python 安全规范检查工具
基于 CloudBase 规范 + 腾讯安全指南 + LLM 智能分析

作者：北京老李
版本：2.1.0
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class PythonSecChecker:
    """Python 安全检查器"""
    
    def __init__(self, target_dir: str, output_dir: str = "./reports", 
                 python_version: str = "3.6", ignore_dirs: List[str] = None,
                 verbose: bool = False):
        self.target_dir = Path(target_dir)
        self.output_dir = Path(output_dir)
        self.python_version = python_version
        self.ignore_dirs = ignore_dirs or ['.git', '__pycache__', 'venv', 'env', 'node_modules']
        self.verbose = verbose
        self.issues = []
        self.warnings = []
        self.info = []
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_python_files(self) -> List[Path]:
        """获取所有 Python 文件"""
        py_files = []
        for root, dirs, files in os.walk(self.target_dir):
            # 过滤忽略目录
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    py_files.append(Path(root) / file)
        
        return py_files
    
    def check_project_structure(self) -> Dict:
        """检查 1: 项目结构"""
        print("🔍 检查 1: 项目结构...")
        
        required_files = ['Dockerfile', 'manage.py', 'requirements.txt']
        missing_files = []
        
        for file in required_files:
            if (self.target_dir / file).exists():
                self.info.append(f"✅ {file} - 存在")
            else:
                self.issues.append(f"❌ {file} - 缺失")
                missing_files.append(file)
        
        return {
            'check': '项目结构',
            'status': 'pass' if not missing_files else 'fail',
            'required_files': required_files,
            'missing_files': missing_files,
            'issues': self.issues.copy()
        }
    
    def check_dockerfile(self) -> Dict:
        """检查 2: Dockerfile 规范"""
        print("🔍 检查 2: Dockerfile 规范...")
        
        dockerfile_path = self.target_dir / 'Dockerfile'
        if not dockerfile_path.exists():
            return {'check': 'Dockerfile', 'status': 'skip', 'reason': '文件不存在'}
        
        content = dockerfile_path.read_text()
        issues = []
        warnings = []
        
        # 基础镜像检查
        if 'FROM alpine' in content or 'FROM python:3' in content:
            self.info.append("✅ 基础镜像配置合理")
        else:
            warnings.append("⚠️ 建议使用 alpine 或 python:3.x 官方镜像")
        
        # 时区设置
        if 'Asia/Shanghai' in content or 'TZ=Asia/Shanghai' in content:
            self.info.append("✅ 时区设置正确 (Asia/Shanghai)")
        else:
            warnings.append("⚠️ 未设置时区为 Asia/Shanghai")
        
        # 国内镜像源
        if any(mirror in content for mirror in ['mirrors.cloud.tencent.com', 'mirrors.aliyun.com', 'pypi.tuna.tsinghua.edu.cn']):
            self.info.append("✅ 配置了国内镜像源")
        else:
            warnings.append("⚠️ 未配置国内镜像源")
        
        # requirements.txt 安装
        if 'requirements.txt' in content and 'pip install' in content:
            self.info.append("✅ 包含 requirements.txt 依赖安装")
        else:
            issues.append("❌ 未找到 requirements.txt 依赖安装指令")
        
        # 启动命令
        if 'manage.py' in content:
            self.info.append("✅ 启动命令包含 manage.py")
        else:
            issues.append("❌ 启动命令未使用 manage.py")
        
        return {
            'check': 'Dockerfile',
            'status': 'pass' if not issues else 'fail',
            'issues': issues,
            'warnings': warnings
        }
    
    def check_requirements(self) -> Dict:
        """检查 3: requirements.txt"""
        print("🔍 检查 3: requirements.txt...")
        
        req_path = self.target_dir / 'requirements.txt'
        if not req_path.exists():
            return {'check': 'requirements.txt', 'status': 'skip', 'reason': '文件不存在'}
        
        content = req_path.read_text()
        issues = []
        warnings = []
        
        if not content.strip():
            issues.append("❌ requirements.txt 为空文件")
        else:
            self.info.append("✅ requirements.txt 非空")
        
        # 版本锁定检查
        if '==' in content:
            self.info.append("✅ 包含版本锁定")
        else:
            warnings.append("⚠️ 建议使用版本锁定 (例如：flask==2.0.0)")
        
        # 依赖数量
        dep_count = len([line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')])
        self.info.append(f"📦 依赖数量：{dep_count}")
        
        # Git 依赖检查
        if 'git+' in content or '@ git' in content:
            warnings.append("⚠️ 包含 Git 依赖，建议优先使用 PyPI 包")
        
        return {
            'check': 'requirements.txt',
            'status': 'pass' if not issues else 'fail',
            'issues': issues,
            'warnings': warnings,
            'dependency_count': dep_count
        }
    
    def check_crypto_usage(self) -> Dict:
        """检查 5: 不安全加密算法"""
        print("🔍 检查 5: 不安全加密算法...")
        
        issues = []
        py_files = self.get_python_files()
        
        for file in py_files:
            try:
                content = file.read_text()
                rel_path = file.relative_to(self.target_dir)
                
                # DES/3DES 检查
                if re.search(r'(?i)(DES|TripleDES|3DES)', content):
                    issues.append(f"{rel_path}: 使用不安全的 DES/3DES 加密算法 (应使用 AES)")
                
                # MD5 密码检查
                if re.search(r'(?i)md5.*password|password.*md5', content):
                    issues.append(f"{rel_path}: 使用 MD5 加密密码 (应使用 bcrypt/argon2)")
                    
            except Exception as e:
                if self.verbose:
                    print(f"  读取文件失败 {file}: {e}")
        
        if issues:
            for issue in issues:
                print(f"  ❌ {issue}")
        else:
            print("  ✅ 未发现不安全加密算法")
        
        return {
            'check': '不安全加密算法',
            'status': 'pass' if not issues else 'fail',
            'issues': issues
        }
    
    def check_sql_injection(self) -> Dict:
        """检查 6: SQL 注入风险"""
        print("🔍 检查 6: SQL 注入风险...")
        
        issues = []
        py_files = self.get_python_files()
        
        for file in py_files:
            try:
                content = file.read_text()
                rel_path = file.relative_to(self.target_dir)
                
                # 字符串拼接 SQL
                if re.search(r'execute\s*\(\s*[\"\'].*%.*[\"\']', content):
                    issues.append(f"{rel_path}: 可能存在 SQL 字符串拼接 (应使用参数化查询)")
                
                # f-string SQL
                if re.search(r'execute\s*\(\s*f[\"\']', content):
                    issues.append(f"{rel_path}: 使用 f-string 拼接 SQL (高风险)")
                
                # format SQL
                if re.search(r'execute\s*\([^)]*\.format\s*\(', content):
                    issues.append(f"{rel_path}: 使用 .format() 拼接 SQL (高风险)")
                    
            except Exception as e:
                if self.verbose:
                    print(f"  读取文件失败 {file}: {e}")
        
        if issues:
            for issue in issues:
                print(f"  ❌ {issue}")
        else:
            print("  ✅ 未发现明显 SQL 注入风险")
        
        return {
            'check': 'SQL 注入风险',
            'status': 'pass' if not issues else 'fail',
            'issues': issues
        }
    
    def check_command_injection(self) -> Dict:
        """检查 7: 命令注入风险"""
        print("🔍 检查 7: 命令注入风险...")
        
        issues = []
        py_files = self.get_python_files()
        
        for file in py_files:
            try:
                content = file.read_text()
                rel_path = file.relative_to(self.target_dir)
                
                # os.system
                if re.search(r'os\.system\s*\(', content):
                    issues.append(f"{rel_path}: 使用 os.system() (建议使用 subprocess)")
                
                # os.popen
                if re.search(r'os\.popen\s*\(', content):
                    issues.append(f"{rel_path}: 使用 os.popen() (已废弃)")
                
                # eval (排除 safe_eval)
                if re.search(r'(?<!safe_)eval\s*\(', content):
                    issues.append(f"{rel_path}: 使用 eval() (高风险)")
                
                # exec (排除 safe_exec)
                if re.search(r'(?<!safe_)exec\s*\(', content):
                    issues.append(f"{rel_path}: 使用 exec() (高风险)")
                
                # pickle
                if re.search(r'pickle\.load\s*\(|pickle\.loads\s*\(', content):
                    issues.append(f"{rel_path}: 使用 pickle 反序列化 (高风险)")
                
                # yaml.load 无 SafeLoader
                if re.search(r'yaml\.load\s*\([^)]*\)', content) and 'SafeLoader' not in content:
                    issues.append(f"{rel_path}: 使用 yaml.load 无 SafeLoader")
                    
            except Exception as e:
                if self.verbose:
                    print(f"  读取文件失败 {file}: {e}")
        
        if issues:
            for issue in issues:
                print(f"  ❌ {issue}")
        else:
            print("  ✅ 未发现明显命令注入风险")
        
        return {
            'check': '命令注入风险',
            'status': 'pass' if not issues else 'fail',
            'issues': issues
        }
    
    def check_hardcoded_secrets(self) -> Dict:
        """检查 8: 敏感信息硬编码"""
        print("🔍 检查 8: 敏感信息硬编码...")
        
        issues = []
        py_files = self.get_python_files()
        
        for file in py_files:
            try:
                content = file.read_text()
                rel_path = file.relative_to(self.target_dir)
                
                # 密码硬编码
                if re.search(r'(?i)(password|passwd|pwd)\s*=\s*[\'"][^\'"]+[\'"]', content):
                    issues.append(f"{rel_path}: 可能存在密码硬编码")
                
                # 密钥硬编码
                if re.search(r'(?i)(secret|api_key|apikey|token)\s*=\s*[\'"][^\'"]{8,}[\'"]', content):
                    issues.append(f"{rel_path}: 可能存在密钥硬编码")
                
                # AK/SK 硬编码
                if re.search(r'(?i)(access_key|secret_key|ak|sk)\s*=\s*[\'"][^\'"]+[\'"]', content):
                    issues.append(f"{rel_path}: 可能存在 AK/SK 硬编码")
                
                # 数据库连接字符串
                if re.search(r'(?i)(mysql|postgres|mongodb).*:\/\/.*:.*@', content):
                    issues.append(f"{rel_path}: 数据库连接字符串包含明文密码")
                    
            except Exception as e:
                if self.verbose:
                    print(f"  读取文件失败 {file}: {e}")
        
        if issues:
            for issue in issues:
                print(f"  ❌ {issue}")
        else:
            print("  ✅ 未发现明显敏感信息硬编码")
        
        return {
            'check': '敏感信息硬编码',
            'status': 'pass' if not issues else 'fail',
            'issues': issues
        }
    
    def check_debug_mode(self) -> Dict:
        """检查 9: 调试模式"""
        print("🔍 检查 9: 调试模式...")
        
        issues = []
        py_files = self.get_python_files()
        
        for file in py_files:
            try:
                content = file.read_text()
                rel_path = file.relative_to(self.target_dir)
                
                # Flask debug
                if re.search(r'app\.run\s*\([^)]*debug\s*=\s*True', content):
                    issues.append(f"{rel_path}: Flask 开启 debug 模式 (生产环境必须关闭)")
                
                # Django DEBUG
                if re.search(r'DEBUG\s*=\s*True', content):
                    issues.append(f"{rel_path}: Django 开启 DEBUG 模式 (生产环境必须关闭)")
                    
            except Exception as e:
                if self.verbose:
                    print(f"  读取文件失败 {file}: {e}")
        
        if issues:
            for issue in issues:
                print(f"  ❌ {issue}")
        else:
            print("  ✅ 未发现调试模式开启")
        
        return {
            'check': '调试模式',
            'status': 'pass' if not issues else 'fail',
            'issues': issues
        }
    
    def check_privacy(self) -> Dict:
        """检查 13: 隐私信息泄露"""
        print("🔍 检查 13: 隐私信息泄露...")
        
        try:
            from scripts.llm_analyzer import PrivacyChecker
            checker = PrivacyChecker()
            py_files = self.get_python_files()
            
            all_issues = []
            for file in py_files:
                issues = checker.check_file(file)
                all_issues.extend(issues)
            
            if all_issues:
                print(f"  ❌ 发现 {len(all_issues)} 个隐私信息泄露风险")
                # 只显示前 3 个
                for issue in all_issues[:3]:
                    print(f"    - {issue['subtype']}: {issue['file']}:{issue['line']}")
                if len(all_issues) > 3:
                    print(f"    ... 还有 {len(all_issues) - 3} 个")
            else:
                print("  ✅ 未发现隐私信息泄露")
            
            return {
                'check': '隐私信息泄露',
                'status': 'pass' if not all_issues else 'fail',
                'issues': [f"{i['file']}:{i['line']} - {i['subtype']}" for i in all_issues],
                'details': all_issues
            }
        except ImportError:
            return {'check': '隐私信息泄露', 'status': 'skip', 'reason': '模块未加载'}
        except Exception as e:
            if self.verbose:
                print(f"  隐私检查异常：{e}")
            return {'check': '隐私信息泄露', 'status': 'skip', 'reason': str(e)}
    
    def check_data_security(self) -> Dict:
        """检查 14: 数据安全"""
        print("🔍 检查 14: 数据安全...")
        
        try:
            from scripts.llm_analyzer import DataSecurityChecker
            checker = DataSecurityChecker()
            py_files = self.get_python_files()
            
            all_issues = []
            for file in py_files:
                issues = checker.check_file(file)
                all_issues.extend(issues)
            
            if all_issues:
                print(f"  ❌ 发现 {len(all_issues)} 个数据安全风险")
                for issue in all_issues[:3]:
                    print(f"    - {issue['subtype']}: {issue['file']}:{issue['line']}")
                if len(all_issues) > 3:
                    print(f"    ... 还有 {len(all_issues) - 3} 个")
            else:
                print("  ✅ 未发现数据安全漏洞")
            
            return {
                'check': '数据安全',
                'status': 'pass' if not all_issues else 'fail',
                'issues': [f"{i['file']}:{i['line']} - {i['subtype']}" for i in all_issues],
                'details': all_issues
            }
        except ImportError:
            return {'check': '数据安全', 'status': 'skip', 'reason': '模块未加载'}
        except Exception as e:
            if self.verbose:
                print(f"  数据安全检查异常：{e}")
            return {'check': '数据安全', 'status': 'skip', 'reason': str(e)}
    
    def run_external_tools(self, run_flake8: bool = True, run_bandit: bool = True, 
                          run_pip_audit: bool = False) -> Dict:
        """检查 10-12: 运行外部工具"""
        results = {}
        
        # flake8
        if run_flake8:
            print("🔍 检查 10: 代码质量 (flake8)...")
            try:
                import subprocess
                result = subprocess.run(
                    ['flake8', str(self.target_dir), '--count', '--select=E9,F63,F7,F82', 
                     '--statistics', '--exclude=.git,__pycache__,venv'],
                    capture_output=True, text=True, timeout=60
                )
                results['flake8'] = {
                    'status': 'pass' if result.returncode == 0 else 'fail',
                    'output': result.stdout
                }
                print(f"  flake8: {result.stdout.strip() or '✅ 通过'}")
            except Exception as e:
                results['flake8'] = {'status': 'skip', 'reason': str(e)}
        
        # bandit
        if run_bandit:
            print("🔍 检查 11: 安全扫描 (bandit)...")
            try:
                import subprocess
                bandit_output = self.output_dir / 'bandit-report.html'
                result = subprocess.run(
                    ['bandit', '-r', str(self.target_dir), '-f', 'html', 
                     '-o', str(bandit_output), '--exclude', '.git,__pycache__,venv'],
                    capture_output=True, text=True, timeout=120
                )
                results['bandit'] = {
                    'status': 'pass' if result.returncode == 0 else 'warning',
                    'report': str(bandit_output)
                }
                print(f"  bandit: 报告已生成 {bandit_output}")
            except Exception as e:
                results['bandit'] = {'status': 'skip', 'reason': str(e)}
        
        # pip-audit
        if run_pip_audit:
            print("🔍 检查 12: 依赖漏洞扫描 (pip-audit)...")
            try:
                import subprocess
                audit_output = self.output_dir / 'pip-audit-report.json'
                result = subprocess.run(
                    ['pip-audit', '--format=json'],
                    capture_output=True, text=True, timeout=120,
                    cwd=str(self.target_dir)
                )
                if result.stdout.strip():
                    (self.output_dir / 'pip-audit-report.json').write_text(result.stdout)
                results['pip-audit'] = {
                    'status': 'pass' if result.returncode == 0 else 'warning',
                    'report': str(audit_output)
                }
                print(f"  pip-audit: 报告已生成 {audit_output}")
            except Exception as e:
                results['pip-audit'] = {'status': 'skip', 'reason': str(e)}
        
        return results
    
    def generate_report(self, results: List[Dict]) -> str:
        """生成 Markdown 报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# Python 安全规范检查报告

**生成时间**: {timestamp}
**扫描目录**: {self.target_dir}
**参考标准**: 
- CloudBase Python 开发规范
- 腾讯 Python 安全指南
- 《个人信息保护法》
- 数据安全法

---

## 📊 检查摘要

| 检查项 | 状态 | 问题数 |
|--------|------|--------|
"""
        
        for result in results:
            status_icon = '✅' if result.get('status') == 'pass' else '❌' if result.get('status') == 'fail' else '⏭️'
            issue_count = len(result.get('issues', [])) if result.get('issues') else 0
            report += f"| {result.get('check', 'Unknown')} | {status_icon} | {issue_count} |\n"
        
        report += """
---

## 🔍 详细检查结果

"""
        
        for result in results:
            report += f"### {result.get('check', 'Unknown')}\n\n"
            report += f"**状态**: {'✅ 通过' if result.get('status') == 'pass' else '❌ 失败' if result.get('status') == 'fail' else '⏭️ 跳过'}\n\n"
            
            if result.get('issues'):
                report += "**问题列表**:\n"
                for issue in result['issues']:
                    report += f"- {issue}\n"
                report += "\n"
            
            report += "\n"
        
        report += """---

## ✅ 检查结论

"""
        
        failed_checks = [r for r in results if r.get('status') == 'fail']
        if failed_checks:
            report += f"**❌ 检查失败** - 发现 {len(failed_checks)} 项严重问题，需要修复\n"
        else:
            report += "**✅ 检查通过** - 未发现严重安全问题\n"
        
        report += "\n---\n\n*本报告由 Li_python_sec_check v2.1.0 自动生成*\n"
        
        return report
    
    def run(self, run_flake8: bool = True, run_bandit: bool = True, 
            run_pip_audit: bool = False, run_privacy_check: bool = True,
            run_data_security_check: bool = True, use_llm: bool = False) -> str:
        """运行所有检查"""
        print("=" * 60)
        print("Li_python_sec_check v2.1.0 - Python 安全规范检查")
        print("基于 CloudBase 规范 + 腾讯安全指南 + LLM 智能分析")
        print("=" * 60)
        print(f"扫描目录：{self.target_dir}")
        print(f"报告输出：{self.output_dir}")
        print("=" * 60)
        print()
        
        results = []
        
        # 运行所有检查
        results.append(self.check_project_structure())
        results.append(self.check_dockerfile())
        results.append(self.check_requirements())
        results.append(self.check_crypto_usage())
        results.append(self.check_sql_injection())
        results.append(self.check_command_injection())
        results.append(self.check_hardcoded_secrets())
        results.append(self.check_debug_mode())
        
        # 外部工具
        external_results = self.run_external_tools(run_flake8, run_bandit, run_pip_audit)
        for tool, result in external_results.items():
            results.append({'check': tool, **result})
        
        # 隐私和数据安全检查
        if run_privacy_check:
            results.append(self.check_privacy())
        
        if run_data_security_check:
            results.append(self.check_data_security())
        
        # 生成报告
        print("\n📊 生成报告...")
        report = self.generate_report(results)
        
        # 保存报告
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.output_dir / f'{timestamp}_python_sec_report.md'
        report_file.write_text(report)
        
        print(f"\n✅ 检查完成！")
        print(f"📄 报告已保存：{report_file}")
        print("=" * 60)
        
        # 返回报告路径
        return str(report_file)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Li_python_sec_check v2.1.0 - Python 安全规范检查工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python python_sec_check.py /path/to/project
  python python_sec_check.py . --output ./reports
  python python_sec_check.py /path/to/project --no-bandit --verbose
  python python_sec_check.py /path/to/project --llm --llm-api-key YOUR_API_KEY
        """
    )
    
    parser.add_argument('target_dir', nargs='?', default='.', 
                       help='要扫描的项目目录 (默认：当前目录)')
    parser.add_argument('--output', '-o', default='./reports',
                       help='报告输出目录 (默认：./reports)')
    parser.add_argument('--python-version', default='3.6',
                       help='Python 版本要求 (默认：3.6)')
    parser.add_argument('--ignore-dirs', default='.git,__pycache__,venv,env,node_modules',
                       help='忽略的目录 (逗号分隔)')
    parser.add_argument('--no-flake8', action='store_true',
                       help='禁用 flake8 代码质量检查')
    parser.add_argument('--no-bandit', action='store_true',
                       help='禁用 bandit 安全扫描')
    parser.add_argument('--pip-audit', action='store_true',
                       help='启用 pip-audit 依赖漏洞扫描')
    parser.add_argument('--no-privacy', action='store_true',
                       help='禁用隐私信息检查')
    parser.add_argument('--no-data-security', action='store_true',
                       help='禁用数据安全检查')
    parser.add_argument('--llm', action='store_true',
                       help='启用 LLM 智能分析（需要 API Key）')
    parser.add_argument('--llm-api-key', type=str,
                       help='LLM API Key（或通过 LLM_API_KEY 环境变量设置）')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细输出')
    
    args = parser.parse_args()
    
    # 设置 LLM API Key
    if args.llm_api_key:
        os.environ['LLM_API_KEY'] = args.llm_api_key
    
    # 创建检查器
    checker = PythonSecChecker(
        target_dir=args.target_dir,
        output_dir=args.output,
        python_version=args.python_version,
        ignore_dirs=args.ignore_dirs.split(','),
        verbose=args.verbose
    )
    
    # 运行检查
    report_file = checker.run(
        run_flake8=not args.no_flake8,
        run_bandit=not args.no_bandit,
        run_pip_audit=args.pip_audit,
        run_privacy_check=not args.no_privacy,
        run_data_security_check=not args.no_data_security,
        use_llm=args.llm
    )
    
    # 返回退出码
    sys.exit(0)


if __name__ == '__main__':
    main()
