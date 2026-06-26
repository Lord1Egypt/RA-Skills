#!/usr/bin/env python3
"""
Security - Security Analysis Tool
Supports: Python, JavaScript, C/C++
"""

import argparse
import ast
import re
import sys
from pathlib import Path

# Import C support library
c_support_path = Path(__file__).parent.parent.parent / 'c-support' / 'lib'
if c_support_path.exists():
    sys.path.insert(0, str(c_support_path))
    try:
        from c_security_rules import CSecurityChecker, CSecurityRules
        C_SUPPORT_AVAILABLE = True
    except ImportError:
        C_SUPPORT_AVAILABLE = False
else:
    C_SUPPORT_AVAILABLE = False


class SecurityScanner:
    """Scans code for security issues - supports Python and C/C++"""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.c_checker = CSecurityChecker() if C_SUPPORT_AVAILABLE else None

    def scan_file(self, filepath: Path) -> list:
        """Scan a file for security issues"""
        # Determine file type
        if filepath.suffix in ['.c', '.h']:
            return self._scan_c_file(filepath)
        elif filepath.suffix == '.py':
            return self._scan_python_file(filepath)
        else:
            # Try both for unknown extensions
            issues = self._scan_python_file(filepath)
            if not issues:
                issues = self._scan_c_file(filepath)
            return issues

    def _scan_c_file(self, filepath: Path) -> list:
        """Scan C/C++ file for security issues"""
        if not self.c_checker:
            return [{
                'line': 0,
                'message': 'C support not available. Install tree-sitter and pycparser',
                'severity': 'warning',
                'type': 'config'
            }]

        try:
            issues = self.c_checker.check_file(str(filepath))
            return [{
                'line': issue.line,
                'message': issue.title,
                'severity': issue.severity.value,
                'type': 'c-security',
                'cwe': issue.cwe_id,
                'fix': issue.fix,
                'description': issue.description
            } for issue in issues]
        except Exception as e:
            return [{
                'line': 0,
                'message': f'C scan error: {e}',
                'severity': 'error',
                'type': 'parse'
            }]

    def _scan_python_file(self, filepath: Path) -> list:
        """Scan Python file for security issues"""
        issues = []

        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.split('\n')
            tree = ast.parse(content)
        except Exception as e:
            return [{'line': 0, 'message': f'Parse error: {e}', 'severity': 'error', 'type': 'parse'}]

        # Check for hardcoded credentials
        issues.extend(self._check_hardcoded_credentials(content, lines, filepath))

        # Check for SQL injection
        issues.extend(self._check_sql_injection(tree, lines, filepath))

        # Check for command injection
        issues.extend(self._check_command_injection(tree, lines, filepath))

        # Check for debug mode
        issues.extend(self._check_debug_mode(tree, lines, filepath))

        return issues

    def _check_hardcoded_credentials(self, content: str, lines: list, filepath: Path) -> list:
        """Check for hardcoded credentials"""
        issues = []

        patterns = [
            (r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
            (r'(api_key|apikey)\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret'),
            (r'token\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded token'),
        ]

        for pattern, message in patterns:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    # Skip comments and example placeholders
                    if '#' in line and ('example' in line.lower() or 'placeholder' in line.lower()):
                        continue
                    if 'xxx' in line.lower() or 'your_' in line.lower():
                        continue

                    issues.append({
                        'line': i,
                        'message': message,
                        'severity': 'critical',
                        'type': 'hardcoded-credentials',
                        'cwe': 'CWE-798',
                        'fix': 'Move to environment variable or secrets manager'
                    })

        return issues

    def _check_sql_injection(self, tree: ast.AST, lines: list, filepath: Path) -> list:
        """Check for SQL injection vulnerabilities"""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_call_name(node)
                if func_name and any(x in func_name.lower() for x in ['execute', 'query', 'raw']):
                    # Check if using f-string or format
                    for arg in node.args:
                        if isinstance(arg, ast.JoinedStr):  # f-string
                            issues.append({
                                'line': node.lineno,
                                'message': f'Potential SQL injection in {func_name}()',
                                'severity': 'high',
                                'type': 'sql-injection',
                                'cwe': 'CWE-89',
                                'fix': 'Use parameterized queries'
                            })

        return issues

    def _check_command_injection(self, tree: ast.AST, lines: list, filepath: Path) -> list:
        """Check for command injection vulnerabilities"""
        issues = []

        dangerous_funcs = ['os.system', 'subprocess.call', 'subprocess.Popen', 'eval', 'exec']

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_call_name(node)
                if func_name and any(func_name.endswith(f) for f in dangerous_funcs):
                    issues.append({
                        'line': node.lineno,
                        'message': f'Dangerous function call: {func_name}()',
                        'severity': 'high',
                        'type': 'command-injection',
                        'cwe': 'CWE-78',
                        'fix': 'Avoid using shell=True; validate inputs'
                    })

        return issues

    def _check_debug_mode(self, tree: ast.AST, lines: list, filepath: Path) -> list:
        """Check for debug mode enabled"""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == 'DEBUG':
                        if isinstance(node.value, ast.Constant) and node.value.value == True:
                            issues.append({
                                'line': node.lineno,
                                'message': 'DEBUG mode enabled',
                                'severity': 'medium',
                                'type': 'debug-mode',
                                'cwe': 'CWE-489',
                                'fix': 'Set DEBUG = False in production'
                            })

        return issues

    def _get_call_name(self, node: ast.Call) -> str:
        """Get function call name"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                return f"{node.func.value.id}.{node.func.attr}"
            return node.func.attr
        return None


class SecretDetector:
    """Detects secrets in code - supports Python and C/C++"""

    PATTERNS = [
        (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
        (r'aws_secret_access_key\s*=\s*["\']?[A-Za-z0-9/+=]{40}["\']?', 'AWS Secret Key'),
        (r'ghp_[A-Za-z0-9]{36}', 'GitHub Personal Access Token'),
        (r'sk-[A-Za-z0-9]{20,}', 'OpenAI/Stripe API Key'),
        (r'private[_-]?key\s*[=:]\s*["\']?-----BEGIN', 'Private Key'),
        (r'database[_-]?url\s*[=:]\s*["\']?\w+://[^:]+:[^@]+@', 'Database URL with credentials'),
    ]

    C_PATTERNS = [
        (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
        (r'api_key\s*=\s*["\'][^"\']+["\']', 'Hardcoded API key'),
        (r'secret\s*=\s*["\'][^"\']+["\']', 'Hardcoded secret'),
    ]

    def scan_file(self, filepath: Path) -> list:
        """Scan file for secrets"""
        findings = []

        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception:
            return []

        is_c_file = filepath.suffix in ['.c', '.h']
        patterns = self.PATTERNS + (self.C_PATTERNS if is_c_file else [])

        for i, line in enumerate(lines, 1):
            for pattern, secret_type in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Skip comments
                    code = line.split('//')[0] if is_c_file else line.split('#')[0]
                    if not re.search(pattern, code, re.IGNORECASE):
                        continue

                    # Mask the secret
                    masked = re.sub(r'["\'][^"\']{10,}["\']', '"***MASKED***"', line.strip())
                    findings.append({
                        'line': i,
                        'type': secret_type,
                        'content': masked,
                        'severity': 'critical'
                    })

        return findings


def run_scan(args):
    """Run security scan"""
    scanner = SecurityScanner(args.root)

    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"❌ File not found: {args.file}")
            return
        files = [filepath]
    elif args.dir:
        dirpath = Path(args.dir)
        if not dirpath.exists():
            print(f"❌ Directory not found: {args.dir}")
            return
        # Scan both Python and C files
        files = list(dirpath.rglob('*.py')) + list(dirpath.rglob('*.c')) + list(dirpath.rglob('*.h'))
    else:
        print("❌ Specify --file or --dir")
        return

    print("\n🔒 Security Scan Results")
    print(f"{'='*60}")

    if not files:
        print("No files found to scan")
        return

    total_issues = 0
    c_files = 0
    py_files = 0

    for filepath in files:
        issues = scanner.scan_file(filepath)
        if issues:
            total_issues += len(issues)
            print(f"\n📄 {filepath}")

            if filepath.suffix in ['.c', '.h']:
                c_files += 1
            elif filepath.suffix == '.py':
                py_files += 1

            for issue in issues:
                emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}.get(issue['severity'], '⚪')
                print(f"  {emoji} Line {issue['line']}: {issue['message']}")
                if 'cwe' in issue:
                    print(f"     📋 {issue['cwe']}")
                if 'fix' in issue:
                    print(f"     💡 {issue['fix']}")

    if total_issues == 0:
        print("\n✅ No security issues found!")
    else:
        print(f"\n{'='*60}")
        print(f"⚠️  Total issues: {total_issues}")
        if c_files > 0:
            print(f"   C files scanned: {c_files}")
        if py_files > 0:
            print(f"   Python files scanned: {py_files}")


def run_deps(args):
    """Check dependencies"""
    print("\n📦 Dependency Check")
    print(f"{'='*60}")

    if args.requirements:
        req_file = Path(args.requirements)
        if req_file.exists():
            content = req_file.read_text()
            packages = []
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    packages.append(line)

            print(f"Found {len(packages)} packages")
            print()
            print("ℹ️  Use safety or pip-audit for comprehensive vulnerability scanning:")
            print("  pip install safety")
            print("  safety check -r requirements.txt")
        else:
            print(f"❌ File not found: {args.requirements}")
    else:
        print("ℹ️  Specify --requirements or --package-json")


def run_secrets(args):
    """Detect secrets"""
    detector = SecretDetector()

    dirpath = Path(args.dir) if args.dir else Path('.')

    if not dirpath.exists():
        print(f"❌ Directory not found: {args.dir}")
        return

    print("\n🔑 Secret Detection")
    print(f"{'='*60}")

    total_secrets = 0
    scanned = 0

    for filepath in dirpath.rglob('*'):
        if filepath.is_file() and filepath.stat().st_size < 1024 * 1024:  # Skip large files
            # Check relevant file types
            if filepath.suffix in ['.py', '.c', '.h', '.js', '.ts', '.json', '.yml', '.yaml', '.env']:
                scanned += 1
                secrets = detector.scan_file(filepath)
                if secrets:
                    total_secrets += len(secrets)
                    print(f"\n🔴 {filepath}")
                    for secret in secrets:
                        print(f"   Line {secret['line']}: {secret['type']}")
                        print(f"   {secret['content']}")

    print(f"\nScanned: {scanned} files")
    if total_secrets == 0:
        print("✅ No secrets found")
    else:
        print(f"⚠️  Secrets found: {total_secrets}")
        print("\n⚡ Action required: Move secrets to environment variables or secrets manager")


def main():
    parser = argparse.ArgumentParser(
        description='Security Analysis Tool - Supports Python and C/C++',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan Python files
  python3 main.py scan --file src.py
  python3 main.py scan --dir src/

  # Scan C files
  python3 main.py scan --file main.c
  python3 main.py scan --dir src/  # Auto-detects .c, .h files

  # Check dependencies
  python3 main.py deps --requirements requirements.txt

  # Detect secrets
  python3 main.py secrets --dir .
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # scan command
    scan_parser = subparsers.add_parser('scan', help='Scan code')
    scan_parser.add_argument('--file', help='File to scan')
    scan_parser.add_argument('--dir', help='Directory to scan')
    scan_parser.add_argument('--root', default='.', help='Project root')
    scan_parser.set_defaults(func=run_scan)

    # deps command
    deps_parser = subparsers.add_parser('deps', help='Check dependencies')
    deps_parser.add_argument('--requirements', help='requirements.txt path')
    deps_parser.add_argument('--package-json', help='package.json path')
    deps_parser.add_argument('--root', default='.', help='Project root')
    deps_parser.set_defaults(func=run_deps)

    # secrets command
    secrets_parser = subparsers.add_parser('secrets', help='Detect secrets')
    secrets_parser.add_argument('--dir', default='.', help='Directory to scan')
    secrets_parser.add_argument('--root', default='.', help='Project root')
    secrets_parser.set_defaults(func=run_secrets)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
