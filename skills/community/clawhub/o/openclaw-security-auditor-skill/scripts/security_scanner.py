#!/usr/bin/env python3
"""
OpenClaw Security Auditor - Core Security Scanner
This script provides the main security scanning functionality for OpenClaw configurations.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add the OSA tool directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "openclaw-security-auditor"))

from osa.scanner_fixed import SecurityScanner
from osa.reporter import ReportGenerator

def scan_openclaw_config(config_path: str = None, mode: str = "balanced") -> Dict[str, Any]:
    """
    Scan OpenClaw configuration for security issues
    
    Args:
        config_path (str): Path to OpenClaw config file. If None, uses default location
        mode (str): Security mode - "conservative", "balanced", or "aggressive"
    
    Returns:
        Dict containing scan results with security score and issues
    """
    # Determine config path
    if config_path is None:
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        if not config_path.exists():
            config_path = Path.home() / ".openclaw" / "config.json"
    
    config_path = Path(config_path)
    
    if not config_path.exists():
        return {
            "error": f"Configuration file not found: {config_path}",
            "score": 0,
            "issues": [],
            "passed_checks": 0,
            "total_checks": 0
        }
    
    try:
        # Create scanner and run scan
        scanner = SecurityScanner(config_path, mode=mode, verbose=False)
        results = scanner.scan()
        
        # Convert results to dictionary
        issues_list = []
        for issue in results.issues:
            issues_list.append({
                "check_name": issue.check_name,
                "severity": issue.severity.value,
                "title": issue.title,
                "title_zh": getattr(issue, 'title_zh', ''),
                "description": issue.description,
                "description_zh": getattr(issue, 'description_zh', ''),
                "current_value": issue.current_value,
                "recommended_value": issue.recommended_value,
                "fix_command": issue.fix_command,
                "risk": issue.risk,
                "risk_zh": getattr(issue, 'risk_zh', '')
            })
        
        return {
            "config_path": str(results.config_path),
            "mode": results.mode,
            "score": results.score,
            "security_level": _get_security_level(results.score),
            "issues": issues_list,
            "passed_checks": results.passed_checks,
            "total_checks": results.total_checks,
            "has_critical_issues": results.has_critical_issues,
            "has_high_issues": results.has_high_issues
        }
        
    except Exception as e:
        return {
            "error": f"Scan failed: {str(e)}",
            "score": 0,
            "issues": [],
            "passed_checks": 0,
            "total_checks": 0
        }

def _get_security_level(score: int) -> str:
    """Get security level based on score"""
    if score >= 90:
        return "excellent"
    elif score >= 75:
        return "good"
    elif score >= 60:
        return "fair"
    elif score >= 40:
        return "at_risk"
    else:
        return "critical"

def main():
    """Command line interface for security scanner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw Security Auditor")
    parser.add_argument("--config", "-c", help="Path to OpenClaw config file")
    parser.add_argument("--mode", "-m", default="balanced", 
                       choices=["conservative", "balanced", "aggressive"],
                       help="Security mode")
    parser.add_argument("--format", "-f", default="json", 
                       choices=["json", "markdown", "bilingual"],
                       help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    # Run scan
    results = scan_openclaw_config(args.config, args.mode)
    
    if "error" in results:
        print(f"Error: {results['error']}", file=sys.stderr)
        sys.exit(1)
    
    # Generate report
    if args.format == "json":
        import json
        output = json.dumps(results, indent=2, ensure_ascii=False)
    else:
        # Create reporter instance
        from osa.models import ScanResults, SecurityIssue, Severity
        from osa.i18n import get_risk_level_translation
        
        # Reconstruct ScanResults object
        scan_results = ScanResults(
            config_path=Path(results["config_path"]),
            mode=results["mode"],
            passed_checks=results["passed_checks"],
            total_checks=results["total_checks"]
        )
        
        # Reconstruct issues
        for issue_data in results["issues"]:
            issue = SecurityIssue(
                check_name=issue_data["check_name"],
                severity=Severity(issue_data["severity"]),
                title=issue_data["title"],
                description=issue_data["description"],
                current_value=issue_data["current_value"],
                recommended_value=issue_data["recommended_value"],
                fix_command=issue_data["fix_command"],
                risk=issue_data["risk"]
            )
            if issue_data.get("title_zh"):
                issue.title_zh = issue_data["title_zh"]
            if issue_data.get("description_zh"):
                issue.description_zh = issue_data["description_zh"]
            if issue_data.get("risk_zh"):
                issue.risk_zh = issue_data["risk_zh"]
            
            scan_results.issues.append(issue)
        
        reporter = ReportGenerator(scan_results, mode=args.mode)
        if args.format == "bilingual":
            output = reporter.generate("bilingual")
        else:
            output = reporter.generate("markdown")
    
    # Output results
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"Report saved to: {args.output}")
    else:
        print(output)

if __name__ == "__main__":
    main()