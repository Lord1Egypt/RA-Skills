#!/usr/bin/env python3
"""
安全与隐私检查脚本 / Security and Privacy Check Script
"""

import os, re, sys
from pathlib import Path

SENSITIVE_PATTERNS = {
    'password': [r'password\s*=\s*["\']([^"\']+)["\']'],
    'api_key': [r'api_key\s*=\s*["\']([^"\']+)["\']'],
    'secret': [r'secret\s*=\s*["\']([^"\']+)["\']'],
    'private_key': [r'-----BEGIN.*PRIVATE KEY-----'],
}

def check_directory(path):
    findings = {}
    path = Path(path)
    print(f"🔍 检查目录 / Checking: {path}")
    
    for file_path in path.rglob('*.py'):
        try:
            content = file_path.read_text(errors='ignore')
            for cat, patterns in SENSITIVE_PATTERNS.items():
                for p in patterns:
                    for m in re.finditer(p, content, re.I):
                        line = content[:m.start()].count('\n') + 1
                        findings.setdefault(str(file_path), []).append({
                            'category': cat, 'line': line, 'match': m.group(0)[:50]
                        })
        except: pass
    
    print(f"✅ 完成 / Complete - 发现 / Found: {len(findings)} 个文件")
    return findings

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    findings = check_directory(path)
    for f, items in findings.items():
        print(f"\n📄 {f}")
        for i in items:
            print(f"  - {i['category']} @ line {i['line']}: {i['match']}...")
    sys.exit(1 if findings else 0)
