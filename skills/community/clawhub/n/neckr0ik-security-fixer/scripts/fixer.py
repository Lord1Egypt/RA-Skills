#!/usr/bin/env python3
"""
Security Fixer for OpenClaw Skills

Automatically fixes security vulnerabilities detected by neckr0ik-security-scanner.

Usage:
    python fixer.py fix <skill-path> [--auto] [--dry-run] [--backup]
    python fixer.py env <skill-path>
    python fixer.py report <skill-path> [--format json|markdown]
"""

import os
import re
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


# Import the audit module
try:
    from audit import audit_skill, Vulnerability, Severity
except ImportError:
    # If running from different directory
    sys.path.insert(0, str(Path(__file__).parent))
    from audit import audit_skill, Vulnerability, Severity


@dataclass
class Fix:
    """Represents a fix for a vulnerability."""
    
    vulnerability: Vulnerability
    original_code: str
    fixed_code: str
    file_path: Path
    line_start: int
    line_end: int
    auto_fixable: bool
    manual_review: bool = False
    notes: str = ""


class Fixer:
    """Applies security fixes to skill files."""
    
    def __init__(self, skill_path: str, dry_run: bool = False, backup: bool = True):
        self.skill_path = Path(skill_path)
        self.dry_run = dry_run
        self.backup = backup
        self.fixes: List[Fix] = []
        self.env_vars: Dict[str, str] = {}
    
    def scan_and_fix(self, auto: bool = False) -> List[Fix]:
        """Scan skill and generate fixes."""
        
        # Run audit
        result = audit_skill(str(self.skill_path))
        
        for vuln in result.vulnerabilities:
            fix = self._generate_fix(vuln)
            if fix:
                self.fixes.append(fix)
        
        return self.fixes
    
    def _generate_fix(self, vuln: Vulnerability) -> Optional[Fix]:
        """Generate a fix for a vulnerability."""
        
        file_path = Path(vuln.file)
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception:
            return None
        
        # Get original code
        line_start = max(1, vuln.line - 2)
        line_end = min(len(lines), vuln.line + 2)
        original_code = '\n'.join(lines[line_start-1:line_end])
        
        # Generate fix based on vulnerability type
        fixed_code = None
        auto_fixable = False
        manual_review = False
        notes = ""
        
        if "SECRET" in vuln.id:
            fixed_code, auto_fixable = self._fix_secret(vuln, lines)
            notes = "Moved secret to environment variable. Add to .env file."
        
        elif "SHELL" in vuln.id:
            fixed_code, auto_fixable = self._fix_shell(vuln, lines)
            notes = "Converted to subprocess.run() with shell=False"
        
        elif "PROMPT" in vuln.id:
            fixed_code, auto_fixable = self._fix_prompt_injection(vuln, lines)
            notes = "Added sanitization wrapper for user input"
        
        elif "PATH" in vuln.id:
            fixed_code, auto_fixable = self._fix_path_traversal(vuln, lines)
            notes = "Added pathlib validation for file paths"
        
        elif "DEP" in vuln.id:
            fixed_code, auto_fixable = self._fix_dependency(vuln, lines)
            notes = "Pinned dependency version"
        
        else:
            manual_review = True
            notes = "Manual review required - no automatic fix available"
        
        if not fixed_code:
            return None
        
        return Fix(
            vulnerability=vuln,
            original_code=original_code,
            fixed_code=fixed_code,
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            auto_fixable=auto_fixable,
            manual_review=manual_review,
            notes=notes
        )
    
    def _fix_secret(self, vuln: Vulnerability, lines: List[str]) -> Tuple[str, bool]:
        """Fix hardcoded secrets."""
        
        line = lines[vuln.line - 1] if vuln.line <= len(lines) else ""
        
        # Extract variable name and generate env var name
        var_match = re.search(r'(\w+)\s*[=:]\s*["\']([^"\']+)["\']', line)
        if not var_match:
            return None, False
        
        var_name = var_match.group(1)
        env_name = var_name.upper().replace('-', '_')
        
        # Add to env vars for .env.example
        self.env_vars[env_name] = "your-value-here"
        
        # Generate fix
        indent = len(line) - len(line.lstrip())
        fixed = f'''{line[:indent]}import os
{line[:indent]}{var_name} = os.environ.get("{env_name}")
{line[:indent]}if not {var_name}:
{line[:indent]}    raise ValueError("{env_name} environment variable required")'''
        
        return fixed, True
    
    def _fix_shell(self, vuln: Vulnerability, lines: List[str]) -> Tuple[str, bool]:
        """Fix shell injection vulnerabilities."""
        
        line = lines[vuln.line - 1] if vuln.line <= len(lines) else ""
        
        # os.system to subprocess
        if 'os.system' in line:
            match = re.search(r'os\.system\s*\(\s*f?["\']([^"\']+)["\']', line)
            if match:
                cmd_template = match.group(1)
                # Simple case: no f-string
                if '{' not in cmd_template:
                    parts = cmd_template.split()
                    fixed = f'''import subprocess
subprocess.run({parts}, check=True)'''
                    return fixed, True
        
        # subprocess with shell=True
        if 'shell=True' in line:
            fixed = line.replace('shell=True', 'shell=False')
            return fixed, True
        
        # eval/exec - flag for manual review
        if 'eval(' in line or 'exec(' in line:
            return "# SECURITY: Manual review required - eval/exec detected\n# " + line, False
        
        return None, False
    
    def _fix_prompt_injection(self, vuln: Vulnerability, lines: List[str]) -> Tuple[str, bool]:
        """Fix prompt injection vulnerabilities."""
        
        line = lines[vuln.line - 1] if vuln.line <= len(lines) else ""
        
        indent = len(line) - len(line.lstrip())
        
        fixed = f'''{line[:indent]}import re
{line[:indent]}def sanitize_for_prompt(text: str) -> str:
{line[:indent]}    return re.sub(r'[<>\\{{\\}}\\[\\]\\\\]', '', text[:1000])
{line[:indent]}
{line[:indent]}# Sanitize user input before use in prompt
{line[:indent]}sanitized_input = sanitize_for_prompt(user_input)'''
        
        return fixed, True
    
    def _fix_path_traversal(self, vuln: Vulnerability, lines: List[str]) -> Tuple[str, bool]:
        """Fix path traversal vulnerabilities."""
        
        line = lines[vuln.line - 1] if vuln.line <= len(lines) else ""
        
        indent = len(line) - len(line.lstrip())
        
        fixed = f'''{line[:indent]}from pathlib import Path
{line[:indent]}import re
{line[:indent]}
{line[:indent]}def safe_path(base_dir: str, user_input: str) -> Path:
{line[:indent]}    safe_name = re.sub(r'[^\\w.-]', '_', Path(user_input).name)
{line[:indent]}    full_path = (Path(base_dir) / safe_name).resolve()
{line[:indent]}    if not str(full_path).startswith(str(Path(base_dir).resolve())):
{line[:indent]}        raise ValueError("Path traversal detected")
{line[:indent]}    return full_path'''
        
        return fixed, True
    
    def _fix_dependency(self, vuln: Vulnerability, lines: List[str]) -> Tuple[str, bool]:
        """Fix unpinned dependencies."""
        
        # This is in requirements.txt or package.json
        # For now, flag for manual review
        return "# SECURITY: Pin this dependency to a specific version\n# Example: package==1.2.3", False
    
    def apply_fixes(self, auto: bool = False) -> List[Fix]:
        """Apply all fixes to files."""
        
        applied = []
        
        for fix in self.fixes:
            if fix.manual_review and not auto:
                print(f"[REVIEW] {fix.file_path}:{fix.vulnerability.line} - {fix.vulnerability.name}")
                print(f"         {fix.notes}")
                continue
            
            if not fix.auto_fixable and not auto:
                print(f"[MANUAL] {fix.file_path}:{fix.vulnerability.line} - {fix.vulnerability.name}")
                print(f"         Requires manual fix")
                continue
            
            # Apply fix
            if self.dry_run:
                print(f"[DRY-RUN] Would fix: {fix.file_path}:{fix.vulnerability.line}")
                print(f"  Original: {fix.original_code[:80]}...")
                print(f"  Fixed:    {fix.fixed_code[:80]}...")
            else:
                self._apply_fix(fix)
                applied.append(fix)
                print(f"[FIXED] {fix.file_path}:{fix.vulnerability.line} - {fix.vulnerability.name}")
        
        return applied
    
    def _apply_fix(self, fix: Fix) -> None:
        """Apply a single fix to a file."""
        
        # Create backup if enabled
        if self.backup:
            backup_path = fix.file_path.with_suffix(fix.file_path.suffix + '.bak')
            shutil.copy2(fix.file_path, backup_path)
        
        # Read file
        content = fix.file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Replace lines
        new_lines = lines[:fix.line_start-1]
        new_lines.extend(fix.fixed_code.split('\n'))
        new_lines.extend(lines[fix.line_end:])
        
        # Write back
        fix.file_path.write_text('\n'.join(new_lines), encoding='utf-8')
    
    def generate_env_example(self) -> None:
        """Generate .env.example file with detected secrets."""
        
        if not self.env_vars:
            print("[INFO] No environment variables detected")
            return
        
        env_path = self.skill_path / '.env.example'
        gitignore_path = self.skill_path / '.gitignore'
        
        # Generate .env.example
        content = "# Environment variables for " + self.skill_path.name + "\n"
        content += "# Copy to .env and fill in your values\n\n"
        
        for var, placeholder in self.env_vars.items():
            content += f"{var}={placeholder}\n"
        
        if not self.dry_run:
            env_path.write_text(content)
            print(f"[CREATED] {env_path}")
        else:
            print(f"[DRY-RUN] Would create: {env_path}")
            print(content)
        
        # Update .gitignore
        gitignore_content = ""
        if gitignore_path.exists():
            gitignore_content = gitignore_path.read_text()
        
        if '.env' not in gitignore_content:
            gitignore_content += "\n# Environment variables\n.env\n.env.local\n"
            
            if not self.dry_run:
                gitignore_path.write_text(gitignore_content)
                print(f"[UPDATED] {gitignore_path}")
            else:
                print(f"[DRY-RUN] Would update: {gitignore_path}")


def main():
    """CLI entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix security vulnerabilities in OpenClaw skills")
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # fix command
    fix_parser = subparsers.add_parser('fix', help='Fix vulnerabilities')
    fix_parser.add_argument('path', help='Path to skill directory')
    fix_parser.add_argument('--auto', action='store_true', help='Apply all fixes automatically')
    fix_parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    fix_parser.add_argument('--no-backup', action='store_true', help='Do not create backup files')
    
    # env command
    env_parser = subparsers.add_parser('env', help='Generate .env.example')
    env_parser.add_argument('path', help='Path to skill directory')
    env_parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    
    # report command
    report_parser = subparsers.add_parser('report', help='Generate fix report')
    report_parser.add_argument('path', help='Path to skill directory')
    report_parser.add_argument('--format', choices=['json', 'markdown', 'summary'], default='summary')
    
    args = parser.parse_args()
    
    if args.command == 'fix':
        fixer = Fixer(
            args.path,
            dry_run=args.dry_run,
            backup=not args.no_backup
        )
        
        print(f"Scanning {args.path}...")
        fixer.scan_and_fix()
        
        print(f"\nFound {len(fixer.fixes)} issues")
        applied = fixer.apply_fixes(auto=args.auto)
        
        if fixer.env_vars:
            fixer.generate_env_example()
        
        print(f"\nApplied {len(applied)} fixes")
        
    elif args.command == 'env':
        fixer = Fixer(args.path, dry_run=args.dry_run)
        fixer.scan_and_fix()
        fixer.generate_env_example()
        
    elif args.command == 'report':
        fixer = Fixer(args.path, dry_run=True)
        fixer.scan_and_fix()
        
        if args.format == 'json':
            report = {
                'skill': args.path,
                'total_issues': len(fixer.fixes),
                'fixes': [
                    {
                        'file': str(f.file_path),
                        'line': f.vulnerability.line,
                        'severity': f.vulnerability.severity.value,
                        'issue': f.vulnerability.name,
                        'auto_fixable': f.auto_fixable,
                        'manual_review': f.manual_review,
                        'notes': f.notes
                    }
                    for f in fixer.fixes
                ]
            }
            print(json.dumps(report, indent=2))
        
        elif args.format == 'markdown':
            print(f"# Security Fix Report: {Path(args.path).name}")
            print(f"\n**Total Issues:** {len(fixer.fixes)}")
            print(f"\n## Fixes\n")
            
            for f in fixer.fixes:
                status = "✅ Auto-fixable" if f.auto_fixable else "⚠️ Manual review"
                print(f"### {f.vulnerability.name}")
                print(f"\n- **File:** `{f.file_path}:{f.vulnerability.line}`")
                print(f"- **Severity:** {f.vulnerability.severity.value.upper()}")
                print(f"- **Status:** {status}")
                print(f"- **Notes:** {f.notes}")
                print()
        
        else:  # summary
            print(f"\n{'='*60}")
            print(f"Security Fix Report: {Path(args.path).name}")
            print(f"{'='*60}")
            print(f"Total Issues: {len(fixer.fixes)}")
            print(f"Auto-fixable: {sum(1 for f in fixer.fixes if f.auto_fixable)}")
            print(f"Manual Review: {sum(1 for f in fixer.fixes if f.manual_review)}")
            print()
            
            for f in fixer.fixes:
                status = "[AUTO]" if f.auto_fixable else "[MANUAL]"
                print(f"  {status} {f.file_path}:{f.vulnerability.line}")
                print(f"         {f.vulnerability.name}")
                print()
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()