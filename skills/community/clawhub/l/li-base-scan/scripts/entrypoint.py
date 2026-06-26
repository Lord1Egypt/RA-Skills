#!/usr/bin/env python3
"""
Entry point for the security scanner skill.
Handles integration with OpenClaw framework.
"""

import json
import sys
import os
import subprocess
import tempfile
from pathlib import Path


def map_tools_to_mode(tools):
    """Map tool list to scan mode."""
    tool_set = set(tools)
    
    # Full scan modes
    if tool_set >= {"nmap", "lynis", "trivy"}:
        return "full"
    elif tool_set >= {"lynis", "trivy"}:
        return "compliance"
    elif tool_set >= {"nmap", "nikto"} and "sqlmap" in tool_set:
        # Web focused with SQL injection
        return "web"
    elif tool_set >= {"nmap", "nikto"}:
        return "web"
    elif tool_set >= {"nmap", "lynis"}:
        return "standard"
    elif "nmap" in tool_set:
        return "quick"
    elif "lynis" in tool_set:
        return "compliance"
    else:
        return "standard"


def main():
    """Main entry point function."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "需要提供扫描参数"}))
        return
    
    # Parse input - could be JSON or natural language
    input_data = sys.argv[1]
    
    try:
        # Try to parse as JSON first
        params = json.loads(input_data)
        target = params.get("target")
        tools = params.get("tools", ["nmap", "nikto"])
        timeout = params.get("timeout", 300)
        output_format = params.get("format", "json")
        interactive = params.get("interactive", False)
        html_report = params.get("html_report")
    except json.JSONDecodeError:
        # Treat as natural language
        target = input_data.strip()
        tools = ["nmap", "nikto"]
        timeout = 300
        output_format = "json"
        interactive = False
        html_report = None
        
        # Parse natural language for options
        if "sql" in target.lower() or "注入" in target.lower():
            tools.append("sqlmap")
        if "系统" in target.lower() or "加固" in target.lower():
            tools.append("lynis")
        if "依赖" in target.lower() or "包" in target.lower():
            tools.append("trivy")
        if "交互" in target.lower() or "对话" in target.lower():
            interactive = True
        if "html" in target.lower() or "报告" in target.lower():
            output_format = "html"
    
    # Validate target
    if not target and not interactive:
        print(json.dumps({"error": "需要指定目标地址"}))
        return
    
    # Build command
    script_path = os.path.join(os.path.dirname(__file__), "li_base_scan.py")
    cmd = [
        sys.executable, script_path,
        "--timeout", str(timeout)
    ]
    
    # Handle interactive mode (not supported by current script)
    if interactive:
        print(json.dumps({"error": "交互模式需要直接运行 li_base_scan.py --conversation"}))
        return
    
    # Determine scan mode based on tools
    mode = map_tools_to_mode(tools)
    cmd.extend(["--mode", mode])
    
    # Add target
    cmd.append(target)
    
    # Handle output format
    if output_format == "json" or output_format == "html":
        cmd.append("--json")
        cmd.append("--no-progress")  # Disable progress bar for clean JSON output
    
    # Execute scan
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 60)
        
        if result.returncode == 0:
            if output_format == "html":
                # Generate HTML from JSON result
                try:
                    # Extract JSON from output (skip non-JSON lines)
                    json_lines = []
                    in_json = False
                    for line in result.stdout.split('\n'):
                        if line.strip().startswith('{'):
                            in_json = True
                        if in_json:
                            json_lines.append(line)
                    
                    if not json_lines:
                        raise ValueError("未找到JSON数据")
                    
                    json_str = '\n'.join(json_lines)
                    scan_results = json.loads(json_str)
                    
                    from html_reporter import HTMLReporter
                    if html_report:
                        report_path = html_report
                    else:
                        safe_target = target.replace('/', '_').replace(':', '_')
                        report_path = f"/tmp/scan_report_{safe_target}.html"
                    
                    reporter = HTMLReporter(scan_results)
                    reporter.save(report_path)
                    
                    print(json.dumps({
                        "status": "success",
                        "format": "html",
                        "report_path": report_path,
                        "message": f"HTML报告已生成: {report_path}"
                    }))
                except Exception as e:
                    print(json.dumps({"error": f"HTML报告生成失败: {str(e)}"}))
            else:
                # For JSON format, extract and re-output clean JSON
                if output_format == "json":
                    try:
                        json_lines = []
                        in_json = False
                        for line in result.stdout.split('\n'):
                            if line.strip().startswith('{'):
                                in_json = True
                            if in_json:
                                json_lines.append(line)
                        
                        if json_lines:
                            json_str = '\n'.join(json_lines)
                            scan_results = json.loads(json_str)
                            print(json.dumps(scan_results, ensure_ascii=False))
                        else:
                            print(result.stdout)
                    except:
                        print(result.stdout)
                else:
                    print(result.stdout)
        else:
            error_msg = result.stderr if result.stderr else "扫描执行失败"
            print(json.dumps({"error": error_msg, "returncode": result.returncode}))
            
    except subprocess.TimeoutExpired:
        print(json.dumps({"error": "扫描超时", "timeout": timeout + 60}))
    except Exception as e:
        print(json.dumps({"error": f"执行异常: {str(e)}"}))


if __name__ == "__main__":
    main()