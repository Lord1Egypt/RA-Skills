#!/usr/bin/env python3
"""
LLM Interactive Scanner
允许用户通过自然语言与扫描器对话
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime


class LLMScannerInterface:
    """Interactive LLM-based security scanner interface."""
    
    def __init__(self, scan_function):
        """
        Initialize LLM scanner interface.
        
        Args:
            scan_function: The actual scan function to call
        """
        self.scan_function = scan_function
        self.conversation_history = []
        self.current_target = None
        self.last_scan_results = None
    
    def process_message(self, message: str) -> str:
        """
        Process user message and return response.
        
        Args:
            message: User's natural language message
            
        Returns:
            Response text
        """
        message_lower = message.lower()
        
        # Detect intent
        intent = self._detect_intent(message)
        
        # Handle different intents
        if intent == "scan":
            return self._handle_scan_request(message)
        elif intent == "quick_scan":
            return self._handle_quick_scan()
        elif intent == "set_target":
            return self._handle_set_target(message)
        elif intent == "get_results":
            return self._handle_get_results()
        elif intent == "vulnerability_summary":
            return self._handle_vulnerability_summary()
        elif intent == "recommendations":
            return self._handle_recommendations()
        elif intent == "help":
            return self._handle_help()
        elif intent == "status":
            return self._handle_status()
        elif intent == "export":
            return self._handle_export(message)
        else:
            return self._handle_general_chat(message)
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message."""
        message_lower = message.lower()
        
        # Scan intents
        if any(kw in message_lower for kw in ["扫描", "scan", "检查", "检测", "开始"]):
            if any(kw in message_lower for kw in ["快速", "quick", "简单"]):
                return "quick_scan"
            return "scan"
        
        # Target setting
        if any(kw in message_lower for kw in ["目标", "target", "扫描", "scan", "设置"]):
            if any(kw in message_lower for kw in ["http", "www", ".com", ".cn", ".org", ".net", "ip", "地址"]):
                return "set_target"
        
        # Results
        if any(kw in message_lower for kw in ["结果", "result", "报告", "report", "发现"]):
            return "get_results"
        
        # Vulnerabilities
        if any(kw in message_lower for kw in ["漏洞", "vulnerab", "问题", "风险", "危险"]):
            return "vulnerability_summary"
        
        # Recommendations
        if any(kw in message_lower for kw in ["建议", "修复", "解决", "怎么办", "recommend"]):
            return "recommendations"
        
        # Help
        if any(kw in message_lower for kw in ["帮助", "help", "怎么用", "说明", "指南"]):
            return "help"
        
        # Status
        if any(kw in message_lower for kw in ["状态", "status", "进度", "进度", "在哪"]):
            return "status"
        
        # Export
        if any(kw in message_lower for kw in ["导出", "export", "保存", "下载", "html", "pdf"]):
            return "export"
        
        return "general"
    
    def _handle_scan_request(self, message: str) -> str:
        """Handle scan request with options parsing."""
        if not self.current_target:
            return """❌ 尚未设置扫描目标。

请提供目标地址，例如：
- "扫描 example.com"
- "设置目标 192.168.1.1"
- "扫描 https://target.com"""
        
        # Parse options from message
        options = self._parse_scan_options(message)
        
        response = f"""🚀 开始扫描目标: {self.current_target}

📋 扫描配置:
- 端口扫描 (nmap): {'✅' if options.get('nmap', True) else '❌'}
- Web漏洞 (nikto): {'✅' if options.get('nikto', True) else '❌'}
- SQL注入 (sqlmap): {'✅' if options.get('sqlmap', False) else '❌'}
- 依赖检查 (trivy): {'✅' if options.get('trivy', False) else '❌'}
- 系统加固 (lynis): {'✅' if options.get('lynis', False) else '❌'}

⏳ 扫描进行中，请稍候..."""
        
        return response
    
    def _handle_quick_scan(self) -> str:
        """Handle quick scan request."""
        if not self.current_target:
            return "❌ 请先设置扫描目标，例如：\"扫描 example.com\""
        
        return f"""⚡ 快速扫描: {self.current_target}

将执行以下检查：
1. 🔍 端口扫描 (常用端口)
2. 🕷️ Web基础漏洞检查
3. 📊 生成简要报告

预计耗时: 30-60秒"""
    
    def _handle_set_target(self, message: str) -> str:
        """Handle target setting."""
        import re
        
        # Extract URL/IP from message
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        domain_pattern = r'\b[a-zA-Z0-9][-a-zA-Z0-9]*\.[a-zA-Z]{2,}\b'
        
        # Try to find target
        urls = re.findall(url_pattern, message)
        ips = re.findall(ip_pattern, message)
        domains = re.findall(domain_pattern, message)
        
        target = None
        if urls:
            target = urls[0]
        elif ips:
            target = ips[0]
        elif domains:
            target = domains[0]
        
        if target:
            self.current_target = target
            return f"""✅ 扫描目标已设置: {target}

可用命令:
- "开始扫描" 或 "scan" - 执行完整扫描
- "快速扫描" - 执行快速检查
- "扫描并检查SQL注入" - 包含SQL注入检测
- "导出HTML报告" - 生成HTML报告"""
        else:
            return """❌ 无法识别目标地址。

请使用以下格式：
- "设置目标 example.com"
- "扫描 https://target.com"
- "检查 192.168.1.1"""
    
    def _handle_get_results(self) -> str:
        """Handle results request."""
        if not self.last_scan_results:
            return "❌ 暂无扫描结果。请先执行扫描。"
        
        summary = self._generate_summary(self.last_scan_results)
        return summary
    
    def _handle_vulnerability_summary(self) -> str:
        """Handle vulnerability summary request."""
        if not self.last_scan_results:
            return "❌ 暂无扫描结果。请先执行扫描。"
        
        vulns = self._extract_vulnerabilities(self.last_scan_results)
        
        if not vulns:
            return """✅ 未发现明显漏洞！

系统当前状态良好，但仍建议：
- 定期执行安全扫描
- 保持系统更新
- 监控异常访问"""
        
        response = f"""🚨 发现 {len(vulns)} 个安全问题：

"""
        for i, vuln in enumerate(vulns[:10], 1):
            severity = vuln.get('severity', 'UNKNOWN')
            emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🔵'}.get(severity, '⚪')
            response += f"{i}. {emoji} [{severity}] {vuln.get('title', 'Unknown')}\n"
        
        if len(vulns) > 10:
            response += f"\n... 还有 {len(vulns) - 10} 个问题"
        
        response += "\n\n输入 \"修复建议\" 查看详细解决方案。"
        return response
    
    def _handle_recommendations(self) -> str:
        """Handle recommendations request."""
        if not self.last_scan_results:
            return "❌ 暂无扫描结果。请先执行扫描。"
        
        vulns = self._extract_vulnerabilities(self.last_scan_results)
        
        if not vulns:
            return """💡 安全建议：

1. **定期扫描**: 建议每周执行一次安全扫描
2. **更新系统**: 及时应用安全补丁
3. **访问控制**: 实施最小权限原则
4. **日志监控**: 启用并定期检查系统日志
5. **备份策略**: 定期备份重要数据"""
        
        response = """🔧 修复建议：

"""
        
        # SQL Injection
        if any('sql' in v.get('title', '').lower() for v in vulns):
            response += """**SQL注入漏洞修复：**
- 使用参数化查询/预处理语句
- 输入验证和过滤
- 使用ORM框架
- 最小权限数据库账户
- 部署WAF防护

"""
        
        # Open ports
        nmap_result = self.last_scan_results.get('results', {}).get('nmap', {})
        open_ports = nmap_result.get('open_ports', [])
        if len(open_ports) > 10:
            response += f"""**开放端口过多：**
- 当前开放 {len(open_ports)} 个端口
- 建议关闭不必要的服务
- 使用防火墙限制访问

"""
        
        response += """**一般安全建议：**
- 及时更新所有软件组件
- 实施强密码策略
- 启用双因素认证
- 定期安全审计"""
        
        return response
    
    def _handle_help(self) -> str:
        """Handle help request."""
        return """🤖 LLM 安全扫描助手 - 使用指南

**基本命令：**
- "扫描 example.com" - 设置目标并开始扫描
- "快速扫描" - 执行快速安全检查
- "查看结果" - 显示扫描结果摘要
- "发现什么漏洞" - 列出发现的漏洞
- "修复建议" - 获取修复方案

**高级用法：**
- "扫描并检查SQL注入" - 包含SQL注入检测
- "扫描系统加固" - 包含Lynis系统检查
- "导出HTML报告" - 生成HTML格式报告
- "导出 /path/to/report.html" - 指定导出路径

**提示：**
可以直接用自然语言描述你的需求，我会尽力理解并执行。"""
    
    def _handle_status(self) -> str:
        """Handle status request."""
        status = []
        
        if self.current_target:
            status.append(f"📍 当前目标: {self.current_target}")
        else:
            status.append("📍 当前目标: 未设置")
        
        if self.last_scan_results:
            status.append("📊 扫描状态: 已完成")
            scan_time = self.last_scan_results.get('scan_time', '未知')
            status.append(f"🕐 扫描时间: {scan_time}")
        else:
            status.append("📊 扫描状态: 未执行")
        
        return "\n".join(status)
    
    def _handle_export(self, message: str) -> str:
        """Handle export request."""
        if not self.last_scan_results:
            return "❌ 暂无扫描结果可导出。请先执行扫描。"
        
        # Try to extract path
        import re
        path_pattern = r'/[\w/.-]+\.(html|json|md)'
        paths = re.findall(path_pattern, message)
        
        if paths:
            output_path = paths[0]
        else:
            output_path = f"/tmp/scan_report_{int(datetime.now().timestamp())}.html"
        
        return f"""📄 导出报告

将生成HTML格式报告到：
{output_path}

报告将包含：
- 执行摘要和安全评分
- 详细扫描结果
- 发现的漏洞列表
- 修复建议

导出完成后可使用 <qqfile>{output_path}</qqfile> 下载。"""
    
    def _handle_general_chat(self, message: str) -> str:
        """Handle general conversation."""
        greetings = ["你好", "hello", "hi", "hey"]
        if any(g in message.lower() for g in greetings):
            if self.current_target:
                return f"""你好！我已准备好扫描 {self.current_target}。

需要我做什么？
- 输入 "开始扫描" 执行扫描
- 输入 "帮助" 查看所有命令"""
            else:
                return """你好！我是安全扫描助手。

请告诉我需要扫描的目标，例如：
- "扫描 example.com"
- "检查 192.168.1.1"
- "扫描 https://target.com"""
        
        return """我不太确定你的意思。可以尝试以下命令：

- "扫描 [目标地址]" - 开始扫描
- "快速扫描" - 快速安全检查
- "查看结果" - 查看扫描结果
- "帮助" - 显示完整帮助

或直接输入目标地址，我会自动识别。"""
    
    def _parse_scan_options(self, message: str) -> Dict[str, bool]:
        """Parse scan options from message."""
        message_lower = message.lower()
        
        options = {
            'nmap': True,      # Always enabled by default
            'nikto': True,     # Always enabled by default
            'sqlmap': False,   # Only if explicitly requested
            'trivy': False,    # Only for local targets
            'lynis': False,    # Only for local targets
        }
        
        # Check for SQL injection request
        if any(kw in message_lower for kw in ['sql', '注入', 'injection']):
            options['sqlmap'] = True
        
        # Check for dependency scan
        if any(kw in message_lower for kw in ['依赖', 'dependency', 'trivy', '包']):
            options['trivy'] = True
        
        # Check for system hardening
        if any(kw in message_lower for kw in ['系统', '加固', 'lynis', 'hardening', '配置']):
            options['lynis'] = True
        
        # Quick scan disables some options
        if any(kw in message_lower for kw in ['快速', 'quick', '简单']):
            options['sqlmap'] = False
            options['trivy'] = False
            options['lynis'] = False
        
        return options
    
    def _generate_summary(self, results: Dict) -> str:
        """Generate text summary of results."""
        target = results.get('target', 'Unknown')
        scan_results = results.get('results', {})
        
        summary = f"""📊 扫描结果摘要: {target}

"""
        
        # Count vulnerabilities
        total_vulns = 0
        for tool, result in scan_results.items():
            if result.get('vulnerable'):
                total_vulns += 1
            if result.get('vulnerabilities'):
                total_vulns += len(result['vulnerabilities'])
        
        if total_vulns == 0:
            summary += "✅ 未发现安全问题\n\n"
        else:
            summary += f"⚠️ 发现 {total_vulns} 个安全问题\n\n"
        
        # Tool-specific summaries
        for tool, result in scan_results.items():
            if tool == 'nmap':
                open_ports = result.get('open_ports', [])
                summary += f"🔍 Nmap: 发现 {len(open_ports)} 个开放端口\n"
            elif tool == 'nikto':
                items = result.get('items', [])
                summary += f"🕷️ Nikto: 发现 {len(items)} 个Web问题\n"
            elif tool == 'sqlmap':
                if result.get('vulnerable'):
                    summary += "💉 SQLMap: 🚨 发现SQL注入漏洞!\n"
                else:
                    summary += "💉 SQLMap: ✅ 未发现注入漏洞\n"
            elif tool == 'trivy':
                vulns = result.get('vulnerabilities', [])
                summary += f"📦 Trivy: 发现 {len(vulns)} 个依赖漏洞\n"
            elif tool == 'lynis':
                score = result.get('hardening_index', 'N/A')
                summary += f"🔧 Lynis: 加固指数 {score}/100\n"
        
        summary += "\n输入 \"详细结果\" 查看完整报告。"
        return summary
    
    def _extract_vulnerabilities(self, results: Dict) -> List[Dict]:
        """Extract all vulnerabilities from results."""
        vulns = []
        scan_results = results.get('results', {})
        
        for tool, result in scan_results.items():
            # Direct vulnerabilities list
            if 'vulnerabilities' in result:
                for v in result['vulnerabilities']:
                    v['source'] = tool
                    vulns.append(v)
            
            # Tool-specific vulnerability indicators
            if tool == 'sqlmap' and result.get('vulnerable'):
                vulns.append({
                    'title': 'SQL Injection Vulnerability',
                    'severity': 'CRITICAL',
                    'source': tool,
                    'description': f"注入点: {', '.join(result.get('injection_points', []))}"
                })
            
            if tool == 'nikto':
                for item in result.get('items', []):
                    vulns.append({
                        'title': item.get('finding', 'Web Issue'),
                        'severity': item.get('severity', 'MEDIUM'),
                        'source': tool
                    })
        
        # Sort by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'INFO': 4}
        vulns.sort(key=lambda x: severity_order.get(x.get('severity', 'INFO'), 5))
        
        return vulns
    
    def update_results(self, results: Dict):
        """Update scan results."""
        self.last_scan_results = results
        results['scan_time'] = datetime.now().isoformat()


def interactive_scan_mode(scan_function):
    """
    Decorator/Wrapper to enable LLM interactive mode.
    
    Usage:
        @interactive_scan_mode
        def run_scan(target, tools=None):
            # Original scan logic
            pass
    """
    interface = LLMScannerInterface(scan_function)
    return interface


# For testing
if __name__ == "__main__":
    # Simulate scan function
    def dummy_scan(target, tools=None):
        return {"target": target, "results": {}}
    
    interface = LLMScannerInterface(dummy_scan)
    
    # Test conversations
    test_messages = [
        "你好",
        "扫描 example.com",
        "开始扫描",
        "查看结果",
        "发现什么漏洞",
        "修复建议",
        "导出报告"
    ]
    
    for msg in test_messages:
        print(f"\nUser: {msg}")
        print(f"Bot: {interface.process_message(msg)}")