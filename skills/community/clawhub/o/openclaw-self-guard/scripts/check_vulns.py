#!/usr/bin/env python3
"""
OpenClaw Self Guard - Main Vulnerability Check Script
Combines all sources, compares with local version, outputs report
"""

import json
import subprocess
import sys
import os
import re
from datetime import datetime
from typing import List, Dict, Optional

# Add script directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_local_version() -> tuple:
    """Get local OpenClaw version"""
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            match = re.search(r'(\d+\.\d+(?:\.\d+)?)', version)
            if match:
                return match.group(1), version
    except Exception:
        pass
    
    # Try package.json
    try:
        path = "/home/raspi/.npm-global/lib/node_modules/openclaw/package.json"
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
                version = data.get('version', 'unknown')
                return version, f"OpenClaw v{version}"
    except Exception:
        pass
    
    return None, "Unknown"


def run_script(script_name: str, *args) -> Optional[dict]:
    """Run a Python script and return its JSON output"""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    cmd = ["python3", script_path] + list(args)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
    except Exception as e:
        print(f"Error running {script_name}: {e}", file=sys.stderr)
    
    return None


def check_version_affected(version: str, affected_ranges: List[Dict]) -> tuple:
    """Check if version is affected by any of the ranges"""
    if not version or version == "unknown":
        return False, None
    
    for aff in affected_ranges:
        range_str = aff.get("range", "")
        fixed = aff.get("fixed", "")
        
        # Simple version comparison
        # e.g., ">= 1.0.0 < 1.5.0" means affected if 1.0.0 <= version < 1.5.0
        if "<" in range_str and ">" in range_str:
            # Complex range, try to parse
            try:
                parts = range_str.split()
                for i, part in enumerate(parts):
                    if part in [">=", "<=", ">", "<", "="]:
                        op = part
                        ver = parts[i + 1] if i + 1 < len(parts) else ""
                        # Simplified check
                        if op == ">=":
                            if version < ver:
                                return True, f"Affected by: {range_str}, Fix: {fixed}"
            except Exception:
                pass
    
    return False, None


def format_output(nvd_data: dict, github_data: dict, local_version: str) -> str:
    """Format the vulnerability report"""
    output = []
    output.append("# 🔒 OpenClaw 安全漏洞报告\n")
    output.append(f"**检查时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.append(f"**本地版本**: {local_version}\n")
    
    has_findings = False
    
    # OpenClaw-specific GitHub advisories
    if github_data and github_data.get("type") == "openclaw_specific":
        advisories = github_data.get("advisories", [])
        if advisories:
            has_findings = True
            output.append("\n## ⚠️ OpenClaw 专用漏洞\n")
            output.append(f"检测到 **{len(advisories)}** 条 OpenClaw 相关安全公告：\n")
            
            for adv in advisories:
                ghsa = adv.get("ghsa_id", "")
                cve = adv.get("cve_id", "")
                severity = adv.get("severity", "")
                desc = adv.get("description", "")[:200]
                published = adv.get("published", "")
                
                sev_emoji = "🔴" if severity == "CRITICAL" else "🟠" if severity == "HIGH" else "🟡"
                
                output.append(f"\n### {sev_emoji} {ghsa} / {cve}\n")
                output.append(f"**严重性**: {severity}\n")
                output.append(f"**公布时间**: {published}\n")
                output.append(f"**描述**: {desc}...\n")
                
                # Affected packages
                for aff in adv.get("affected", []):
                    pkg = aff.get("package", "")
                    range_str = aff.get("range", "")
                    fixed = aff.get("fixed", "")
                    output.append(f"- 包: `{pkg}`\n")
                    output.append(f"  - 影响版本: {range_str}\n")
                    output.append(f"  - 修复版本: {fixed}\n")
            
            output.append("\n## 🛠️ 补救建议\n")
            output.append("1. 立即查看 GitHub 安全公告页面获取详情\n")
            output.append("2. 根据指示升级到修复版本\n")
            output.append("3. 重启 OpenClaw 服务\n")
    
    # High-severity CVEs from NVD
    nvd_cves = nvd_data.get("cves", []) if nvd_data else []
    if nvd_cves:
        has_findings = True
        output.append(f"\n## 📢 高危 CVE 预警\n")
        output.append(f"检测到 **{len(nvd_cves)}** 条近期高危漏洞（CVSS ≥ 7.0）：\n")
        
        output.append("| CVE ID | CVSS | 严重性 | 公布时间 | 描述 |")
        output.append("|--------|------|--------|----------|------|")
        
        for cve in nvd_cves[:10]:  # Top 10
            cve_id = cve.get("cve_id", "")
            score = cve.get("cvss_score", "N/A")
            severity = cve.get("cvss_severity", "")
            published = cve.get("published", "")
            desc = cve.get("description", "")[:80]
            
            sev_emoji = "🔴" if float(score) >= 9.0 else "🟠" if float(score) >= 7.0 else "🟡"
            
            output.append(f"| {cve_id} | {score} | {sev_emoji}{severity} | {published} | {desc}... |")
        
        output.append("\n**建议**: 定期更新系统组件和依赖包\n")
    
    if not has_findings:
        output.append("\n✅ **未检测到 OpenClaw 相关安全漏洞**\n")
        output.append("本地版本安全，建议继续保持定期更新。\n")
    
    output.append("\n---\n")
    output.append("*此报告由 OpenClaw Self Guard 自动生成*\n")
    
    return "".join(output)


def main():
    """Main check routine"""
    # Get local version
    local_version, display_version = get_local_version()
    
    # Fetch vulnerability data
    print(f"Checking OpenClaw version: {display_version}", file=sys.stderr)
    print("Fetching NVD CVE data...", file=sys.stderr)
    nvd_data = run_script("fetch_nvd.py", "--openclaw-only")
    
    print("Fetching GitHub Security Advisories...", file=sys.stderr)
    github_data = run_script("fetch_github.py", "--openclaw")
    
    # Check if any findings are relevant to our version
    findings = []
    
    if github_data and github_data.get("advisories"):
        for adv in github_data.get("advisories", []):
            affected = adv.get("affected", [])
            is_affected, reason = check_version_affected(local_version, affected)
            if is_affected:
                adv["local_affected"] = reason
                findings.append(adv)
    
    # Generate output
    if findings or (nvd_data and nvd_data.get("cves") and len(nvd_data.get("cves", [])) > 0):
        # Has vulnerabilities
        output = format_output(nvd_data, github_data, display_version)
        
        if "--json" in sys.argv:
            print(json.dumps({
                "has_vulnerabilities": True,
                "local_version": display_version,
                "nvd_count": len(nvd_data.get("cves", [])) if nvd_data else 0,
                "github_count": len(findings),
                "report": output
            }))
        else:
            print(output)
    else:
        # No vulnerabilities - silent mode
        if "--json" in sys.argv:
            print(json.dumps({
                "has_vulnerabilities": False,
                "local_version": display_version,
                "nvd_count": 0,
                "github_count": 0,
                "report": None
            }))
        else:
            # Silent - only print if --verbose
            if "--verbose" in sys.argv:
                print(f"✅ OpenClaw v{local_version} - No vulnerabilities detected")
            # Otherwise silent


if __name__ == "__main__":
    main()
