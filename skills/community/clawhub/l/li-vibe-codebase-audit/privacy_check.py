#!/usr/bin/env python3
"""
Privacy and Security Check for Skill Publishing
检查 skill 发布前的隐私和安全问题
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

class PrivacyChecker:
    """检查技能包中的隐私和安全问题"""
    
    def __init__(self, skill_dir: str):
        self.skill_dir = Path(skill_dir)
        self.findings = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
            "info": []
        }
        self.scanned_files = []
    
    def check_all(self) -> dict:
        """运行所有检查"""
        print("🔍 开始隐私和安全检查...\n")
        
        # 收集所有文件
        files = self._collect_files()
        print(f"📄 找到 {len(files)} 个文件需要检查\n")
        
        # 检查每个文件
        for file_path in files:
            self._check_file(file_path)
        
        # 生成报告
        report = self._generate_report()
        
        # 打印结果
        self._print_findings()
        
        return report
    
    def _collect_files(self) -> list:
        """收集需要检查的文件"""
        files = []
        ignore_patterns = ['.git', '__pycache__', '.pyc', 'node_modules', '.DS_Store']
        
        for file_path in self.skill_dir.rglob('*'):
            if file_path.is_file():
                # 跳过忽略的目录
                if any(part in ignore_patterns for part in file_path.parts):
                    continue
                
                # 跳过二进制文件
                if self._is_binary(file_path):
                    continue
                
                files.append(file_path)
        
        return files
    
    def _is_binary(self, file_path: Path) -> bool:
        """检查是否为二进制文件"""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\0' in chunk
        except:
            return True
    
    def _check_file(self, file_path: Path):
        """检查单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                self.scanned_files.append(str(file_path.relative_to(self.skill_dir)))
                
                # 运行所有检查
                self._check_user_paths(file_path, content)
                self._check_api_keys(file_path, content)
                self._check_emails(file_path, content)
                self._check_passwords(file_path, content)
                self._check_private_info(file_path, content)
                self._check_ip_addresses(file_path, content)
                self._check_phone_numbers(file_path, content)
                
        except Exception as e:
            self.findings["info"].append({
                "file": str(file_path.relative_to(self.skill_dir)),
                "issue": f"无法检查文件: {str(e)}"
            })
    
    def _check_user_paths(self, file_path: Path, content: str):
        """检查用户路径"""
        patterns = [
            (r'C:\\Users\\[^\\]+\\', "Windows用户路径"),
            (r'/Users/[^/]+/', "macOS用户路径"),
            (r'/home/[^/]+/', "Linux用户路径"),
        ]
        
        for pattern, desc in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                # 检查是否是示例路径
                if any(word in match.group(0).lower() for word in 
                       ['your_user', 'username', 'user_name', 'yourname']):
                    severity = "low"
                    issue = f"发现示例{desc}（可接受）"
                else:
                    severity = "high"
                    issue = f"发现真实{desc}"
                
                self.findings[severity].append({
                    "file": str(file_path.relative_to(self.skill_dir)),
                    "issue": issue,
                    "match": match.group(0),
                    "line_number": content[:match.start()].count('\n') + 1
                })
    
    def _check_api_keys(self, file_path: Path, content: str):
        """检查API密钥"""
        patterns = [
            (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
            (r'sk-ant-api03-[a-zA-Z0-9\-_]{95}', "Anthropic API Key"),
            (r'sk-or-v1-[a-zA-Z0-9]{64}', "OpenRouter API Key"),
            (r'AKIA[0-9A-Z]{16}', "AWS Access Key"),
            (r'ghp_[a-zA-Z0-9]{36}', "GitHub Token"),
        ]
        
        for pattern, key_type in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                # 检查是否是示例
                if 'example' in content[max(0, match.start()-50):match.start()].lower():
                    severity = "low"
                    issue = f"发现示例{key_type}（可接受）"
                else:
                    severity = "critical"
                    issue = f"发现真实{key_type}"
                
                self.findings[severity].append({
                    "file": str(file_path.relative_to(self.skill_dir)),
                    "issue": issue,
                    "match": match.group(0)[:20] + "...",
                    "line_number": content[:match.start()].count('\n') + 1
                })
    
    def _check_emails(self, file_path: Path, content: str):
        """检查邮箱地址"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        matches = re.finditer(pattern, content)
        
        safe_domains = ['example.com', 'test.com', 'localhost', 'users.noreply.github.com']
        
        for match in matches:
            email = match.group(0)
            
            if any(domain in email.lower() for domain in safe_domains):
                severity = "low"
                issue = f"发现示例邮箱（可接受）"
            else:
                severity = "medium"
                issue = f"发现真实邮箱地址"
            
            self.findings[severity].append({
                "file": str(file_path.relative_to(self.skill_dir)),
                "issue": issue,
                "match": email,
                "line_number": content[:match.start()].count('\n') + 1
            })
    
    def _check_passwords(self, file_path: Path, content: str):
        """检查密码"""
        pattern = r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']([^"\']{3,})["\']'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            # 检查是否是示例
            context = content[max(0, match.start()-100):match.end()+100]
            if any(word in context.lower() for word in 
                   ['example', 'placeholder', 'your_', 'xxx', 'replace']):
                severity = "low"
                issue = "发现示例密码（可接受）"
            else:
                severity = "critical"
                issue = "发现真实密码"
            
            self.findings[severity].append({
                "file": str(file_path.relative_to(self.skill_dir)),
                "issue": issue,
                "match": match.group(0)[:30] + "...",
                "line_number": content[:match.start()].count('\n') + 1
            })
    
    def _check_private_info(self, file_path: Path, content: str):
        """检查其他隐私信息"""
        # 检查Obsidian路径
        if re.search(r'obsidian[/\\]vault', content, re.IGNORECASE):
            self.findings["high"].append({
                "file": str(file_path.relative_to(self.skill_dir)),
                "issue": "发现Obsidian vault路径引用"
            })
        
        # 检查私人文件路径
        if re.search(r'/Documents/[^/]+/[^/]+', content):
            self.findings["medium"].append({
                "file": str(file_path.relative_to(self.skill_dir)),
                "issue": "发现私人文档路径"
            })
    
    def _check_ip_addresses(self, file_path: Path, content: str):
        """检查IP地址"""
        pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        matches = re.finditer(pattern, content)
        
        safe_ips = ['127.0.0.1', '0.0.0.0', '255.255.255.255', '192.168.', '10.', '172.16.']
        
        for match in matches:
            ip = match.group(0)
            
            if any(safe_ip in ip for safe_ip in safe_ips):
                continue  # 安全的IP，跳过
            else:
                self.findings["medium"].append({
                    "file": str(file_path.relative_to(self.skill_dir)),
                    "issue": "发现真实IP地址",
                    "match": ip,
                    "line_number": content[:match.start()].count('\n') + 1
                })
    
    def _check_phone_numbers(self, file_path: Path, content: str):
        """检查电话号码"""
        pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        matches = re.finditer(pattern, content)
        
        for match in matches:
            # 检查是否是示例
            context = content[max(0, match.start()-50):match.end()+50]
            if any(word in context.lower() for word in ['example', 'test', 'xxx']):
                severity = "low"
                issue = "发现示例电话号码（可接受）"
            else:
                severity = "medium"
                issue = "发现可能的真实电话号码"
            
            self.findings[severity].append({
                "file": str(file_path.relative_to(self.skill_dir)),
                "issue": issue,
                "match": match.group(0),
                "line_number": content[:match.start()].count('\n') + 1
            })
    
    def _generate_report(self) -> dict:
        """生成检查报告"""
        total_findings = sum(len(v) for v in self.findings.values() if isinstance(v, list))
        
        # 计算风险分数
        risk_score = (
            len(self.findings["critical"]) * 20 +
            len(self.findings["high"]) * 10 +
            len(self.findings["medium"]) * 5 +
            len(self.findings["low"]) * 2
        )
        
        # 确定风险等级
        if risk_score >= 80:
            risk_level = "CRITICAL"
        elif risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 20:
            risk_level = "MEDIUM"
        elif risk_score > 0:
            risk_level = "LOW"
        else:
            risk_level = "SAFE"
        
        return {
            "skill_dir": str(self.skill_dir),
            "scan_time": datetime.now().isoformat(),
            "files_scanned": len(self.scanned_files),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "total_findings": total_findings,
            "findings_by_severity": {
                "critical": len(self.findings["critical"]),
                "high": len(self.findings["high"]),
                "medium": len(self.findings["medium"]),
                "low": len(self.findings["low"]),
                "info": len(self.findings["info"])
            },
            "findings": self.findings,
            "safe_to_publish": risk_level in ["SAFE", "LOW"]
        }
    
    def _print_findings(self):
        """打印检查结果"""
        print("\n" + "="*80)
        print("🔒 隐私和安全检查报告")
        print("="*80 + "\n")
        
        # 风险等级
        risk_colors = {
            "SAFE": "✅",
            "LOW": "🟢",
            "MEDIUM": "🟡",
            "HIGH": "🟠",
            "CRITICAL": "🔴"
        }
        
        total = sum(len(v) for v in self.findings.values() if isinstance(v, list))
        
        print(f"📊 扫描结果:")
        print(f"  - 文件数: {len(self.scanned_files)}")
        print(f"  - 发现问题: {total}")
        print()
        
        print(f"🚨 风险等级:")
        print(f"  - 🔴 Critical: {len(self.findings['critical'])}")
        print(f"  - 🟠 High: {len(self.findings['high'])}")
        print(f"  - 🟡 Medium: {len(self.findings['medium'])}")
        print(f"  - 🟢 Low: {len(self.findings['low'])}")
        print(f"  - ℹ️ Info: {len(self.findings['info'])}")
        print()
        
        # 显示详细信息
        if self.findings["critical"]:
            print("\n🔴 CRITICAL 问题（必须修复）:")
            for finding in self.findings["critical"]:
                print(f"  - {finding['file']}:{finding.get('line_number', '?')}")
                print(f"    {finding['issue']}: {finding.get('match', 'N/A')}")
        
        if self.findings["high"]:
            print("\n🟠 HIGH 问题（强烈建议修复）:")
            for finding in self.findings["high"]:
                print(f"  - {finding['file']}:{finding.get('line_number', '?')}")
                print(f"    {finding['issue']}: {finding.get('match', 'N/A')}")
        
        if self.findings["medium"]:
            print("\n🟡 MEDIUM 问题（建议修复）:")
            for finding in self.findings["medium"]:
                print(f"  - {finding['file']}:{finding.get('line_number', '?')}")
                print(f"    {finding['issue']}: {finding.get('match', 'N/A')}")
        
        if self.findings["low"]:
            print("\n🟢 LOW 问题（可选修复）:")
            for finding in self.findings["low"][:5]:  # 只显示前5个
                print(f"  - {finding['file']}: {finding['issue']}")
            if len(self.findings["low"]) > 5:
                print(f"  ... 还有 {len(self.findings['low']) - 5} 个")
        
        print("\n" + "="*80)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="检查 skill 发布前的隐私和安全问题")
    parser.add_argument("skill_dir", nargs="?", 
                       default=os.environ.get('SKILL_DIR', '.'),
                       help="Skill 目录路径（默认：当前目录）")
    parser.add_argument("--output", "-o", help="输出报告文件（JSON）")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    
    args = parser.parse_args()
    
    # 运行检查
    checker = PrivacyChecker(args.skill_dir)
    report = checker.check_all()
    
    # 保存报告
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n📄 报告已保存到: {args.output}")
    
    # JSON输出
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    
    # 最终结论
    print("\n" + "="*80)
    if report['safe_to_publish']:
        print("✅ 可以安全发布！")
        print("   未发现严重的隐私或安全问题。")
    else:
        print("⛔ 不建议发布！")
        print(f"   发现 {report['findings_by_severity']['critical']} 个严重问题和 "
              f"{report['findings_by_severity']['high']} 个高危问题需要修复。")
    print("="*80 + "\n")
    
    # 返回状态码
    sys.exit(0 if report['safe_to_publish'] else 1)


if __name__ == "__main__":
    main()
