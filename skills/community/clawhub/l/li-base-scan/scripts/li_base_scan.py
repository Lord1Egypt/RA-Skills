#!/usr/bin/env python3
"""
Li Base Scan - Linux Security Baseline Scanner v0.0.2
Integrates: nmap, lynis, nikto, sqlmap, trivy
Security Hardened + Enhanced Features
"""

import subprocess
import json
import sys
import re
import argparse
import os
import tempfile
import logging
import signal
import time
import hashlib
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


# Security: Setup logging with no sensitive data
# Use user's home directory to avoid permission issues
log_dir = Path.home() / '.openclaw' / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / 'li-base-scan.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('li-base-scan')

# Security: Set restrictive permissions on log file
try:
    os.chmod(log_file, 0o600)
except:
    pass  # May not have permission, continue anyway


SCAN_MODES = {
    "quick": {
        "tools": ["nmap"],
        "description": "快速扫描 - nmap端口扫描",
        "time_estimate": "30秒"
    },
    "standard": {
        "tools": ["nmap", "lynis"],
        "description": "标准扫描 - 端口+系统审计",
        "time_estimate": "2-5分钟"
    },
    "full": {
        "tools": ["nmap", "lynis", "trivy"],
        "description": "完整扫描 - 全部工具",
        "time_estimate": "5-10分钟"
    },
    "web": {
        "tools": ["nmap", "nikto"],
        "description": "Web专项 - 端口+Web扫描",
        "time_estimate": "2-3分钟"
    },
    "web_sql": {
        "tools": ["nmap", "nikto", "sqlmap"],
        "description": "Web+SQL注入 - Web扫描+SQL注入检测",
        "time_estimate": "5-10分钟"
    },
    "compliance": {
        "tools": ["lynis", "trivy"],
        "description": "合规检查 - 系统+配置",
        "time_estimate": "3-5分钟"
    },
    "stealth": {
        "tools": ["nmap"],
        "description": "隐蔽扫描 - 慢速扫描避免检测",
        "time_estimate": "5-10分钟"
    }
}

NMAP_PROFILES = {
    "quick": ["-T4", "-F", "--open"],
    "standard": ["-T4", "-sV", "-sC", "--open"],
    "full": ["-T4", "-p-", "-sV", "-sC", "-O", "--open"],
    "stealth": ["-T2", "-sS", "-f", "--data-length", "24", "--randomize-hosts"]
}


class SecureSubprocess:
    """Secure subprocess wrapper with proper timeout handling."""
    
    @staticmethod
    def run(cmd: List[str], timeout: int = 300, capture_output: bool = True) -> Tuple[int, str, str]:
        """Run command with secure timeout handling."""
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                text=True
            )
            
            try:
                stdout, stderr = proc.communicate(timeout=timeout)
                return proc.returncode, stdout or "", stderr or ""
            except subprocess.TimeoutExpired:
                logger.warning(f"Command timed out: {' '.join(cmd[:3])}...")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                return -1, "", "扫描超时"
                
        except Exception as e:
            logger.error(f"Command execution failed: {type(e).__name__}")
            return -1, "", "执行失败"


class ScanHistory:
    """Manage scan history with SQLite."""
    
    def __init__(self, db_path: str = "/root/.openclaw/skills/li-base-scan/history.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                target_hash TEXT,
                mode TEXT,
                risk_level TEXT,
                total_findings INTEGER,
                report_hash TEXT,
                report_path TEXT
            )
        ''')
        conn.commit()
        conn.close()
        # Security: Set restrictive permissions on database
        os.chmod(self.db_path, 0o600)
    
    def add_scan(self, target: str, mode: str, risk_level: str, 
                 total_findings: int, report_path: str):
        """Add scan to history with privacy protection."""
        conn = sqlite3.connect(self.db_path)
        # Security: Store hash instead of plaintext target
        target_hash = hashlib.sha256(target.encode()).hexdigest()[:16]
        report_hash = hashlib.sha256(
            f"{target}{mode}{datetime.now()}".encode()
        ).hexdigest()[:16]
        
        conn.execute('''
            INSERT INTO scans (timestamp, target_hash, mode, risk_level, 
                             total_findings, report_hash, report_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), target_hash, mode, risk_level,
              total_findings, report_hash, report_path))
        conn.commit()
        conn.close()
        return report_hash
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Get scan history."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM scans ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results


class ProgressBar:
    """Simple progress bar for terminal."""
    
    def __init__(self, total: int, width: int = 40):
        self.total = total
        self.width = width
        self.current = 0
    
    def update(self, step: int = 1, message: str = ""):
        """Update progress."""
        self.current += step
        percent = min(100, int(100 * self.current / self.total))
        filled = int(self.width * self.current / self.total)
        bar = "█" * filled + "░" * (self.width - filled)
        print(f"\r|{bar}| {percent}% {message}", end="", flush=True)
    
    def finish(self, message: str = "完成"):
        """Finish progress bar."""
        self.current = self.total
        self.update(0, message)
        print()


def validate_target(target: str) -> Tuple[bool, str]:
    """Validate single host target, reject CIDR/ranges."""
    # Extract host from URL if present
    original_target = target
    if target.startswith(('http://', 'https://')):
        # Extract hostname from URL
        import urllib.parse
        try:
            parsed = urllib.parse.urlparse(target)
            if parsed.hostname:
                target = parsed.hostname
            else:
                return False, f"无效URL格式: {original_target}"
        except:
            return False, f"无效URL格式: {original_target}"
    
    # CIDR pattern - REJECTED
    cidr_pattern = r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$'
    if re.match(cidr_pattern, target):
        return False, f"拒绝扫描网段 {original_target}: 仅支持单主机扫描"
    
    # Range notation
    if '-' in target and target[0].isdigit():
        return False, f"拒绝扫描范围 {original_target}: 仅支持单主机扫描"
    
    # Multiple targets
    if ',' in target:
        return False, f"拒绝多目标扫描: 每次仅支持一个主机"
    
    # Single IP
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ip_pattern, target):
        parts = target.split('.')
        if all(0 <= int(p) <= 255 for p in parts):
            return True, ""
        return False, f"无效IP地址: {original_target}"
    
    # Domain
    domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    if re.match(domain_pattern, target):
        if len(target) <= 253:
            return True, ""
        return False, f"域名过长: {original_target}"
    
    return False, f"无效目标格式: {original_target}"


def check_tool(tool: str) -> Tuple[bool, str]:
    """Check if tool is installed and return full path."""
    result = subprocess.run(["which", tool], capture_output=True, text=True)
    if result.returncode == 0:
        return True, result.stdout.strip()
    
    # Check common paths
    common_paths = [f"/usr/sbin/{tool}", f"/sbin/{tool}", 
                    f"/usr/bin/{tool}", f"/bin/{tool}"]
    for path in common_paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return True, path
    
    return False, ""


def run_nmap(target: str, profile: str = "standard", timeout: int = 300) -> Dict[str, Any]:
    """Run nmap scan."""
    has_tool, tool_path = check_tool("nmap")
    if not has_tool:
        return {"error": "nmap未安装", "tool": "nmap"}
    
    args = NMAP_PROFILES.get(profile, NMAP_PROFILES["standard"])
    cmd = [tool_path, "-oX", "-"] + args + [target]
    
    try:
        returncode, stdout, stderr = SecureSubprocess.run(cmd, timeout)
        if returncode == -1:
            return {"error": "扫描超时", "tool": "nmap"}
        return parse_nmap_xml(stdout)
    except Exception as e:
        logger.error(f"Nmap scan failed")
        return {"error": "扫描执行失败", "tool": "nmap"}


def parse_nmap_xml(xml_output: str) -> Dict[str, Any]:
    """Parse nmap XML output."""
    import xml.etree.ElementTree as ET
    
    try:
        root = ET.fromstring(xml_output)
    except:
        return {"error": "解析nmap输出失败", "tool": "nmap"}
    
    hosts = []
    for host in root.findall('.//host'):
        host_data = {"address": "", "hostname": "", "ports": [], "os": []}
        
        addr = host.find('.//address[@addrtype="ipv4"]')
        if addr is not None:
            host_data["address"] = addr.get('addr', '')
        
        hostname = host.find('.//hostnames/hostname')
        if hostname is not None:
            host_data["hostname"] = hostname.get('name', '')
        
        for port in host.findall('.//port'):
            state_elem = port.find('.//state')
            state = state_elem.get('state', '') if state_elem is not None else 'unknown'
            
            port_data = {
                "port": port.get('portid', ''),
                "protocol": port.get('protocol', ''),
                "state": state,
                "service": "",
                "product": "",
                "version": ""
            }
            service = port.find('.//service')
            if service is not None:
                port_data["service"] = service.get('name', '')
                port_data["product"] = service.get('product', '')
                port_data["version"] = service.get('version', '')
            host_data["ports"].append(port_data)
        
        hosts.append(host_data)
    
    return {"tool": "nmap", "hosts": hosts}


def run_lynis(audit_type: str = "system", timeout: int = 300) -> Dict[str, Any]:
    """Run lynis security audit."""
    has_tool, tool_path = check_tool("lynis")
    if not has_tool:
        return {"error": "lynis未安装", "tool": "lynis"}
    
    cmd = [tool_path, "audit", audit_type, "--quiet", "--no-colors"]
    
    try:
        returncode, stdout, stderr = SecureSubprocess.run(cmd, timeout)
        if returncode == -1:
            return {"error": "审计超时", "tool": "lynis"}
        return parse_lynis_output(stdout + stderr)
    except Exception as e:
        logger.error(f"Lynis audit failed")
        return {"error": "审计执行失败", "tool": "lynis"}


def parse_lynis_output(output: str) -> Dict[str, Any]:
    """Parse lynis output."""
    result = {
        "tool": "lynis",
        "score": None,
        "warnings": [],
        "suggestions": [],
        "tests_performed": 0
    }
    
    # Extract hardening index
    score_match = re.search(r'Hardening index.*?(\d+)', output)
    if score_match:
        result["score"] = int(score_match.group(1))
    
    # Extract warnings
    for line in output.split('\n'):
        if '[WARNING]' in line:
            result["warnings"].append(line.strip())
        elif '[SUGGESTION]' in line:
            result["suggestions"].append(line.strip())
    
    # Extract test count
    tests_match = re.search(r'(\d+) tests performed', output)
    if tests_match:
        result["tests_performed"] = int(tests_match.group(1))
    
    return result


def run_nikto(target: str, timeout: int = 300) -> Dict[str, Any]:
    """Run nikto web scan."""
    has_tool, tool_path = check_tool("nikto")
    if not has_tool:
        return {"error": "nikto未安装", "tool": "nikto"}
    
    # Ensure target has protocol
    if not target.startswith(('http://', 'https://')):
        target = f"http://{target}"
    
    cmd = [tool_path, "-h", target, "-Format", "json", "-Tuning", "x1234567890"]
    
    try:
        returncode, stdout, stderr = SecureSubprocess.run(cmd, timeout)
        if returncode == -1:
            return {"error": "扫描超时", "tool": "nikto"}
        if stdout:
            try:
                return {"tool": "nikto", "data": json.loads(stdout)}
            except:
                return {"tool": "nikto", "raw": stdout[:2000]}
        return {"tool": "nikto", "error": "无输出"}
    except Exception as e:
        logger.error(f"Nikto scan failed")
        return {"error": "扫描执行失败", "tool": "nikto"}


def run_sqlmap(target: str, timeout: int = 300, level: int = 1, risk: int = 1) -> Dict[str, Any]:
    """Run sqlmap for SQL injection detection with enhanced parsing.
    
    Args:
        target: HTTP/HTTPS URL to test
        timeout: Scan timeout in seconds
        level: Test level (1-5, higher = more tests)
        risk: Risk level (1-3, higher = riskier tests)
    """
    has_tool, tool_path = check_tool("sqlmap")
    if not has_tool:
        return {"error": "sqlmap未安装", "tool": "sqlmap"}
    
    # Validate target URL
    is_valid, error = validate_target(target)
    if not is_valid:
        return {"error": error, "tool": "sqlmap"}
    
    # Ensure target has protocol
    if not target.startswith(('http://', 'https://')):
        target = f"http://{target}"
    
    # Create secure output directory
    output_dir = f"/tmp/sqlmap_{int(time.time())}_{os.getpid()}"
    os.makedirs(output_dir, mode=0o700, exist_ok=True)
    
    try:
        logger.info(f"Running sqlmap on {target} (level={level}, risk={risk})")
        
        # Build safe sqlmap command
        # --batch: Never ask for user input
        # --level: Test level (1-5)
        # --risk: Risk level (1-3)
        cmd = [
            tool_path, "-u", target,
            "--batch",
            "--level", str(min(level, 3)),  # Cap at level 3 for safety
            "--risk", str(min(risk, 1)),    # Keep risk low by default
            "--threads", "5",
            "--timeout", "10",
            "--retries", "1",
            "--output-dir", output_dir,
            "--forms",  # Test forms
            "--smart",  # Smart detection
            "--exclude-sysdbs",  # Don't scan system databases
            "--answers", "follow=Y,crack=N,dict=N",
        ]
        
        returncode, stdout, stderr = SecureSubprocess.run(cmd, timeout)
        
        if returncode == -1:
            return {"error": "扫描超时", "tool": "sqlmap"}
        
        # Parse sqlmap output
        output = stdout + stderr
        
        vulns = []
        is_vulnerable = False
        db_type = None
        injection_points = []
        techniques = []
        
        # Parse vulnerability indicators
        if "is vulnerable" in output.lower():
            is_vulnerable = True
            vulns.append("发现SQL注入漏洞")
            
        if "injectable" in output.lower():
            is_vulnerable = True
            
        if "sql injection" in output.lower():
            is_vulnerable = True
            if "发现SQL注入漏洞" not in vulns:
                vulns.append("发现SQL注入漏洞")
        
        # Extract database type
        db_patterns = [
            r"back-end DBMS: (\w+)",
            r"web application technology: ([^,]+)",
        ]
        for pattern in db_patterns:
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                db_type = match.group(1)
                break
        
        # Extract injection points
        injection_patterns = [
            r"Parameter: (\w+)",
            r"GET parameter '(\w+)'",
            r"POST parameter '(\w+)'",
        ]
        for pattern in injection_patterns:
            matches = re.findall(pattern, output, re.IGNORECASE)
            injection_points.extend(matches)
        
        # Determine techniques found
        if "error-based" in output.lower():
            techniques.append("Error-based")
        if "union query" in output.lower() or "union-based" in output.lower():
            techniques.append("Union-based")
        if "blind" in output.lower() or "time-based" in output.lower():
            techniques.append("Time-based blind")
        if "boolean-based" in output.lower():
            techniques.append("Boolean-based blind")
        if "stacked queries" in output.lower():
            techniques.append("Stacked queries")
        
        # Check for log files with more details
        target_log_dir = os.path.join(output_dir, target.replace('://', '_').replace('/', '_'))
        detailed_findings = []
        if os.path.exists(target_log_dir):
            log_file = os.path.join(target_log_dir, "log")
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        log_content = f.read()
                        if log_content:
                            detailed_findings = log_content[:2000]
                except:
                    pass
        
        return {
            "tool": "sqlmap",
            "target": target,
            "vulnerable": is_vulnerable,
            "findings": vulns,
            "db_type": db_type,
            "injection_points": list(set(injection_points)),
            "techniques": techniques,
            "output": output[:2000] if output else None,
            "detailed_log": detailed_findings if detailed_findings else None,
            "risk_level": risk,
            "test_level": level,
        }
        
    except Exception as e:
        logger.exception(f"SQLMap scan failed: {e}")
        return {"error": f"扫描执行失败: {str(e)}", "tool": "sqlmap"}
    finally:
        # Cleanup output directory
        try:
            import shutil
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir, ignore_errors=True)
        except:
            pass


def run_trivy(target: str = ".", timeout: int = 300) -> Dict[str, Any]:
    """Run trivy filesystem scan with secure temp file."""
    has_tool, tool_path = check_tool("trivy")
    if not has_tool:
        return {"error": "trivy未安装", "tool": "trivy"}
    
    # Security: Use secure temp file
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', 
                                         delete=False, dir='/tmp') as f:
            temp_file = f.name
        
        # Set restrictive permissions
        os.chmod(temp_file, 0o600)
        
        cmd = [tool_path, "fs", "--scanners", "vuln,secret,config,misconfig", 
               "-f", "json", "-o", temp_file, target]
        
        returncode, stdout, stderr = SecureSubprocess.run(cmd, timeout)
        
        if returncode == -1:
            return {"error": "扫描超时", "tool": "trivy"}
        
        if os.path.exists(temp_file):
            with open(temp_file, 'r') as f:
                data = json.load(f)
            
            vulns = []
            secrets = []
            misconfigs = []
            
            if "Results" in data:
                for result in data["Results"]:
                    if "Vulnerabilities" in result:
                        for v in result["Vulnerabilities"]:
                            vulns.append({
                                "id": v.get("VulnerabilityID", ""),
                                "title": v.get("Title", ""),
                                "severity": v.get("Severity", ""),
                                "pkg": v.get("PkgName", "")
                            })
                    if "Secrets" in result:
                        for s in result["Secrets"]:
                            secrets.append({
                                "rule": s.get("RuleID", ""),
                                "severity": s.get("Severity", "")
                            })
                    if "Misconfigurations" in result:
                        for m in result["Misconfigurations"]:
                            misconfigs.append({
                                "id": m.get("ID", ""),
                                "title": m.get("Title", ""),
                                "severity": m.get("Severity", "")
                            })
            
            return {
                "tool": "trivy",
                "vulnerabilities": vulns,
                "secrets": secrets,
                "misconfigurations": misconfigs
            }
        
        return {"tool": "trivy", "error": "无输出文件"}
        
    except Exception as e:
        logger.error(f"Trivy scan failed")
        return {"error": "扫描执行失败", "tool": "trivy"}
    finally:
        # Security: Always cleanup temp file
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass


def run_scan(target: str, mode: str, show_progress: bool = True) -> Dict[str, Any]:
    """Run complete scan based on mode."""
    if mode not in SCAN_MODES:
        return {"error": f"未知扫描模式: {mode}"}
    
    is_valid, error = validate_target(target)
    if not is_valid:
        return {"error": error}
    
    scan_config = SCAN_MODES[mode]
    tools = scan_config["tools"]
    
    results = {
        "scan_time": datetime.now().isoformat(),
        "target": target,
        "mode": mode,
        "mode_description": scan_config["description"],
        "tools": {},
        "summary": {}
    }
    
    print(f"🚀 开始{scan_config['description']}...")
    print(f"⏱️  预计时间: {scan_config['time_estimate']}\n")
    
    # Progress tracking
    progress = ProgressBar(len(tools)) if show_progress else None
    
    # Run nmap
    if "nmap" in tools:
        if progress:
            progress.update(0, "nmap 端口扫描...")
        nmap_profile = "quick" if mode == "quick" else "stealth" if mode == "stealth" else "standard"
        results["tools"]["nmap"] = run_nmap(target, nmap_profile)
        if progress:
            progress.update(1)
    
    # Run lynis
    if "lynis" in tools:
        if progress:
            progress.update(0, "lynis 系统审计...")
        results["tools"]["lynis"] = run_lynis()
        if progress:
            progress.update(1)
    
    # Run nikto
    if "nikto" in tools:
        if progress:
            progress.update(0, "nikto Web扫描...")
        results["tools"]["nikto"] = run_nikto(target)
        if progress:
            progress.update(1)
    
    # Run sqlmap
    if "sqlmap" in tools and target.startswith(('http://', 'https://')):
        if progress:
            progress.update(0, "sqlmap 注入检测...")
        results["tools"]["sqlmap"] = run_sqlmap(target)
        if progress:
            progress.update(1)
    
    # Run trivy
    if "trivy" in tools:
        if progress:
            progress.update(0, "trivy 文件系统扫描...")
        results["tools"]["trivy"] = run_trivy("/")
        if progress:
            progress.update(1)
    
    if progress:
        progress.finish("扫描完成!")
    
    # Generate summary
    results["summary"] = generate_summary(results)
    
    return results


def generate_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate scan summary."""
    summary = {
        "risk_level": "low",
        "total_findings": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "info": 0
    }
    
    tools_data = results.get("tools", {})
    
    # Check nmap results
    if "nmap" in tools_data:
        nmap = tools_data["nmap"]
        if "hosts" in nmap:
            for host in nmap["hosts"]:
                ports = host.get("ports", [])
                risky = ["telnet", "ftp", "redis", "mysql", "postgres", "mongodb"]
                for p in ports:
                    if p.get("service", "").lower() in risky:
                        summary["high"] += 1
    
    # Check lynis
    if "lynis" in tools_data:
        lynis = tools_data["lynis"]
        if lynis.get("score") and lynis["score"] < 60:
            summary["medium"] += 1
        summary["low"] += len(lynis.get("suggestions", []))
        summary["info"] += len(lynis.get("warnings", []))
    
    # Check trivy
    if "trivy" in tools_data:
        trivy = tools_data["trivy"]
        for v in trivy.get("vulnerabilities", []):
            sev = v.get("severity", "").upper()
            if sev == "CRITICAL":
                summary["critical"] += 1
            elif sev == "HIGH":
                summary["high"] += 1
            elif sev == "MEDIUM":
                summary["medium"] += 1
            else:
                summary["low"] += 1
        
        # Secrets are high priority
        if trivy.get("secrets"):
            summary["high"] += len(trivy.get("secrets", []))
    
    summary["total_findings"] = (summary["critical"] + summary["high"] + 
                                  summary["medium"] + summary["low"] + 
                                  summary["info"])
    
    # Determine risk level
    if summary["critical"] > 0:
        summary["risk_level"] = "critical"
    elif summary["high"] > 0:
        summary["risk_level"] = "high"
    elif summary["medium"] > 0:
        summary["risk_level"] = "medium"
    
    return summary


def generate_report(results: Dict[str, Any]) -> str:
    """Generate human-readable report."""
    lines = ["# Li Base Scan 安全报告\n"]
    lines.append(f"**目标**: {results.get('target', 'N/A')}\n")
    lines.append(f"**扫描模式**: {results.get('mode_description', 'N/A')}\n")
    lines.append(f"**扫描时间**: {results.get('scan_time', 'N/A')}\n\n")
    
    # Summary
    summary = results.get("summary", {})
    risk_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
    risk_level = summary.get("risk_level", "low")
    lines.append(f"## 风险评估\n\n")
    lines.append(f"**总体评级**: {risk_emoji.get(risk_level, '🟢')} **{risk_level.upper()}**\n\n")
    lines.append(f"- 🔴 严重: {summary.get('critical', 0)}\n")
    lines.append(f"- 🟠 高危: {summary.get('high', 0)}\n")
    lines.append(f"- 🟡 中危: {summary.get('medium', 0)}\n")
    lines.append(f"- 🟢 低危: {summary.get('low', 0)}\n")
    lines.append(f"- ℹ️  信息: {summary.get('info', 0)}\n")
    lines.append(f"- **总计**: {summary.get('total_findings', 0)} 项发现\n\n")
    
    # Tool results
    tools = results.get("tools", {})
    
    if "nmap" in tools:
        lines.append("## 🔍 Nmap 端口扫描\n\n")
        nmap = tools["nmap"]
        if "hosts" in nmap:
            for host in nmap["hosts"]:
                addr = host.get("address", "Unknown")
                ports = host.get("ports", [])
                if ports:
                    lines.append(f"### 主机: {addr}\n\n")
                    lines.append("| 端口 | 协议 | 状态 | 服务 | 版本 |\n")
                    lines.append("|------|------|------|------|------|\n")
                    for p in ports:
                        lines.append(f"| {p.get('port', '')} | {p.get('protocol', '')} | {p.get('state', '')} | {p.get('service', '')} | {p.get('version', '')} |\n")
                    lines.append("\n")
                else:
                    lines.append(f"*主机 {addr}: 无开放端口*\n\n")
        if "error" in nmap:
            lines.append(f"⚠️  {nmap['error']}\n\n")
    
    if "lynis" in tools:
        lines.append("## 🔐 Lynis 系统审计\n\n")
        lynis = tools["lynis"]
        score = lynis.get("score")
        if score is not None:
            score_emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
            lines.append(f"**安全评分**: {score_emoji} **{score}/100**\n\n")
        warnings = lynis.get("warnings", [])
        if warnings:
            lines.append("### ⚠️ 警告\n\n")
            for w in warnings[:10]:
                lines.append(f"- {w}\n")
            if len(warnings) > 10:
                lines.append(f"- ... 还有 {len(warnings) - 10} 项\n")
            lines.append("\n")
        suggestions = lynis.get("suggestions", [])
        if suggestions:
            lines.append("### 💡 建议\n\n")
            for s in suggestions[:5]:
                lines.append(f"- {s}\n")
            if len(suggestions) > 5:
                lines.append(f"- ... 还有 {len(suggestions) - 5} 项\n")
            lines.append("\n")
        if "error" in lynis:
            lines.append(f"⚠️  {lynis['error']}\n\n")
    
    if "nikto" in tools:
        lines.append("## 🌐 Nikto Web扫描\n\n")
        nikto = tools["nikto"]
        if "error" in nikto:
            lines.append(f"⚠️  {nikto['error']}\n\n")
        elif "data" in nikto:
            data = nikto["data"]
            if isinstance(data, dict) and "vulnerabilities" in data:
                vulns = data["vulnerabilities"]
                lines.append(f"发现 **{len(vulns)}** 个Web安全问题\n\n")
                for v in vulns[:5]:
                    lines.append(f"- {v.get('msg', 'Unknown')}\n")
        else:
            lines.append("Web扫描完成\n\n")
    
    if "trivy" in tools:
        lines.append("## 📦 Trivy 漏洞扫描\n\n")
        trivy = tools["trivy"]
        vulns = trivy.get("vulnerabilities", [])
        if vulns:
            lines.append(f"发现 **{len(vulns)}** 个CVE漏洞\n\n")
            critical_high = [v for v in vulns if v.get("severity") in ["CRITICAL", "HIGH"]]
            if critical_high:
                lines.append("### 🔴 严重/高危漏洞\n\n")
                for v in critical_high[:5]:
                    lines.append(f"- **{v.get('id', '')}** ({v.get('severity', '')}): {v.get('title', '')[:60]}...\n")
                lines.append("\n")
        secrets = trivy.get("secrets", [])
        if secrets:
            lines.append(f"⚠️  发现 **{len(secrets)}** 个敏感信息泄露\n\n")
            for s in secrets[:5]:
                lines.append(f"- 规则: {s.get('rule', '')} (严重: {s.get('severity', '')})\n")
            lines.append("\n")
        misconfigs = trivy.get("misconfigurations", [])
        if misconfigs:
            lines.append(f"⚙️  发现 **{len(misconfigs)}** 个配置问题\n\n")
        if "error" in trivy:
            lines.append(f"⚠️  {trivy['error']}\n\n")
    
    # Recommendations
    lines.append("## 🛡️ 优先修复建议\n\n")
    if summary.get("critical", 0) > 0:
        lines.append("### 🔴 立即处理 (Critical)\n\n")
        lines.append("1. 修复发现的严重CVE漏洞\n")
        lines.append("2. 检查并清理敏感信息泄露\n")
        lines.append("3. 升级受影响的软件包\n\n")
    if summary.get("high", 0) > 0:
        lines.append("### 🟠 高优先级 (High)\n\n")
        lines.append("1. 关闭不必要的服务端口\n")
        lines.append("2. 升级存在漏洞的软件版本\n")
        lines.append("3. 检查敏感信息泄露位置\n\n")
    if summary.get("medium", 0) > 0:
        lines.append("### 🟡 中优先级 (Medium)\n\n")
        lines.append("1. 根据Lynis建议加固系统配置\n")
        lines.append("2. 启用防火墙规则\n")
        lines.append("3. 定期运行安全扫描\n\n")
    
    lines.append("---\n\n")
    lines.append("*报告由 Li Base Scan 生成*\n")
    
    # Add AI Analysis Section
    lines.append("\n---\n")
    lines.append(generate_ai_analysis_prompt(results))
    
    return "".join(lines)


def generate_ai_analysis_prompt(results: Dict[str, Any]) -> str:
    """Generate AI analysis section for LLM processing."""
    lines = ["## 🤖 AI 深度分析\n\n"]
    
    summary = results.get("summary", {})
    tools = results.get("tools", {})
    target = results.get("target", "Unknown")
    
    lines.append(f"**扫描目标**: {target}\n")
    lines.append(f"**扫描模式**: {results.get('mode_description', 'N/A')}\n")
    lines.append(f"**总体风险**: {summary.get('risk_level', 'unknown').upper()}\n\n")
    
    # Prepare data for AI
    lines.append("### 📊 原始扫描数据\n\n")
    
    # Nmap data
    if "nmap" in tools:
        nmap = tools["nmap"]
        lines.append("**Nmap 端口发现**:\n\n")
        if "hosts" in nmap:
            for host in nmap["hosts"]:
                ports = host.get("ports", [])
                if ports:
                    lines.append(f"主机 {host.get('address', 'N/A')} 开放端口:\n")
                    for p in ports:
                        lines.append(f"- Port {p.get('port')}/{p.get('protocol')}: {p.get('service')} ({p.get('product')} {p.get('version')})\n")
                else:
                    lines.append("无开放端口\n")
        lines.append("\n")
    
    # Lynis data
    if "lynis" in tools:
        lynis = tools["lynis"]
        lines.append("**Lynis 系统审计**:\n\n")
        score = lynis.get("score")
        if score:
            lines.append(f"- 安全评分: {score}/100\n")
        warnings = lynis.get("warnings", [])
        if warnings:
            lines.append(f"- 警告数量: {len(warnings)}\n")
            lines.append("- 主要警告:\n")
            for w in warnings[:5]:
                lines.append(f"  * {w}\n")
        suggestions = lynis.get("suggestions", [])
        if suggestions:
            lines.append(f"- 建议数量: {len(suggestions)}\n")
        lines.append("\n")
    
    # Trivy data
    if "trivy" in tools:
        trivy = tools["trivy"]
        lines.append("**Trivy 漏洞扫描**:\n\n")
        vulns = trivy.get("vulnerabilities", [])
        if vulns:
            severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
            for v in vulns:
                sev = v.get("severity", "UNKNOWN")
                severity_count[sev] = severity_count.get(sev, 0) + 1
            lines.append(f"- 漏洞总数: {len(vulns)}\n")
            for sev, count in severity_count.items():
                if count > 0:
                    lines.append(f"- {sev}: {count}\n")
            lines.append("- 关键漏洞详情:\n")
            critical_high = [v for v in vulns if v.get("severity") in ["CRITICAL", "HIGH"]][:5]
            for v in critical_high:
                lines.append(f"  * {v.get('id')}: {v.get('title', 'N/A')[:50]}... (Severity: {v.get('severity')})\n")
        secrets = trivy.get("secrets", [])
        if secrets:
            lines.append(f"- 敏感信息泄露: {len(secrets)} 处\n")
        misconfigs = trivy.get("misconfigurations", [])
        if misconfigs:
            lines.append(f"- 配置问题: {len(misconfigs)} 处\n")
        lines.append("\n")
    
    # AI Analysis Request
    lines.append("---\n\n")
    lines.append("### 💬 请AI助手分析以下内容:\n\n")
    lines.append("基于以上扫描数据，请提供:\n\n")
    lines.append("1. **执行摘要** - 用1-2句话总结最关键的安全问题\n")
    lines.append("2. **风险分析** - 针对每个发现的具体风险解释其危害\n")
    lines.append("3. **CVE关联** - 对发现的软件版本，列出可能存在的已知CVE（如有）\n")
    lines.append("4. **修复优先级** - 按P0/P1/P2/P3分级给出修复顺序\n")
    lines.append("5. **具体修复命令** - 提供可直接执行的加固命令\n")
    lines.append("6. **持续监控建议** - 如何设置定期检查和告警\n\n")
    
    return "".join(lines)


def export_report(results: Dict[str, Any], format: str = "markdown", 
                  output_dir: str = "/root/.openclaw/skills/li-base-scan/reports") -> str:
    """Export report to file with security hardening."""
    os.makedirs(output_dir, exist_ok=True)
    # Security: Set restrictive permissions on reports directory
    os.chmod(output_dir, 0o700)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Security: Use SHA256 with 16 chars instead of MD5 with 8 chars
    target_hash = hashlib.sha256(results.get('target', '').encode()).hexdigest()[:16]
    
    if format == "json":
        filename = f"scan_{target_hash}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    else:
        filename = f"scan_{target_hash}_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(generate_report(results))
    
    # Security: Set restrictive permissions
    os.chmod(filepath, 0o600)
    
    return filepath


def parse_conversation_input(user_input: str) -> Tuple[str, str]:
    """Parse natural language to extract target and mode."""
    user_input_lower = user_input.lower()
    
    # Detect mode
    mode = "standard"
    if any(w in user_input_lower for w in ["快速", "quick", "fast"]):
        mode = "quick"
    elif any(w in user_input_lower for w in ["完整", "full", "全面", "全部"]):
        mode = "full"
    elif any(w in user_input_lower for w in ["sql", "注入", "injection"]):
        mode = "web_sql"
    elif any(w in user_input_lower for w in ["web", "网站", "http", "https"]):
        mode = "web"
    elif any(w in user_input_lower for w in ["合规", "compliance", "基线", "baseline"]):
        mode = "compliance"
    elif any(w in user_input_lower for w in ["隐蔽", "stealth", "慢速", "slow"]):
        mode = "stealth"
    elif any(w in user_input_lower for w in ["本地", "localhost", "本机"]):
        mode = "standard"
    
    # Detect target
    ip_pattern = r'\b(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?\b'
    url_pattern = r'https?://[^\s]+'
    domain_pattern = r'\b([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
    
    url_match = re.search(url_pattern, user_input)
    ip_match = re.search(ip_pattern, user_input)
    domain_match = re.search(domain_pattern, user_input)
    
    target = None
    if url_match:
        target = url_match.group(0)
    elif ip_match:
        target = ip_match.group(0)
    elif domain_match:
        target = domain_match.group(0)
    elif "本地" in user_input or "localhost" in user_input_lower:
        target = "127.0.0.1"
    
    return target, mode


def show_history(limit: int = 10):
    """Show scan history."""
    history = ScanHistory()
    scans = history.get_history(limit)
    
    if not scans:
        print("暂无扫描历史")
        return
    
    print(f"\n📊 最近 {len(scans)} 次扫描记录\n")
    print(f"{'时间':<20} {'目标哈希':<20} {'模式':<12} {'风险':<8} {'发现':<6}")
    print("-" * 70)
    
    for scan in scans:
        time = scan['timestamp'][:16].replace('T', ' ') if 'timestamp' in scan else 'N/A'
        target = scan.get('target_hash', 'N/A')[:18]
        mode = scan.get('mode', 'N/A')[:10]
        risk = scan.get('risk_level', 'unknown')[:6]
        findings = str(scan.get('total_findings', 0))
        print(f"{time:<20} {target:<20} {mode:<12} {risk:<8} {findings:<6}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Li Base Scan v0.0.2 - Linux Security Baseline Scanner'
    )
    parser.add_argument('target', nargs='?', help='Target IP, domain, or URL')
    parser.add_argument('--mode', '-m', default='standard',
                        choices=list(SCAN_MODES.keys()),
                        help='Scan mode')
    parser.add_argument('--conversation', '-c', help='Natural language input')
    parser.add_argument('--json', '-j', action='store_true', help='Output JSON')
    parser.add_argument('--timeout', '-t', type=int, default=300, 
                        help='Timeout per tool (seconds)')
    parser.add_argument('--export', '-e', choices=['markdown', 'json'],
                        help='Export report to file')
    parser.add_argument('--history', action='store_true',
                        help='Show scan history')
    parser.add_argument('--no-progress', action='store_true',
                        help='Disable progress bar')
    
    args = parser.parse_args()
    
    # Show history
    if args.history:
        show_history()
        return
    
    # Parse conversation input
    if args.conversation:
        target, mode = parse_conversation_input(args.conversation)
        if not target:
            print(json.dumps({"error": "无法从输入中提取目标"}, ensure_ascii=False))
            sys.exit(1)
    elif args.target:
        target = args.target
        mode = args.mode
    else:
        print(json.dumps({"error": "请提供目标或使用 --conversation"}, ensure_ascii=False))
        parser.print_help()
        sys.exit(1)
    
    # Log scan start (no sensitive data)
    logger.info(f"Starting scan: mode={mode}, target_hash={hashlib.sha256(target.encode()).hexdigest()[:8]}")
    
    # Run scan
    show_progress = not args.no_progress and not args.json
    results = run_scan(target, mode, show_progress=show_progress)
    
    if "error" in results and not results.get("tools"):
        print(json.dumps(results, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    # Export if requested
    if args.export:
        report_path = export_report(results, args.export)
        print(f"\n📄 报告已导出: {report_path}")
        
        # Add to history
        summary = results.get("summary", {})
        history = ScanHistory()
        report_hash = history.add_scan(
            target=target,
            mode=mode,
            risk_level=summary.get("risk_level", "unknown"),
            total_findings=summary.get("total_findings", 0),
            report_path=report_path
        )
        print(f"🔖 扫描记录ID: {report_hash}")
    
    # Output results
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("\n" + generate_report(results))


if __name__ == '__main__':
    main()
