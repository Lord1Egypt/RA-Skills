#!/usr/bin/env python3
"""
OpenClaw Security Auditor - Report Generator
This script generates security audit reports in multiple formats.
"""

import json
from pathlib import Path
from typing import Dict, Any

def generate_security_report(scan_results: Dict[str, Any], format: str = "bilingual") -> str:
    """
    Generate security report from scan results
    
    Args:
        scan_results: Dictionary containing scan results from security_scanner.py
        format: Report format - "bilingual", "markdown", "json", or "html"
    
    Returns:
        Formatted report as string
    """
    if format == "json":
        return json.dumps(scan_results, indent=2, ensure_ascii=False)
    
    elif format == "bilingual":
        return _generate_bilingual_markdown(scan_results)
    
    elif format == "markdown":
        return _generate_markdown(scan_results)
    
    elif format == "html":
        return _generate_html(scan_results)
    
    else:
        raise ValueError(f"Unsupported format: {format}")

def _generate_bilingual_markdown(results: Dict[str, Any]) -> str:
    """Generate bilingual Markdown report"""
    # Security level translations
    level_translations = {
        "excellent": {"en": "Excellent 🟢", "zh": "优秀 🟢"},
        "good": {"en": "Good 🟡", "zh": "良好 🟡"},
        "fair": {"en": "Fair 🟠", "zh": "中等 🟠"},
        "at_risk": {"en": "At Risk 🔴", "zh": "风险 🔴"},
        "critical": {"en": "Critical ⚫", "zh": "危险 ⚫"}
    }
    
    security_level = results.get("security_level", "critical")
    level_en = level_translations.get(security_level, {}).get("en", "Unknown")
    level_zh = level_translations.get(security_level, {}).get("zh", "未知")
    
    report = f"""# OpenClaw Security Audit Report / OpenClaw 安全审计报告

## 📊 Overview / 概览
- **Security Score / 安全评分**: {results['score']}/100 ({level_en})
- **安全等级 / Security Level**: {level_zh}
- **Scan Time / 扫描时间**: {results.get('timestamp', 'N/A')}
- **Configuration File / 配置文件**: `{results['config_path']}`
- **Security Mode / 安全模式**: {results['mode']}

## 📋 Summary / 摘要
- **Total Checks / 总检查项**: {results['total_checks']}
- **Passed / 通过**: {results['passed_checks']}
- **Issues Found / 发现问题**: {len(results['issues'])}

"""
    
    # Issue breakdown by severity
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for issue in results['issues']:
        severity = issue.get('severity', 'info')
        if severity in severity_counts:
            severity_counts[severity] += 1
    
    report += f"""### Issue Breakdown / 问题分类
- 🔴 Critical / 严重: {severity_counts['critical']}
- 🟠 High / 高: {severity_counts['high']}  
- 🟡 Medium / 中: {severity_counts['medium']}
- 🟢 Low / 低: {severity_counts['low']}
- ℹ️ Info / 提示: {severity_counts['info']}

"""
    
    # Group issues by severity
    severity_order = ['critical', 'high', 'medium', 'low', 'info']
    severity_emojis = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢', 'info': 'ℹ️'}
    
    for severity in severity_order:
        severity_issues = [issue for issue in results['issues'] if issue.get('severity') == severity]
        if severity_issues:
            for issue in severity_issues:
                title_en = issue.get('title', 'Unknown issue')
                title_zh = issue.get('title_zh', title_en)
                desc_en = issue.get('description', 'No description')
                desc_zh = issue.get('description_zh', desc_en)
                risk_en = issue.get('risk', 'Unknown risk')
                risk_zh = issue.get('risk_zh', risk_en)
                
                report += f"""### {title_en} / {title_zh}

- **Description / 描述**: {desc_en}
- **描述**: {desc_zh}
- **Risk / 风险**: {risk_en}
- **风险**: {risk_zh}
- **Current Value / 当前值**: `{issue.get('current_value', 'N/A')}`
- **Recommended Value / 推荐值**: `{issue.get('recommended_value', 'N/A')}`
- **Fix Command / 修复命令**: `{issue.get('fix_command', 'N/A')}`

"""
    
    # Recommendations
    report += f"""
## 💡 Security Mode Recommendations / 安全模式建议

Based on your current configuration, we recommend applying the **{results['mode'].title()} mode** profile.
根据您当前的配置，我们建议应用 **{results['mode'].title()} 模式** 配置文件。

### Conservative Mode (Strict) / 保守模式（严格）
For production environments and sensitive deployments
适用于生产环境和敏感部署
```bash
# Apply conservative security profile
python3 security_scanner.py --mode conservative
```

### Balanced Mode (Recommended) / 平衡模式（推荐）  
For personal development and small teams
适用于个人开发和小型团队
```bash
# Apply balanced security profile (recommended)
python3 security_scanner.py --mode balanced
```

### Aggressive Mode (Permissive) / 激进模式（宽松）
For isolated test environments only
仅适用于隔离的测试环境
```bash
# Apply aggressive security profile
python3 security_scanner.py --mode aggressive
```

## 📚 References / 参考资料
- [OpenClaw Security Documentation](https://docs.openclaw.ai/security)
- [OpenClaw 安全文档](https://docs.openclaw.ai/security)
- [Security Best Practices Guide](https://docs.openclaw.ai/best-practices)
- [安全最佳实践指南](https://docs.openclaw.ai/best-practices)

---
*Generated by OpenClaw Security Auditor*
*由 OpenClaw 安全审计器生成*
"""
    
    return report

def _generate_markdown(results: Dict[str, Any]) -> str:
    """Generate English-only Markdown report"""
    # Similar to bilingual but English only
    level_translations = {
        "excellent": "Excellent 🟢",
        "good": "Good 🟡", 
        "fair": "Fair 🟠",
        "at_risk": "At Risk 🔴",
        "critical": "Critical ⚫"
    }
    
    security_level = results.get("security_level", "critical")
    level_display = level_translations.get(security_level, "Unknown")
    
    report = f"""# OpenClaw Security Audit Report

## 📊 Overview
- **Security Score**: {results['score']}/100 ({level_display})
- **Scan Time**: {results.get('timestamp', 'N/A')}
- **Configuration File**: `{results['config_path']}`
- **Security Mode**: {results['mode']}

## 📋 Summary
- **Total Checks**: {results['total_checks']}
- **Passed**: {results['passed_checks']}
- **Issues Found**: {len(results['issues'])}

"""
    
    # Issue breakdown
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for issue in results['issues']:
        severity = issue.get('severity', 'info')
        if severity in severity_counts:
            severity_counts[severity] += 1
    
    report += f"""### Issue Breakdown
- 🔴 Critical: {severity_counts['critical']}
- 🟠 High: {severity_counts['high']}  
- 🟡 Medium: {severity_counts['medium']}
- 🟢 Low: {severity_counts['low']}
- ℹ️ Info: {severity_counts['info']}

"""
    
    # Issues
    severity_order = ['critical', 'high', 'medium', 'low', 'info']
    severity_emojis = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢', 'info': 'ℹ️'}
    
    for severity in severity_order:
        severity_issues = [issue for issue in results['issues'] if issue.get('severity') == severity]
        if severity_issues:
            for issue in severity_issues:
                report += f"""### {issue.get('title', 'Unknown issue')}

- **Description**: {issue.get('description', 'No description')}
- **Risk**: {issue.get('risk', 'Unknown risk')}
- **Current Value**: `{issue.get('current_value', 'N/A')}`
- **Recommended Value**: `{issue.get('recommended_value', 'N/A')}`
- **Fix Command**: `{issue.get('fix_command', 'N/A')}`

"""
    
    return report

def _generate_html(results: Dict[str, Any]) -> str:
    """Generate HTML report"""
    # Basic HTML template
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>OpenClaw Security Audit Report</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
        .score-excellent {{ color: #22c55e; font-weight: bold; }}
        .score-good {{ color: #84cc16; font-weight: bold; }}
        .score-fair {{ color: #f59e0b; font-weight: bold; }}
        .score-risk {{ color: #ef4444; font-weight: bold; }}
        .score-critical {{ color: #7f1d1d; font-weight: bold; }}
        .issue {{ margin: 20px 0; padding: 15px; border-left: 4px solid #ccc; }}
        .critical {{ border-left-color: #ef4444; }}
        .high {{ border-left-color: #f97316; }}
        .medium {{ border-left-color: #eab308; }}
        .low {{ border-left-color: #22c55e; }}
        .info {{ border-left-color: #64748b; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>OpenClaw Security Audit Report</h1>
        <p><strong>Security Score:</strong> <span class="score-{results.get('security_level', 'critical')}">{results['score']}/100</span></p>
        <p><strong>Configuration File:</strong> {results['config_path']}</p>
        <p><strong>Security Mode:</strong> {results['mode']}</p>
    </div>
    
    <h2>Summary</h2>
    <p>Total Checks: {results['total_checks']}</p>
    <p>Passed: {results['passed_checks']}</p>
    <p>Issues Found: {len(results['issues'])}</p>
"""
    
    # Add issues
    for issue in results['issues']:
        severity = issue.get('severity', 'info')
        html += f"""
    <div class="issue {severity}">
        <h3>{issue.get('title', 'Unknown issue')}</h3>
        <p><strong>Description:</strong> {issue.get('description', 'No description')}</p>
        <p><strong>Risk:</strong> {issue.get('risk', 'Unknown risk')}</p>
        <p><strong>Current Value:</strong> {issue.get('current_value', 'N/A')}</p>
        <p><strong>Recommended Value:</strong> {issue.get('recommended_value', 'N/A')}</p>
        <p><strong>Fix Command:</strong> <code>{issue.get('fix_command', 'N/A')}</code></p>
    </div>
"""
    
    html += """
</body>
</html>"""
    
    return html

def main():
    """Command line interface for report generation"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="OpenClaw Security Report Generator")
    parser.add_argument("--input", "-i", required=True, help="Input JSON scan results file")
    parser.add_argument("--format", "-f", default="bilingual", 
                       choices=["bilingual", "markdown", "json", "html"],
                       help="Output format")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    
    args = parser.parse_args()
    
    # Load scan results
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            scan_results = json.load(f)
    except Exception as e:
        print(f"Error loading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Generate report
    try:
        report = generate_security_report(scan_results, args.format)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report generated: {args.output}")
    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()