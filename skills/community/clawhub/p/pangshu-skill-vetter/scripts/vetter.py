#!/usr/bin/env python3
"""
Skill Security Vetter
Scans skill code for security risks before installation.
"""

import os
import re
import sys
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from pathlib import Path


@dataclass
class Finding:
    severity: str  # 'CRITICAL', 'WARNING', 'INFO'
    line_num: int
    pattern: str
    context: str
    description: str


@dataclass
class VetReport:
    skill_name: str
    skill_path: str
    scan_time: datetime
    findings: List[Finding] = field(default_factory=list)
    
    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == 'CRITICAL')
    
    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == 'WARNING')
    
    @property
    def info_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == 'INFO')
    
    @property
    def verdict(self) -> Tuple[str, str]:
        """Returns (emoji, label)"""
        if self.critical_count > 0:
            return '🚫', 'BLOCK INSTALL'
        elif self.warning_count > 3:
            return '⚠️', 'WARN + CONFIRM'
        elif self.warning_count > 0:
            return '✅', 'INSTALL WITH CAUTION'
        else:
            return '✅', 'CLEAR TO INSTALL'


# Dangerous patterns - CRITICAL (block)
CRITICAL_PATTERNS = [
    (r'rm\s+-rf\s+[/~]\s*$', 'Disk wipe command'),
    (r'rm\s+-rf\s+\$\w+\s*$', 'Recursive rm with variable'),
    (r'dd\s+if=.*of=/dev/sd[a-z]', 'Direct disk write'),
    (r'mkfs', 'Filesystem format'),
    (r':\(\)\s*\{\s*:\|:\s*&\s*\}\s*:', 'Fork bomb'),
    (r'fork\(\).*fork\(\)', 'Fork loop'),
    (r'umount\s+-f', 'Force unmount'),
    (r'chmod\s+777\s+/etc', 'System file permission change'),
    (r'sudo\s+rm\s+-rf', 'Privilege escalation rm'),
    (r'shred\s+-u', 'Secure file deletion'),
]

# Warning patterns - MEDIUM
WARNING_PATTERNS = [
    (r'curl.*\|.*sh', 'Curl pipe to shell'),
    (r'wget.*\|.*sh', 'Wget pipe to shell'),
    (r'\.env', 'Environment file access'),
    (r'\.aws/', 'AWS credentials access'),
    (r'ssh-keygen', 'SSH key generation'),
    (r'chmod\s+[0-7]{3,4}', 'Permission change'),
    (r'setfacl', 'ACL modification'),
    (r'eval\s+\$', 'Eval with variable'),
    (r'exec\s+>', 'File descriptor redirect'),
    (r'base64.*-d.*\|', 'Base64 decode pipe'),
    (r'eval\s+`', 'Backtick eval'),
    (r'NcACRSb', 'Obfuscated command'),
    (r'\\x[0-9a-f]{2}', 'Hex encoded chars'),
    (r'chr\([0-9]\+\)', 'Char code obfuscation'),
]

# Info patterns
INFO_PATTERNS = [
    (r'/etc/cron', 'System crontab access'),
    (r'/usr/local/bin', 'System bin write'),
    (r'~/Library', 'macOS Library access'),
    (r'\.git/config', 'Git config access'),
]


def is_code_block(filepath: Path) -> bool:
    """Check if file is actual code (not documentation)."""
    code_extensions = {'.py', '.sh', '.js', '.ts', '.bash', '.zsh', '.rb', '.pl', '.php'}
    return filepath.suffix in code_extensions


def scan_file(filepath: Path) -> List[Tuple[int, str, str, str]]:
    """Scan a single file. Returns list of (line_num, severity, pattern, context)."""
    findings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return findings
    
    # For non-code files (markdown, yaml, json), only scan if suspicious
    # For code files, scan everything
    is_code = is_code_block(filepath)
    
    try:
        lines = content.splitlines()
    except Exception:
        return findings
    
    # Track if we're inside a code block (for markdown)
    in_code_block = False
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Track markdown code blocks
        if filepath.suffix == '.md':
            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue
            if not in_code_block:
                # Outside code block in markdown - skip entirely
                continue
        
        # Skip pure comment lines
        if stripped.startswith('#') or stripped.startswith('//'):
            continue
        
        # Skip pattern definition lines (the scanner scanning itself)
        # Lines like: (r'dangerous pattern', 'description')
        if is_code and re.search(r'^\s*\(r[\'"]', stripped):
            continue
        
        # Skip commented-out patterns (lines that mention dangerous patterns as examples)
        # Only relevant in actual code
        if is_code and re.match(r'^\s*#.*$', line):
            continue
        
        # Check CRITICAL patterns (only in code files or inside code blocks)
        if is_code or in_code_block:
            for pattern, desc in CRITICAL_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append((i, 'CRITICAL', pattern, f"[{filepath.name}:{i}] {desc}"))
        
        # Check WARNING patterns (only in code files or inside code blocks)
        if is_code or in_code_block:
            for pattern, desc in WARNING_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append((i, 'WARNING', pattern, f"[{filepath.name}:{i}] {desc}"))
        
        # Check INFO patterns (only in code files)
        if is_code:
            for pattern, desc in INFO_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append((i, 'INFO', pattern, f"[{filepath.name}:{i}] {desc}"))
    
    return findings


def get_context_line(filepath: Path, line_num: int, context: int = 1) -> str:
    """Get surrounding lines for context."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        start = max(0, line_num - context - 1)
        end = min(len(lines), line_num + context)
        
        context_lines = []
        for i in range(start, end):
            prefix = '>>> ' if i == line_num - 1 else '    '
            context_lines.append(f"{prefix}{i+1}: {lines[i].rstrip()}")
        
        return '\n'.join(context_lines)
    except Exception:
        return f"[{filepath.name}:{line_num}]"


def scan_skill(skill_path: str) -> VetReport:
    """Scan an entire skill directory."""
    skill_path = Path(skill_path)
    skill_name = skill_path.name
    
    report = VetReport(
        skill_name=skill_name,
        skill_path=str(skill_path),
        scan_time=datetime.now()
    )
    
    # Scan all code/text files
    for ext in ['.py', '.sh', '.js', '.ts', '.md', '.yaml', '.yml', '.json']:
        for filepath in skill_path.rglob(f'*{ext}'):
            # Skip node_modules, .git, etc.
            if any(x in filepath.parts for x in ['node_modules', '.git', '__pycache__', '.venv']):
                continue
            
            for line_num, severity, pattern, desc in scan_file(filepath):
                context = get_context_line(filepath, line_num)
                report.findings.append(Finding(
                    severity=severity,
                    line_num=line_num,
                    pattern=pattern,
                    context=context,
                    description=desc
                ))
    
    return report


def format_report(report: VetReport) -> str:
    """Format the report for display."""
    verdict_emoji, verdict_label = report.verdict
    
    lines = [
        f"╔{'═' * 60}╗",
        f"║ 🛡️  Skill Security Vetting Report{' ' * 27}║",
        f"╠{'═' * 60}╣",
        f"║ Skill: {report.skill_name:<49}║",
        f"║ Scan Time: {report.scan_time.strftime('%Y-%m-%d %H:%M:%S'):<42}║",
        f"║{' ' * 60}║",
        f"║ 🔴 CRITICAL: {report.critical_count:<5} 🟡 WARNING: {report.warning_count:<5} 🔵 INFO: {report.info_count:<5}║",
        f"╠{'═' * 60}╣",
        f"║ Findings:{'':51}║",
    ]
    
    if not report.findings:
        lines.append(f"║   (no issues found){'':46}║")
    else:
        # Group by severity
        for finding in sorted(report.findings, key=lambda x: (0 if x.severity == 'CRITICAL' else 1 if x.severity == 'WARNING' else 2, x.line_num)):
            emoji = '🔴' if finding.severity == 'CRITICAL' else '🟡' if finding.severity == 'WARNING' else '🔵'
            # Wrap long descriptions
            desc = finding.description
            lines.append(f"║ {emoji} {desc[:54]:<55}║")
            lines.append(f"║   Pattern: {finding.pattern[:49]:<50}║")
    
    lines.extend([
        f"╠{'═' * 60}╣",
        f"║ Verdict: {verdict_emoji} {verdict_label:<50}║",
        f"╚{'═' * 60}╝",
    ])
    
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: vetter.py scan <skill-path>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'scan':
        if len(sys.argv) < 3:
            print("Usage: vetter.py scan <skill-path>")
            sys.exit(1)
        skill_path = sys.argv[2]
        
        if not os.path.exists(skill_path):
            print(f"Error: Path not found: {skill_path}")
            sys.exit(1)
        
        report = scan_skill(skill_path)
        print(format_report(report))
        
        # Exit code based on severity
        if report.critical_count > 0:
            sys.exit(2)  # Block
        elif report.warning_count > 3:
            sys.exit(1)  # Warn
        else:
            sys.exit(0)  # OK
    else:
        print(f"Unknown command: {command}")
        print("Available: scan")
        sys.exit(1)


if __name__ == '__main__':
    main()
