#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巡检报告生成器

提供统一的报告生成功能，包括：
- 各独立巡检工具的单独报告
- 汇总巡检报告
- HTML格式报告
"""

import time
import json
from datetime import datetime, timezone
from typing import Dict, Any, List


def generate_sub_inspection_report(check_name: str, check_data: dict, issues: list, 
                                    inspection_time: str = None) -> dict:
    """生成单个巡检项的详细报告
    
    Args:
        check_name: 巡检项名称
        check_data: 巡检结果数据
        issues: 问题列表
        inspection_time: 巡检时间
    
    Returns:
        包含详细报告的字典
    """
    report = {
        "inspection_name": check_data.get("name", check_name),
        "inspection_time": inspection_time or time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "status": check_data.get("status", "UNKNOWN"),
        "checked": check_data.get("checked", False),
        "summary": {},
        "details": {},
        "issues": issues,
        "recommendations": []
    }
    
    # 根据不同的巡检类型生成详细报告
    if check_name == "pods" or check_name == "pod_status":
        report["summary"] = {
            "total_pods": check_data.get("total", 0),
            "running": check_data.get("running", 0),
            "pending": check_data.get("pending", 0),
            "failed": check_data.get("failed", 0),
            "restart_pod_count": len(check_data.get("restart_pods", [])),
            "abnormal_pod_count": len(check_data.get("abnormal_pods", []))
        }
        report["details"] = {
            "restart_pods": check_data.get("restart_pods", []),
            "abnormal_pods": check_data.get("abnormal_pods", []),
            "abnormal_summary": check_data.get("abnormal_summary", {})
        }
        if check_data.get("restart_pods"):
            for pod in check_data["restart_pods"]:
                report["recommendations"].append({
                    "target": pod.get("pod"),
                    "issue": f"容器 {pod.get('container')} 重启 {pod.get('restart_count')} 次",
                    "suggestion": "检查应用日志，确认容器退出原因；检查健康检查配置是否正确；确认应用是否有资源瓶颈"
                })
    
    elif check_name == "nodes" or check_name == "node_status":
        report["summary"] = {
            "total_nodes": check_data.get("total", 0),
            "ready": check_data.get("ready", 0),
            "not_ready": check_data.get("not_ready", 0),
            "abnormal_count": len(check_data.get("abnormal_nodes", []))
        }
        report["details"] = {
            "node_details": check_data.get("node_details", []),
            "abnormal_nodes": check_data.get("abnormal_nodes", [])
        }
        if check_data.get("abnormal_nodes"):
            for node in check_data["abnormal_nodes"]:
                report["recommendations"].append({
                    "target": node.get("name"),
                    "issue": f"节点状态异常: {node.get('status')}",
                    "suggestion": node.get("reason", "检查节点网络、kubelet服务状态，必要时重启节点或重新加入集群")
                })
    
    elif check_name == "addon_pod_monitoring":
        report["summary"] = {
            "namespaces": check_data.get("namespaces", []),
            "high_cpu_count": check_data.get("high_cpu_count", 0),
            "high_memory_count": check_data.get("high_memory_count", 0)
        }
        report["details"] = {
            "high_cpu_pods": check_data.get("high_cpu_pods_top10", []),
            "high_memory_pods": check_data.get("high_memory_pods_top10", [])
        }
        for pod in check_data.get("high_cpu_pods_top10", []):
            report["recommendations"].append({
                "target": f"{pod.get('namespace')}/{pod.get('pod')}",
                "issue": f"CPU使用率 {pod.get('cpu_usage_percent')}%",
                "suggestion": "考虑增加CPU资源限制或优化应用性能"
            })
    
    elif check_name == "biz_pod_monitoring":
        report["summary"] = {
            "namespaces": check_data.get("namespaces", []),
            "high_cpu_count": check_data.get("high_cpu_count", 0),
            "high_memory_count": check_data.get("high_memory_count", 0)
        }
        report["details"] = {
            "high_cpu_pods": check_data.get("high_cpu_pods_top10", []),
            "high_memory_pods": check_data.get("high_memory_pods_top10", []),
            "monitoring_curves": check_data.get("monitoring_curves", {})
        }
        for pod in check_data.get("high_cpu_pods_top10", []):
            report["recommendations"].append({
                "target": f"{pod.get('namespace')}/{pod.get('pod')}",
                "issue": f"CPU使用率 {pod.get('cpu_usage_percent')}%",
                "suggestion": "考虑增加CPU资源限制、水平扩展副本数或优化应用性能"
            })
    
    elif check_name == "node_monitoring" or check_name == "node_resource":
        report["summary"] = {
            "high_cpu_count": check_data.get("high_cpu_count", 0),
            "high_memory_count": check_data.get("high_memory_count", 0),
            "high_disk_count": check_data.get("high_disk_count", 0)
        }
        report["details"] = {
            "high_cpu_nodes": check_data.get("high_cpu_nodes_top10", []),
            "high_memory_nodes": check_data.get("high_memory_nodes_top10", []),
            "high_disk_nodes": check_data.get("high_disk_nodes_top10", []),
            "monitoring_curves": check_data.get("monitoring_curves", {})
        }
        for node in check_data.get("high_cpu_nodes_top10", []):
            report["recommendations"].append({
                "target": node.get("node_ip"),
                "issue": f"CPU使用率 {node.get('cpu_usage_percent')}%",
                "suggestion": "检查该节点上的Pod分布，考虑调度分散或扩容节点池"
            })
    
    elif check_name == "events":
        report["summary"] = {
            "total_events": check_data.get("total", 0),
            "normal_events": check_data.get("normal", 0),
            "warning_events": check_data.get("warning", 0),
            "critical_events_count": len(check_data.get("critical_events", []))
        }
        report["details"] = {
            "critical_events": check_data.get("critical_events", []),
            "events_by_reason": check_data.get("events_by_reason", {}),
            "events_by_namespace": check_data.get("events_by_namespace", {})
        }
    
    elif check_name == "alarms" or check_name == "aom_alarm":
        sb = check_data.get("severity_breakdown", {})
        report["summary"] = {
            "total_alarms": check_data.get("total", 0),
            "critical": sb.get("Critical", 0),
            "major": sb.get("Major", 0),
            "minor": sb.get("Minor", 0),
            "info": sb.get("Info", 0)
        }
        report["details"] = {
            "cluster_alarms": check_data.get("cluster_alarms", []),
            "alarms_by_type": check_data.get("alarms_by_type", {})
        }
        for alarm in check_data.get("cluster_alarms", []):
            if alarm.get("severity") in ["Critical", "Major"]:
                report["recommendations"].append({
                    "target": alarm.get("name"),
                    "issue": f"{alarm.get('severity')}级别告警",
                    "suggestion": "请及时处理该告警，避免影响业务"
                })
    
    elif check_name == "elb_monitoring":
        report["summary"] = {
            "total_loadbalancers": check_data.get("total_loadbalancers", 0),
            "high_connection_count": len(check_data.get("high_connection_usage_elbs", [])),
            "high_bandwidth_count": len(check_data.get("high_bandwidth_usage_elbs", [])),
            "eip_over_limit_count": len(check_data.get("high_bandwidth_eips", []))
        }
        report["details"] = {
            "loadbalancer_services": check_data.get("loadbalancer_services", []),
            "elb_metrics": check_data.get("elb_metrics", []),
            "high_connection_usage_elbs": check_data.get("high_connection_usage_elbs", []),
            "high_bandwidth_usage_elbs": check_data.get("high_bandwidth_usage_elbs", []),
            "high_bandwidth_eips": check_data.get("high_bandwidth_eips", [])
        }
        for elb in check_data.get("high_bandwidth_eips", []):
            report["recommendations"].append({
                "target": elb.get("public_ip"),
                "issue": f"EIP {'出' if elb.get('direction') == 'out' else '入'}带宽使用率 {elb.get('usage_percent')}%",
                "suggestion": "考虑增加EIP带宽或优化流量使用"
            })
    
    return report


def generate_summary_report(sub_reports: dict, cluster_id: str, region: str, 
                            inspection_time: str) -> dict:
    """生成汇总巡检报告
    
    Args:
        sub_reports: 各巡检子工具的报告
        cluster_id: 集群ID
        region: 区域
        inspection_time: 巡检时间
    
    Returns:
        汇总报告字典
    """
    total_issues = 0
    critical_issues = 0
    warning_issues = 0
    all_issues = []
    all_recommendations = []
    
    for check_name, report in sub_reports.items():
        issues = report.get("issues", [])
        for issue in issues:
            all_issues.append({
                "source": report.get("inspection_name"),
                **issue
            })
            if issue.get("severity") == "CRITICAL":
                critical_issues += 1
            else:
                warning_issues += 1
            total_issues += 1
        
        all_recommendations.extend(report.get("recommendations", []))
    
    # 确定总体状态
    if critical_issues > 0:
        overall_status = "CRITICAL"
    elif warning_issues > 0:
        overall_status = "WARNING"
    else:
        overall_status = "HEALTHY"
    
    summary_report = {
        "inspection_time": inspection_time,
        "cluster_id": cluster_id,
        "region": region,
        "overall_status": overall_status,
        "total_issues": total_issues,
        "critical_issues": critical_issues,
        "warning_issues": warning_issues,
        "sub_reports": sub_reports,
        "all_issues": all_issues,
        "all_recommendations": all_recommendations
    }
    
    return summary_report


def generate_detailed_html_report(summary_report: dict) -> str:
    """生成详细的HTML格式汇总报告
    
    Args:
        summary_report: 汇总报告数据
    
    Returns:
        HTML格式报告字符串
    """
    status = summary_report.get("overall_status", "UNKNOWN")
    status_class = status.lower()
    status_icons = {"HEALTHY": "✅", "WARNING": "⚠️", "CRITICAL": "❌"}
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CCE集群巡检详细报告</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; margin: 0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .status-badge {{ display: inline-block; padding: 10px 20px; border-radius: 20px; font-weight: 600; font-size: 18px; margin-top: 15px; }}
        .status-healthy {{ background: #d4edda; color: #155724; }}
        .status-warning {{ background: #fff3cd; color: #856404; }}
        .status-critical {{ background: #f8d7da; color: #721c24; }}
        .summary-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; }}
        .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .card h3 {{ font-size: 14px; color: #666; margin-bottom: 10px; }}
        .card .value {{ font-size: 36px; font-weight: 700; }}
        .card.critical .value {{ color: #dc3545; }}
        .card.warning .value {{ color: #ffc107; }}
        .card.healthy .value {{ color: #28a745; }}
        
        .section {{ background: white; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); overflow: hidden; }}
        .section-header {{ padding: 15px 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; cursor: pointer; }}
        .section-header:hover {{ background: #f8f9fa; }}
        .section-header h2 {{ font-size: 18px; margin: 0; display: flex; align-items: center; gap: 10px; }}
        .section-status {{ padding: 5px 12px; border-radius: 15px; font-size: 14px; font-weight: 600; }}
        .pass {{ background: #d4edda; color: #155724; }}
        .warn {{ background: #fff3cd; color: #856404; }}
        .fail {{ background: #f8d7da; color: #721c24; }}
        .skip {{ background: #e2e3e5; color: #383d41; }}
        .section-content {{ padding: 20px; }}
        .section-content.collapsed {{ display: none; }}
        
        .data-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 15px; }}
        .data-item {{ background: #f8f9fa; padding: 12px 15px; border-radius: 6px; }}
        .data-item label {{ font-size: 12px; color: #666; display: block; margin-bottom: 5px; }}
        .data-item .value {{ font-size: 18px; font-weight: 600; }}
        
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f9fa; font-weight: 600; }}
        tr:hover {{ background: #f8f9fa; }}
        
        .issue-item {{ background: #fff3cd; padding: 12px 15px; border-radius: 6px; margin-bottom: 10px; border-left: 4px solid #ffc107; }}
        .issue-item.critical {{ background: #f8d7da; border-left-color: #dc3545; }}
        .issue-item .severity {{ font-weight: 600; text-transform: uppercase; font-size: 12px; margin-bottom: 5px; }}
        .issue-item .severity.critical {{ color: #dc3545; }}
        .issue-item .severity.warning {{ color: #856404; }}
        .issue-item .message {{ font-size: 14px; }}
        
        .recommendation {{ background: #e7f3ff; padding: 12px 15px; border-radius: 6px; margin-bottom: 10px; border-left: 4px solid #0066cc; }}
        .recommendation .target {{ font-weight: 600; color: #0066cc; }}
        .recommendation .suggestion {{ margin-top: 5px; color: #333; }}
        
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; }}
        .toggle-icon {{ transition: transform 0.3s; }}
        .toggle-icon.collapsed {{ transform: rotate(-90deg); }}
        
        /* 监控图表样式 */
        .monitoring-charts {{
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        .chart-container {{
            margin-bottom: 30px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .chart-container h4 {{
            margin-top: 0;
            color: #667eea;
        }}
        .chart-container canvas {{
            max-height: 300px;
            width: 100% !important;
        }}
    </style>
    
    <!-- 引入 Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 CCE 集群巡检详细报告</h1>
            <p>集群ID: {summary_report.get('cluster_id')} | 区域: {summary_report.get('region')} | 巡检时间: {summary_report.get('inspection_time')}</p>
            <span class="status-badge status-{status_class}">
                {status_icons.get(status, '❓')} 巡检结果: {status}
            </span>
        </div>
        
        <div class="summary-cards">
            <div class="card {'critical' if summary_report.get('critical_issues', 0) > 0 else ''}">
                <h3>🚨 严重问题</h3>
                <div class="value">{summary_report.get('critical_issues', 0)}</div>
            </div>
            <div class="card {'warning' if summary_report.get('warning_issues', 0) > 0 else ''}">
                <h3>⚠️ 警告问题</h3>
                <div class="value">{summary_report.get('warning_issues', 0)}</div>
            </div>
            <div class="card">
                <h3>📋 总问题数</h3>
                <div class="value">{summary_report.get('total_issues', 0)}</div>
            </div>
            <div class="card healthy">
                <h3>🔍 巡检项数</h3>
                <div class="value">{len(summary_report.get('sub_reports', {}))}</div>
            </div>
        </div>
"""
    
    # 各巡检子工具详细报告
    sub_reports = summary_report.get("sub_reports", {})
    for check_name, report in sub_reports.items():
        status = report.get("status", "UNKNOWN")
        status_class = status.lower()
        checked = report.get("checked", False)
        
        html += f"""
        <div class="section">
            <div class="section-header" onclick="toggleSection('{check_name}')">
                <h2><span class="toggle-icon" id="icon-{check_name}">▼</span> {report.get('inspection_name', check_name)}</h2>
                <span class="section-status {status_class if checked else 'skip'}">{status if checked else 'SKIPPED'}</span>
            </div>
            <div class="section-content" id="content-{check_name}">
"""
        
        # 摘要信息
        summary = report.get("summary", {})
        if summary:
            html += '<div class="data-grid">'
            for key, value in summary.items():
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value) if value else "无"
                html += f"""
                <div class="data-item">
                    <label>{_format_key(key)}</label>
                    <div class="value">{value}</div>
                </div>
"""
            html += '</div>'
        
        # 详细数据表格
        details = report.get("details", {})
        for detail_key, detail_value in details.items():
            if isinstance(detail_value, list) and detail_value:
                html += f'<h4 style="margin-top: 15px;">{_format_key(detail_key)}</h4>'
                if isinstance(detail_value[0], dict):
                    html += '<div style="overflow-x: auto;"><table><thead><tr>'
                    headers = list(detail_value[0].keys())[:8]  # 最多显示8列
                    for h in headers:
                        html += f'<th>{_format_key(h)}</th>'
                    html += '</tr></thead><tbody>'
                    for item in detail_value[:20]:  # 最多显示20条
                        html += '<tr>'
                        for h in headers:
                            val = item.get(h, '-')
                            if isinstance(val, (int, float)):
                                val = f"{val:.2f}" if isinstance(val, float) else val
                            html += f'<td>{val}</td>'
                        html += '</tr>'
                    html += '</tbody></table></div>'
        
        # 问题列表
        issues = report.get("issues", [])
        if issues:
            html += '<h4 style="margin-top: 15px;">发现的问题</h4>'
            for issue in issues[:10]:
                severity = issue.get("severity", "WARNING")
                html += f"""
                <div class="issue-item {'critical' if severity == 'CRITICAL' else ''}">
                    <div class="severity {severity.lower()}">{severity}</div>
                    <div class="message"><strong>{issue.get('category')}:</strong> {issue.get('item')} - {issue.get('details')}</div>
                </div>
"""
        
        # 监控曲线
        monitoring_curves = report.get("details", {}).get("monitoring_curves", {}) or report.get("monitoring_curves", {})
        if monitoring_curves:
            html += '<div class="monitoring-charts">'
            html += '<h3 style="margin-top: 0; color: #667eea;">📈 监控曲线</h3>'
            
            for curve_key, curve_data in monitoring_curves.items():
                # 解析曲线key获取资源信息
                parts = curve_key.split("_")
                metric_type = parts[0] if parts else "unknown"
                resource_name = "_".join(parts[1:]) if len(parts) > 1 else "unknown"
                
                # 获取时间和值数据
                metric = curve_data.get("metric", {})
                values = curve_data.get("values", [])
                
                if values:
                    html += f'<div class="chart-container" id="chart-container-{curve_key}">'
                    html += f'<h4>{_format_key(metric_type)} - {resource_name}</h4>'
                    html += f'<canvas id="chart-{curve_key}"></canvas>'
                    html += '</div>'
                    
                    # 准备图表数据
                    labels = []
                    data_points = []
                    for ts, val in values:
                        try:
                            dt = datetime.fromtimestamp(int(float(ts)), timezone.utc)
                            labels.append(dt.strftime('%H:%M:%S'))
                            data_points.append(round(float(val), 2))
                        except:
                            pass
                    
                    # 添加图表初始化脚本
                    html += f"""
                    <script>
                    (function() {{
                        var ctx = document.getElementById('chart-{curve_key}').getContext('2d');
                        new Chart(ctx, {{
                            type: 'line',
                            data: {{
                                labels: {json.dumps(labels)},
                                datasets: [{{
                                    label: '{_format_key(metric_type)} (%)',
                                    data: {json.dumps(data_points)},
                                    borderColor: '#667eea',
                                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                                    borderWidth: 2,
                                    fill: true,
                                    tension: 0.4,
                                    pointRadius: 3
                                }}]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: true,
                                plugins: {{
                                    legend: {{
                                        display: true
                                    }},
                                    tooltip: {{
                                        mode: 'index',
                                        intersect: false
                                    }}
                                }},
                                scales: {{
                                    x: {{
                                        display: true,
                                        title: {{
                                            display: true,
                                            text: '时间'
                                        }}
                                    }},
                                    y: {{
                                        display: true,
                                        title: {{
                                            display: true,
                                            text: '使用率 (%)'
                                        }},
                                        min: 0,
                                        max: 100
                                    }}
                                }}
                            }}
                        }});
                    }})();
                    </script>
                    """
            html += '</div>'
        
        # 建议
        recommendations = report.get("recommendations", [])
        if recommendations:
            html += '<h4 style="margin-top: 15px;">💡 处理建议</h4>'
            for rec in recommendations[:5]:
                html += f"""
                <div class="recommendation">
                    <div class="target">📌 {rec.get('target')}</div>
                    <div class="message">{rec.get('issue')}</div>
                    <div class="suggestion">💡 {rec.get('suggestion')}</div>
                </div>
"""
        
        html += """
            </div>
        </div>
"""
    
    # 所有问题汇总
    all_issues = summary_report.get("all_issues", [])
    if all_issues:
        html += """
        <div class="section">
            <div class="section-header">
                <h2>📋 所有问题汇总</h2>
            </div>
            <div class="section-content">
                <table>
                    <thead>
                        <tr>
                            <th>严重程度</th>
                            <th>来源</th>
                            <th>类别</th>
                            <th>对象</th>
                            <th>详情</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for issue in all_issues:
            severity = issue.get("severity", "WARNING")
            html += f"""
                        <tr>
                            <td><span class="section-status {severity.lower()}">{severity}</span></td>
                            <td>{issue.get('source', '-')}</td>
                            <td>{issue.get('category', '-')}</td>
                            <td>{issue.get('item', '-')}</td>
                            <td>{issue.get('details', '-')}</td>
                        </tr>
"""
        html += """
                    </tbody>
                </table>
            </div>
        </div>
"""
    
    # 所有建议汇总
    all_recommendations = summary_report.get("all_recommendations", [])
    if all_recommendations:
        html += """
        <div class="section">
            <div class="section-header">
                <h2>💡 处理建议汇总</h2>
            </div>
            <div class="section-content">
"""
        for rec in all_recommendations:
            html += f"""
                <div class="recommendation">
                    <div class="target">📌 {rec.get('target')}</div>
                    <div class="message">{rec.get('issue')}</div>
                    <div class="suggestion">💡 {rec.get('suggestion')}</div>
                </div>
"""
        html += """
            </div>
        </div>
"""
    
    html += """
        <div class="footer">
            <p>CCE集群巡检工具 | 由AI助手自动生成 | 详细报告</p>
        </div>
    </div>
    
    <script>
        function toggleSection(name) {
            var content = document.getElementById('content-' + name);
            var icon = document.getElementById('icon-' + name);
            if (content.classList.contains('collapsed')) {
                content.classList.remove('collapsed');
                icon.classList.remove('collapsed');
            } else {
                content.classList.add('collapsed');
                icon.classList.add('collapsed');
            }
        }
    </script>
</body>
</html>
"""
    return html


def generate_sub_inspection_html(check_name: str, report: dict, cluster_id: str, region: str) -> str:
    """生成单个巡检项的HTML报告
    
    Args:
        check_name: 巡检项名称
        report: 巡检报告数据
        cluster_id: 集群ID
        region: 区域
    
    Returns:
        HTML格式报告字符串
    """
    status = report.get("status", "UNKNOWN")
    status_class = status.lower()
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report.get('inspection_name', check_name)}报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; background: #f5f7fa; color: #333; line-height: 1.6; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; margin-bottom: 20px; }}
        .header h1 {{ font-size: 24px; margin-bottom: 10px; }}
        .status-badge {{ display: inline-block; padding: 8px 16px; border-radius: 20px; font-weight: 600; }}
        .pass {{ background: #d4edda; color: #155724; }}
        .warn {{ background: #fff3cd; color: #856404; }}
        .fail {{ background: #f8d7da; color: #721c24; }}
        .skip {{ background: #e2e3e5; color: #383d41; }}
        .section {{ background: white; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 20px; }}
        .section h3 {{ margin-top: 0; color: #667eea; }}
        .data-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .data-item {{ background: #f8f9fa; padding: 12px; border-radius: 6px; }}
        .data-item label {{ font-size: 12px; color: #666; display: block; }}
        .data-item .value {{ font-size: 20px; font-weight: 600; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f9fa; }}
        .issue {{ background: #fff3cd; padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 4px solid #ffc107; }}
        .issue.critical {{ background: #f8d7da; border-left-color: #dc3545; }}
        .recommendation {{ background: #e7f3ff; padding: 10px; border-radius: 6px; margin-bottom: 8px; border-left: 4px solid #0066cc; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 {report.get('inspection_name', check_name)}</h1>
            <p>集群ID: {cluster_id} | 区域: {region} | 时间: {report.get('inspection_time')}</p>
            <span class="status-badge {status_class}">{status}</span>
        </div>
"""
    
    # 摘要
    summary = report.get("summary", {})
    if summary:
        html += '<div class="section"><h3>📊 检查摘要</h3><div class="data-grid">'
        for key, value in summary.items():
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value) if value else "无"
            html += f'<div class="data-item"><label>{_format_key(key)}</label><div class="value">{value}</div></div>'
        html += '</div></div>'
    
    # 问题列表
    issues = report.get("issues", [])
    if issues:
        html += '<div class="section"><h3>⚠️ 发现的问题</h3>'
        for issue in issues:
            severity = issue.get("severity", "WARNING")
            html += f'<div class="issue {"critical" if severity == "CRITICAL" else ""}"><strong>{severity}</strong>: {issue.get("category")} - {issue.get("item")}<br><small>{issue.get("details")}</small></div>'
        html += '</div>'
    
    # 建议
    recommendations = report.get("recommendations", [])
    if recommendations:
        html += '<div class="section"><h3>💡 处理建议</h3>'
        for rec in recommendations:
            html += f'<div class="recommendation"><strong>{rec.get("target")}</strong>: {rec.get("issue")}<br>💡 {rec.get("suggestion")}</div>'
        html += '</div>'
    
    html += """
        <div style="text-align: center; padding: 20px; color: #666;">
            <p>CCE集群巡检工具 - 独立巡检报告</p>
        </div>
    </div>
</body>
</html>
"""
    return html


def _format_key(key: str) -> str:
    """格式化key为可读的中文标题"""
    key_map = {
        "total_pods": "Pod总数",
        "total_nodes": "节点总数",
        "running": "运行中",
        "pending": "待调度",
        "failed": "失败",
        "ready": "Ready",
        "not_ready": "NotReady",
        "restart_pod_count": "重启Pod数",
        "abnormal_pod_count": "异常Pod数",
        "abnormal_count": "异常节点数",
        "high_cpu_count": "CPU超限数",
        "high_memory_count": "内存超限数",
        "high_disk_count": "磁盘超限数",
        "namespaces": "命名空间",
        "total_events": "事件总数",
        "normal_events": "正常事件",
        "warning_events": "警告事件",
        "critical_events_count": "关键事件数",
        "total_alarms": "告警总数",
        "critical": "严重",
        "major": "重要",
        "minor": "次要",
        "info": "提示",
        "total_loadbalancers": "负载均衡数",
        "high_connection_count": "高连接数ELB",
        "high_bandwidth_count": "高带宽ELB",
        "eip_over_limit_count": "EIP超限数",
        "pod": "Pod",
        "namespace": "命名空间",
        "container": "容器",
        "restart_count": "重启次数",
        "state_reason": "状态原因",
        "node": "节点",
        "cpu_usage_percent": "CPU使用率(%)",
        "memory_usage_percent": "内存使用率(%)",
        "node_ip": "节点IP",
        "node_name": "节点名称",
        "status": "状态",
        "reason": "原因",
        "name": "名称",
        "id": "ID",
        "ip": "IP地址",
        "flavor": "规格",
        "count": "数量",
        "message": "消息",
        "severity": "严重程度",
        "elb_id": "ELB ID",
        "elb_ip": "ELB IP",
        "elb_type": "ELB类型",
        "connection_num": "连接数",
        "l4_connection_usage_percent": "L4连接使用率(%)",
        "high_cpu_pods": "高CPU使用Pod",
        "high_memory_pods": "高内存使用Pod",
        "high_cpu_nodes": "高CPU节点",
        "high_memory_nodes": "高内存节点",
        "high_disk_nodes": "高磁盘节点",
        "restart_pods": "重启Pod列表",
        "abnormal_pods": "异常Pod列表",
        "node_details": "节点详情",
        "abnormal_nodes": "异常节点",
        "critical_events": "关键事件",
        "cluster_alarms": "集群告警",
        "loadbalancer_services": "LoadBalancer服务",
        "elb_metrics": "ELB监控指标",
    }
    return key_map.get(key, key.replace("_", " ").title())