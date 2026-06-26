#!/usr/bin/env python3
"""HTML Report Generator for Security Scan Results"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List


class HTMLReporter:
    """Generate professional HTML security scan reports."""
    
    # Severity colors
    SEVERITY_COLORS = {
        "CRITICAL": "#dc3545",
        "HIGH": "#fd7e14", 
        "MEDIUM": "#ffc107",
        "LOW": "#17a2b8",
        "INFO": "#6c757d",
    }
    
    def __init__(self, results: Dict[str, Any]):
        self.results = results
        self.scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.target = results.get("target", "Unknown")
    
    def generate(self) -> str:
        """Generate complete HTML report."""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>安全扫描报告 - {self.target}</title>
    <style>
        {self._get_css()}
    </style>
</head>
<body>
    {self._generate_header()}
    {self._generate_summary()}
    {self._generate_details()}
    {self._generate_recommendations()}
    {self._generate_footer()}
</body>
</html>"""
        return html
    
    def _get_css(self) -> str:
        """Return CSS styles for the report."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 8px 8px 0 0; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header .meta { opacity: 0.9; font-size: 0.95em; }
        .summary { padding: 30px; background: #f8f9fa; border-bottom: 1px solid #e9ecef; }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px; }
        .summary-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }
        .summary-card .number { font-size: 2.5em; font-weight: bold; color: #667eea; }
        .summary-card .label { color: #6c757d; margin-top: 5px; }
        .severity-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            color: white;
        }
        .severity-critical { background: #dc3545; }
        .severity-high { background: #fd7e14; }
        .severity-medium { background: #ffc107; color: #333; }
        .severity-low { background: #17a2b8; }
        .severity-info { background: #6c757d; }
        .details { padding: 30px; }
        .section { margin-bottom: 40px; }
        .section h2 { color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 20px; }
        .tool-result { background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; margin-bottom: 20px; border-radius: 0 8px 8px 0; }
        .tool-result h3 { color: #667eea; margin-bottom: 15px; }
        .finding { background: white; padding: 15px; margin: 10px 0; border-radius: 6px; border: 1px solid #e9ecef; }
        .finding-title { font-weight: 600; margin-bottom: 5px; }
        .finding-desc { color: #6c757d; font-size: 0.9em; }
        .code-block { background: #f8f9fa; padding: 15px; border-radius: 6px; overflow-x: auto; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.9em; border: 1px solid #e9ecef; }
        .vulnerability { background: #fff5f5; border-left: 4px solid #dc3545; }
        .recommendations { padding: 30px; background: #f8f9fa; }
        .recommendation { background: white; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #28a745; }
        .recommendation h4 { color: #28a745; margin-bottom: 10px; }
        .footer { padding: 20px; text-align: center; color: #6c757d; font-size: 0.85em; border-top: 1px solid #e9ecef; }
        .status-success { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-danger { color: #dc3545; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e9ecef; }
        th { background: #f8f9fa; font-weight: 600; color: #333; }
        tr:hover { background: #f8f9fa; }
        .tag { display: inline-block; padding: 2px 8px; background: #e9ecef; border-radius: 4px; font-size: 0.8em; margin: 2px; }
        .progress-bar { background: #e9ecef; border-radius: 10px; height: 20px; overflow: hidden; }
        .progress-fill { height: 100%; border-radius: 10px; transition: width 0.3s; }
        .expandable { cursor: pointer; }
        .expandable:hover { background: #f8f9fa; }
        .hidden { display: none; }
    """
    
    def _generate_header(self) -> str:
        """Generate report header."""
        return f"""
        <div class="header">
            <h1>🔒 安全扫描报告</h1>
            <div class="meta">
                <p>📍 目标: <strong>{self.target}</strong></p>
                <p>🕐 扫描时间: {self.scan_time}</p>
            </div>
        </div>
        """
    
    def _generate_summary(self) -> str:
        """Generate executive summary."""
        scan_results = self.results.get("results", {})
        
        # Calculate statistics
        total_tools = len(scan_results)
        vulnerable_count = 0
        critical_count = 0
        high_count = 0
        medium_count = 0
        
        for tool_name, result in scan_results.items():
            if result.get("vulnerable") or result.get("vulnerabilities"):
                vulnerable_count += 1
            
            # Check for severity counts
            vulns = result.get("vulnerabilities", [])
            for v in vulns:
                severity = v.get("severity", "").upper()
                if severity == "CRITICAL":
                    critical_count += 1
                elif severity == "HIGH":
                    high_count += 1
                elif severity == "MEDIUM":
                    medium_count += 1
        
        overall_score = max(0, 100 - (critical_count * 20 + high_count * 10 + medium_count * 5))
        
        return f"""
        <div class="summary">
            <h2>📊 执行摘要</h2>
            <div class="summary-grid">
                <div class="summary-card">
                    <div class="number {'status-danger' if overall_score < 50 else 'status-warning' if overall_score < 80 else 'status-success'}">{overall_score}</div>
                    <div class="label">安全评分</div>
                </div>
                <div class="summary-card">
                    <div class="number {('status-danger' if vulnerable_count > 0 else 'status-success')}">{vulnerable_count}</div>
                    <div class="label">发现漏洞的工具</div>
                </div>
                <div class="summary-card">
                    <div class="number {'status-danger' if critical_count > 0 else 'status-success'}">{critical_count}</div>
                    <div class="label">严重漏洞</div>
                </div>
                <div class="summary-card">
                    <div class="number {('status-warning' if high_count > 0 else 'status-success')}">{high_count}</div>
                    <div class="label">高危漏洞</div>
                </div>
                <div class="summary-card">
                    <div class="number">{medium_count}</div>
                    <div class="label">中危漏洞</div>
                </div>
                <div class="summary-card">
                    <div class="number">{total_tools}</div>
                    <div class="label">扫描工具</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_details(self) -> str:
        """Generate detailed findings."""
        sections = []
        
        scan_results = self.results.get("results", {})
        
        # Nmap Results
        if "nmap" in scan_results:
            sections.append(self._format_nmap_result(scan_results["nmap"]))
        
        # Nikto Results
        if "nikto" in scan_results:
            sections.append(self._format_nikto_result(scan_results["nikto"]))
        
        # SQLMap Results
        if "sqlmap" in scan_results:
            sections.append(self._format_sqlmap_result(scan_results["sqlmap"]))
        
        # Trivy Results
        if "trivy" in scan_results:
            sections.append(self._format_trivy_result(scan_results["trivy"]))
        
        # Lynis Results
        if "lynis" in scan_results:
            sections.append(self._format_lynis_result(scan_results["lynis"]))
        
        return f"""
        <div class="details">
            <h2>🔍 详细结果</h2>
            {''.join(sections) if sections else '<p class="finding-desc">无详细扫描数据</p>'}
        </div>
        """
    
    def _format_nmap_result(self, result: Dict) -> str:
        """Format nmap results."""
        open_ports = result.get("open_ports", [])
        services = result.get("services", [])
        os_info = result.get("os", "未知")
        
        ports_html = ""
        if open_ports:
            ports_rows = ""
            for port_info in open_ports:
                port = port_info.get("port", "")
                service = port_info.get("service", "")
                version = port_info.get("version", "")
                ports_rows += f"<tr><td>{port}</td><td>{service}</td><td>{version}</td></tr>"
            
            ports_html = f"""
            <table>
                <tr><th>端口</th><th>服务</th><th>版本</th></tr>
                {ports_rows}
            </table>
            """
        else:
            ports_html = "<p class='finding-desc'>未发现开放端口或扫描被阻止</p>"
        
        return f"""
        <div class="tool-result">
            <h3>🌐 Nmap 端口扫描</h3>
            <p><strong>操作系统识别:</strong> {os_info}</p>
            <h4>开放端口</h4>
            {ports_html}
        </div>
        """
    
    def _format_nikto_result(self, result: Dict) -> str:
        """Format nikto results."""
        items = result.get("items", [])
        
        if not items:
            return """
            <div class="tool-result">
                <h3>🕷️ Nikto Web扫描</h3>
                <p class="finding-desc">未发现明显漏洞</p>
            </div>
            """
        
        findings_html = ""
        for item in items[:20]:  # Limit to 20 findings
            finding = item.get("finding", "")
            findings_html += f"<div class='finding'><div class='finding-title'>⚠️ {finding}</div></div>"
        
        return f"""
        <div class="tool-result">
            <h3>🕷️ Nikto Web扫描</h3>
            <p>发现 {len(items)} 个安全问题</p>
            {findings_html}
        </div>
        """
    
    def _format_sqlmap_result(self, result: Dict) -> str:
        """Format sqlmap results."""
        is_vulnerable = result.get("vulnerable", False)
        db_type = result.get("db_type", "未知")
        techniques = result.get("techniques", [])
        injection_points = result.get("injection_points", [])
        
        if not is_vulnerable:
            return """
            <div class="tool-result">
                <h3>💉 SQLMap 注入检测</h3>
                <p class="status-success">✅ 未发现SQL注入漏洞</p>
            </div>
            """
        
        techniques_html = ""
        if techniques:
            techniques_html = "<p><strong>发现的注入技术:</strong> " + ", ".join(techniques) + "</p>"
        
        injection_html = ""
        if injection_points:
            injection_html = "<p><strong>注入点:</strong> " + ", ".join(injection_points) + "</p>"
        
        return f"""
        <div class="tool-result vulnerability">
            <h3>💉 SQLMap 注入检测</h3>
            <p class="status-danger">🚨 发现SQL注入漏洞！</p>
            <p><strong>数据库类型:</strong> {db_type}</p>
            {techniques_html}
            {injection_html}
        </div>
        """
    
    def _format_trivy_result(self, result: Dict) -> str:
        """Format trivy results."""
        vulns = result.get("vulnerabilities", [])
        secrets = result.get("secrets", [])
        misconfigs = result.get("misconfigurations", [])
        
        if not vulns and not secrets and not misconfigs:
            return """
            <div class="tool-result">
                <h3>📦 Trivy 依赖扫描</h3>
                <p class="status-success">✅ 未发现漏洞或敏感信息</p>
            </div>
            """
        
        vulns_html = ""
        if vulns:
            vulns_rows = ""
            for v in vulns[:10]:  # Limit to 10
                vid = v.get("id", "N/A")
                title = v.get("title", "Unknown")
                severity = v.get("severity", "Unknown")
                pkg = v.get("pkg", "Unknown")
                color = self.SEVERITY_COLORS.get(severity.upper(), "#6c757d")
                vulns_rows += f"<tr><td><span class='severity-badge' style='background:{color}'>{severity}</span></td><td>{vid}</td><td>{title}</td><td>{pkg}</td></tr>"
            
            vulns_html = f"""
            <table>
                <tr><th>严重度</th><th>CVE</th><th>描述</th><th>组件</th></tr>
                {vulns_rows}
            </table>
            """
        
        return f"""
        <div class="tool-result vulnerability">
            <h3>📦 Trivy 依赖扫描</h3>
            <p>发现 {len(vulns)} 个漏洞</p>
            {vulns_html}
        </div>
        """
    
    def _format_lynis_result(self, result: Dict) -> str:
        """Format lynis results."""
        score = result.get("hardening_index", "N/A")
        warnings = result.get("warnings", [])
        suggestions = result.get("suggestions", [])
        
        warnings_html = ""
        if warnings:
            for w in warnings[:10]:
                warnings_html += f"<div class='finding vulnerability'><div class='finding-title'>⚠️ {w}</div></div>"
        
        suggestions_html = ""
        if suggestions:
            for s in suggestions[:10]:
                suggestions_html += f"<div class='finding'><div class='finding-title'>💡 {s}</div></div>"
        
        return f"""
        <div class="tool-result">
            <h3>🔧 Lynis 系统加固</h3>
            <p><strong>加固指数:</strong> <span class="number">{score}</span>/100</p>
            <h4>警告</h4>
            {warnings_html or '<p class="finding-desc">无警告</p>'}
            <h4>建议</h4>
            {suggestions_html or '<p class="finding-desc">无建议</p>'}
        </div>
        """
    
    def _generate_recommendations(self) -> str:
        """Generate security recommendations."""
        recommendations = []
        
        scan_results = self.results.get("results", {})
        
        # Check for SQL injection
        sqlmap_result = scan_results.get("sqlmap", {})
        if sqlmap_result.get("vulnerable"):
            recommendations.append({
                "title": "修复SQL注入漏洞",
                "content": """
                发现SQL注入漏洞，建议立即采取措施：<br>
                1. 使用参数化查询（Prepared Statements）<br>
                2. 输入验证和过滤<br>
                3. 使用ORM框架<br>
                4. 最小权限数据库账户<br>
                5. 部署WAF防护
                """
            })
        
        # Check for open ports
        nmap_result = scan_results.get("nmap", {})
        open_ports = nmap_result.get("open_ports", [])
        if len(open_ports) > 10:
            recommendations.append({
                "title": "减少开放端口",
                "content": f"检测到 {len(open_ports)} 个开放端口，建议关闭不必要的服务，减少攻击面。"
            })
        
        # Check for web vulnerabilities
        nikto_result = scan_results.get("nikto", {})
        if nikto_result.get("items"):
            recommendations.append({
                "title": "修复Web安全漏洞",
                "content": """
                发现Web安全问题，建议：<br>
                1. 及时更新Web服务器和组件<br>
                2. 配置安全HTTP头（HSTS, CSP等）<br>
                3. 禁用不必要的服务器信息泄露<br>
                4. 实施访问控制
                """
            })
        
        # Check lynis score
        lynis_result = scan_results.get("lynis", {})
        score = lynis_result.get("hardening_index", 0)
        if score and score < 60:
            recommendations.append({
                "title": "提升系统加固等级",
                "content": f"当前加固指数 {score}/100 偏低，建议运行 lynis audit system 查看详细加固建议。"
            })
        
        # Default recommendations
        if not recommendations:
            recommendations.append({
                "title": "保持安全基线",
                "content": """
                未发现严重问题，建议：<br>
                1. 定期执行安全扫描<br>
                2. 及时更新系统和依赖<br>
                3. 监控日志和异常行为<br>
                4. 实施纵深防御策略
                """
            })
        
        recs_html = ""
        for rec in recommendations:
            recs_html += f"""
            <div class="recommendation">
                <h4>{rec['title']}</h4>
                <p>{rec['content']}</p>
            </div>
            """
        
        return f"""
        <div class="recommendations">
            <h2>💡 修复建议</h2>
            {recs_html}
        </div>
        """
    
    def _generate_footer(self) -> str:
        """Generate report footer."""
        return f"""
        <div class="footer">
            <p>报告由 li-base-scan 生成 | 扫描时间: {self.scan_time}</p>
            <p class="finding-desc">本报告仅供参考，请结合实际情况进行安全加固</p>
        </div>
        """
    
    def save(self, output_path: str) -> str:
        """Save report to file."""
        html = self.generate()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return output_path


def generate_html_report(results: Dict[str, Any], output_path: str = None) -> str:
    """Convenience function to generate HTML report.
    
    Args:
        results: Scan results dictionary
        output_path: Optional path to save report
        
    Returns:
        HTML content string
    """
    reporter = HTMLReporter(results)
    
    if output_path:
        reporter.save(output_path)
    
    return reporter.generate()


if __name__ == "__main__":
    # Test with sample data
    sample_results = {
        "target": "example.com",
        "results": {
            "nmap": {
                "open_ports": [
                    {"port": "80/tcp", "service": "http", "version": "nginx 1.18"},
                    {"port": "443/tcp", "service": "https", "version": "nginx 1.18"},
                    {"port": "22/tcp", "service": "ssh", "version": "OpenSSH 8.2"},
                ],
                "os": "Linux 5.x"
            },
            "sqlmap": {
                "vulnerable": False
            }
        }
    }
    
    reporter = HTMLReporter(sample_results)
    print(reporter.generate()[:2000])