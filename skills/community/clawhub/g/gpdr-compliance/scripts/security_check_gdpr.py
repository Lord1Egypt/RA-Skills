#!/usr/bin/env python3
"""
GDPR Compliance - 安全检查脚本
用于验证技能的安全性和纯本地运行特性
"""

import os
import sys
import re
import subprocess
from pathlib import Path

class SecurityCheckerGDPR:
    """GDPR安全检查器"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.project_root = self.script_dir.parent
        
        # 网络调用关键词（GDPR特定）
        self.network_keywords = [
            'import requests', 'import urllib', 'import http', 'import socket',
            'import ftplib', 'import aiohttp', 'import paramiko',
            'requests.get', 'requests.post', 'urllib.request',
            'http.client', 'socket.socket', 'subprocess.run.*curl',
            'subprocess.run.*wget', 'subprocess.Popen.*curl',
            'subprocess.Popen.*wget',
            # GDPR特定可能的外部调用
            'edpb', 'supervisory.*authority', 'europa.eu',
            'data.*transfer', 'cross.*border.*api'
        ]
        
        # 自动更新/上报关键词
        self.update_keywords = [
            'check_for_updates', 'auto_update', 'telemetry',
            'upload.*data', 'post.*data', 'send.*report',
            'external.*api', 'api.*endpoint', 'webhook',
            'callback.*url', 'report.*server',
            'gdpr.*notification', 'data.*breach.*api'
        ]
        
        # 外部URL模式
        self.url_patterns = [
            r'http://[^\s"\']+',
            r'https://[^\s"\']+',
            r'ftp://[^\s"\']+',
            r'ws://[^\s"\']+',
            r'wss://[^\s"\']+'
        ]
        
        # GDPR特定关键词（应当存在的）
        self.gdpr_keywords = [
            'gdpr', 'data.*protection', 'privacy.*by.*design',
            'data.*subject', 'right.*to.*erasure', 'consent',
            'legitimate.*interest', 'data.*controller', 'processor',
            'data.*protection.*officer', 'dpo', 'dpia',
            'cross.*border.*transfer', 'standard.*contractual.*clauses',
            'adequacy.*decision'
        ]
        
        self.findings = []
        self.gdpr_compliance_score = 0
        self.max_gdpr_score = 0
    
    def check_python_files(self):
        """检查所有Python文件"""
        print("🔍 检查Python文件...")
        
        python_files = list(self.script_dir.rglob("*.py"))
        print(f"  发现 {len(python_files)} 个Python文件")
        
        for file_path in python_files:
            relative_path = file_path.relative_to(self.project_root)
            
            # 跳过安全检查脚本本身（避免检查关键词列表）
            if file_path.name == 'security_check_gdpr.py':
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查网络调用
                for keyword in self.network_keywords:
                    # 跳过GDPR术语关键词（不是实际网络调用）
                    gdpr_terms = ['edpb', 'supervisory.*authority', 'europa.eu', 'data.*transfer', 'cross.*border.*api']
                    if any(gdpr_term in keyword for gdpr_term in gdpr_terms):
                        continue
                    
                    if re.search(keyword, content, re.IGNORECASE):
                        self.findings.append({
                            'file': str(relative_path),
                            'type': 'network_call',
                            'keyword': keyword,
                            'severity': 'high'
                        })
                
                # 检查自动更新逻辑
                for keyword in self.update_keywords:
                    if re.search(keyword, content, re.IGNORECASE):
                        self.findings.append({
                            'file': str(relative_path),
                            'type': 'auto_update',
                            'keyword': keyword,
                            'severity': 'medium'
                        })
                
                # 检查外部URL
                for pattern in self.url_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        # 跳过package.json中的已知URL
                        if 'clawhub.ai' in match and 'package.json' in str(relative_path):
                            continue
                        self.findings.append({
                            'file': str(relative_path),
                            'type': 'external_url',
                            'url': match,
                            'severity': 'medium'
                        })
                
                # 检查GDPR特定关键词
                gdpr_found = 0
                for keyword in self.gdpr_keywords:
                    if re.search(keyword, content, re.IGNORECASE):
                        gdpr_found += 1
                
                if gdpr_found > 0:
                    self.gdpr_compliance_score += min(gdpr_found, 5)  # 最多加5分
                        
            except Exception as e:
                print(f"  警告: 无法检查文件 {relative_path}: {e}")
        
        self.max_gdpr_score = len(self.gdpr_keywords) * 0.5  # 每个最多0.5分
        print(f"  完成Python文件检查")
    
    def check_requirements(self):
        """检查依赖文件"""
        print("🔍 检查依赖文件...")
        
        req_file = self.project_root / 'requirements.txt'
        if req_file.exists():
            with open(req_file, 'r') as f:
                content = f.read()
            
            # 检查依赖数量
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
            print(f"  发现 {len(lines)} 个依赖包")
            
            for line in lines:
                if 'requests' in line.lower() or 'urllib' in line.lower() or 'http' in line.lower():
                    self.findings.append({
                        'file': 'requirements.txt',
                        'type': 'network_dependency',
                        'dependency': line,
                        'severity': 'high'
                    })
                
                # GDPR合规包检查
                if 'pandas' in line.lower():
                    self.gdpr_compliance_score += 2
                if 'jinja2' in line.lower():
                    self.gdpr_compliance_score += 2
        else:
            print("  未找到requirements.txt文件")
        
        print(f"  完成依赖文件检查")
    
    def check_skill_md(self):
        """检查SKILL.md中的声明"""
        print("🔍 检查SKILL.md声明...")
        
        skill_file = self.project_root / 'SKILL.md'
        if skill_file.exists():
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查纯本地声明
            local_keywords = ['纯本地运行', '无网络调用', '本地运行', '无需网络']
            found_local_declaration = False
            
            for keyword in local_keywords:
                if keyword in content:
                    found_local_declaration = True
                    break
            
            if not found_local_declaration:
                self.findings.append({
                    'file': 'SKILL.md',
                    'type': 'missing_local_declaration',
                    'severity': 'medium',
                    'note': '建议添加纯本地运行的明确声明'
                })
            else:
                print(f"  ✅ SKILL.md中包含纯本地运行声明")
                self.gdpr_compliance_score += 5
            
            # 检查GDPR免责条款
            disclaimer_keywords = ['免责条款', '非法律建议', '专业咨询', '责任限制']
            found_disclaimer = 0
            for keyword in disclaimer_keywords:
                if keyword in content:
                    found_disclaimer += 1
            
            if found_disclaimer >= 3:
                print(f"  ✅ SKILL.md中包含完整的免责条款")
                self.gdpr_compliance_score += 10
            elif found_disclaimer > 0:
                print(f"  ⚠️ SKILL.md中包含部分免责条款")
                self.gdpr_compliance_score += 5
            else:
                self.findings.append({
                    'file': 'SKILL.md',
                    'type': 'missing_disclaimer',
                    'severity': 'high',
                    'note': '强烈建议添加完整的法律免责条款'
                })
        
        print(f"  完成SKILL.md检查")
    
    def check_gdpr_references(self):
        """检查GDPR参考文档"""
        print("🔍 检查GDPR参考文档...")
        
        ref_dir = self.project_root / 'references'
        if ref_dir.exists():
            ref_files = list(ref_dir.rglob("*.md"))
            print(f"  发现 {len(ref_files)} 个参考文档")
            
            for file_path in ref_files:
                if 'gdpr' in file_path.name.lower():
                    self.gdpr_compliance_score += 10
                    print(f"  ✅ 找到GDPR法规参考文档: {file_path.name}")
        
        print(f"  完成GDPR参考文档检查")
    
    def run_gdpr_functional_tests(self):
        """运行GDPR功能测试"""
        print("🔍 运行GDPR功能测试...")
        
        test_commands = [
            ['python', str(self.script_dir / 'gdpr-check.py'), '--help'],
            ['python', str(self.script_dir / 'data-subject-rights.py'), '--help'],
            ['python', str(self.script_dir / 'cross-border-transfer.py'), '--help'],
        ]
        
        for cmd in test_commands:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    print(f"  ✅ 命令 {' '.join(cmd)} 执行成功")
                    self.gdpr_compliance_score += 5
                else:
                    self.findings.append({
                        'type': 'test_failure',
                        'command': ' '.join(cmd),
                        'error': result.stderr[:100],
                        'severity': 'medium'
                    })
                    
            except subprocess.TimeoutExpired:
                self.findings.append({
                    'type': 'test_timeout',
                    'command': ' '.join(cmd),
                    'severity': 'medium',
                    'note': '命令执行超时，可能有问题'
                })
            except Exception as e:
                self.findings.append({
                    'type': 'test_exception',
                    'command': ' '.join(cmd),
                    'error': str(e),
                    'severity': 'medium'
                })
        
        print(f"  完成GDPR功能测试")
    
    def generate_report(self):
        """生成检查报告"""
        print("\n" + "="*60)
        print("📋 GDPR安全检查报告")
        print("="*60)
        
        # 计算GDPR合规评分
        total_score = self.gdpr_compliance_score
        max_score = 100
        
        print(f"\n🔐 GDPR合规评分: {total_score}/{max_score}")
        
        if total_score >= 80:
            print("  🥇 优秀 - GDPR合规性良好")
        elif total_score >= 60:
            print("  🥈 良好 - GDPR合规性较好")
        elif total_score >= 40:
            print("  🥉 中等 - GDPR合规性一般")
        else:
            print("  ⚠️  需要改进 - GDPR合规性不足")
        
        if not self.findings:
            print("\n✅ 所有安全检查通过！")
            print("\n🎉 GDPR Compliance技能看起来是安全的，符合纯本地运行的要求")
            return True
        
        # 按严重程度分类
        high_findings = [f for f in self.findings if f['severity'] == 'high']
        medium_findings = [f for f in self.findings if f['severity'] == 'medium']
        low_findings = [f for f in self.findings if f['severity'] == 'low']
        
        print(f"\n发现的问题:")
        print(f"  🔴 高风险: {len(high_findings)} 个")
        print(f"  🟡 中风险: {len(medium_findings)} 个")
        print(f"  🟢 低风险: {len(low_findings)} 个")
        
        if high_findings:
            print("\n🔴 高风险问题:")
            for finding in high_findings:
                print(f"  • {finding.get('file', '未知文件')}")
                print(f"    类型: {finding['type']}")
                if 'keyword' in finding:
                    print(f"    关键词: {finding['keyword']}")
                if 'note' in finding:
                    print(f"    说明: {finding['note']}")
                print()
        
        if medium_findings:
            print("\n🟡 中风险问题:")
            for finding in medium_findings:
                print(f"  • {finding.get('file', '未知文件')}")
                print(f"    类型: {finding['type']}")
                if 'keyword' in finding:
                    print(f"    关键词: {finding['keyword']}")
                if 'note' in finding:
                    print(f"    说明: {finding['note']}")
                print()
        
        if low_findings:
            print("\n🟢 低风险问题:")
            for finding in low_findings:
                print(f"  • {finding.get('file', '未知文件')}")
                print(f"    类型: {finding['type']}")
                if 'note' in finding:
                    print(f"    说明: {finding['note']}")
                print()
        
        # 提供建议
        print("\n💡 建议:")
        if high_findings:
            print("  ❗ 存在高风险问题，建议在安装前修复")
            return False
        elif medium_findings:
            print("  ⚠️  存在中风险问题，建议审查后再使用")
            return True
        else:
            print("  ✅ 只有低风险或无风险问题，可以安全使用")
            return True
    
    def print_gdpr_specific_advice(self):
        """打印GDPR特定的建议"""
        print("\n" + "="*60)
        print("🚀 GDPR合规安装和使用建议")
        print("="*60)
        
        print("""
1. 📋 GDPR特定检查
   - 确认工具包含完整的GDPR法规参考
   - 验证数据主体权利检查功能
   - 检查跨境传输合规工具
   - 确认包含DPIA生成功能

2. 🛡️ GDPR安全使用建议
   - 始终在受控环境下运行GDPR检查
   - 确保不包含敏感个人数据的测试
   - 验证所有GDPR合规逻辑
   - 关注GDPR法规更新

3. 🔧 GDPR环境要求
   - 了解欧盟数据保护要求
   - 准备数据保护官（DPO）联系方式
   - 了解成员国特定要求
   - 准备跨境传输机制

4. ⚖️ GDPR法律注意事项
   - 本工具仅供GDPR合规辅助参考
   - 重大GDPR合规决策必须咨询DPO或律师
   - 跨境数据传输需特别谨慎
   - 数据泄露需遵守72小时通知要求
""")

def main():
    """主函数"""
    print("🔐 GDPR Compliance - 安全检查")
    print("="*60)
    
    checker = SecurityCheckerGDPR()
    
    # 运行所有检查
    checker.check_python_files()
    checker.check_requirements()
    checker.check_skill_md()
    checker.check_gdpr_references()
    checker.run_gdpr_functional_tests()
    
    # 生成报告
    is_safe = checker.generate_report()
    
    # 打印建议
    checker.print_gdpr_specific_advice()
    
    # 返回退出码
    return 0 if is_safe else 1

if __name__ == "__main__":
    sys.exit(main())