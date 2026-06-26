#!/usr/bin/env python3
"""
OpenClaw Security Audit Tool
A comprehensive security scanner for OpenClaw configurations
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class OpenClawSecurityAuditor:
    """Security auditor for OpenClaw instances"""
    
    # Sensitive file patterns to detect
    SENSITIVE_PATTERNS = [
        r'\.env$',
        r'\.key$',
        r'\.pem$',
        r'\.p12$',
        r'\.pfx$',
        r'credentials',
        r'password',
        r'secret',
        r'token',
    ]
    
    # Known safe files (false positives)
    DEFAULT_WHITELIST = [
        'secret-input.ts',
        'secret-input.d.ts',
        'secret-input.js',
    ]
    
    # Regex patterns for credential detection
    CREDENTIAL_PATTERNS = {
        'api_key': r'["\']?(api[_-]?key|apikey)["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{20,}["\']?',
        'secret': r'["\']?(app[_-]?secret|client[_-]?secret)["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{20,}["\']?',
        'token': r'["\']?(auth[_-]?token|access[_-]?token|bearer)["\']?\s*[:=]\s*["\']?[a-zA-Z0-9_\-\.]{20,}["\']?',
        'password': r'["\']?password["\']?\s*[:=]\s*["\'][^"\']{8,}["\']',
        'private_key': r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
    }
    
    def __init__(self, openclaw_path: str = None, config_path: str = None):
        """Initialize auditor
        
        Args:
            openclaw_path: Path to OpenClaw directory (default: ~/.openclaw)
            config_path: Path to config file (default: skill directory/config.json)
        """
        self.openclaw_path = Path(openclaw_path or os.path.expanduser("~/.openclaw"))
        
        # Try to find config in multiple locations
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Check skill directory first, then current directory
            skill_config = Path(__file__).parent / "config.json"
            local_config = Path("config.json")
            if skill_config.exists():
                self.config_path = skill_config
            else:
                self.config_path = local_config
        
        self.config = self._load_config()
        self.findings: List[Dict[str, Any]] = []
        self.scanned_files = 0
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json"""
        default_config = {
            "exclude_dirs": ["node_modules", ".git", "__pycache__", "dist", "build", ".venv", "venv"],
            "whitelist": self.DEFAULT_WHITELIST,
            "sensitive_extensions": [".env", ".key", ".pem", ".p12", ".pfx", ".crt", ".cer"],
            "sensitive_keywords": ["password", "secret", "credentials", "private_key"]
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults
                    for key, value in default_config.items():
                        if key not in loaded:
                            loaded[key] = value
                    return loaded
            except Exception as e:
                print(f"[WARN] Failed to load config: {e}, using defaults")
        
        return default_config
        
    def scan_sensitive_files(self) -> None:
        """Scan for sensitive files in OpenClaw directory"""
        print("[SCAN] Scanning for sensitive files...")
        
        exclude_dirs = set(self.config.get('exclude_dirs', []))
        whitelist = set(self.config.get('whitelist', []))
        sensitive_exts = self.config.get('sensitive_extensions', [])
        sensitive_keywords = self.config.get('sensitive_keywords', [])
        
        # Build scan patterns
        patterns = [re.escape(ext) + '$' for ext in sensitive_exts]
        patterns.extend(sensitive_keywords)
        
        if not self.openclaw_path.exists():
            print(f"[WARN] OpenClaw path not found: {self.openclaw_path}")
            return
        
        for pattern in patterns:
            try:
                for file_path in self.openclaw_path.rglob("*"):
                    if not file_path.is_file():
                        continue
                    
                    if re.search(pattern, file_path.name, re.IGNORECASE):
                        # Skip excluded directories
                        if any(excluded in str(file_path) for excluded in exclude_dirs):
                            continue
                        # Skip whitelisted files
                        if file_path.name in whitelist:
                            continue
                        
                        risk_level = self._assess_file_risk(file_path)
                        self.findings.append({
                            'type': 'sensitive_file',
                            'severity': risk_level,
                            'path': str(file_path.relative_to(self.openclaw_path)),
                            'filename': file_path.name,
                            'size': file_path.stat().st_size,
                            'message': f'Found sensitive file: {file_path.name}'
                        })
            except PermissionError:
                continue  # Skip directories we can't access
                    
    def scan_credential_exposure(self) -> None:
        """Scan config files for exposed credentials"""
        print("[SCAN] Scanning for credential exposure...")
        
        config_files = [
            self.openclaw_path / "openclaw.json",
            self.openclaw_path / "gateway.json",
        ]
        
        for config_file in config_files:
            if not config_file.exists():
                continue
                
            try:
                content = config_file.read_text(encoding='utf-8')
                self.scanned_files += 1
                
                for cred_type, pattern in self.CREDENTIAL_PATTERNS.items():
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Mask the actual credential value
                        masked = self._mask_credential(match.group(0))
                        severity = 'CRITICAL' if cred_type == 'password' else 'HIGH'
                        
                        self.findings.append({
                            'type': 'credential_exposure',
                            'severity': severity,
                            'path': str(config_file.relative_to(self.openclaw_path)),
                            'credential_type': cred_type,
                            'pattern_found': masked,
                            'message': f'Config file contains exposed {cred_type}'
                        })
                        
            except Exception as e:
                self.findings.append({
                    'type': 'scan_error',
                    'severity': 'LOW',
                    'path': str(config_file.relative_to(self.openclaw_path)) if config_file.exists() else str(config_file),
                    'message': f'Scan failed: {str(e)}'
                })
                
    def check_gateway_configuration(self) -> None:
        """Check Gateway security configuration"""
        print("[SCAN] Checking Gateway configuration...")
        
        config_file = self.openclaw_path / "openclaw.json"
        if not config_file.exists():
            return
            
        try:
            config = json.loads(config_file.read_text(encoding='utf-8'))
            gateway_config = config.get('gateway', {})
            
            # Check bind mode
            bind_mode = gateway_config.get('bind', 'loopback')
            if bind_mode == '0.0.0.0':
                self.findings.append({
                    'type': 'gateway_misconfig',
                    'severity': 'CRITICAL',
                    'path': 'openclaw.json',
                    'message': 'Gateway bound to 0.0.0.0 - exposed to public network!'
                })
            elif bind_mode == 'loopback' or bind_mode == '127.0.0.1':
                self.findings.append({
                    'type': 'gateway_config',
                    'severity': 'INFO',
                    'path': 'openclaw.json',
                    'message': 'Gateway bound to loopback - secure configuration'
                })
            else:
                self.findings.append({
                    'type': 'gateway_config',
                    'severity': 'MEDIUM',
                    'path': 'openclaw.json',
                    'message': f'Gateway bound to {bind_mode} - verify if intentional'
                })
                
            # Check authentication mode
            auth_config = gateway_config.get('auth', {})
            auth_mode = auth_config.get('mode', 'none')
            
            if auth_mode == 'none':
                self.findings.append({
                    'type': 'gateway_misconfig',
                    'severity': 'HIGH',
                    'path': 'openclaw.json',
                    'message': 'Gateway authentication is disabled'
                })
            elif auth_mode == 'token':
                self.findings.append({
                    'type': 'gateway_config',
                    'severity': 'INFO',
                    'path': 'openclaw.json',
                    'message': 'Gateway uses token authentication'
                })
                
        except json.JSONDecodeError as e:
            self.findings.append({
                'type': 'config_parse_error',
                'severity': 'MEDIUM',
                'path': 'openclaw.json',
                'message': f'Failed to parse config: {str(e)}'
            })
        except Exception as e:
            self.findings.append({
                'type': 'config_parse_error',
                'severity': 'LOW',
                'path': 'openclaw.json',
                'message': f'Error checking gateway: {str(e)}'
            })
            
    def _assess_file_risk(self, file_path: Path) -> str:
        """Assess risk level of a sensitive file"""
        name = file_path.name.lower()
        
        if any(x in name for x in ['password', 'secret', 'key', 'credential']):
            return 'CRITICAL'
        elif any(x in name for x in ['token', 'auth']):
            return 'HIGH'
        elif any(x in name for x in ['.env', '.key', '.pem']):
            return 'MEDIUM'
        else:
            return 'LOW'
            
    def _mask_credential(self, text: str) -> str:
        """Mask credential value for safe display"""
        if len(text) <= 10:
            return text[:3] + '***'
        return text[:5] + '***' + text[-5:]
        
    def generate_report(self) -> Dict[str, Any]:
        """Generate security audit report"""
        severity_count = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
        for finding in self.findings:
            severity_count[finding.get('severity', 'INFO')] += 1
            
        report = {
            'scan_timestamp': datetime.now().isoformat(),
            'tool_version': '1.0.0',
            'summary': {
                'total_findings': len(self.findings),
                'severity_distribution': severity_count,
                'scanned_files': self.scanned_files
            },
            'findings': self.findings,
            'recommendations': self._generate_recommendations(severity_count)
        }
        
        return report
        
    def _generate_recommendations(self, severity_count: Dict[str, int]) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if severity_count['CRITICAL'] > 0:
            recommendations.append("CRITICAL issues found - immediate action required!")
            
        if severity_count['HIGH'] > 0:
            recommendations.append("HIGH severity issues found - fix within 24 hours")
            
        # General recommendations
        recommendations.extend([
            "Run this audit regularly (recommended: weekly)",
            "Store credentials in environment variables, not config files",
            "Use strong, unique tokens for Gateway authentication",
            "Keep OpenClaw updated to the latest version",
            "Review and rotate credentials periodically"
        ])
        
        return recommendations
        
    def run(self) -> Dict[str, Any]:
        """Run complete security audit"""
        print("=" * 60)
        print("OpenClaw Security Audit Tool v1.0.0")
        print("=" * 60)
        print(f"Scanning: {self.openclaw_path}")
        print()
        
        self.scan_sensitive_files()
        self.scan_credential_exposure()
        self.check_gateway_configuration()
        
        report = self.generate_report()
        
        # Save report
        output_dir = self.openclaw_path / "security-reports"
        output_dir.mkdir(exist_ok=True)
        
        report_filename = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = output_dir / report_filename
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[WARN] Could not save report: {e}")
        
        # Print summary
        print()
        print("=" * 60)
        print("Audit Complete")
        print("=" * 60)
        print(f"Total findings: {report['summary']['total_findings']}")
        print(f"  CRITICAL: {report['summary']['severity_distribution']['CRITICAL']}")
        print(f"  HIGH:     {report['summary']['severity_distribution']['HIGH']}")
        print(f"  MEDIUM:   {report['summary']['severity_distribution']['MEDIUM']}")
        print(f"  LOW:      {report['summary']['severity_distribution']['LOW']}")
        print(f"  INFO:     {report['summary']['severity_distribution']['INFO']}")
        if report_path.exists():
            print(f"Report saved: {report_path}")
        print("=" * 60)
        
        return report


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Security Audit Tool')
    parser.add_argument('--path', '-p', help='OpenClaw directory path (default: ~/.openclaw)')
    parser.add_argument('--config', '-c', help='Config file path')
    parser.add_argument('--json', '-j', action='store_true', help='Output report as JSON to stdout')
    
    args = parser.parse_args()
    
    auditor = OpenClawSecurityAuditor(
        openclaw_path=args.path,
        config_path=args.config
    )
    
    report = auditor.run()
    
    if args.json:
        print(json.dumps(report, indent=2))
    
    # Exit with error code if critical/high issues found
    critical = report['summary']['severity_distribution']['CRITICAL']
    high = report['summary']['severity_distribution']['HIGH']
    
    if critical > 0:
        exit(2)
    elif high > 0:
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    main()
