#!/usr/bin/env python3
"""
Security Suite for OpenClaw Skills

Complete security toolkit: scan, fix, and certify your skills.

Usage:
    python suite.py scan <skill-path> [options]
    python suite.py fix <skill-path> [options]
    python suite.py report <skill-path> [options]
    python suite.py certify <skill-path> [options]
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Import sibling modules
sys.path.insert(0, str(Path(__file__).parent.parent / "neckr0ik-security-scanner" / "scripts"))
sys.path.insert(0, str(Path(__file__).parent.parent / "neckr0ik-security-fixer" / "scripts"))

try:
    from audit import audit_skill, Severity, Vulnerability
    from fixer import Fixer
except ImportError:
    # If modules not available, use standalone
    pass


class Framework(Enum):
    SOC2 = "soc2"
    HIPAA = "hipaa"
    PCI = "pci"
    GDPR = "gdpr"
    CUSTOM = "custom"


@dataclass
class ComplianceResult:
    """Result of a compliance check."""
    
    framework: Framework
    compliant: bool
    controls: Dict[str, bool]
    findings: List[Dict]
    certificate_id: str
    timestamp: str


# Compliance frameworks control mappings
FRAMEWORKS = {
    Framework.SOC2: {
        "name": "SOC 2 Type II",
        "controls": {
            "CC6.1": "Access Controls",
            "CC6.7": "Encryption",
            "CC8.1": "Change Management",
            "CC9.2": "Risk Mitigation",
        },
        "mappings": {
            "SECRET": ["CC6.1", "CC6.7"],
            "SHELL": ["CC9.2"],
            "EXEC": ["CC9.2"],
            "PROMPT": ["CC6.1"],
            "PATH": ["CC6.1"],
            "NET": ["CC6.7"],
        }
    },
    Framework.HIPAA: {
        "name": "HIPAA",
        "controls": {
            "§164.312(a)": "Access Controls",
            "§164.312(b)": "Audit Controls",
            "§164.312(c)": "Integrity",
            "§164.312(d)": "Authentication",
            "§164.312(e)": "Transmission Security",
        },
        "mappings": {
            "SECRET": ["§164.312(a)", "§164.312(d)"],
            "SHELL": ["§164.312(c)"],
            "EXEC": ["§164.312(c)"],
            "PROMPT": ["§164.312(a)"],
            "PATH": ["§164.312(c)"],
            "NET": ["§164.312(e)"],
        }
    },
    Framework.PCI: {
        "name": "PCI-DSS",
        "controls": {
            "Req 3": "Protect Stored Cardholder Data",
            "Req 4": "Encrypt Transmission",
            "Req 7": "Restrict Access",
            "Req 8": "Identify Users",
            "Req 10": "Track Access",
        },
        "mappings": {
            "SECRET": ["Req 3", "Req 7", "Req 8"],
            "SHELL": ["Req 7"],
            "EXEC": ["Req 7"],
            "PROMPT": ["Req 7"],
            "PATH": ["Req 3", "Req 7"],
            "NET": ["Req 4"],
        }
    },
    Framework.GDPR: {
        "name": "GDPR",
        "controls": {
            "Art 5": "Data Minimization",
            "Art 32": "Security Measures",
            "Art 25": "Privacy by Design",
            "Art 30": "Records of Processing",
        },
        "mappings": {
            "SECRET": ["Art 32"],
            "SHELL": ["Art 32"],
            "EXEC": ["Art 32"],
            "PROMPT": ["Art 5", "Art 25"],
            "PATH": ["Art 32"],
            "NET": ["Art 32"],
        }
    },
}


def generate_certificate_id() -> str:
    """Generate a unique certificate ID."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    random_suffix = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:8].upper()
    return f"SOC2-{timestamp}-{random_suffix}"


def check_compliance(skill_path: str, framework: Framework, vulnerabilities: List[Vulnerability]) -> ComplianceResult:
    """Check compliance against a framework."""
    
    framework_info = FRAMEWORKS.get(framework, FRAMEWORKS[Framework.SOC2])
    controls = {ctrl: True for ctrl in framework_info["controls"]}
    findings = []
    
    for vuln in vulnerabilities:
        # Map vulnerability to controls
        for prefix, affected_controls in framework_info["mappings"].items():
            if vuln.id.startswith(prefix):
                for ctrl in affected_controls:
                    if ctrl in controls:
                        controls[ctrl] = False
                        
                        findings.append({
                            "control": ctrl,
                            "control_name": framework_info["controls"][ctrl],
                            "vulnerability": vuln.id,
                            "severity": vuln.severity.value,
                            "description": vuln.description,
                            "file": vuln.file,
                            "line": vuln.line,
                        })
    
    # Overall compliance
    compliant = all(controls.values())
    
    return ComplianceResult(
        framework=framework,
        compliant=compliant,
        controls=controls,
        findings=findings,
        certificate_id=generate_certificate_id() if compliant else "NOT-COMPLIANT",
        timestamp=datetime.now().isoformat(),
    )


def format_certificate(result: ComplianceResult, skill_name: str, version: str = "1.0.0") -> str:
    """Format compliance result as certificate."""
    
    framework_info = FRAMEWORKS.get(result.framework, FRAMEWORKS[Framework.SOC2])
    status = "✅ COMPLIANT" if result.compliant else "❌ NON-COMPLIANT"
    
    lines = [
        "╔" + "═" * 60 + "╗",
        f"║{framework_info['name']:^60}║",
        f"║{'SECURITY COMPLIANCE CERTIFICATE':^60}║",
        "╠" + "═" * 60 + "╣",
        f"║ Skill: {skill_name:<52}║",
        f"║ Version: {version:<50}║",
        f"║ Scan Date: {result.timestamp[:10]:<48}║",
        f"║ Framework: {framework_info['name']:<47}║",
        "╠" + "═" * 60 + "╣",
        f"║ STATUS: {status:<51}║",
        "╠" + "═" * 60 + "╣",
        "║ Controls Checked:" + " " * 42 + "║",
    ]
    
    for ctrl, passed in result.controls.items():
        status_icon = "✅" if passed else "❌"
        ctrl_name = framework_info["controls"][ctrl]
        lines.append(f"║   {status_icon} {ctrl} - {ctrl_name:<43}║")
    
    lines.extend([
        "╠" + "═" * 60 + "╣",
        f"║ Vulnerabilities Found: {len(result.findings):<35}║",
        f"║ Certificate ID: {result.certificate_id:<42}║",
        "╚" + "═" * 60 + "╝",
    ])
    
    return "\n".join(lines)


def format_report_json(result: ComplianceResult, skill_name: str, vulnerabilities: List[Vulnerability]) -> dict:
    """Format compliance result as JSON."""
    
    return {
        "skill": skill_name,
        "framework": result.framework.value,
        "compliant": result.compliant,
        "certificate_id": result.certificate_id,
        "timestamp": result.timestamp,
        "controls": result.controls,
        "findings": result.findings,
        "vulnerabilities": [
            {
                "id": v.id,
                "name": v.name,
                "severity": v.severity.value,
                "file": v.file,
                "line": v.line,
                "description": v.description,
            }
            for v in vulnerabilities
        ],
    }


def main():
    """CLI entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Security Suite for OpenClaw Skills")
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # scan command
    scan_parser = subparsers.add_parser('scan', help='Scan skill for vulnerabilities')
    scan_parser.add_argument('path', help='Path to skill directory')
    scan_parser.add_argument('--format', choices=['json', 'markdown', 'summary'], default='summary')
    scan_parser.add_argument('--severity', choices=['critical', 'high', 'medium', 'low', 'info'], default='info')
    
    # fix command
    fix_parser = subparsers.add_parser('fix', help='Fix vulnerabilities')
    fix_parser.add_argument('path', help='Path to skill directory')
    fix_parser.add_argument('--auto', action='store_true', help='Apply all fixes automatically')
    fix_parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    fix_parser.add_argument('--no-backup', action='store_true', help='Do not create backup files')
    
    # report command
    report_parser = subparsers.add_parser('report', help='Generate compliance report')
    report_parser.add_argument('path', help='Path to skill directory')
    report_parser.add_argument('--framework', choices=['soc2', 'hipaa', 'pci', 'gdpr'], default='soc2')
    report_parser.add_argument('--format', choices=['json', 'markdown', 'certificate'], default='certificate')
    report_parser.add_argument('--output', help='Output file path')
    
    # certify command
    certify_parser = subparsers.add_parser('certify', help='Certify skill for compliance')
    certify_parser.add_argument('path', help='Path to skill directory')
    certify_parser.add_argument('--framework', choices=['soc2', 'hipaa', 'pci', 'gdpr'], default='soc2')
    certify_parser.add_argument('--auto-fix', action='store_true', help='Apply fixes before certification')
    certify_parser.add_argument('--output', help='Certificate output path')
    
    args = parser.parse_args()
    
    if args.command == 'scan':
        result = audit_skill(args.path)
        
        # Filter by severity
        severity_order = ['critical', 'high', 'medium', 'low', 'info']
        min_severity = severity_order.index(args.severity)
        filtered = [v for v in result.vulnerabilities 
                    if severity_order.index(v.severity.value) <= min_severity]
        
        if args.format == 'json':
            output = {
                "skill": result.skill_name,
                "passed": result.passed,
                "summary": result.summary,
                "vulnerabilities": [
                    {
                        "id": v.id,
                        "name": v.name,
                        "severity": v.severity.value,
                        "file": v.file,
                        "line": v.line,
                        "description": v.description,
                        "remediation": v.remediation,
                    }
                    for v in filtered
                ]
            }
            print(json.dumps(output, indent=2))
        elif args.format == 'markdown':
            print(f"# Security Scan: {result.skill_name}")
            print(f"\n**Status:** {'✅ PASSED' if result.passed else '❌ FAILED'}")
            print(f"\n## Summary\n")
            print(f"| Severity | Count |")
            print(f"|----------|-------|")
            for sev, count in result.summary.items():
                print(f"| {sev.capitalize()} | {count} |")
            print(f"\n## Vulnerabilities\n")
            for v in filtered:
                print(f"### {v.name}")
                print(f"- **Severity:** {v.severity.value.upper()}")
                print(f"- **File:** `{v.file}:{v.line}`")
                print(f"- **Description:** {v.description}")
                print(f"- **Fix:** {v.remediation}\n")
        else:
            status = "✅ PASSED" if result.passed else "❌ FAILED"
            print(f"\n{'='*60}")
            print(f"Security Scan: {result.skill_name}")
            print(f"{'='*60}")
            print(f"Status: {status}")
            print(f"\nVulnerabilities by Severity:")
            for sev, count in result.summary.items():
                print(f"  {sev.capitalize()}: {count}")
            
            if filtered:
                print(f"\nIssues Found:\n")
                for v in sorted(filtered, key=lambda x: severity_order.index(x.severity.value)):
                    print(f"  [{v.severity.value.upper():8}] {v.file}:{v.line} - {v.name}")
                    print(f"             {v.description[:80]}...")
                    print()
        
        sys.exit(0 if result.passed else 1)
    
    elif args.command == 'fix':
        fixer = Fixer(args.path, dry_run=args.dry_run, backup=not args.no_backup)
        
        print(f"Scanning {args.path}...")
        fixer.scan_and_fix()
        
        print(f"\nFound {len(fixer.fixes)} issues")
        applied = fixer.apply_fixes(auto=args.auto)
        
        if fixer.env_vars:
            fixer.generate_env_example()
        
        print(f"\nApplied {len(applied)} fixes")
    
    elif args.command == 'report':
        # Scan
        scan_result = audit_skill(args.path)
        
        # Check compliance
        framework = Framework(args.framework)
        compliance_result = check_compliance(args.path, framework, scan_result.vulnerabilities)
        
        # Format output
        if args.format == 'json':
            output = format_report_json(compliance_result, scan_result.skill_name, scan_result.vulnerabilities)
            output_str = json.dumps(output, indent=2)
        elif args.format == 'markdown':
            lines = [
                f"# Compliance Report: {scan_result.skill_name}",
                f"\n**Framework:** {FRAMEWORKS[framework]['name']}",
                f"**Status:** {'✅ COMPLIANT' if compliance_result.compliant else '❌ NON-COMPLIANT'}",
                f"\n## Controls\n",
            ]
            for ctrl, passed in compliance_result.controls.items():
                status = "✅" if passed else "❌"
                lines.append(f"- {status} {ctrl}: {FRAMEWORKS[framework]['controls'][ctrl]}")
            
            if compliance_result.findings:
                lines.append(f"\n## Findings\n")
                for f in compliance_result.findings:
                    lines.append(f"- **{f['control']}**: {f['vulnerability']} ({f['severity']})")
            
            output_str = "\n".join(lines)
        else:
            output_str = format_certificate(compliance_result, scan_result.skill_name)
        
        # Output
        if args.output:
            Path(args.output).write_text(output_str)
            print(f"Report written to: {args.output}")
        else:
            print(output_str)
        
        sys.exit(0 if compliance_result.compliant else 1)
    
    elif args.command == 'certify':
        skill_path = Path(args.path)
        
        # Auto-fix if requested
        if args.auto_fix:
            print("Applying auto-fixes...")
            fixer = Fixer(args.path, backup=True)
            fixer.scan_and_fix()
            fixer.apply_fixes(auto=True)
            print()
        
        # Scan
        scan_result = audit_skill(args.path)
        
        # Check compliance
        framework = Framework(args.framework)
        compliance_result = check_compliance(args.path, framework, scan_result.vulnerabilities)
        
        # Generate certificate
        skill_md = skill_path / "SKILL.md"
        version = "1.0.0"
        if skill_md.exists():
            content = skill_md.read_text()
            import re
            version_match = re.search(r'version:\s*([\d.]+)', content)
            if version_match:
                version = version_match.group(1)
        
        certificate = format_certificate(compliance_result, skill_path.name, version)
        
        # Output
        if args.output:
            Path(args.output).write_text(certificate)
            print(f"Certificate written to: {args.output}")
        else:
            print(certificate)
        
        # Exit with appropriate code
        sys.exit(0 if compliance_result.compliant else 1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()