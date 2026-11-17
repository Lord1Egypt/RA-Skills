#!/usr/bin/env python3
"""
Vibe Codebase Audit Tools - Multi-Agent Security Audit Implementation
Supports OpenCode, Hermes, OpenClaw, and other MCP-compatible agents.
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

class ProjectAuditor:
    """Automated security scanner for codebases."""
    
    def __init__(self, project_path: str, severity_threshold: int = 3):
        self.project_path = Path(project_path)
        self.severity_threshold = severity_threshold
        self.findings = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
            "info": []
        }
        self.scanned_files = []
        self.custom_patterns = {}
        
    def scan(self) -> Dict[str, Any]:
        """Run complete security audit."""
        if not self.project_path.exists():
            return {"error": f"Project path '{self.project_path}' does not exist"}
        
        files = self._get_files_to_scan()
        
        for file_path in files:
            self._scan_file(file_path)
        
        return self._generate_report()
    
    def _get_files_to_scan(self) -> List[Path]:
        """Get all files that should be scanned."""
        files = []
        ignore_patterns = {'.git', '__pycache__', 'node_modules', '.DS_Store', 
                          '*.pyc', 'venv', '.venv', 'dist', 'build', '.env'}
        
        for root, dirs, filenames in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in ignore_patterns]
            
            for filename in filenames:
                if not any(filename.endswith(pattern.replace('*', '')) 
                          for pattern in ignore_patterns if '*' in pattern):
                    files.append(Path(root) / filename)
        
        return files
    
    def _scan_file(self, file_path: Path):
        """Scan a single file for issues."""
        try:
            if self._is_binary(file_path):
                return
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                self.scanned_files.append(str(file_path.relative_to(self.project_path)))
                
                self._check_secrets(file_path, content)
                self._check_personal_data(file_path, content)
                self._check_file_paths(file_path, content)
                self._check_security_patterns(file_path, content)
                self._check_code_quality(file_path, content)
                self._check_custom_patterns(file_path, content)
                
        except Exception as e:
            self.findings["info"].append({
                "file": str(file_path.relative_to(self.project_path)),
                "issue": f"Could not scan file: {str(e)}",
                "severity_score": 1
            })
    
    def _is_binary(self, file_path: Path) -> bool:
        """Check if file is binary."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\0' in chunk
        except:
            return True
    
    def _check_secrets(self, file_path: Path, content: str):
        """Check for hardcoded secrets and API keys."""
        patterns = {
            "API Key": r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']([^"\']{20,})["\']',
            "Secret Key": r'(?i)(secret[_-]?key|secretkey)\s*[:=]\s*["\']([^"\']{20,})["\']',
            "AWS Key": r'AKIA[0-9A-Z]{16}',
            "GitHub Token": r'ghp_[a-zA-Z0-9]{36}',
            "Slack Token": r'xox[baprs]-[0-9a-zA-Z]{10,48}',
            "Private Key": r'-----BEGIN (RSA |DSA |EC )?PRIVATE KEY-----',
            "Bearer Token": r'(?i)bearer\s+[a-zA-Z0-9\-._~+/]{20,}',
            "Password": r'(?i)password\s*[:=]\s*["\']([^"\']{3,})["\']',
            "Anthropic API Key": r'sk-ant-api03-[a-zA-Z0-9\-_]{95}',
            "OpenAI API Key": r'sk-[a-zA-Z0-9]{20,}',
            "OpenRouter Key": r'sk-or-v1-[a-zA-Z0-9]{64}',
            "Generic Secret": r'(?i)(secret|token|key|password|auth)\s*[:=]\s*["\']([a-zA-Z0-9+/=]{32,})["\']',
        }
        
        for secret_type, pattern in patterns.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                line_start = content.rfind('\n', 0, match.start()) + 1
                line = content[line_start:content.find('\n', match.start())]
                
                severity = "critical"
                severity_score = 5
                issue = f"Potential {secret_type} found"
                
                if any(word in line.lower() for word in 
                       ['example', 'placeholder', 'your_', 'xxx', 'TODO', 'REPLACE', 'INSERT']):
                    severity = "low"
                    severity_score = 2
                    issue += " (appears to be placeholder)"
                
                self.findings[severity].append({
                    "file": str(file_path.relative_to(self.project_path)),
                    "issue": issue,
                    "line": line.strip(),
                    "match": match.group(0)[:50] + "..." if len(match.group(0)) > 50 else match.group(0),
                    "severity_score": severity_score
                })
    
    def _check_personal_data(self, file_path: Path, content: str):
        """Check for personal information."""
        patterns = {
            "Email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "Phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
            "Credit Card": r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
        }
        
        for data_type, pattern in patterns.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                if data_type == "Email" and any(domain in match.group(0).lower() for domain in
                    ['example.com', 'test.com', 'localhost', 'anthropic.com', 
                     'noreply@', 'users.noreply.github.com']):
                    continue
                
                line_start = content.rfind('\n', 0, match.start()) + 1
                line = content[line_start:content.find('\n', match.start())]
                
                self.findings["high"].append({
                    "file": str(file_path.relative_to(self.project_path)),
                    "issue": f"Potential {data_type} found",
                    "line": line.strip(),
                    "severity_score": 4
                })
    
    def _check_file_paths(self, file_path: Path, content: str):
        """Check for exposed file system paths."""
        patterns = [
            (r'/Users/[^/\s,\'"]+', "macOS user path"),
            (r'/home/[^/\s,\'"]+', "Linux user path"),
            (r'C:\\Users\\[^\\s,\'"]+', "Windows user path"),
            (r'(?i)obsidian[/\\][^/\\\s,\'"]+', "Obsidian vault path"),
            (r'/Documents/[^/\s,\'"]+/[^/\s,\'"]+', "Personal documents path"),
        ]
        
        for pattern, description in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                line_start = content.rfind('\n', 0, match.start()) + 1
                line = content[line_start:content.find('\n', match.start())]
                
                self.findings["medium"].append({
                    "file": str(file_path.relative_to(self.project_path)),
                    "issue": f"Exposed {description}",
                    "line": line.strip(),
                    "path": match.group(0),
                    "severity_score": 3
                })
    
    def _check_security_patterns(self, file_path: Path, content: str):
        """Check for common security vulnerabilities."""
        if not any(str(file_path).endswith(ext) for ext in 
                   ['.js', '.py', '.ts', '.jsx', '.tsx', '.go', '.rs', '.php', '.java']):
            return
        
        security_patterns = {
            "Command Injection": r'(exec|system|shell_exec|passthru|eval)\s*\(',
            "SQL Injection": r'(execute|query|exec)\s*\([^)]*[\+\$]',
            "Path Traversal": r'\.\.[/\\]',
            "Unsafe Deserialization": r'(pickle\.loads|yaml\.load|unserialize)\s*\(',
            "Weak Crypto": r'(md5|sha1)\s*\(',
            "Debug Mode": r'(?i)(debug\s*[:=]\s*true|debug:\s*true)',
        }
        
        for vuln_type, pattern in security_patterns.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_start = content.rfind('\n', 0, match.start()) + 1
                line = content[line_start:content.find('\n', match.start())]
                
                self.findings["high"].append({
                    "file": str(file_path.relative_to(self.project_path)),
                    "issue": f"Potential {vuln_type} vulnerability",
                    "line": line.strip(),
                    "severity_score": 4
                })
    
    def _check_code_quality(self, file_path: Path, content: str):
        """Check for code quality issues."""
        patterns = {
            "TODO": r'(?i)TODO:?\s*(.+)',
            "FIXME": r'(?i)FIXME:?\s*(.+)',
            "HACK": r'(?i)HACK:?\s*(.+)',
        }
        
        for marker_type, pattern in patterns.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                comment = match.group(1) if len(match.groups()) > 0 else ""
                if any(word in comment.lower() for word in 
                       ['security', 'auth', 'secure', 'validate', 'sanitize']):
                    self.findings["medium"].append({
                        "file": str(file_path.relative_to(self.project_path)),
                        "issue": f"{marker_type} comment related to security",
                        "comment": comment.strip(),
                        "severity_score": 3
                    })
    
    def _check_custom_patterns(self, file_path: Path, content: str):
        """Check custom security patterns."""
        for pattern_name, pattern in self.custom_patterns.items():
            try:
                matches = re.finditer(pattern, content)
                for match in matches:
                    line_start = content.rfind('\n', 0, match.start()) + 1
                    line = content[line_start:content.find('\n', match.start())]
                    
                    self.findings["high"].append({
                        "file": str(file_path.relative_to(self.project_path)),
                        "issue": f"Custom pattern '{pattern_name}' matched",
                        "line": line.strip(),
                        "severity_score": 4
                    })
            except Exception as e:
                self.findings["info"].append({
                    "file": str(file_path.relative_to(self.project_path)),
                    "issue": f"Invalid custom pattern '{pattern_name}': {str(e)}",
                    "severity_score": 1
                })
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate the final audit report."""
        total_findings = sum(len(v) for v in self.findings.values() if isinstance(v, list))
        
        risk_score = min(100, (
            len(self.findings["critical"]) * 20 +
            len(self.findings["high"]) * 10 +
            len(self.findings["medium"]) * 5 +
            len(self.findings["low"]) * 2
        ))
        
        if risk_score >= 80:
            risk_level = "CRITICAL"
        elif risk_score >= 50:
            risk_level = "HIGH"
        elif risk_score >= 20:
            risk_level = "MEDIUM"
        elif risk_score > 0:
            risk_level = "LOW"
        else:
            risk_level = "SAFE"
        
        return {
            "project": str(self.project_path),
            "timestamp": datetime.now().isoformat(),
            "files_scanned": len(self.scanned_files),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "total_findings": total_findings,
            "findings_by_severity": {
                "critical": len(self.findings["critical"]),
                "high": len(self.findings["high"]),
                "medium": len(self.findings["medium"]),
                "low": len(self.findings["low"]),
                "info": len(self.findings["info"])
            },
            "findings": self.findings,
            "scanned_files": self.scanned_files,
            "recommendations": self._generate_recommendations(risk_level)
        }
    
    def _generate_recommendations(self, risk_level: str) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        if self.findings["critical"]:
            recommendations.append("🚨 CRITICAL: Remove all API keys and secrets before publishing")
        
        if self.findings["high"]:
            recommendations.append("⚠️ HIGH: Review and fix security vulnerabilities")
        
        if any("Obsidian" in f.get("issue", "") for f in self.findings["medium"]):
            recommendations.append("📁 Remove references to Obsidian vaults or personal directories")
        
        if risk_level in ["CRITICAL", "HIGH"]:
            recommendations.append("🔒 Do NOT publish until issues are resolved")
        elif risk_level == "MEDIUM":
            recommendations.append("🔍 Review findings and consider fixes before publishing")
        else:
            recommendations.append("✅ Safe to publish - minor issues detected")
        
        return recommendations


class MultiModelAuditor:
    """Multi-model AI consensus auditor."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('OPENROUTER_API_KEY')
        self.models = {
            "claude": "anthropic/claude-3.5-sonnet",
            "gpt4": "openai/gpt-4-turbo",
            "gemini": "google/gemini-pro-1.5"
        }
    
    def read_project_files(self, project_path: str, max_file_size: int = 1_000_000) -> dict:
        """Read all text files from the project."""
        project = Path(project_path)
        files_content = {}
        
        if not project.exists():
            return {"error": f"Project path '{project_path}' does not exist"}
        
        for file_path in project.rglob('*'):
            if file_path.is_file() and not any(part.startswith('.git') for part in file_path.parts):
                if file_path.stat().st_size > max_file_size:
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if '\0' not in content:
                            rel_path = str(file_path.relative_to(project))
                            files_content[rel_path] = content
                except:
                    continue
        
        return files_content
    
    def create_audit_prompt(self, files_content: dict) -> str:
        """Create the audit prompt for AI models."""
        files_list = "\n".join([f"- {path}" for path in files_content.keys()])
        
        full_content = ""
        for path, content in files_content.items():
            full_content += f"\n{'='*80}\n"
            full_content += f"FILE: {path}\n"
            full_content += f"{'='*80}\n"
            full_content += content
            full_content += "\n"
        
        prompt = f"""You are conducting a security audit of a software project that will be published publicly on GitHub.

**CRITICAL CONCERNS:**
1. **Private Data Leakage**: Check for any personal information, API keys, tokens, passwords, or file paths that reveal user information
2. **Security Vulnerabilities**: Look for common vulnerabilities like code injection, XSS, SQL injection, insecure patterns
3. **Data Exposure**: Ensure no references to private notebooks (Obsidian), personal directories, or sensitive user data
4. **Code Execution Risks**: Check if any code could be exploited to access unauthorized data or systems

**PROJECT FILES:**
{files_list}

**FULL PROJECT CONTENT:**
{full_content}

**AUDIT REQUIREMENTS:**
Please provide a comprehensive security audit with:

1. **RISK ASSESSMENT** (0-100 score where 0 is safe, 100 is critical):
   - Overall risk score
   - Risk level (SAFE/LOW/MEDIUM/HIGH/CRITICAL)

2. **SECURITY FINDINGS**:
   - List each security issue found with severity (CRITICAL/HIGH/MEDIUM/LOW)
   - Explain the risk in plain English
   - Specify the file and location

3. **PRIVATE DATA CHECK**:
   - Explicitly confirm if any private data was found (YES/NO)
   - List any personal information, API keys, file paths, or user-specific data

4. **PUBLISH RECOMMENDATION**:
   - Is it SAFE to publish this project publicly? (YES/NO/WITH_FIXES)
   - What fixes are needed before publishing?

5. **PLAIN ENGLISH SUMMARY**:
   - Explain the findings in simple terms anyone can understand
   - What are the risks of publishing this code as-is?

Format your response as JSON:
{{
  "risk_score": <0-100>,
  "risk_level": "<SAFE|LOW|MEDIUM|HIGH|CRITICAL>",
  "findings": [
    {{
      "severity": "<CRITICAL|HIGH|MEDIUM|LOW>",
      "issue": "description",
      "file": "filename",
      "explanation": "plain English explanation"
    }}
  ],
  "private_data_found": "<YES|NO>",
  "private_data_details": ["list of any private data found"],
  "publish_safe": "<YES|NO|WITH_FIXES>",
  "required_fixes": ["list of fixes needed"],
  "plain_english_summary": "simple explanation of audit results"
}}
"""
        
        return prompt
    
    def audit_with_openrouter(self, prompt: str, model: str) -> dict:
        """Run audit using OpenRouter API."""
        if not self.api_key:
            return {"error": "OPENROUTER_API_KEY not set. Set environment variable or pass api_key parameter."}
        
        try:
            import requests
        except ImportError:
            return {"error": "requests library not installed. Run: pip install requests"}
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()
                
                return json.loads(content)
            else:
                return {"error": f"API error: {response.status_code} - {response.text}"}
        
        except Exception as e:
            return {"error": str(e)}
    
    def run_multi_model_audit(self, project_path: str, 
                              models: Optional[List[str]] = None,
                              consensus_mode: str = "conservative") -> dict:
        """Run audit with multiple AI models."""
        files_content = self.read_project_files(project_path)
        
        if "error" in files_content:
            return files_content
        
        if not files_content:
            return {"error": "No files found to audit"}
        
        prompt = self.create_audit_prompt(files_content)
        
        results = {}
        
        selected_models = {k: v for k, v in self.models.items() 
                          if models is None or k in models}
        
        for name, model in selected_models.items():
            result = self.audit_with_openrouter(prompt, model)
            results[name] = result
        
        return self._generate_consensus_report(results, consensus_mode)
    
    def _generate_consensus_report(self, results: dict, consensus_mode: str) -> dict:
        """Generate a consensus report from all model results."""
        valid_results = {k: v for k, v in results.items() if "error" not in v}
        
        if not valid_results:
            return {"error": "No valid audit results", "model_errors": results}
        
        risk_scores = [r.get('risk_score', 0) for r in valid_results.values()]
        
        if consensus_mode == "conservative":
            consensus_risk_score = max(risk_scores)
        else:
            consensus_risk_score = sum(risk_scores) / len(risk_scores)
        
        private_data_found = any(r.get('private_data_found') == 'YES' 
                                 for r in valid_results.values())
        
        publish_recommendations = [r.get('publish_safe') for r in valid_results.values()]
        consensus_publish = "YES" if all(rec == "YES" for rec in publish_recommendations) \
                           else "NO" if any(rec == "NO" for rec in publish_recommendations) \
                           else "WITH_FIXES"
        
        all_findings = []
        for model_name, result in valid_results.items():
            for finding in result.get('findings', []):
                finding['detected_by'] = model_name
                all_findings.append(finding)
        
        if consensus_risk_score >= 80:
            consensus_risk_level = "CRITICAL"
        elif consensus_risk_score >= 50:
            consensus_risk_level = "HIGH"
        elif consensus_risk_score >= 20:
            consensus_risk_level = "MEDIUM"
        elif consensus_risk_score > 0:
            consensus_risk_level = "LOW"
        else:
            consensus_risk_level = "SAFE"
        
        return {
            "timestamp": datetime.now().isoformat(),
            "consensus_risk_score": consensus_risk_score,
            "consensus_risk_level": consensus_risk_level,
            "private_data_found": private_data_found,
            "consensus_publish_recommendation": consensus_publish,
            "all_findings": all_findings,
            "model_results": valid_results,
            "models_audited": list(valid_results.keys()),
            "model_errors": {k: v for k, v in results.items() if "error" in v}
        }


def format_report(report: Dict[str, Any], output_format: str = "console") -> str:
    """Format report for different outputs."""
    if output_format == "json":
        return json.dumps(report, indent=2)
    
    elif output_format == "markdown":
        md = f"# 🔒 Vibe Codebase Audit Report\n\n"
        md += f"**Timestamp:** {report.get('timestamp', 'N/A')}\n\n"
        md += f"## Risk Assessment\n\n"
        md += f"- **Risk Level:** {report.get('risk_level', report.get('consensus_risk_level', 'N/A'))}\n"
        md += f"- **Risk Score:** {report.get('risk_score', report.get('consensus_risk_score', 'N/A'))}/100\n"
        
        if 'findings_by_severity' in report:
            md += f"\n## Findings by Severity\n\n"
            for severity, count in report['findings_by_severity'].items():
                md += f"- {severity.upper()}: {count}\n"
        
        if report.get('recommendations'):
            md += f"\n## Recommendations\n\n"
            for rec in report['recommendations']:
                md += f"- {rec}\n"
        
        return md
    
    else:
        lines = []
        lines.append("="*80)
        lines.append("🔒 VIBE CODEBASE AUDIT REPORT")
        lines.append("="*80)
        lines.append("")
        
        risk_emoji = {
            "CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", 
            "LOW": "🟢", "SAFE": "✅"
        }
        
        risk_level = report.get('risk_level', report.get('consensus_risk_level', 'UNKNOWN'))
        risk_score = report.get('risk_score', report.get('consensus_risk_score', 0))
        
        lines.append(f"Risk Level: {risk_emoji.get(risk_level, '❓')} {risk_level}")
        lines.append(f"Risk Score: {risk_score}/100")
        lines.append("")
        
        if 'findings_by_severity' in report:
            lines.append("📊 Findings by Severity:")
            for severity, count in report['findings_by_severity'].items():
                emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", 
                        "low": "🟢", "info": "ℹ️"}.get(severity, "❓")
                lines.append(f"  {emoji} {severity.upper()}: {count}")
            lines.append("")
        
        if report.get('recommendations'):
            lines.append("💡 Recommendations:")
            for rec in report['recommendations']:
                lines.append(f"  {rec}")
        
        lines.append("")
        lines.append("="*80)
        lines.append("✨ AUDIT COMPLETE")
        lines.append("="*80)
        
        return "\n".join(lines)


def vibe_audit_scan(project_path: str, 
                   output_format: str = "json",
                   severity_threshold: int = 3,
                   custom_patterns: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Tool 1: Automated Pattern Scanner
    
    Fast local security scan using pattern matching and static analysis.
    
    Args:
        project_path: Path to the project directory to audit
        output_format: Report format - "json", "markdown", or "console"
        severity_threshold: Minimum severity to report (1-5, default: 3)
        custom_patterns: Optional custom security patterns to check
    
    Returns:
        Audit report with risk score, findings, and recommendations
    """
    auditor = ProjectAuditor(project_path, severity_threshold)
    
    if custom_patterns:
        auditor.custom_patterns = custom_patterns
    
    report = auditor.scan()
    
    if output_format != "json":
        report["formatted_report"] = format_report(report, output_format)
    
    return report


def vibe_audit_multi_model(project_path: str,
                          models: Optional[List[str]] = None,
                          openrouter_api_key: Optional[str] = None,
                          consensus_mode: str = "conservative",
                          output_format: str = "json") -> Dict[str, Any]:
    """
    Tool 2: Multi-Model AI Consensus Auditor
    
    Multi-model AI audit using Claude, GPT-4, and Gemini via OpenRouter API.
    
    Args:
        project_path: Path to the project directory to audit
        models: List of AI models to use (default: ["claude", "gpt4", "gemini"])
        openrouter_api_key: OpenRouter API key (or use env var OPENROUTER_API_KEY)
        consensus_mode: How to determine consensus - "conservative" or "average"
        output_format: Report format - "json", "markdown", or "console"
    
    Returns:
        Consensus audit report with all model results
    """
    auditor = MultiModelAuditor(api_key=openrouter_api_key)
    
    report = auditor.run_multi_model_audit(project_path, models, consensus_mode)
    
    if output_format != "json":
        report["formatted_report"] = format_report(report, output_format)
    
    return report


def vibe_audit_full(project_path: str,
                   auto_fix_suggestions: bool = True,
                   output_format: str = "json",
                   models: Optional[List[str]] = None,
                   openrouter_api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Tool 3: Complete Security Workflow
    
    Automated scan followed by multi-model consensus audit.
    
    Args:
        project_path: Path to the project directory to audit
        auto_fix_suggestions: Generate fix suggestions for findings
        output_format: Report format - "json", "markdown", or "console"
        models: List of AI models to use (default: ["claude", "gpt4", "gemini"])
        openrouter_api_key: OpenRouter API key (or use env var OPENROUTER_API_KEY)
    
    Returns:
        Combined results from both audit methods with actionable recommendations
    """
    print("🔍 Running automated scan...")
    scan_result = vibe_audit_scan(project_path, "json")
    
    print(f"📊 Scan Result: {scan_result.get('risk_level', 'UNKNOWN')} - Score: {scan_result.get('risk_score', 0)}/100")
    
    should_run_multi_model = scan_result.get('risk_score', 0) > 20
    
    if should_run_multi_model:
        print("\n🤖 Running multi-model AI audit...")
        multi_model_result = vibe_audit_multi_model(
            project_path, models, openrouter_api_key, "conservative", "json"
        )
    else:
        print("\n✅ Risk score below threshold - skipping multi-model audit")
        multi_model_result = {"status": "skipped", "reason": "Low risk score"}
    
    combined_report = {
        "project_path": project_path,
        "timestamp": datetime.now().isoformat(),
        "automated_scan": scan_result,
        "multi_model_audit": multi_model_result,
        "workflow_recommendation": _generate_workflow_recommendation(
            scan_result, multi_model_result
        )
    }
    
    if auto_fix_suggestions:
        combined_report["fix_suggestions"] = _generate_fix_suggestions(
            scan_result, multi_model_result
        )
    
    if output_format != "json":
        combined_report["formatted_report"] = _format_full_report(combined_report, output_format)
    
    return combined_report


def _generate_workflow_recommendation(scan_result: Dict, multi_model_result: Dict) -> Dict[str, Any]:
    """Generate workflow recommendation based on audit results."""
    scan_risk = scan_result.get('risk_score', 0)
    
    recommendation = {
        "safe_to_publish": False,
        "action_required": [],
        "priority": "low"
    }
    
    if scan_risk >= 80:
        recommendation["safe_to_publish"] = False
        recommendation["action_required"] = [
            "Fix CRITICAL issues immediately",
            "Remove all secrets and credentials",
            "Do not publish under any circumstances"
        ]
        recommendation["priority"] = "critical"
    
    elif scan_risk >= 50:
        recommendation["safe_to_publish"] = False
        recommendation["action_required"] = [
            "Review HIGH severity findings",
            "Fix security vulnerabilities",
            "Re-audit after fixes"
        ]
        recommendation["priority"] = "high"
    
    elif scan_risk >= 20:
        recommendation["safe_to_publish"] = True
        recommendation["action_required"] = [
            "Review MEDIUM severity findings",
            "Consider fixing before publishing"
        ]
        recommendation["priority"] = "medium"
    
    else:
        recommendation["safe_to_publish"] = True
        recommendation["action_required"] = [
            "Review any LOW severity findings",
            "Generally safe to publish"
        ]
        recommendation["priority"] = "low"
    
    if multi_model_result.get("status") != "skipped":
        if multi_model_result.get("private_data_found"):
            recommendation["safe_to_publish"] = False
            recommendation["action_required"].append("Remove private data before publishing")
    
    return recommendation


def _generate_fix_suggestions(scan_result: Dict, multi_model_result: Dict) -> List[Dict[str, str]]:
    """Generate fix suggestions for identified issues."""
    suggestions = []
    
    if scan_result.get('findings'):
        for severity in ['critical', 'high', 'medium']:
            for finding in scan_result['findings'].get(severity, []):
                issue = finding.get('issue', '')
                
                if 'API Key' in issue or 'Token' in issue or 'Secret' in issue:
                    suggestions.append({
                        "file": finding.get('file', ''),
                        "issue": issue,
                        "suggestion": "Use environment variables or secure secret management instead of hardcoding credentials",
                        "severity": severity
                    })
                
                elif 'path' in finding:
                    suggestions.append({
                        "file": finding.get('file', ''),
                        "issue": issue,
                        "suggestion": "Remove or redact file paths that reveal user information",
                        "severity": severity
                    })
                
                elif 'Injection' in issue:
                    suggestions.append({
                        "file": finding.get('file', ''),
                        "issue": issue,
                        "suggestion": "Implement proper input validation and parameterized queries",
                        "severity": severity
                    })
    
    return suggestions


def _format_full_report(report: Dict, output_format: str) -> str:
    """Format full workflow report."""
    if output_format == "markdown":
        md = f"# 🔒 Vibe Codebase Audit - Full Workflow Report\n\n"
        md += f"**Timestamp:** {report.get('timestamp', 'N/A')}\n\n"
        
        md += f"## Automated Scan Results\n\n"
        scan = report.get('automated_scan', {})
        md += f"- **Risk Level:** {scan.get('risk_level', 'N/A')}\n"
        md += f"- **Risk Score:** {scan.get('risk_score', 0)}/100\n"
        md += f"- **Files Scanned:** {scan.get('files_scanned', 0)}\n\n"
        
        multi = report.get('multi_model_audit', {})
        if multi.get('status') != 'skipped':
            md += f"## Multi-Model Consensus\n\n"
            md += f"- **Consensus Risk Level:** {multi.get('consensus_risk_level', 'N/A')}\n"
            md += f"- **Private Data Found:** {'Yes' if multi.get('private_data_found') else 'No'}\n"
            md += f"- **Models Used:** {', '.join(multi.get('models_audited', []))}\n\n"
        
        workflow = report.get('workflow_recommendation', {})
        md += f"## Workflow Recommendation\n\n"
        md += f"- **Safe to Publish:** {'Yes' if workflow.get('safe_to_publish') else 'No'}\n"
        md += f"- **Priority:** {workflow.get('priority', 'unknown').upper()}\n\n"
        
        if workflow.get('action_required'):
            md += f"### Action Required\n\n"
            for action in workflow['action_required']:
                md += f"- {action}\n"
        
        return md
    
    else:
        lines = []
        lines.append("="*80)
        lines.append("🔒 VIBE CODEBASE AUDIT - FULL WORKFLOW")
        lines.append("="*80)
        lines.append("")
        
        scan = report.get('automated_scan', {})
        lines.append(f"📊 Automated Scan: {scan.get('risk_level', 'UNKNOWN')} - Score: {scan.get('risk_score', 0)}/100")
        
        multi = report.get('multi_model_audit', {})
        if multi.get('status') != 'skipped':
            lines.append(f"🤖 Multi-Model: {multi.get('consensus_risk_level', 'UNKNOWN')} - Private Data: {'Found' if multi.get('private_data_found') else 'None'}")
        else:
            lines.append(f"🤖 Multi-Model: Skipped (low risk)")
        
        lines.append("")
        
        workflow = report.get('workflow_recommendation', {})
        lines.append(f"{'✅' if workflow.get('safe_to_publish') else '⛔'} Safe to Publish: {workflow.get('safe_to_publish')}")
        lines.append(f"⚡ Priority: {workflow.get('priority', 'unknown').upper()}")
        
        if workflow.get('action_required'):
            lines.append("")
            lines.append("Action Required:")
            for action in workflow['action_required']:
                lines.append(f"  - {action}")
        
        lines.append("")
        lines.append("="*80)
        
        return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Vibe Codebase Audit Tools")
    parser.add_argument("project_path", help="Path to project to audit")
    parser.add_argument("--tool", choices=["scan", "multi-model", "full"], 
                       default="scan", help="Which audit tool to use")
    parser.add_argument("--format", choices=["json", "markdown", "console"],
                       default="console", help="Output format")
    parser.add_argument("--models", nargs="+", help="AI models to use for multi-model audit")
    parser.add_argument("--api-key", help="OpenRouter API key")
    
    args = parser.parse_args()
    
    if args.tool == "scan":
        result = vibe_audit_scan(args.project_path, args.format)
    elif args.tool == "multi-model":
        result = vibe_audit_multi_model(
            args.project_path, args.models, args.api_key, "conservative", args.format
        )
    else:
        result = vibe_audit_full(
            args.project_path, True, args.format, args.models, args.api_key
        )
    
    if args.format == "json":
        print(json.dumps(result, indent=2))
    elif "formatted_report" in result:
        print(result["formatted_report"])
    else:
        print(format_report(result, "console"))
