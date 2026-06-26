#!/usr/bin/env python3
"""
OpenClaw Security Audit Script
Automated security checks for external resources before execution.
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple

# ANSI color codes for terminal output
COLORS = {
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'RED': '\033[91m',
    'BLUE': '\033[94m',
    'RESET': '\033[0m',
}

# High-risk file extensions
HIGH_RISK_EXTENSIONS = {
    '.exe', '.bat', '.cmd', '.msi', '.app', '.dmg',
    '.pkg', '.deb', '.rpm', '.sh', '.ps1', '.vbs',
    '.dll', '.so', '.dylib', '.bin'
}

# Safe source code extensions
SAFE_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.rs',
    '.java', '.c', '.cpp', '.h', '.hpp', '.php', '.rb',
    '.swift', '.kt', '.dart', '.lua', '.r', '.m'
}

# Suspicious patterns in text files
SUSPICIOUS_PATTERNS = [
    r'base64\s*\([^)]{100,}\)',  # Long base64 strings
    r'[a-zA-Z0-9+/]{100,}={0,2}',  # Base64-like strings
    r'eval\s*\([^)]+\)',  # eval() usage
    r'exec\s*\([^)]+\)',  # exec() usage
    r'__import__\s*\(\s*[\'""][^\'"]+[\'"]\s*\)',  # Dynamic imports
    r'shellcode',  # Shellcode keyword
    r'malware|virus|trojan|backdoor',  # Malware keywords
]


def color_print(text: str, color: str = 'RESET'):
    """Print colored text to terminal."""
    if sys.stdout.isatty():
        print(f"{COLORS.get(color, '')}{text}{COLORS['RESET']}")
    else:
        print(text)


def get_file_extension(filepath: Path) -> str:
    """Get file extension in lowercase."""
    return filepath.suffix.lower()


def is_high_risk_file(filepath: Path) -> bool:
    """Check if file is high-risk type."""
    ext = get_file_extension(filepath)
    return ext in HIGH_RISK_EXTENSIONS


def is_safe_source_file(filepath: Path) -> bool:
    """Check if file is safe source code."""
    ext = get_file_extension(filepath)
    return ext in SAFE_EXTENSIONS


def is_text_file(filepath: Path) -> bool:
    """Check if file is text type by reading first bytes."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            # Check for null bytes (binary indicator)
            if b'\x00' in chunk:
                return False
            # Try to decode as UTF-8
            chunk.decode('utf-8')
            return True
    except (UnicodeDecodeError, IOError):
        return False


def scan_text_file(filepath: Path) -> Dict[str, List[int]]:
    """Scan text file for suspicious patterns."""
    results = {pattern: [] for pattern in SUSPICIOUS_PATTERNS}
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                # Remove Python comments and string literals to reduce false positives
                cleaned_line = line
                # Remove single-line comments
                cleaned_line = re.sub(r'#.*$', '', cleaned_line)
                # Remove multi-line strings (Python triple quotes)
                cleaned_line = re.sub(r'"""[\s\S]*?"""', '', cleaned_line)
                cleaned_line = re.sub(r"'''[\s\S]*?'''", '', cleaned_line)
                # Remove regular string literals
                cleaned_line = re.sub(r'"[^"]*"', '', cleaned_line)
                cleaned_line = re.sub(r"'[^']*'", '', cleaned_line)
                
                for pattern in SUSPICIOUS_PATTERNS:
                    if re.search(pattern, cleaned_line, re.IGNORECASE):
                        results[pattern].append(line_num)
    except Exception as e:
        pass
    
    return results


def check_single_line_large_file(filepath: Path) -> bool:
    """Check if file has extremely long single line (potential shellcode)."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if len(line) > 50000:  # Threshold: 50KB single line
                    return True
    except Exception:
        pass
    return False


def check_readme_mismatch(directory: Path) -> Tuple[bool, str]:
    """Check if README description matches actual content."""
    readme_files = list(directory.glob('README*')) + list(directory.glob('readme*'))
    
    if not readme_files:
        return False, "No README found"
    
    readme_path = readme_files[0]
    
    try:
        with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
            readme_content = f.read().lower()
    except Exception:
        return False, "Cannot read README"
    
    # Check for suspicious claims vs actual files
    has_source_code = any(
        is_safe_source_file(f)
        for f in directory.rglob('*')
        if f.is_file()
    )
    
    # Check for direct download links in README
    if '.zip' in readme_content and 'raw.githubusercontent' in readme_content:
        return True, "README contains direct download links (suspicious)"
    
    # Check for memory/AI claims without actual AI code
    memory_keywords = ['memory', 'ai', 'intelligence', 'three-layer', '三层']
    if any(keyword in readme_content for keyword in memory_keywords):
        if not has_source_code:
            return True, "Claims AI/memory features but no source code found"
    
    return False, "OK"


def scan_directory(directory: Path, verbose: bool = False) -> Dict:
    """Scan directory for security issues."""
    results = {
        'high_risk_files': [],
        'source_files': [],
        'suspicious_patterns': {},
        'large_single_line_files': [],
        'readme_mismatch': False,
        'readme_msg': '',
        'total_files': 0,
    }
    
    for filepath in directory.rglob('*'):
        if not filepath.is_file():
            continue
        
        results['total_files'] += 1
        
        # Check file type
        if is_high_risk_file(filepath):
            results['high_risk_files'].append(str(filepath))
            if verbose:
                color_print(f"⚠️  High-risk file: {filepath}", 'YELLOW')
        
        elif is_safe_source_file(filepath):
            results['source_files'].append(str(filepath))
            if verbose:
                color_print(f"✅ Source file: {filepath}", 'GREEN')
        
        # Check text files
        if is_text_file(filepath):
            # Check for large single line
            if check_single_line_large_file(filepath):
                results['large_single_line_files'].append(str(filepath))
                if verbose:
                    color_print(f"🚨 Large single-line file: {filepath}", 'RED')
            
            # Scan for suspicious patterns
            suspicious = scan_text_file(filepath)
            for pattern, lines in suspicious.items():
                if lines:
                    if pattern not in results['suspicious_patterns']:
                        results['suspicious_patterns'][pattern] = []
                    results['suspicious_patterns'][pattern].extend(
                        [f"{filepath}:{line}" for line in lines]
                    )
                    if verbose:
                        color_print(f"⚠️  Suspicious pattern in {filepath} (line {lines[0]})", 'YELLOW')
    
    # Check README
    mismatch, msg = check_readme_mismatch(directory)
    results['readme_mismatch'] = mismatch
    results['readme_msg'] = msg
    
    return results


def calculate_risk_level(results: Dict) -> str:
    """Calculate overall risk level."""
    critical_score = 0
    
    # High-risk executables without source code
    if results['high_risk_files'] and not results['source_files']:
        critical_score += 3
    
    # Large single-line files (potential shellcode)
    if results['large_single_line_files']:
        critical_score += 3
    
    # README mismatch
    if results['readme_mismatch']:
        critical_score += 2
    
    # Suspicious patterns
    if results['suspicious_patterns']:
        critical_score += len(results['suspicious_patterns'])
    
    if critical_score >= 5:
        return 'CRITICAL'
    elif critical_score >= 2:
        return 'WARNING'
    else:
        return 'SAFE'


def print_report(results: Dict, output_file: str = None):
    """Print security audit report."""
    risk_level = calculate_risk_level(results)
    
    # Header
    if risk_level == 'CRITICAL':
        color_print("\n🚨 Security Audit: BLOCKED", 'RED')
    elif risk_level == 'WARNING':
        color_print("\n⚠️  Security Audit: WARNING", 'YELLOW')
    else:
        color_print("\n🛡️ Security Audit: PASSED", 'GREEN')
    
    color_print("=" * 50, 'BLUE')
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   Total files scanned: {results['total_files']}")
    print(f"   Source code files: {len(results['source_files'])}")
    print(f"   High-risk files: {len(results['high_risk_files'])}")
    print(f"   Suspicious patterns: {sum(len(v) for v in results['suspicious_patterns'].values())}")
    
    # Detailed findings
    if results['high_risk_files']:
        color_print("\n🚨 High-Risk Files (Executable):", 'RED')
        for f in results['high_risk_files']:
            color_print(f"   - {f}", 'RED')
    
    if results['source_files'] and not results['high_risk_files']:
        color_print("\n✅ Source Code Found:", 'GREEN')
        for f in results['source_files'][:5]:
            color_print(f"   - {f}", 'GREEN')
        if len(results['source_files']) > 5:
            print(f"   ... and {len(results['source_files']) - 5} more")
    
    if results['large_single_line_files']:
        color_print("\n🚨 Large Single-Line Files (Potential Shellcode):", 'RED')
        for f in results['large_single_line_files']:
            color_print(f"   - {f}", 'RED')
    
    if results['suspicious_patterns']:
        color_print("\n⚠️  Suspicious Patterns Found:", 'YELLOW')
        for pattern, locations in results['suspicious_patterns'].items():
            print(f"   Pattern: {pattern}")
            for loc in locations[:3]:
                color_print(f"     - {loc}", 'YELLOW')
            if len(locations) > 3:
                print(f"     ... and {len(locations) - 3} more")
    
    if results['readme_mismatch']:
        color_print(f"\n🚨 README Mismatch: {results['readme_msg']}", 'RED')
    
    # Recommendation
    color_print("\n" + "=" * 50, 'BLUE')
    if risk_level == 'CRITICAL':
        color_print("\n🛑 DO NOT EXECUTE", 'RED')
        color_print("Recommendation: Delete immediately - this appears to be malware", 'RED')
    elif risk_level == 'WARNING':
        color_print("\n⚠️ Review Before Execution", 'YELLOW')
        color_print("Recommendation: Manual review required", 'YELLOW')
    else:
        color_print("\n✅ Safe to Use", 'GREEN')
        color_print("Recommendation: No immediate concerns", 'GREEN')
    
    print()
    
    # Save to file if requested
    if output_file:
        with open(output_file, 'w') as f:
            f.write(f"Security Audit Report\n")
            f.write(f"Risk Level: {risk_level}\n")
            f.write(f"Total Files: {results['total_files']}\n")
            f.write(f"\nDetails:\n{results}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Security audit for external resources'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory to scan (default: current directory)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed output during scan'
    )
    parser.add_argument(
        '-o', '--output',
        help='Save report to file'
    )
    
    args = parser.parse_args()
    
    directory = Path(args.directory).resolve()
    
    if not directory.exists():
        color_print(f"❌ Directory not found: {directory}", 'RED')
        sys.exit(1)
    
    color_print(f"🔍 Scanning: {directory}", 'BLUE')
    print()
    
    results = scan_directory(directory, verbose=args.verbose)
    print_report(results, output_file=args.output)


if __name__ == '__main__':
    main()
