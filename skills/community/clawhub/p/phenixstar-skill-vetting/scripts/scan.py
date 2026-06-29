#!/usr/bin/env python3
"""
Security scanner for ClawHub skills
Detects common malicious patterns and security risks
"""

import os
import re
import sys
import json
import argparse
import base64
from pathlib import Path
from typing import List, Dict, Tuple

class SkillScanner:
    """Scan skill files for security issues"""

    # Whitelist patterns to reduce false positives
    WHITELIST = [
        r'^\s*#',       # Comments
        r'^\s*"""',      # Docstrings
        r"^\s*'''",      # Docstrings
        r'localhost|127\.0\.0\.1',  # Local only
    ]

    # Dangerous patterns to detect
    PATTERNS = {
        'code_execution': [
            (r'\beval\s*\(', 'eval() execution'),
            (r'\bexec\s*\(', 'exec() execution'),
            (r'__import__\s*\(', 'dynamic imports'),
            (r'compile\s*\(', 'code compilation'),
        ],
        'subprocess': [
            (r'subprocess\.(call|run|Popen).*shell\s*=\s*True', 'shell=True'),
            (r'os\.system\s*\(', 'os.system()'),
            (r'os\.popen\s*\(', 'os.popen()'),
            (r'commands\.(getoutput|getstatusoutput)', 'commands module'),
        ],
        'obfuscation': [
            (r'base64\.b64decode', 'base64 decoding'),
            (r'codecs\.decode.*[\'"]hex[\'"]', 'hex decoding'),
            (r'\\x[0-9a-fA-F]{2}', 'hex escapes'),
            (r'\\u[0-9a-fA-F]{4}', 'unicode escapes'),
            (r'chr\s*\(\s*\d+\s*\)', 'chr() obfuscation'),
        ],
        'network': [
            (r'requests\.(get|post|put|delete)\s*\(', 'HTTP requests'),
            (r'urllib\.request\.urlopen', 'urllib requests'),
            (r'socket\.socket\s*\(', 'raw sockets'),
            (r'http\.client\.(HTTPConnection|HTTPSConnection)', 'http.client'),
        ],
        'file_operations': [
            (r'open\s*\(.*[\'"]w[\'"]', 'file writing'),
            (r'os\.remove\s*\(', 'file deletion'),
            (r'shutil\.(rmtree|move|copy)', 'bulk file ops'),
            (r'pathlib\.Path.*\.unlink\s*\(', 'path deletion'),
        ],
        'env_access': [
            (r'os\.environ\[', 'env variable access'),
            (r'os\.getenv\s*\(', 'env variable reading'),
            (r'subprocess.*env\s*=', 'env manipulation'),
        ],
        'prompt_injection': [
            (r'<!--.*(?:ignore|disregard|forget).*instruction', 'hidden instructions (HTML)'),
            (r'\[.*(?:ignore|disregard|forget).*instruction', 'hidden instructions (markdown)'),
            (r'(?:^|\n)#.*(?:system|assistant|user):', 'role manipulation in comments'),
        ],
    }
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.findings: List[Dict] = []

    @property
    def risk_score(self) -> int:
        """Calculate risk score (0-100)"""
        critical = {'code_execution', 'subprocess', 'prompt_injection'}
        crit_cnt = sum(1 for f in self.findings if f['category'] in critical)
        warn_cnt = sum(1 for f in self.findings if f['category'] not in critical)
        return min(100, crit_cnt * 30 + min(warn_cnt, 10) * 3)

    @property
    def risk_level(self) -> str:
        """Get risk level based on score"""
        s = self.risk_score
        return "BLOCKED" if s >= 81 else "DANGER" if s >= 51 else "CAUTION" if s >= 21 else "SAFE"
        
    def scan(self) -> Tuple[List[Dict], int]:
        """Scan all files in skill directory"""
        if not self.skill_path.exists():
            print(f"Error: Path not found: {self.skill_path}", file=sys.stderr)
            return [], 1

        for file_path in self.skill_path.rglob('*'):
            if file_path.is_file() and self._is_text_file(file_path):
                self._scan_file(file_path)
        return self.findings, 0 if len(self.findings) == 0 else 1
    
    def _is_text_file(self, path: Path) -> bool:
        """Check if file is likely a text file"""
        text_extensions = {'.py', '.md', '.txt', '.sh', '.bash', '.js', '.json', '.yaml', '.yml', '.toml'}
        return path.suffix.lower() in text_extensions or path.name == 'SKILL.md'
    
    def _scan_file(self, file_path: Path):
        """Scan a single file for issues"""
        try:
            content = file_path.read_text()
            relative_path = file_path.relative_to(self.skill_path)
            is_doc = file_path.suffix.lower() in ('.md', '.rst', '.txt')
            lines = content.split('\n')

            for category, patterns in self.PATTERNS.items():
                # Skip doc files for non-prompt categories
                if is_doc and category != 'prompt_injection':
                    continue

                for pattern, description in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1

                        # Check whitelist
                        line_content = lines[line_num - 1] if line_num <= len(lines) else ''
                        if any(re.search(wp, line_content) for wp in self.WHITELIST):
                            continue

                        self.findings.append({
                            'file': str(relative_path),
                            'line': line_num,
                            'category': category,
                            'description': description,
                            'match': match.group(0)[:50],  # truncate long matches
                        })
        except Exception as e:
            print(f"Warning: Could not scan {file_path}: {e}", file=sys.stderr)
    
    def print_report(self):
        """Print findings in readable format"""
        name = self.skill_path.name
        print("══════════════════════════════════════")
        print(f"  SKILL SECURITY AUDIT: {name}")
        print("══════════════════════════════════════")
        print(f"\nRISK SCORE: {self.risk_score}/100 - {self.risk_level}\n")

        if not self.findings:
            print("✅ No security issues detected")
        else:
            print(f"⚠️  Found {len(self.findings)} potential security issues:\n")
            # Group by category
            by_category = {}
            for f in self.findings:
                by_category.setdefault(f['category'], []).append(f)

            for category, findings in sorted(by_category.items()):
                print(f"📦 {category.upper().replace('_', ' ')}")
                for f in findings:
                    print(f"   {f['file']}:{f['line']} - {f['description']}")
                    print(f"      Match: {f['match']}")
                print()

        print("──────────────────────────────────────")
        recs = {"SAFE": "APPROVE - Safe to install", "CAUTION": "CAUTION - Review findings before proceeding",
                "DANGER": "DANGER - Detailed review required", "BLOCKED": "BLOCK - Do NOT install"}
        print(f"RECOMMENDATION: {recs[self.risk_level]}")
        print("══════════════════════════════════════")


def main():
    parser = argparse.ArgumentParser(description='Security scanner for ClawHub skills')
    parser.add_argument('skill_directory', help='Path to skill directory to scan')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--install-if-safe', action='store_true', help='Exit 0 only if safe')

    args = parser.parse_args()

    scanner = SkillScanner(args.skill_directory)
    findings, _ = scanner.scan()

    if args.json:
        output = {
            'skill_name': scanner.skill_path.name,
            'risk_score': scanner.risk_score,
            'risk_level': scanner.risk_level,
            'findings_count': len(findings),
            'findings': findings
        }
        print(json.dumps(output, indent=2))
    else:
        scanner.print_report()

    if args.install_if_safe:
        sys.exit(0 if scanner.risk_level == "SAFE" else 1)
    else:
        sys.exit(0 if len(findings) == 0 else 1)


if __name__ == '__main__':
    main()
