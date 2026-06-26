#!/usr/bin/env python3
"""
MCP Security Auditor - Enterprise-grade security scanning for OpenClaw MCP servers
Detects vulnerabilities, malware patterns, and compliance issues in MCP configurations
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class Severity(Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class SecurityFinding:
    id: str
    title: str
    description: str
    severity: Severity
    category: str
    location: str
    remediation: str
    cve_id: Optional[str] = None

class MCPSecurityAuditor:
    def __init__(self, mcp_path: str):
        self.mcp_path = Path(mcp_path)
        self.findings: List[SecurityFinding] = []
        
        # Security patterns to check
        self.malware_patterns = [
            r'eval\s*\(',
            r'exec\s*\(',
            r'__import__\s*\(',
            r'subprocess\.call\s*\([^)]*shell\s*=\s*True',
            r'os\.system\s*\(',
            r'pickle\.loads\s*\(',
            r'marshal\.loads\s*\(',
            r'shelve\.open\s*\(',
            r'yaml\.load\s*\([^)]*Loader\s*=\s*yaml\.Loader',
            r'jwt\.decode\s*\([^)]*verify\s*=\s*False',
        ]
        
        self.vulnerability_patterns = [
            (r'password\s*=\s*["\'][^"\']*["\']', "Hardcoded password detected"),
            (r'api_key\s*=\s*["\'][^"\']*["\']', "Hardcoded API key detected"),
            (r'secret\s*=\s*["\'][^"\']*["\']', "Hardcoded secret detected"),
            (r'token\s*=\s*["\'][^"\']*["\']', "Hardcoded token detected"),
            (r'bind\s*[:\s]*0\.0\.0\.0', "Binding to all interfaces (0.0.0.0)"),
            (r'bind\s*[:\s]*::', "Binding to all IPv6 interfaces"),
            (r'--disable-web-security', "Web security disabled flag"),
            (r'--allow-running-insecure-content', "Insecure content allowed"),
        ]
        
        self.compliance_patterns = [
            (r'logging\.basicConfig\s*\([^)]*level\s*=\s*logging\.DEBUG', "Debug logging may leak sensitive info"),
            (r'print\s*\([^)]*password', "Password may be logged to console"),
            (r'print\s*\([^)]*token', "Token may be logged to console"),
            (r'print\s*\([^)]*key', "Key may be logged to console"),
        ]

    def audit_file(self, file_path: Path) -> List[SecurityFinding]:
        """Audit a single file for security issues"""
        findings = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Check for malware patterns
            for pattern in self.malware_patterns:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append(SecurityFinding(
                            id=f"MAL-{len(findings)+1:03d}",
                            title="Potential Malware Pattern Detected",
                            description=f"Suspicious code pattern found: {pattern}",
                            severity=Severity.HIGH,
                            category="Malware",
                            location=f"{file_path.name}:{i}",
                            remediation="Review this code carefully - it may contain malicious functionality",
                            cve_id=None
                        ))
            
            # Check for vulnerabilities
            for pattern, description in self.vulnerability_patterns:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        severity = Severity.HIGH if any(x in pattern.lower() for x in ['password', 'api_key', 'secret', 'token']) else Severity.MEDIUM
                        findings.append(SecurityFinding(
                            id=f"VULN-{len(findings)+1:03d}",
                            title="Security Vulnerability Detected",
                            description=description,
                            severity=severity,
                            category="Vulnerability",
                            location=f"{file_path.name}:{i}",
                            remediation="Remove hardcoded credentials or use secure vault/environment variables",
                            cve_id=None
                        ))
            
            # Check for compliance issues
            for pattern, description in self.compliance_patterns:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append(SecurityFinding(
                            id=f"COMP-{len(findings)+1:03d}",
                            title="Compliance Issue Detected",
                            description=description,
                            severity=Severity.LOW,
                            category="Compliance",
                            location=f"{file_path.name}:{i}",
                            remediation="Review logging and output to prevent sensitive data exposure",
                            cve_id=None
                        ))
                        
        except Exception as e:
            findings.append(SecurityFinding(
                id=f"ERR-{len(findings)+1:03d}",
                title="File Read Error",
                description=f"Could not read file: {str(e)}",
                severity=Severity.MEDIUM,
                category="Error",
                location=str(file_path),
                remediation="Check file permissions and encoding",
                cve_id=None
            ))
        
        return findings

    def audit_directory(self) -> Dict[str, Any]:
        """Audit entire MCP directory"""
        if not self.mcp_path.exists():
            return {
                "error": f"MCP path does not exist: {self.mcp_path}",
                "findings": [],
                "score": 0,
                "grade": "F"
            }
        
        # Scan all relevant files
        extensions = ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.txt', '.md', '.env', '.config', '.conf']
        files_to_scan = []
        
        for ext in extensions:
            files_to_scan.extend(self.mcp_path.rglob(f"*{ext}"))
        
        # Also check for common config files
        common_files = ['.env', '.env.local', '.env.production', 'docker-compose.yml', 'Dockerfile']
        for cf in common_files:
            files_to_scan.extend(self.mcp_path.rglob(cf))
        
        # Remove duplicates and audit
        unique_files = list(set(files_to_scan))
        all_findings = []
        
        for file_path in unique_files:
            if file_path.is_file():
                findings = self.audit_file(file_path)
                all_findings.extend(findings)
        
        self.findings = all_findings
        return self.generate_report()

    def generate_report(self) -> Dict[str, Any]:
        """Generate security audit report"""
        if not self.findings:
            return {
                "score": 100,
                "grade": "A+",
                "findings": [],
                "summary": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                    "info": 0
                },
                "recommendations": ["No security issues found - excellent work!"]
            }
        
        # Count by severity
        severity_counts = {
            "critical": len([f for f in self.findings if f.severity == Severity.CRITICAL]),
            "high": len([f for f in self.findings if f.severity == Severity.HIGH]),
            "medium": len([f for f in self.findings if f.severity == Severity.MEDIUM]),
            "low": len([f for f in self.findings if f.severity == Severity.LOW]),
            "info": len([f for f in self.findings if f.severity == Severity.INFO])
        }
        
        # Calculate score (0-100)
        penalty = (
            severity_counts["critical"] * 25 +
            severity_counts["high"] * 15 +
            severity_counts["medium"] * 8 +
            severity_counts["low"] * 3 +
            severity_counts["info"] * 1
        )
        score = max(0, 100 - penalty)
        
        # Determine grade
        if score >= 95:
            grade = "A+"
        elif score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        
        # Generate recommendations
        recommendations = []
        if severity_counts["critical"] > 0:
            recommendations.append("[CRITICAL] Address critical security findings immediately")
        if severity_counts["high"] > 0:
            recommendations.append("[HIGH] Fix high severity vulnerabilities soon")
        if any(f.category == "Malware" for f in self.findings):
            recommendations.append("[MALWARE] Potential malicious code detected - investigate immediately")
        if any("password" in f.description.lower() or "api_key" in f.description.lower() for f in self.findings):
            recommendations.append("[CREDENTIALS] Remove hardcoded credentials, use environment variables or vault")
        if any("0.0.0.0" in f.description or "::" in f.description for f in self.findings):
            recommendations.append("[NETWORK] Restrict binding to specific interfaces only")
        if not recommendations:
            recommendations.append("[OK] Review low/medium severity findings for improvement")
        
        # Convert findings to JSON-serializable format
        findings_serializable = []
        for f in self.findings:
            f_dict = asdict(f)
            # Convert enum to string
            f_dict['severity'] = f.severity.value
            findings_serializable.append(f_dict)
        
        return {
            "score": score,
            "grade": grade,
            "findings": findings_serializable,
            "summary": severity_counts,
            "recommendations": recommendations,
            "metadata": {
                "auditor": "MCP Security Auditor v1.0.0",
                "timestamp": str(Path().cwd()),
                "files_scanned": len(list(self.mcp_path.rglob("*"))) if self.mcp_path.exists() else 0
            }
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python audit.py <mcp_directory_path>")
        print("Example: python audit.py ./mcp_server")
        sys.exit(1)
    
    mcp_path = sys.argv[1]
    auditor = MCPSecurityAuditor(mcp_path)
    report = auditor.audit_directory()
    
    # Print formatted report
    print("=" * 60)
    print("MCP SECURITY AUDIT REPORT")
    print("=" * 60)
    print(f"Path: {mcp_path}")
    print(f"Score: {report['score']}/100")
    print(f"Grade: {report['grade']}")
    print("-" * 60)
    print("Summary:")
    print(f"  Critical: {report['summary']['critical']}")
    print(f"  High: {report['summary']['high']}")
    print(f"  Medium: {report['summary']['medium']}")
    print(f"  Low: {report['summary']['low']}")
    print(f"  Info: {report['summary']['info']}")
    print("-" * 60)
    print("Recommendations:")
    for rec in report['recommendations']:
        print(f"  {rec}")
    print("-" * 60)
    
    if report['findings']:
        print("Detailed Findings:")
        for finding in report['findings'][:10]:  # Show first 10
            severity = finding['severity']
            if hasattr(severity, 'value'):
                severity_str = severity.value.upper()
            else:
                severity_str = str(severity).upper()
            print(f"  [{severity_str}] {finding['title']}")
            print(f"    {finding['description']}")
            print(f"    Location: {finding['location']}")
            print(f"    Fix: {finding['remediation']}")
            print()
        
        if len(report['findings']) > 10:
            print(f"  ... and {len(report['findings']) - 10} more findings")
    else:
        print("✅ No security issues found!")
    
    print("=" * 60)
    
    # Return appropriate exit code
    if report['score'] < 70:
        sys.exit(1)  # Fail if score too low
    elif report['score'] < 90:
        sys.exit(0)  # Warn but don't fail
    else:
        sys.exit(0)  # Success

if __name__ == "__main__":
    main()