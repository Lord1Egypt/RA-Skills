#!/usr/bin/env python3
"""
安全报告生成脚本
整合所有检测结果，生成结构化安全报告
"""

import json
import os
from datetime import datetime


def generate_html_report(results, output_path='security_report.html'):
    """生成 HTML 格式报告"""
    
    html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>安全检测报告</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        .header h1 { margin: 0; font-size: 24px; }
        .header .meta { margin-top: 10px; opacity: 0.9; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        .summary-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .summary-card .value { font-size: 32px; font-weight: bold; }
        .summary-card .label { color: #666; margin-top: 5px; }
        .summary-card.high .value { color: #e74c3c; }
        .summary-card.medium .value { color: #f39c12; }
        .summary-card.low .value { color: #27ae60; }
        .section { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .section h2 { margin-top: 0; color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
        .issue { padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid; }
        .issue.high { background: #ffebee; border-color: #e74c3c; }
        .issue.medium { background: #fff8e1; border-color: #f39c12; }
        .issue.low { background: #e8f5e9; border-color: #27ae60; }
        .issue-title { font-weight: bold; margin-bottom: 5px; }
        .issue-desc { color: #666; }
        .recommendation { background: #e3f2fd; padding: 15px; border-radius: 5px; margin-top: 10px; }
        .recommendation h3 { margin-top: 0; color: #1976d2; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; font-weight: 600; }
        .risk-badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
        .risk-high { background: #e74c3c; color: white; }
        .risk-medium { background: #f39c12; color: white; }
        .risk-low { background: #27ae60; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 安全检测报告</h1>
        <div class="meta">
            <div>检测时间: {timestamp}</div>
            <div>目标主机: {target}</div>
        </div>
    </div>
    
    <div class="summary">
        <div class="summary-card high">
            <div class="value">{high_risk}</div>
            <div class="label">🔴 高危问题</div>
        </div>
        <div class="summary-card medium">
            <div class="value">{medium_risk}</div>
            <div class="label">🟡 中危问题</div>
        </div>
        <div class="summary-card low">
            <div class="value">{low_risk}</div>
            <div class="label">🟢 低危问题</div>
        </div>
        <div class="summary-card">
            <div class="value">{total_ports}</div>
            <div class="label">开放端口</div>
        </div>
    </div>
    
    <div class="section">
        <h2>📋 端口扫描结果</h2>
        <table>
            <thead>
                <tr>
                    <th>端口</th>
                    <th>服务</th>
                    <th>风险等级</th>
                    <th>建议</th>
                </tr>
            </thead>
            <tbody>
                {port_rows}
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>⚠️ 发现的问题</h2>
        {issues_html}
    </div>
    
    <div class="section">
        <div class="recommendation">
            <h3>💡 修复建议</h3>
            <ol>
                <li>关闭不必要的服务端口</li>
                <li>使用强密码或密钥认证</li>
                <li>限制数据库服务仅本地访问</li>
                <li>启用防火墙规则</li>
                <li>定期进行安全检测和更新</li>
            </ol>
        </div>
    </div>
    
    <div class="section">
        <p style="color: #999; font-size: 12px; text-align: center;">
            本报告由 Net-Vuln-Scan 自动生成 | 仅用于授权的安全检测
        </p>
    </div>
</body>
</html>
"""
    
    # 计算统计
    high_risk = len([r for r in results.get('ports', []) if r.get('risk_level') in ['极高', '高']])
    medium_risk = len([r for r in results.get('ports', []) if r.get('risk_level') == '中'])
    low_risk = len([r for r in results.get('ports', []) if r.get('risk_level') == '低'])
    total_ports = len(results.get('ports', []))
    
    # 生成端口表格
    port_rows = ""
    for port in results.get('ports', []):
        risk_class = port.get('risk_level', '低')
        risk_badge_class = 'high' if risk_class in ['极高', '高'] else ('medium' if risk_class == '中' else 'low')
        port_rows += f"""
            <tr>
                <td>{port.get('port')}/tcp</td>
                <td>{port.get('service')}</td>
                <td><span class="risk-badge risk-{risk_badge_class}">{risk_class}</span></td>
                <td>{port.get('recommendation', '-')}</td>
            </tr>
        """
    
    # 生成问题列表
    issues_html = ""
    for issue in results.get('issues', []):
        issue_class = 'high' if issue.get('risk') in ['极高', '高'] else ('medium' if issue.get('risk') == '中' else 'low')
        issues_html += f"""
            <div class="issue {issue_class}">
                <div class="issue-title">{issue.get('title')}</div>
                <div class="issue-desc">{issue.get('description')}</div>
            </div>
        """
    
    # 填充模板
    html = html_template.format(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        target=results.get('target', 'localhost'),
        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk,
        total_ports=total_ports,
        port_rows=port_rows,
        issues_html=issues_html if issues_html else '<p style="color: #27ae60;">✅ 未发现严重安全问题</p>'
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_path


def generate_json_report(results, output_path='security_report.json'):
    """生成 JSON 格式报告"""
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'target': results.get('target'),
        'summary': {
            'high_risk': len([r for r in results.get('ports', []) if r.get('risk_level') in ['极高', '高']]),
            'medium_risk': len([r for r in results.get('ports', []) if r.get('risk_level') == '中']),
            'low_risk': len([r for r in results.get('ports', []) if r.get('risk_level') == '低']),
            'total_open_ports': len(results.get('ports', []))
        },
        'ports': results.get('ports', []),
        'issues': results.get('issues', []),
        'ssl': results.get('ssl', {}),
        'weakpass': results.get('weakpass', [])
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return output_path


def main():
    if len(sys.argv) < 2:
        print("用法: python report_gen.py <检测结果文件.json>")
        print("示例: python report_gen.py scan_results.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"错误: 文件 {input_file} 不存在")
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # 生成报告
    html_path = generate_html_report(results, 'security_report.html')
    json_path = generate_json_report(results, 'security_report.json')
    
    print(f"\n报告生成完成:")
    print(f"  - HTML 报告: {html_path}")
    print(f"  - JSON 报告: {json_path}")


if __name__ == '__main__':
    import sys
    main()
