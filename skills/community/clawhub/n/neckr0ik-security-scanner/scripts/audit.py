#!/usr/bin/env python3
"""
Skill Security Audit Tool for OpenClaw Skills

Scans skill directories for security vulnerabilities including:
- Hardcoded secrets (API keys, tokens, passwords)
- Shell injection risks
- Code execution vulnerabilities
- Unauthorized network access
- Prompt injection vectors
- File path traversal
- Outdated dependencies

Usage:
    python audit.py <skill-path> [--format json|markdown|summary]
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class Vulnerability:
    """Represents a security vulnerability found in a skill."""
    
    id: str
    name: str
    severity: Severity
    file: str
    line: int
    description: str
    code_snippet: str
    remediation: str
    references: List[str] = field(default_factory=list)


@dataclass
class AuditResult:
    """Complete audit result for a skill."""
    
    skill_name: str
    skill_path: str
    passed: bool
    vulnerabilities: List[Vulnerability]
    summary: Dict[str, int]
    
    def to_dict(self) -> dict:
        return {
            "skill_name": self.skill_name,
            "skill_path": self.skill_path,
            "passed": self.passed,
            "vulnerabilities": [
                {
                    "id": v.id,
                    "name": v.name,
                    "severity": v.severity.value,
                    "file": v.file,
                    "line": v.line,
                    "description": v.description,
                    "code_snippet": v.code_snippet,
                    "remediation": v.remediation,
                    "references": v.references
                }
                for v in self.vulnerabilities
            ],
            "summary": self.summary
        }


# ============================================================================
# SECURITY PATTERNS
# ============================================================================

# Regex patterns for detecting hardcoded secrets
SECRET_PATTERNS = [
    # API Keys
    (r'(?:api[_-]?key|apikey)\s*[=:]\s*["\']([a-zA-Z0-9_-]{20,})["\']', "API Key"),
    (r'(?:secret|token|auth)\s*[=:]\s*["\']([a-zA-Z0-9_-]{20,})["\']', "Secret/Token"),
    (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
    (r'AIza[a-zA-Z0-9_-]{35}', "Google API Key"),
    (r'xox[baprs]-[a-zA-Z0-9-]{10,}', "Slack Token"),
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Token"),
    (r'gho_[a-zA-Z0-9]{36}', "GitHub OAuth Token"),
    (r'github_pat_[a-zA-Z0-9_]{22,}', "GitHub PAT"),
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key"),
    (r'aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\']([a-zA-Z0-9/+=]{40})["\']', "AWS Secret Key"),
    (r'sk_live_[a-zA-Z0-9]{24,}', "Stripe Live Key"),
    (r'rk_live_[a-zA-Z0-9]{24,}', "Stripe Restricted Key"),
    (r'-----BEGIN (?:RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----', "Private Key"),
    
    # Passwords
    (r'(?:password|passwd|pwd)\s*[=:]\s*["\']([^"\']{8,})["\']', "Password"),
    (r'mongodb://[^:]+:([^@]+)@', "MongoDB Password in URI"),
    (r'postgres://[^:]+:([^@]+)@', "PostgreSQL Password in URI"),
    (r'mysql://[^:]+:([^@]+)@', "MySQL Password in URI"),
    (r'redis://[^:]+:([^@]+)@', "Redis Password in URI"),
]

# Shell injection patterns
SHELL_INJECTION_PATTERNS = [
    (r'os\.system\s*\(', "os.system() - shell command execution"),
    (r'os\.popen\s*\(', "os.popen() - shell command execution"),
    (r'subprocess\.(?:call|run|Popen)\s*\([^)]*shell\s*=\s*True', "subprocess with shell=True"),
    (r'eval\s*\(', "eval() - dynamic code execution"),
    (r'exec\s*\(', "exec() - dynamic code execution"),
    (r'__import__\s*\(', "__import__() - dynamic module loading"),
    (r'compile\s*\([^)]*string', "compile() with string input"),
    (r'commands\.getoutput', "commands.getoutput - deprecated shell execution"),
    (r'commands\.getstatusoutput', "commands.getstatusoutput - deprecated shell execution"),
]

# Network access patterns
NETWORK_PATTERNS = [
    (r'requests\.(?:get|post|put|delete|patch)\s*\(["\']https?://([^"\']+)["\']', "HTTP request to external domain"),
    (r'urllib\.request\.urlopen\s*\(["\']https?://([^"\']+)["\']', "urllib request to external domain"),
    (r'httpx\.(?:get|post|put|delete|patch)\s*\(["\']https?://([^"\']+)["\']', "httpx request to external domain"),
    (r'aiohttp\.ClientSession\(\)[^)]*\.get\s*\(["\']https?://([^"\']+)["\']', "aiohttp request to external domain"),
    (r'\.fetch\s*\(["\']https?://([^"\']+)["\']', "fetch request to external domain"),
    (r'axios\.(?:get|post|put|delete)\s*\(["\']https?://([^"\']+)["\']', "axios request to external domain"),
]

# Known suspicious domains
SUSPICIOUS_DOMAINS = [
    r'pastebin\.com',
    r'webhook\.site',
    r'requestbin\.',
    r'ngrok\.io',
    r'burpcollaborator',
    r'interactsh',
]

# Known safe domains (whitelisted)
SAFE_DOMAINS = [
    r'api\.openai\.com',
    r'api\.anthropic\.com',
    r'github\.com',
    r'api\.github\.com',
    r'pypi\.org',
    r'npmjs\.com',
    r'clawhub\.ai',
    r'openclaw\.ai',
    r'localhost',
    r'127\.0\.0\.1',
]

# Prompt injection patterns
PROMPT_INJECTION_PATTERNS = [
    (r'f["\'][^"\']*\{[^}]*user[^}]*\}[^"\']*["\']', "f-string with user input in prompt"),
    (r'\.format\s*\([^)]*user', ".format() with user input"),
    (r'%\s*\(.*user', "% formatting with user input"),
    (r'system\s*[=:]\s*["\'][^"\']*\{', "System prompt with interpolation"),
]

# File path traversal patterns
PATH_TRAVERSAL_PATTERNS = [
    (r'open\s*\([^)]*\+[^)]*user', "open() with concatenated user input"),
    (r'open\s*\([^)]*f["\'][^"\']*\{', "open() with f-string path"),
    (r'\.join\s*\([^)]*user', "path.join() with user input"),
    (r'os\.path\.\w+\s*\([^)]*user', "os.path function with user input"),
]


# ============================================================================
# AUDIT FUNCTIONS
# ============================================================================

def scan_file(filepath: Path) -> List[Vulnerability]:
    """Scan a single file for vulnerabilities."""
    
    vulnerabilities = []
    
    # Skip documentation and example files
    if filepath.suffix == '.md':
        return vulnerabilities
    if 'example' in filepath.name.lower():
        return vulnerabilities
    if 'doc' in filepath.name.lower() and filepath.suffix in ['.txt', '.rst']:
        return vulnerabilities
    
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
        lines = content.split('\n')
    except Exception as e:
        return vulnerabilities
    
    # Helper to check if line is a comment or string literal (not executable)
    def is_comment_or_string(line_num: int) -> bool:
        line = lines[line_num - 1].strip() if line_num <= len(lines) else ""
        # Skip Python comments
        if line.startswith('#'):
            return True
        # Skip docstrings (rough heuristic)
        if '"""' in line or "'''" in line:
            return True
        return False
    
    # Check for hardcoded secrets
    for pattern, name in SECRET_PATTERNS:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            line_num = content[:match.start()].count('\n') + 1
            line = lines[line_num - 1] if line_num <= len(lines) else ""
            
            # Skip if in comment or docstring
            if is_comment_or_string(line_num):
                continue
            
            vulnerabilities.append(Vulnerability(
                id=f"SECRET-{name.upper().replace(' ', '-')}",
                name=f"Hardcoded {name}",
                severity=Severity.CRITICAL,
                file=str(filepath),
                line=line_num,
                description=f"Potential hardcoded {name.lower()} detected in code. This exposes credentials and should be moved to environment variables.",
                code_snippet=line.strip()[:200],
                remediation=f"Move the {name.lower()} to an environment variable and access it via os.environ.get() or use a secrets manager.",
                references=["https://owasp.org/www-community/vulnerabilities/Hardcoded_password"]
            ))
    
    # Check for shell injection risks
    for pattern, name in SHELL_INJECTION_PATTERNS:
        for match in re.finditer(pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            line = lines[line_num - 1] if line_num <= len(lines) else ""
            
            # Skip if in comment or docstring
            if is_comment_or_string(line_num):
                continue
            
            # Check if user input is involved
            context_start = max(0, match.start() - 200)
            context = content[context_start:match.end() + 200]
            has_user_input = bool(re.search(r'user|input|request|param|arg', context, re.IGNORECASE))
            
            severity = Severity.CRITICAL if has_user_input else Severity.HIGH
            
            vulnerabilities.append(Vulnerability(
                id=f"SHELL-{name}",
                name=f"Shell/Code Execution: {name}",
                severity=severity,
                file=str(filepath),
                line=line_num,
                description=f"Potential {name} detected. This can lead to arbitrary code execution if user input is passed.",
                code_snippet=line.strip()[:200],
                remediation="Use subprocess without shell=True, or sanitize inputs with shlex.quote(). Avoid eval/exec with user input.",
                references=["https://owasp.org/www-community/attacks/Command_Injection"]
            ))
    
    # Check for network access
    for pattern, name in NETWORK_PATTERNS:
        for match in re.finditer(pattern, content):
            domain = match.group(1) if match.groups() else "unknown"
            line_num = content[:match.start()].count('\n') + 1
            line = lines[line_num - 1] if line_num <= len(lines) else ""
            
            # Check if domain is suspicious
            is_suspicious = any(re.search(p, domain) for p in SUSPICIOUS_DOMAINS)
            is_safe = any(re.search(p, domain) for p in SAFE_DOMAINS)
            
            if is_suspicious:
                severity = Severity.CRITICAL
                description = f"Network request to suspicious domain: {domain}"
            elif is_safe:
                severity = Severity.INFO
                description = f"Network request to known safe domain: {domain}"
            else:
                severity = Severity.MEDIUM
                description = f"Network request to external domain: {domain}"
            
            vulnerabilities.append(Vulnerability(
                id=f"NET-{domain.replace('.', '-')}",
                name=f"Network Access: {domain}",
                severity=severity,
                file=str(filepath),
                line=line_num,
                description=description,
                code_snippet=line.strip()[:200],
                remediation="Review the external domain. Ensure it's necessary and the connection is HTTPS. Consider adding domain to allowlist.",
                references=["https://owasp.org/www-community/attacks/Injection_Flaws"]
            ))
    
    # Check for prompt injection
    for pattern, name in PROMPT_INJECTION_PATTERNS:
        for match in re.finditer(pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            line = lines[line_num - 1] if line_num <= len(lines) else ""
            
            vulnerabilities.append(Vulnerability(
                id=f"PROMPT-INJECTION",
                name="Potential Prompt Injection",
                severity=Severity.HIGH,
                file=str(filepath),
                line=line_num,
                description="User input is interpolated into a prompt string without sanitization. This can lead to prompt injection attacks.",
                code_snippet=line.strip()[:200],
                remediation="Sanitize user input before including in prompts. Use fixed prompts with separate context injection, or validate input against allowlists.",
                references=["https://owasp.org/www-community/attacks/Prompt_Injection"]
            ))
    
    # Check for path traversal
    for pattern, name in PATH_TRAVERSAL_PATTERNS:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            line_num = content[:match.start()].count('\n') + 1
            line = lines[line_num - 1] if line_num <= len(lines) else ""
            
            vulnerabilities.append(Vulnerability(
                id=f"PATH-TRAVERSAL",
                name="Potential Path Traversal",
                severity=Severity.HIGH,
                file=str(filepath),
                line=line_num,
                description="User input is used in file path operations without sanitization. This can lead to arbitrary file read/write.",
                code_snippet=line.strip()[:200],
                remediation="Sanitize filenames with regex, use pathlib for safe path handling, and restrict paths to a sandbox directory.",
                references=["https://owasp.org/www-community/attacks/Path_Traversal"]
            ))
    
    return vulnerabilities


def check_dependencies(skill_path: Path) -> List[Vulnerability]:
    """Check for outdated/insecure dependencies."""
    
    vulnerabilities = []
    
    # Check for requirements.txt
    req_file = skill_path / "requirements.txt"
    if req_file.exists():
        try:
            content = req_file.read_text()
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Check for unpinned versions
                if '==' not in line and line and not line.startswith('-'):
                    vulnerabilities.append(Vulnerability(
                        id=f"DEP-UNPINNED-{i}",
                        name="Unpinned Dependency",
                        severity=Severity.MEDIUM,
                        file="requirements.txt",
                        line=i,
                        description=f"Dependency '{line}' has no version pin. This can lead to unpredictable behavior.",
                        code_snippet=line,
                        remediation=f"Pin the version: {line}==x.y.z",
                        references=[]
                    ))
        except Exception:
            pass
    
    # Check for package.json
    pkg_file = skill_path / "package.json"
    if pkg_file.exists():
        try:
            data = json.loads(pkg_file.read_text())
            
            for dep_type in ['dependencies', 'devDependencies']:
                deps = data.get(dep_type, {})
                for name, version in deps.items():
                    # Check for unpinned versions
                    if version.startswith('^') or version.startswith('~') or version == '*':
                        vulnerabilities.append(Vulnerability(
                            id=f"DEP-UNPINNED-{name}",
                            name="Loose Dependency Version",
                            severity=Severity.MEDIUM,
                            file="package.json",
                            line=1,
                            description=f"Dependency '{name}' has loose version '{version}'. This can lead to breaking changes.",
                            code_snippet=f"{name}: {version}",
                            remediation=f"Pin the version: {name}: {version.lstrip('^~')}",
                            references=[]
                        ))
        except Exception:
            pass
    
    return vulnerabilities


def check_skill_manifest(skill_path: Path) -> List[Vulnerability]:
    """Check SKILL.md for security issues."""
    
    vulnerabilities = []
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        vulnerabilities.append(Vulnerability(
            id="MANIFEST-MISSING",
            name="Missing SKILL.md",
            severity=Severity.CRITICAL,
            file="SKILL.md",
            line=0,
            description="Skill is missing required SKILL.md manifest file.",
            code_snippet="",
            remediation="Create a SKILL.md file with proper YAML frontmatter.",
            references=[]
        ))
        return vulnerabilities
    
    try:
        content = skill_md.read_text()
        
        # Check for secrets in manifest
        for pattern, name in SECRET_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                vulnerabilities.append(Vulnerability(
                    id=f"MANIFEST-SECRET-{name.upper().replace(' ', '-')}",
                    name=f"Secret in SKILL.md",
                    severity=Severity.CRITICAL,
                    file="SKILL.md",
                    line=1,
                    description=f"Potential {name.lower()} found in skill manifest. Never include secrets in documentation.",
                    code_snippet="",
                    remediation=f"Remove the {name.lower()} from SKILL.md and use environment variables instead.",
                    references=[]
                ))
        
        # Check for required frontmatter
        if not re.search(r'^---\s*$', content, re.MULTILINE):
            vulnerabilities.append(Vulnerability(
                id="MANIFEST-FRONTMATTER",
                name="Missing YAML Frontmatter",
                severity=Severity.HIGH,
                file="SKILL.md",
                line=1,
                description="SKILL.md is missing YAML frontmatter section.",
                code_snippet="",
                remediation="Add YAML frontmatter with 'name' and 'description' fields.",
                references=[]
            ))
        else:
            # Check for required fields
            if 'name:' not in content:
                vulnerabilities.append(Vulnerability(
                    id="MANIFEST-NAME",
                    name="Missing 'name' in Frontmatter",
                    severity=Severity.HIGH,
                    file="SKILL.md",
                    line=1,
                    description="SKILL.md frontmatter is missing 'name' field.",
                    code_snippet="",
                    remediation="Add 'name' field to YAML frontmatter.",
                    references=[]
                ))
            
            if 'description:' not in content:
                vulnerabilities.append(Vulnerability(
                    id="MANIFEST-DESC",
                    name="Missing 'description' in Frontmatter",
                    severity=Severity.MEDIUM,
                    file="SKILL.md",
                    line=1,
                    description="SKILL.md frontmatter is missing 'description' field.",
                    code_snippet="",
                    remediation="Add 'description' field to YAML frontmatter.",
                    references=[]
                ))
    
    except Exception:
        pass
    
    return vulnerabilities


# Directories to exclude from scanning
EXCLUDE_DIRS = {
    'node_modules', '.git', '__pycache__', '.venv', 'venv', 
    'dist', 'build', '.pytest_cache', '.mypy_cache', 'egg-info'
}

def should_scan_file(filepath: Path) -> bool:
    """Check if file should be scanned (excludes common ignore directories)."""
    parts = filepath.parts
    for part in parts:
        if part in EXCLUDE_DIRS:
            return False
    return True

def audit_skill(skill_path: str) -> AuditResult:
    """Main audit function for a skill directory."""
    
    path = Path(skill_path)
    
    if not path.exists():
        return AuditResult(
            skill_name=path.name,
            skill_path=str(path),
            passed=False,
            vulnerabilities=[Vulnerability(
                id="PATH-NOT-FOUND",
                name="Skill Directory Not Found",
                severity=Severity.CRITICAL,
                file="",
                line=0,
                description=f"Skill directory does not exist: {skill_path}",
                code_snippet="",
                remediation="Provide a valid skill directory path.",
                references=[]
            )],
            summary={"critical": 1, "high": 0, "medium": 0, "low": 0, "info": 0}
        )
    
    all_vulnerabilities = []
    
    # Check manifest
    all_vulnerabilities.extend(check_skill_manifest(path))
    
    # Check dependencies
    all_vulnerabilities.extend(check_dependencies(path))
    
    # Scan all Python files (excluding ignored dirs)
    for py_file in path.rglob("*.py"):
        if should_scan_file(py_file):
            all_vulnerabilities.extend(scan_file(py_file))
    
    # Scan all JavaScript files (excluding ignored dirs)
    for js_file in path.rglob("*.js"):
        if should_scan_file(js_file):
            all_vulnerabilities.extend(scan_file(js_file))
    
    # Scan all TypeScript files (excluding ignored dirs)
    for ts_file in path.rglob("*.ts"):
        if should_scan_file(ts_file):
            all_vulnerabilities.extend(scan_file(ts_file))
    
    # Calculate summary
    summary = {
        "critical": sum(1 for v in all_vulnerabilities if v.severity == Severity.CRITICAL),
        "high": sum(1 for v in all_vulnerabilities if v.severity == Severity.HIGH),
        "medium": sum(1 for v in all_vulnerabilities if v.severity == Severity.MEDIUM),
        "low": sum(1 for v in all_vulnerabilities if v.severity == Severity.LOW),
        "info": sum(1 for v in all_vulnerabilities if v.severity == Severity.INFO),
    }
    
    # Determine pass/fail
    passed = summary["critical"] == 0 and summary["high"] == 0
    
    return AuditResult(
        skill_name=path.name,
        skill_path=str(path.absolute()),
        passed=passed,
        vulnerabilities=all_vulnerabilities,
        summary=summary
    )


def format_report(result: AuditResult, format_type: str = "summary") -> str:
    """Format audit result for output."""
    
    if format_type == "json":
        return json.dumps(result.to_dict(), indent=2)
    
    elif format_type == "markdown":
        lines = [
            f"# Security Audit: {result.skill_name}",
            "",
            f"**Status:** {'✅ PASSED' if result.passed else '❌ FAILED'}",
            f"**Path:** `{result.skill_path}`",
            "",
            "## Summary",
            "",
            f"| Severity | Count |",
            f"|----------|-------|",
            f"| Critical | {result.summary['critical']} |",
            f"| High | {result.summary['high']} |",
            f"| Medium | {result.summary['medium']} |",
            f"| Low | {result.summary['low']} |",
            f"| Info | {result.summary['info']} |",
            "",
            "## Vulnerabilities",
            "",
        ]
        
        if not result.vulnerabilities:
            lines.append("No vulnerabilities found.")
        else:
            for v in result.vulnerabilities:
                lines.extend([
                    f"### {v.name}",
                    "",
                    f"- **ID:** {v.id}",
                    f"- **Severity:** {v.severity.value.upper()}",
                    f"- **File:** `{v.file}:{v.line}`",
                    f"- **Description:** {v.description}",
                    f"- **Code:** `{v.code_snippet}`",
                    f"- **Fix:** {v.remediation}",
                    "",
                ])
        
        return '\n'.join(lines)
    
    else:  # summary format
        status = "✅ PASSED" if result.passed else "❌ FAILED"
        lines = [
            f"\n{'='*60}",
            f"Security Audit: {result.skill_name}",
            f"{'='*60}",
            f"Status: {status}",
            f"Path: {result.skill_path}",
            f"",
            f"Vulnerabilities by Severity:",
            f"  Critical: {result.summary['critical']}",
            f"  High:      {result.summary['high']}",
            f"  Medium:    {result.summary['medium']}",
            f"  Low:       {result.summary['low']}",
            f"  Info:      {result.summary['info']}",
            f"",
        ]
        
        if result.vulnerabilities:
            lines.append("Issues Found:")
            lines.append("")
            for v in sorted(result.vulnerabilities, key=lambda x: list(Severity).index(x.severity)):
                lines.append(f"  [{v.severity.value.upper():8}] {v.file}:{v.line} - {v.name}")
                lines.append(f"             {v.description[:80]}...")
                lines.append("")
        
        return '\n'.join(lines)


def main():
    """CLI entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Audit OpenClaw skills for security vulnerabilities")
    parser.add_argument("path", help="Path to skill directory")
    parser.add_argument("--format", "-f", choices=["summary", "json", "markdown"], default="summary",
                        help="Output format (default: summary)")
    
    args = parser.parse_args()
    
    result = audit_skill(args.path)
    print(format_report(result, args.format))
    
    # Exit with appropriate code
    if result.summary["critical"] > 0:
        sys.exit(2)
    elif result.summary["high"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()