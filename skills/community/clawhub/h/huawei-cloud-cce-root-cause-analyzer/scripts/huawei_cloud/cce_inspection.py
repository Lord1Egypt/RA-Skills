#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCE 集群巡检核心模块

包含：
- 8 大巡检函数（Event / AOM告警 / ELB / Node状态 / 节点资源 / Pod状态 / 插件Pod / 业务Pod）
- 串行巡检（cce_cluster_inspection）
- 并行巡检（cce_cluster_inspection_parallel）
- Subagent 分发与聚合
- 报告生成
"""

from __future__ import annotations

import os
import sys
import json
import time
import argparse
import concurrent.futures
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from .common import get_credentials_with_region
from .cce import (
    get_kubernetes_events, get_kubernetes_services, get_kubernetes_nodes,
    get_kubernetes_pods, list_cce_clusters, list_cce_cluster_nodes,
)
from .aom import list_aom_current_alarms, list_aom_alarms, get_aom_prom_metrics_http, list_aom_instances
from .elb import get_elb_metrics
from .network import get_eip_metrics, list_eip_addresses
from .hss import list_vul_host_hosts
from .report_generator import (
    generate_sub_inspection_report,
    generate_summary_report,
    generate_detailed_html_report,
    generate_sub_inspection_html,
)


def event_inspection(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """Event 巡检
    
    检查内容：
    - 事件类型统计 (Normal/Warning)
    - 关键事件识别
    - 按原因/命名空间归一统计
    
    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
    
    Returns:
        Event 巡检结果
    """
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    
    result = {
        "name": "Event巡检",
        "status": "PASS",
        "checked": False,
        "total": 0,
        "normal": 0,
        "warning": 0,
        "critical_events": [],
        "events_by_reason": {},
        "events_by_namespace": {}
    }
    
    issues = []
    
    def add_issue(severity: str, category: str, item: str, details: str):
        issues.append({
            "severity": severity,
            "category": category,
            "item": item,
            "details": details
        })
    
    try:
        events_result = get_kubernetes_events(region, cluster_id, access_key, secret_key, proj_id)
        if events_result.get("success"):
            result["checked"] = True
            events = events_result.get("events", [])
            result["total"] = len(events)
            
            critical_keywords = [
                "Failed", "Error", "CrashLoopBackOff", "OOMKilled",
                "Evicted", "Insufficient", "BackOff", "Unhealthy",
                "FailedScheduling", "Killing", "FailedMount"
            ]
            
            critical_events = []
            events_by_reason = {}
            events_by_namespace = {}
            
            for event in events:
                event_type = event.get("type", "Normal")
                if event_type == "Normal":
                    result["normal"] += 1
                else:
                    result["warning"] += 1
                
                reason = event.get("reason", "Unknown")
                namespace = event.get("namespace", "default")
                
                # 按原因归一
                if reason not in events_by_reason:
                    events_by_reason[reason] = {"count": 0, "events": []}
                events_by_reason[reason]["count"] += 1
                events_by_reason[reason]["events"].append(event)
                
                # 按命名空间归一
                if namespace not in events_by_namespace:
                    events_by_namespace[namespace] = {"count": 0, "events": []}
                events_by_namespace[namespace]["count"] += 1
                events_by_namespace[namespace]["events"].append(event)
                
                # 检查关键事件
                for keyword in critical_keywords:
                    if keyword in reason or keyword in event.get("message", ""):
                        critical_events.append({
                            "reason": reason,
                            "namespace": namespace,
                            "involved_object": event.get("involved_object", ""),
                            "count": event.get("count", 1),
                            "message": event.get("message", "")[:200]
                        })
                        add_issue("WARNING", "关键事件", event.get("involved_object", ""),
                            f"原因: {reason}, 命名空间: {namespace}, 消息: {event.get('message', '')[:100]}")
                        break
            
            result["critical_events"] = critical_events[:20]
            result["events_by_reason"] = {k: v for k, v in list(events_by_reason.items())[:20]}
            result["events_by_namespace"] = {k: v for k, v in list(events_by_namespace.items())[:20]}
            
            if critical_events:
                result["status"] = "WARN"
    except Exception as e:
        result["error"] = str(e)
    
    return result, issues


def aom_alarm_inspection(region: str, cluster_id: str, cluster_name: str, ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """AOM 告警巡检（活跃+历史合并）
    
    检查内容：
    - 获取活跃告警 + 历史已恢复告警（合并去重）
    - 严重级别分类 (Critical/Major/Minor/Info)
    - 按告警类型归一统计
    - 重点标注资源类告警(CPU/内存/磁盘等)不管是否恢复
    
    重要原则：只查活跃告警会漏掉已恢复的关键告警，必须同时查历史！
    
    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        cluster_name: 集群名称
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
    
    Returns:
        AOM 告警巡检结果
    """
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    
    result = {
        "name": "AOM告警巡检",
        "status": "PASS",
        "checked": False,
        "total": 0,
        "firing_count": 0,
        "resolved_count": 0,
        "severity_breakdown": {},
        "cluster_alarms": [],
        "alarms_by_type": {},
        "resource_alarms": []
    }
    
    issues = []
    
    def add_issue(severity: str, category: str, item: str, details: str):
        issues.append({
            "severity": severity,
            "category": category,
            "item": item,
            "details": details
        })
    
    try:
        # 同时查活跃+历史告警，合并去重
        alarm_result = list_aom_alarms(
            region=region,
            ak=access_key,
            sk=secret_key,
            project_id=proj_id,
            cluster_name=cluster_name,
            hours=1,
            limit=500
        )
        
        if alarm_result.get("success"):
            result["checked"] = True
            alarms = alarm_result.get("events", [])
            
            result["total"] = len(alarms)
            result["firing_count"] = alarm_result.get("firing_count", 0)
            result["resolved_count"] = alarm_result.get("resolved_count", 0)
            
            severity_breakdown = {"Critical": 0, "Major": 0, "Minor": 0, "Info": 0}
            cluster_alarms = []
            alarms_by_type = {}
            resource_alarms = []
            
            RESOURCE_KEYWORDS = [
                'CPU', 'cpu', 'Memory', 'memory', '内存', '磁盘', 'Disk',
                'OOM', 'oom', 'Evicted', 'evicted', '驱赶',
                'CrashLoopBackOff', 'crashloopbackoff',
                'Pressure', 'pressure', '压力'
            ]
            
            for alarm in alarms:
                severity = alarm.get("event_severity", "Info")
                if severity in severity_breakdown:
                    severity_breakdown[severity] += 1
                
                alarm_type = alarm.get("event_name", "Unknown")
                if alarm_type not in alarms_by_type:
                    alarms_by_type[alarm_type] = {"count": 0, "firing": 0, "resolved": 0, "alarms": []}
                alarms_by_type[alarm_type]["count"] += 1
                if alarm.get("status") == "firing":
                    alarms_by_type[alarm_type]["firing"] += 1
                else:
                    alarms_by_type[alarm_type]["resolved"] += 1
                alarms_by_type[alarm_type]["alarms"].append({
                    "name": alarm.get("event_name"),
                    "severity": severity,
                    "status": alarm.get("status"),
                    "resource_id": alarm.get("resource_id"),
                    "message": (alarm.get("message", ""))[:200]
                })
                
                # 检查是否为资源类告警
                alarm_text = alarm_type + ' ' + alarm.get("message", "")
                is_resource_alarm = any(kw in alarm_text for kw in RESOURCE_KEYWORDS)
                if is_resource_alarm:
                    resource_alarms.append({
                        "name": alarm.get("event_name"),
                        "severity": severity,
                        "status": alarm.get("status"),
                        "pod_name": alarm.get("pod_name"),
                        "namespace": alarm.get("namespace"),
                        "message": (alarm.get("message", ""))[:200]
                    })
                
                resource_id = alarm.get("resource_id", "")
                alarm_cluster_id = alarm.get("cluster_id", "")
                alarm_cluster_name = alarm.get("cluster_name", "")
                
                if cluster_id in resource_id or cluster_id == alarm_cluster_id or cluster_name == alarm_cluster_name:
                    cluster_alarms.append({
                        "name": alarm.get("event_name"),
                        "severity": severity,
                        "status": alarm.get("status"),
                        "resource_id": resource_id,
                        "message": (alarm.get("message", ""))[:200],
                        "pod_name": alarm.get("pod_name"),
                        "namespace": alarm.get("namespace")
                    })
                    if severity == "Critical":
                        add_issue("CRITICAL", "重要告警", alarm.get("event_name"),
                            f"严重级别: {severity}, 状态: {alarm.get('status','')}, 资源: {resource_id}")
                    elif severity == "Major" and is_resource_alarm:
                        # 资源类 Major 告警即使已恢复也要告警
                        add_issue("WARNING", "资源告警", alarm.get("event_name"),
                            f"严重级别: {severity}, 状态: {alarm.get('status','')}, 资源: {resource_id}")
            
            result["severity_breakdown"] = severity_breakdown
            result["cluster_alarms"] = cluster_alarms[:30]
            result["alarms_by_type"] = {k: v for k, v in list(alarms_by_type.items())[:30]}
            result["resource_alarms"] = resource_alarms[:20]
            
            if severity_breakdown.get("Critical", 0) > 0:
                result["status"] = "FAIL"
            elif severity_breakdown.get("Major", 0) > 0 and resource_alarms:
                result["status"] = "WARN"
            elif severity_breakdown.get("Major", 0) > 0:
                result["status"] = "WARN"
        else:
            result["error"] = alarm_result.get("error", "Unknown error")
    except Exception as e:
        result["error"] = str(e)
    
    return result, issues


def elb_monitoring_inspection(region: str, cluster_id: str, aom_instance_id: str,
                               cluster_name: str, ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """ELB 负载均衡监控巡检
    
    检查内容：
    - LoadBalancer Service 列表
    - ELB 监控指标 (连接数/带宽/使用率)
    - 公网 EIP 带宽监控
    
    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        aom_instance_id: AOM 实例 ID
        cluster_name: 集群名称
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
    
    Returns:
        ELB 监控巡检结果
    """
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    
    result = {
        "name": "ELB负载均衡监控巡检",
        "status": "PASS",
        "checked": False,
        "loadbalancer_services": [],
        "elb_metrics": [],
        "eip_metrics": [],
        "high_bandwidth_usage_elbs": [],
        "high_connection_usage_elbs": [],
        "high_bandwidth_eips": [],
        "total_loadbalancers": 0
    }
    
    issues = []
    
    def add_issue(severity: str, category: str, item: str, details: str):
        issues.append({
            "severity": severity,
            "category": category,
            "item": item,
            "details": details
        })
    
    if not aom_instance_id:
        result["status"] = "SKIP"
        result["message"] = "未找到CCE类型的AOM实例"
        return result, issues
    
    result["checked"] = True
    
    try:
        services_result = get_kubernetes_services(region, cluster_id, access_key, secret_key, proj_id)
        
        # 获取EIP列表
        eip_list_result = list_eip_addresses(region, access_key, secret_key, proj_id)
        eip_map = {}
        if eip_list_result.get("success"):
            for eip in eip_list_result.get("eips", []):
                eip_map[eip.get("ip_address")] = eip
        
        if services_result.get("success"):
            lb_services = []
            for svc in services_result.get("services", []):
                if svc.get("type") == "LoadBalancer":
                    annotations = svc.get("annotations", {})
                    elb_id = annotations.get("kubernetes.io/elb.id", "")
                    
                    if elb_id:
                        lb_services.append({
                            "service_name": svc.get("name"),
                            "namespace": svc.get("namespace"),
                            "elb_id": elb_id,
                            "cluster_ip": svc.get("cluster_ip"),
                            "load_balancer_ip": svc.get("load_balancer_ip"),
                            "ports": svc.get("ports", []),
                            "annotations": annotations
                        })
            
            result["loadbalancer_services"] = lb_services
            result["total_loadbalancers"] = len(lb_services)
            
            # 获取每个ELB的监控数据
            for lb_svc in lb_services:
                elb_id = lb_svc.get("elb_id")
                if elb_id:
                    elb_metrics_result = get_elb_metrics(region, elb_id, access_key, secret_key, proj_id)
                    
                    if elb_metrics_result.get("success"):
                        summary = elb_metrics_result.get("summary", {})
                        
                        elb_info = {
                            "service_name": lb_svc.get("service_name"),
                            "namespace": lb_svc.get("namespace"),
                            "elb_id": elb_id,
                            "elb_ip": lb_svc.get("load_balancer_ip"),
                            "elb_type": elb_metrics_result.get("elb_type", "未知"),
                            "connection_num": summary.get("connection_num"),
                            "in_bandwidth_bps": summary.get("in_bandwidth_bps"),
                            "l4_connection_usage_percent": summary.get("l4_connection_usage_percent"),
                            "l4_bandwidth_usage_percent": summary.get("l4_bandwidth_usage_percent"),
                            "normal_servers": summary.get("normal_servers"),
                            "abnormal_servers": summary.get("abnormal_servers")
                        }
                        
                        # 检查L4使用率
                        l4_con = summary.get("l4_connection_usage_percent")
                        l4_bw = summary.get("l4_bandwidth_usage_percent")
                        
                        if l4_con and l4_con > 80:
                            result["high_connection_usage_elbs"].append({
                                "service": lb_svc.get("service_name"),
                                "namespace": lb_svc.get("namespace"),
                                "elb_id": elb_id,
                                "layer": "L4",
                                "usage_percent": round(l4_con, 2),
                                "status": "critical" if l4_con > 90 else "warning"
                            })
                            add_issue("WARNING", "ELB连接使用率高", elb_id,
                                f"Service: {lb_svc.get('namespace')}/{lb_svc.get('service_name')}, L4连接使用率: {round(l4_con, 2)}%")
                        
                        if l4_bw and l4_bw > 80:
                            result["high_bandwidth_usage_elbs"].append({
                                "service": lb_svc.get("service_name"),
                                "namespace": lb_svc.get("namespace"),
                                "elb_id": elb_id,
                                "layer": "L4",
                                "usage_percent": round(l4_bw, 2),
                                "status": "critical" if l4_bw > 90 else "warning"
                            })
                            add_issue("WARNING", "ELB带宽使用率高", elb_id,
                                f"Service: {lb_svc.get('namespace')}/{lb_svc.get('service_name')}, L4带宽使用率: {round(l4_bw, 2)}%")
                        
                        # 检查是否有公网EIP
                        lb_ip = lb_svc.get("load_balancer_ip")
                        if lb_ip:
                            eip_info = eip_map.get(lb_ip)
                            if eip_info:
                                eip_id = eip_info.get("id")
                                elb_info["has_public_eip"] = True
                                elb_info["public_ip"] = lb_ip
                                elb_info["eip_id"] = eip_id
                                
                                # 获取EIP监控
                                eip_metrics_result = get_eip_metrics(region, eip_id, access_key, secret_key, proj_id)
                                if eip_metrics_result.get("success"):
                                    eip_summary = eip_metrics_result.get("summary", {})
                                    bw_in = eip_summary.get("bw_usage_in_percent")
                                    bw_out = eip_summary.get("bw_usage_out_percent")
                                    
                                    elb_info["eip_bw_usage_in_percent"] = bw_in
                                    elb_info["eip_bw_usage_out_percent"] = bw_out
                                    
                                    result["eip_metrics"].append({
                                        "service_name": lb_svc.get("service_name"),
                                        "namespace": lb_svc.get("namespace"),
                                        "eip_id": eip_id,
                                        "public_ip": lb_ip,
                                        "bw_usage_in_percent": bw_in,
                                        "bw_usage_out_percent": bw_out
                                    })
                                    
                                    # 检查EIP带宽超限
                                    if bw_in and bw_in > 80:
                                        result["high_bandwidth_eips"].append({
                                            "service": lb_svc.get("service_name"),
                                            "namespace": lb_svc.get("namespace"),
                                            "eip_id": eip_id,
                                            "public_ip": lb_ip,
                                            "direction": "in",
                                            "usage_percent": round(bw_in, 2),
                                            "status": "critical" if bw_in > 90 else "warning"
                                        })
                                        add_issue("WARNING", "EIP入带宽超限", eip_id,
                                            f"Service: {lb_svc.get('namespace')}/{lb_svc.get('service_name')}, 公网IP: {lb_ip}, 入带宽使用率: {round(bw_in, 2)}%")
                                    
                                    if bw_out and bw_out > 80:
                                        result["high_bandwidth_eips"].append({
                                            "service": lb_svc.get("service_name"),
                                            "namespace": lb_svc.get("namespace"),
                                            "eip_id": eip_id,
                                            "public_ip": lb_ip,
                                            "direction": "out",
                                            "usage_percent": round(bw_out, 2),
                                            "status": "critical" if bw_out > 90 else "warning"
                                        })
                                        add_issue("WARNING", "EIP出带宽超限", eip_id,
                                            f"Service: {lb_svc.get('namespace')}/{lb_svc.get('service_name')}, 公网IP: {lb_ip}, 出带宽使用率: {round(bw_out, 2)}%")
                        
                        result["elb_metrics"].append(elb_info)
            
            if result["high_bandwidth_usage_elbs"] or result["high_connection_usage_elbs"] or result["high_bandwidth_eips"]:
                result["status"] = "WARN"
                
    except Exception as e:
        result["error"] = str(e)
    
    return result, issues


def node_status_inspection(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """Node 状态巡检
    
    检查内容：
    - 节点状态检查 (Active/Error/Deleting/Installing/Abnormal)
    - Ready/NotReady 统计
    
    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
    
    Returns:
        Node 状态巡检结果
    """
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    
    result = {
        "name": "Node状态巡检",
        "status": "PASS",
        "checked": False,
        "total": 0,
        "ready": 0,
        "not_ready": 0,
        "node_details": [],
        "abnormal_nodes": []
    }
    
    issues = []
    
    def add_issue(severity: str, category: str, item: str, details: str):
        issues.append({
            "severity": severity,
            "category": category,
            "item": item,
            "details": details
        })
    
    try:
        nodes_result = list_cce_cluster_nodes(region, cluster_id, access_key, secret_key, proj_id)
        if nodes_result.get("success"):
            result["checked"] = True
            nodes = nodes_result.get("nodes", [])
            result["total"] = len(nodes)
            
            abnormal_nodes = []
            status_map = {
                "Active": "健康",
                "Error": "节点处于错误状态，可能需要重启或重新加入集群",
                "Deleting": "节点正在删除中",
                "Installing": "节点正在安装中，请等待安装完成",
                "Abnormal": "节点状态异常，请检查节点网络或 kubelet 服务"
            }
            
            for node in nodes:
                status = node.get("status", "Unknown")
                if status == "Active":
                    result["ready"] += 1
                else:
                    result["not_ready"] += 1
                    reason = status_map.get(status, "节点状态异常")
                    abnormal_nodes.append({
                        "name": node.get("name"),
                        "id": node.get("id"),
                        "ip": node.get("ip"),
                        "flavor": node.get("flavor"),
                        "status": status,
                        "reason": reason
                    })
                    add_issue("CRITICAL", "节点状态异常", node.get("name"),
                        f"节点: {node.get('name')}, IP: {node.get('ip')}, 状态: {status}, 原因: {reason}")
            
            result["node_details"] = nodes
            result["abnormal_nodes"] = abnormal_nodes
            
            if abnormal_nodes:
                result["status"] = "FAIL"
    except Exception as e:
        result["error"] = str(e)
    
    return result, issues


def node_vul_inspection(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """节点漏洞巡检
    
    检查内容：
    - CCE 集群节点在 HSS 中的漏洞状态
    - 统计每个节点的 unfix（未处理）漏洞数量
    - 高危漏洞节点标记为问题
    
    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
    
    Returns:
        (巡检结果, 问题列表)
    """
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    
    result = {
        "name": "节点漏洞巡检",
        "status": "PASS",
        "checked": False,
        "total_nodes": 0,
        "vulnerable_nodes": 0,
        "clean_nodes": 0,
        "node_vul_details": [],
        "high_risk_nodes": [],
    }
    
    issues: List[Dict[str, Any]] = []
    
    def add_issue(severity: str, category: str, item: str, details: str):
        issues.append({
            "severity": severity,
            "category": category,
            "item": item,
            "details": details
        })
    
    try:
        # 1. Get all nodes in the CCE cluster
        nodes_result = list_cce_cluster_nodes(region, cluster_id, access_key, secret_key, proj_id)
        if not nodes_result.get("success"):
            result["error"] = nodes_result.get("error", "Failed to get cluster nodes")
            return result, issues
        
        nodes = nodes_result.get("nodes", [])
        result["total_nodes"] = len(nodes)
        
        if not nodes:
            result["checked"] = True
            return result, issues
        
        
        # 2. Get all hosts from HSS
        hss_result = list_vul_host_hosts(region, enterprise_project_id="all_granted_eps",
                                         limit=100, ak=access_key, sk=secret_key)
        if not hss_result.get("success"):
            result["error"] = hss_result.get("error", "Failed to get HSS vulnerability data")
            return result, issues
        
        hss_hosts_by_id = {h["host_id"]: h for h in hss_result.get("hosts", [])}
        hss_hosts_by_name = {h["host_name"]: h for h in hss_result.get("hosts", [])}
        result["checked"] = True
        
        # 3. Match CCE nodes to HSS hosts (by server_id first, then by node_name fallback)
        for node in nodes:
            server_id = node.get("server_id")  # ECS instance ID = HSS host_id
            node_name = node.get("name", "unknown")  # CCE node name = HSS host_name
            labels = node.get("labels", {})
            
            # OS / Kernel 版本（K8s well-known node labels）
            os_version = labels.get("node.kubernetes.io/os_version", "")
            kernel_version = labels.get("node.kubernetes.io/kernel_version", "")
            
            # 优先用 server_id 匹配，fallback 到 node_name
            hss_data = hss_hosts_by_id.get(server_id) if server_id else None
            if hss_data is None:
                hss_data = hss_hosts_by_name.get(node_name)
            
            in_hss = hss_data is not None
            
            vul_info = {
                "node_name": node_name,
                "server_id": server_id,
                "status": node.get("status"),
                "os_version": os_version,
                "kernel_version": kernel_version,
                "in_hss": in_hss,
                "total_vul_num": 0,
                "unfix_total": 0,
                "unfix_high": 0,
                "unfix_medium": 0,
                "unfix_low": 0,
            }
            
            if hss_data:
                vul_info["total_vul_num"] = hss_data.get("total_vul_num", 0)
                vul_info["unfix_total"] = hss_data.get("unfix_total", 0)
                vul_info["unfix_high"] = hss_data.get("unfix_high", 0)
                vul_info["unfix_medium"] = hss_data.get("unfix_medium", 0)
                vul_info["unfix_low"] = hss_data.get("unfix_low", 0)
            
            result["node_vul_details"].append(vul_info)
            
            # Count clean vs vulnerable
            if vul_info["unfix_total"] > 0:
                result["vulnerable_nodes"] += 1
            else:
                result["clean_nodes"] += 1
            
            # Flag high-risk nodes (unfix_high > 0 or unfix_total >= 5)
            if vul_info["unfix_high"] > 0 or vul_info["unfix_total"] >= 5:
                result["high_risk_nodes"].append({
                    "node_name": node_name,
                    "server_id": server_id,
                    "os_version": os_version,
                    "kernel_version": kernel_version,
                    "unfix_total": vul_info["unfix_total"],
                    "unfix_high": vul_info["unfix_high"],
                    "unfix_medium": vul_info["unfix_medium"],
                })
                sev = "CRITICAL" if vul_info["unfix_high"] > 0 else "WARNING"
                os_info = f"OS:{os_version} kernel:{kernel_version}" if os_version or kernel_version else ""
                add_issue(sev, "节点漏洞", node_name,
                    f"节点 {node_name} {os_info} 存在 {vul_info['unfix_total']} 个未处理漏洞"
                    f"（高:{vul_info['unfix_high']} / 中:{vul_info['unfix_medium']} / 低:{vul_info['unfix_low']}）")
        
        if result["high_risk_nodes"]:
            result["status"] = "FAIL"
        elif result["vulnerable_nodes"] > 0:
            result["status"] = "WARNING"
    
    except Exception as e:
        result["error"] = str(e)
    
    return result, issues


def node_resource_monitoring_inspection(region: str, cluster_id: str, aom_instance_id: str,
                                         cluster_name: str, ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """节点资源监控巡检
    
    检查内容：
    - CPU 使用率 > 80% 的节点数量及 Top 10
    - 内存使用率 > 80% 的节点数量及 Top 10
    - 磁盘使用率 > 80% 的节点数量及 Top 10
    
    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        aom_instance_id: AOM 实例 ID
        cluster_name: 集群名称
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
    
    Returns:
        节点资源监控巡检结果
    """
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    
    result = {
        "name": "节点资源监控巡检",
        "status": "PASS",
        "checked": False,
        "high_cpu_count": 0,
        "high_memory_count": 0,
        "high_disk_count": 0,
        "high_cpu_nodes_top10": [],
        "high_memory_nodes_top10": [],
        "high_disk_nodes_top10": [],
        "all_high_resource_nodes": [],
        "monitoring_curves": {}
    }
    
    issues = []
    
    def add_issue(severity: str, category: str, item: str, details: str):
        issues.append({
            "severity": severity,
            "category": category,
            "item": item,
            "details": details
        })
    
    if not aom_instance_id:
        result["status"] = "SKIP"
        result["message"] = "未找到CCE类型的AOM实例"
        return result, issues
    
    result["checked"] = True
    result["aom_instance_id"] = aom_instance_id
    
    # 获取节点信息映射
    node_info_map = {}
    k8s_nodes_result = get_kubernetes_nodes(region, cluster_id, access_key, secret_key, proj_id)
    if k8s_nodes_result.get("success"):
        for node in k8s_nodes_result.get("nodes", []):
            node_name = node.get("name", "")
            if node_name:
                node_info_map[node_name] = {
                    "name": node_name,
                    "ip": node_name,
                    "status": node.get("status", "Unknown")
                }
    
    # CPU 数量查询
    cpu_count_query = f"count(100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode='idle', cluster_name='{cluster_name}'}}[5m])) * 100) > 80)"
    cpu_count_result = get_aom_prom_metrics_http(region, aom_instance_id, cpu_count_query, ak=access_key, sk=secret_key, project_id=proj_id)
    
    if cpu_count_result.get("success") and cpu_count_result.get("result", {}).get("data", {}).get("result"):
        for item in cpu_count_result["result"]["data"]["result"]:
            values = item.get("values", [])
            if values:
                try:
                    result["high_cpu_count"] = int(float(values[-1][1]))
                except (ValueError, IndexError):
                    pass
    
    # CPU Top 10
    if result["high_cpu_count"] > 0:
        cpu_top10_query = f"topk(10, 100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode='idle', cluster_name='{cluster_name}'}}[5m])) * 100))"
        cpu_top10_result = get_aom_prom_metrics_http(region, aom_instance_id, cpu_top10_query, ak=access_key, sk=secret_key, project_id=proj_id)
        
        if cpu_top10_result.get("success") and cpu_top10_result.get("result", {}).get("data", {}).get("result"):
            for item in cpu_top10_result["result"]["data"]["result"]:
                metric = item.get("metric", {})
                values = item.get("values", [])
                if values:
                    try:
                        latest_value = float(values[-1][1])
                        instance = metric.get("instance", "unknown")
                        instance_ip = instance.split(":")[0] if ":" in instance else instance
                        
                        if latest_value > 80:
                            node_info = node_info_map.get(instance_ip, {})
                            resource_info = {
                                "instance": instance,
                                "node_ip": instance_ip,
                                "node_name": node_info.get("name", instance_ip),
                                "cpu_usage_percent": round(latest_value, 2),
                                "status": "critical" if latest_value > 90 else "warning"
                            }
                            result["high_cpu_nodes_top10"].append(resource_info)
                            add_issue("WARNING", "节点CPU高", instance_ip,
                                f"节点: {instance_ip}, CPU使用率: {round(latest_value, 2)}%")
                            
                            cpu_curve_query = f"100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode='idle', instance='{instance}', cluster_name='{cluster_name}'}}[5m])) * 100)"
                            cpu_curve_result = get_aom_prom_metrics_http(region, aom_instance_id, cpu_curve_query, hours=1, step=60, ak=access_key, sk=secret_key, project_id=proj_id)
                            if cpu_curve_result.get("success") and cpu_curve_result.get("result", {}).get("data", {}).get("result"):
                                key = f"cpu_{instance_ip}"
                                result["monitoring_curves"][key] = cpu_curve_result["result"]["data"]["result"][0]
                    except (ValueError, IndexError):
                        pass
    
    # 内存数量查询
    mem_count_query = f"count(avg by (instance) ((1 - node_memory_MemAvailable_bytes{{cluster_name='{cluster_name}'}} / node_memory_MemTotal_bytes{{cluster_name='{cluster_name}'}})) * 100 > 80)"
    mem_count_result = get_aom_prom_metrics_http(region, aom_instance_id, mem_count_query, ak=access_key, sk=secret_key, project_id=proj_id)
    
    if mem_count_result.get("success") and mem_count_result.get("result", {}).get("data", {}).get("result"):
        for item in mem_count_result["result"]["data"]["result"]:
            values = item.get("values", [])
            if values:
                try:
                    result["high_memory_count"] = int(float(values[-1][1]))
                except (ValueError, IndexError):
                    pass
    
    # 内存 Top 10
    if result["high_memory_count"] > 0:
        mem_top10_query = f"topk(10, avg by (instance) ((1 - node_memory_MemAvailable_bytes{{cluster_name='{cluster_name}'}} / node_memory_MemTotal_bytes{{cluster_name='{cluster_name}'}})) * 100)"
        mem_top10_result = get_aom_prom_metrics_http(region, aom_instance_id, mem_top10_query, ak=access_key, sk=secret_key, project_id=proj_id)
        
        if mem_top10_result.get("success") and mem_top10_result.get("result", {}).get("data", {}).get("result"):
            for item in mem_top10_result["result"]["data"]["result"]:
                metric = item.get("metric", {})
                values = item.get("values", [])
                if values:
                    try:
                        latest_value = float(values[-1][1])
                        instance = metric.get("instance", "unknown")
                        instance_ip = instance.split(":")[0] if ":" in instance else instance
                        
                        if latest_value > 80:
                            node_info = node_info_map.get(instance_ip, {})
                            resource_info = {
                                "instance": instance,
                                "node_ip": instance_ip,
                                "node_name": node_info.get("name", instance_ip),
                                "memory_usage_percent": round(latest_value, 2),
                                "status": "critical" if latest_value > 90 else "warning"
                            }
                            result["high_memory_nodes_top10"].append(resource_info)
                            add_issue("WARNING", "节点内存高", instance_ip,
                                f"节点: {instance_ip}, 内存使用率: {round(latest_value, 2)}%")
                            
                            mem_curve_query = f"avg by (instance) ((1 - node_memory_MemAvailable_bytes{{instance='{instance}', cluster_name='{cluster_name}'}} / node_memory_MemTotal_bytes{{instance='{instance}', cluster_name='{cluster_name}'}})) * 100"
                            mem_curve_result = get_aom_prom_metrics_http(region, aom_instance_id, mem_curve_query, hours=1, step=60, ak=access_key, sk=secret_key, project_id=proj_id)
                            if mem_curve_result.get("success") and mem_curve_result.get("result", {}).get("data", {}).get("result"):
                                key = f"memory_{instance_ip}"
                                result["monitoring_curves"][key] = mem_curve_result["result"]["data"]["result"][0]
                    except (ValueError, IndexError):
                        pass
    
    # 磁盘数量查询
    disk_count_query = f"count(avg by (instance) ((1 - node_filesystem_avail_bytes{{mountpoint='/',fstype!~'tmpfs|fuse.lxcfs',cluster_name='{cluster_name}'}} / node_filesystem_size_bytes{{mountpoint='/',fstype!~'tmpfs|fuse.lxcfs',cluster_name='{cluster_name}'}})) * 100 > 80)"
    disk_count_result = get_aom_prom_metrics_http(region, aom_instance_id, disk_count_query, ak=access_key, sk=secret_key, project_id=proj_id)
    
    if disk_count_result.get("success") and disk_count_result.get("result", {}).get("data", {}).get("result"):
        for item in disk_count_result["result"]["data"]["result"]:
            values = item.get("values", [])
            if values:
                try:
                    result["high_disk_count"] = int(float(values[-1][1]))
                except (ValueError, IndexError):
                    pass
    
    # 磁盘 Top 10
    if result["high_disk_count"] > 0:
        disk_top10_query = f"topk(10, avg by (instance) ((1 - node_filesystem_avail_bytes{{mountpoint='/',fstype!~'tmpfs|fuse.lxcfs',cluster_name='{cluster_name}'}} / node_filesystem_size_bytes{{mountpoint='/',fstype!~'tmpfs|fuse.lxcfs',cluster_name='{cluster_name}'}})) * 100)"
        disk_top10_result = get_aom_prom_metrics_http(region, aom_instance_id, disk_top10_query, ak=access_key, sk=secret_key, project_id=proj_id)
        
        if disk_top10_result.get("success") and disk_top10_result.get("result", {}).get("data", {}).get("result"):
            for item in disk_top10_result["result"]["data"]["result"]:
                metric = item.get("metric", {})
                values = item.get("values", [])
                if values:
                    try:
                        latest_value = float(values[-1][1])
                        instance = metric.get("instance", "unknown")
                        instance_ip = instance.split(":")[0] if ":" in instance else instance
                        
                        if latest_value > 80:
                            node_info = node_info_map.get(instance_ip, {})
                            resource_info = {
                                "instance": instance,
                                "node_ip": instance_ip,
                                "node_name": node_info.get("name", instance_ip),
                                "disk_usage_percent": round(latest_value, 2),
                                "status": "critical" if latest_value > 90 else "warning"
                            }
                            result["high_disk_nodes_top10"].append(resource_info)
                            add_issue("WARNING", "节点磁盘高", instance_ip,
                                f"节点: {instance_ip}, 磁盘使用率: {round(latest_value, 2)}%")
                            
                            disk_curve_query = f"avg by (instance) ((1 - node_filesystem_avail_bytes{{mountpoint='/',fstype!~'tmpfs|fuse.lxcfs',instance='{instance}',cluster_name='{cluster_name}'}} / node_filesystem_size_bytes{{mountpoint='/',fstype!~'tmpfs|fuse.lxcfs',instance='{instance}',cluster_name='{cluster_name}'}})) * 100"
                            disk_curve_result = get_aom_prom_metrics_http(region, aom_instance_id, disk_curve_query, hours=1, step=60, ak=access_key, sk=secret_key, project_id=proj_id)
                            if disk_curve_result.get("success") and disk_curve_result.get("result", {}).get("data", {}).get("result"):
                                key = f"disk_{instance_ip}"
                                result["monitoring_curves"][key] = disk_curve_result["result"]["data"]["result"][0]
                    except (ValueError, IndexError):
                        pass
    
    if result["high_cpu_count"] > 0 or result["high_memory_count"] > 0 or result["high_disk_count"] > 0:
        result["status"] = "WARN"
    
    return result, issues


def pod_status_inspection(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """Pod 状态巡检
    
    检查内容：
    - Pod 运行状态统计
    - 容器重启次数检查
    - 异常状态识别
    
    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
    
    Returns:
        Pod 状态巡检结果
    """
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    
    result = {
        "name": "Pod状态巡检",
        "status": "PASS",
        "checked": False,
        "total": 0,
        "running": 0,
        "pending": 0,
        "failed": 0,
        "restart_pods": [],
        "abnormal_pods": [],
        "abnormal_summary": {}
    }
    
    issues = []
    
    def add_issue(severity: str, category: str, item: str, details: str):
        issues.append({
            "severity": severity,
            "category": category,
            "item": item,
            "details": details
        })
    
    try:
        pods_result = get_kubernetes_pods(region, cluster_id, access_key, secret_key, proj_id)
        if pods_result.get("success"):
            result["checked"] = True
            pods = pods_result.get("pods", [])
            result["total"] = len(pods)
            
            restart_pods = []
            abnormal_pods = []
            abnormal_summary = {}
            
            for pod in pods:
                status = pod.get("status", "Unknown")
                if status == "Running":
                    result["running"] += 1
                elif status == "Pending":
                    result["pending"] += 1
                elif status in ["Failed", "Unknown"]:
                    result["failed"] += 1
                
                # 检查重启次数
                containers = pod.get("containers", [])
                for container in containers:
                    restart_count = container.get("restart_count", 0)
                    if restart_count >= 5:
                        add_issue("CRITICAL", "Pod异常重启", pod.get("name"),
                            f"命名空间: {pod.get('namespace')}, 容器: {container.get('name')}, 重启次数: {restart_count}")
                        restart_pods.append({
                            "pod": pod.get("name"),
                            "namespace": pod.get("namespace"),
                            "container": container.get("name"),
                            "restart_count": restart_count,
                            "state_reason": container.get("state_reason", "Unknown"),
                            "node": pod.get("node", "Unknown")
                        })
                    elif restart_count >= 2:
                        add_issue("WARNING", "Pod异常重启", pod.get("name"),
                            f"命名空间: {pod.get('namespace')}, 容器: {container.get('name')}, 重启次数: {restart_count}")
                        restart_pods.append({
                            "pod": pod.get("name"),
                            "namespace": pod.get("namespace"),
                            "container": container.get("name"),
                            "restart_count": restart_count,
                            "state_reason": container.get("state_reason", "Unknown"),
                            "node": pod.get("node", "Unknown")
                        })
                
                # 检查异常状态
                if status in ["Failed", "Unknown"] or pod.get("state_reason") in [
                    "CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull",
                    "OOMKilled", "Evicted", "CreateContainerConfigError"
                ]:
                    reason = pod.get("state_reason", status)
                    abnormal_pods.append({
                        "pod": pod.get("name"),
                        "namespace": pod.get("namespace"),
                        "status": status,
                        "reason": reason,
                        "node": pod.get("node", "Unknown")
                    })
                    if reason not in abnormal_summary:
                        abnormal_summary[reason] = []
                    abnormal_summary[reason].append(pod.get("name"))
            
            result["restart_pods"] = restart_pods
            result["abnormal_pods"] = abnormal_pods
            result["abnormal_summary"] = abnormal_summary
            
            if restart_pods or abnormal_pods:
                result["status"] = "WARN"
            if result["failed"] > 0:
                result["status"] = "FAIL"
    except Exception as e:
        result["error"] = str(e)
    
    return result, issues


def addon_pod_monitoring_inspection(region: str, cluster_id: str, aom_instance_id: str,
                                   cluster_name: str, ak: str, sk: str, project_id: str = None,
                                   all_pods_map: dict = None) -> Dict[str, Any]:
    """插件 Pod 监控巡检 (kube-system + monitoring)
    
    检查内容：
    - CPU 使用率 > 80% 的 Pod 数量及 Top 10
    - 内存使用率 > 80% 的 Pod 数量及 Top 10
    
    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        aom_instance_id: AOM 实例 ID
        cluster_name: 集群名称
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
        all_pods_map: Pod 信息映射 (可选)
    
    Returns:
        插件 Pod 监控巡检结果
    """
    result = {
        "name": "插件Pod监控巡检",
        "status": "PASS",
        "checked": False,
        "high_cpu_count": 0,
        "high_memory_count": 0,
        "high_cpu_pods_top10": [],
        "high_memory_pods_top10": [],
        "namespaces": ["kube-system", "monitoring"]
    }
    
    issues = []
    
    def add_issue(severity: str, category: str, item: str, details: str):
        issues.append({
            "severity": severity,
            "category": category,
            "item": item,
            "details": details
        })
    
    if not aom_instance_id:
        result["status"] = "SKIP"
        result["message"] = "未找到CCE类型的AOM实例"
        return result, issues
    
    result["checked"] = True
    result["aom_instance_id"] = aom_instance_id
    
    # CPU数量查询
    cpu_count_query = 'count(sum by (pod, namespace) (rate(container_cpu_usage_seconds_total{image!="",namespace=~"kube-system|monitoring"}[5m])) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{resource="cpu",namespace=~"kube-system|monitoring"}) * 100 > 80)'
    cpu_count_result = get_aom_prom_metrics_http(region, aom_instance_id, cpu_count_query, ak=ak, sk=sk, project_id=project_id)
    
    if cpu_count_result.get("success") and cpu_count_result.get("result", {}).get("data", {}).get("result"):
        for item in cpu_count_result["result"]["data"]["result"]:
            values = item.get("values", [])
            if values:
                try:
                    result["high_cpu_count"] = int(float(values[-1][1]))
                except (ValueError, IndexError):
                    pass
    
    # CPU Top 10
    if result["high_cpu_count"] > 0:
        cpu_top10_query = 'topk(10, sum by (pod, namespace) (rate(container_cpu_usage_seconds_total{image!="",namespace=~"kube-system|monitoring"}[5m])) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{resource="cpu",namespace=~"kube-system|monitoring"}) * 100)'
        cpu_top10_result = get_aom_prom_metrics_http(region, aom_instance_id, cpu_top10_query, ak=ak, sk=sk, project_id=project_id)
        
        if cpu_top10_result.get("success") and cpu_top10_result.get("result", {}).get("data", {}).get("result"):
            for item in cpu_top10_result["result"]["data"]["result"]:
                metric = item.get("metric", {})
                values = item.get("values", [])
                if values:
                    try:
                        latest_value = float(values[-1][1])
                        pod_name = metric.get("pod", "unknown")
                        namespace = metric.get("namespace", "unknown")
                        
                        if latest_value > 80:
                            pod_info = all_pods_map.get(pod_name, {}) if all_pods_map else {}
                            resource_info = {
                                "pod": pod_name,
                                "namespace": namespace,
                                "cpu_usage_percent": round(latest_value, 2),
                                "node": pod_info.get("node", "Unknown"),
                                "status": "critical" if latest_value > 90 else "warning"
                            }
                            result["high_cpu_pods_top10"].append(resource_info)
                            add_issue("WARNING", "插件Pod CPU使用率高", pod_name,
                                f"命名空间: {namespace}, CPU使用率: {round(latest_value, 2)}%")
                    except (ValueError, IndexError):
                        pass
    
    # 内存数量查询
    mem_count_query = 'count(sum by (pod, namespace) (container_memory_working_set_bytes{image!="",namespace=~"kube-system|monitoring"}) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{resource="memory",namespace=~"kube-system|monitoring"}) * 100 > 80)'
    mem_count_result = get_aom_prom_metrics_http(region, aom_instance_id, mem_count_query, ak=ak, sk=sk, project_id=project_id)
    
    if mem_count_result.get("success") and mem_count_result.get("result", {}).get("data", {}).get("result"):
        for item in mem_count_result["result"]["data"]["result"]:
            values = item.get("values", [])
            if values:
                try:
                    result["high_memory_count"] = int(float(values[-1][1]))
                except (ValueError, IndexError):
                    pass
    
    # 设置状态
    if result["high_cpu_count"] > 0 or result["high_memory_count"] > 0:
        result["status"] = "WARN"
    
    return result, issues


def biz_pod_monitoring_inspection(region: str, cluster_id: str, aom_instance_id: str,
                                   cluster_name: str, ak: str, sk: str, project_id: str = None,
                                   all_pods_map: dict = None, all_namespaces: list = None) -> Dict[str, Any]:
    """业务 Pod 监控巡检 (其他命名空间)
    
    检查内容：
    - CPU 使用率 > 80% 的 Pod 数量及 Top 10
    - 内存使用率 > 80% 的 Pod 数量及 Top 10
    
    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        aom_instance_id: AOM 实例 ID
        cluster_name: 集群名称
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
        all_pods_map: Pod 信息映射 (可选)
        all_namespaces: 业务命名空间列表 (可选)
    
    Returns:
        业务 Pod 监控巡检结果
    """
    result = {
        "name": "业务Pod监控巡检",
        "status": "PASS",
        "checked": False,
        "high_cpu_count": 0,
        "high_memory_count": 0,
        "high_cpu_pods_top10": [],
        "high_memory_pods_top10": [],
        "namespaces": all_namespaces or [],
        "monitoring_curves": {}
    }
    
    issues = []
    
    def add_issue(severity: str, category: str, item: str, details: str):
        issues.append({
            "severity": severity,
            "category": category,
            "item": item,
            "details": details
        })
    
    if not aom_instance_id:
        result["status"] = "SKIP"
        result["message"] = "未找到CCE类型的AOM实例"
        return result, issues
    
    result["checked"] = True
    result["aom_instance_id"] = aom_instance_id
    
    # CPU数量查询
    cpu_count_query = 'count(sum by (pod, namespace) (rate(container_cpu_usage_seconds_total{image!="",namespace!~"kube-system|monitoring"}[5m])) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{resource="cpu",namespace!~"kube-system|monitoring"}) * 100 > 80)'
    cpu_count_result = get_aom_prom_metrics_http(region, aom_instance_id, cpu_count_query, ak=ak, sk=sk, project_id=project_id)
    
    if cpu_count_result.get("success") and cpu_count_result.get("result", {}).get("data", {}).get("result"):
        for item in cpu_count_result["result"]["data"]["result"]:
            values = item.get("values", [])
            if values:
                try:
                    result["high_cpu_count"] = int(float(values[-1][1]))
                except (ValueError, IndexError):
                    pass
    
    # CPU Top 10
    if result["high_cpu_count"] > 0:
        cpu_top10_query = 'topk(10, sum by (pod, namespace) (rate(container_cpu_usage_seconds_total{image!="",namespace!~"kube-system|monitoring"}[5m])) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{resource="cpu",namespace!~"kube-system|monitoring"}) * 100)'
        cpu_top10_result = get_aom_prom_metrics_http(region, aom_instance_id, cpu_top10_query, ak=ak, sk=sk, project_id=project_id)
        
        if cpu_top10_result.get("success") and cpu_top10_result.get("result", {}).get("data", {}).get("result"):
            for item in cpu_top10_result["result"]["data"]["result"]:
                metric = item.get("metric", {})
                values = item.get("values", [])
                if values:
                    try:
                        latest_value = float(values[-1][1])
                        pod_name = metric.get("pod", "unknown")
                        namespace = metric.get("namespace", "unknown")
                        
                        if latest_value > 80:
                            pod_info = all_pods_map.get(pod_name, {}) if all_pods_map else {}
                            resource_info = {
                                "pod": pod_name,
                                "namespace": namespace,
                                "cpu_usage_percent": round(latest_value, 2),
                                "node": pod_info.get("node", "Unknown"),
                                "status": "critical" if latest_value > 90 else "warning"
                            }
                            result["high_cpu_pods_top10"].append(resource_info)
                            add_issue("WARNING", "业务Pod CPU使用率高", pod_name,
                                f"命名空间: {namespace}, CPU使用率: {round(latest_value, 2)}%")
                            
                            cpu_curve_query = f'sum by (pod, namespace) (rate(container_cpu_usage_seconds_total{{image!="",pod="{pod_name}",namespace="{namespace}"}}[5m])) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{{resource="cpu",pod="{pod_name}",namespace="{namespace}"}}) * 100'
                            cpu_curve_result = get_aom_prom_metrics_http(region, aom_instance_id, cpu_curve_query, hours=1, step=60, ak=ak, sk=sk, project_id=project_id)
                            if cpu_curve_result.get("success") and cpu_curve_result.get("result", {}).get("data", {}).get("result"):
                                key = f"cpu_{namespace}_{pod_name}"
                                result["monitoring_curves"][key] = cpu_curve_result["result"]["data"]["result"][0]
                    except (ValueError, IndexError):
                        pass
    
    # 内存数量查询
    mem_count_query = 'count(sum by (pod, namespace) (container_memory_working_set_bytes{image!="",namespace!~"kube-system|monitoring"}) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{resource="memory",namespace!~"kube-system|monitoring"}) * 100 > 80)'
    mem_count_result = get_aom_prom_metrics_http(region, aom_instance_id, mem_count_query, ak=ak, sk=sk, project_id=project_id)
    
    if mem_count_result.get("success") and mem_count_result.get("result", {}).get("data", {}).get("result"):
        for item in mem_count_result["result"]["data"]["result"]:
            values = item.get("values", [])
            if values:
                try:
                    result["high_memory_count"] = int(float(values[-1][1]))
                except (ValueError, IndexError):
                    pass
    
    # 内存 Top 10
    if result["high_memory_count"] > 0:
        mem_top10_query = 'topk(10, sum by (pod, namespace) (container_memory_working_set_bytes{image!="",namespace!~"kube-system|monitoring"}) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{resource="memory",namespace!~"kube-system|monitoring"}) * 100)'
        mem_top10_result = get_aom_prom_metrics_http(region, aom_instance_id, mem_top10_query, ak=ak, sk=sk, project_id=project_id)
        
        if mem_top10_result.get("success") and mem_top10_result.get("result", {}).get("data", {}).get("result"):
            for item in mem_top10_result["result"]["data"]["result"]:
                metric = item.get("metric", {})
                values = item.get("values", [])
                if values:
                    try:
                        latest_value = float(values[-1][1])
                        pod_name = metric.get("pod", "unknown")
                        namespace = metric.get("namespace", "unknown")
                        
                        if latest_value > 80:
                            pod_info = all_pods_map.get(pod_name, {}) if all_pods_map else {}
                            resource_info = {
                                "pod": pod_name,
                                "namespace": namespace,
                                "memory_usage_percent": round(latest_value, 2),
                                "node": pod_info.get("node", "Unknown"),
                                "status": "critical" if latest_value > 90 else "warning"
                            }
                            result["high_memory_pods_top10"].append(resource_info)
                            add_issue("WARNING", "业务Pod内存使用率高", pod_name,
                                f"命名空间: {namespace}, 内存使用率: {round(latest_value, 2)}%")
                            
                            mem_curve_query = f'sum by (pod, namespace) (container_memory_working_set_bytes{{image!="",pod="{pod_name}",namespace="{namespace}"}}) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{{resource="memory",pod="{pod_name}",namespace="{namespace}"}}) * 100'
                            mem_curve_result = get_aom_prom_metrics_http(region, aom_instance_id, mem_curve_query, hours=1, step=60, ak=ak, sk=sk, project_id=project_id)
                            if mem_curve_result.get("success") and mem_curve_result.get("result", {}).get("data", {}).get("result"):
                                key = f"memory_{namespace}_{pod_name}"
                                result["monitoring_curves"][key] = mem_curve_result["result"]["data"]["result"][0]
                    except (ValueError, IndexError):
                        pass
    
    if result["high_cpu_count"] > 0 or result["high_memory_count"] > 0:
        result["status"] = "WARN"
    
    return result, issues
# ========== 巡检任务定义 ==========

INSPECTION_TASKS = {
    "pods": {
        "name": "Pod状态巡检",
        "action": "huawei_pod_status_inspection",
        "description": "检查Pod运行状态、容器重启次数、异常状态"
    },
    "nodes": {
        "name": "Node状态巡检",
        "action": "huawei_node_status_inspection",
        "description": "检查节点状态、Ready/NotReady统计"
    },
    "addon_pod_monitoring": {
        "name": "插件Pod监控巡检",
        "action": "huawei_addon_pod_monitoring_inspection",
        "description": "检查kube-system/monitoring命名空间的CPU/内存使用率"
    },
    "biz_pod_monitoring": {
        "name": "业务Pod监控巡检",
        "action": "huawei_biz_pod_monitoring_inspection",
        "description": "检查业务命名空间的CPU/内存使用率Top 10"
    },
    "node_monitoring": {
        "name": "节点资源监控巡检",
        "action": "huawei_node_resource_inspection",
        "description": "检查CPU/内存/磁盘使用率Top 10"
    },
    "events": {
        "name": "Event巡检",
        "action": "huawei_event_inspection",
        "description": "检查集群事件和Warning事件"
    },
    "alarms": {
        "name": "AOM告警巡检",
        "action": "huawei_aom_alarm_inspection",
        "description": "检查当前活跃告警"
    },
    "elb_monitoring": {
        "name": "ELB负载均衡监控巡检",
        "action": "huawei_elb_monitoring_inspection",
        "description": "检查LoadBalancer类型Service的ELB监控数据"
    }
}


def _get_aom_instance(region: str, ak: str, sk: str, project_id: str = None) -> str:
    """获取可用的 AOM 实例 ID"""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    aom_instances = list_aom_instances(region, access_key, secret_key, proj_id)
    if aom_instances.get("success"):
        for instance in aom_instances.get("instances", []):
            if instance.get("type") == "CCE":
                test_result = get_aom_prom_metrics_http(region, instance.get("id"), "up",
                                                        ak=access_key, sk=secret_key, project_id=proj_id)
                if test_result.get("success") and test_result.get("result", {}).get("data", {}).get("result"):
                    return instance.get("id")
    return None


def _get_cluster_name(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> str:
    """获取集群名称"""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    cluster_name = cluster_id
    try:
        clusters_result = list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters_result.get("success"):
            for c in clusters_result.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass
    return cluster_name


def _get_all_pods_map(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> dict:
    """获取所有 Pod 信息映射"""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    all_pods_map = {}
    all_pods_result = get_kubernetes_pods(region, cluster_id, access_key, secret_key, proj_id)
    if all_pods_result.get("success"):
        for pod in all_pods_result.get("pods", []):
            all_pods_map[pod.get("name", "")] = pod
    return all_pods_map


def _get_all_namespaces(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> list:
    """获取所有业务命名空间列表"""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    all_namespaces = set()
    all_pods_result = get_kubernetes_pods(region, cluster_id, access_key, secret_key, proj_id)
    if all_pods_result.get("success"):
        for pod in all_pods_result.get("pods", []):
            ns = pod.get("namespace", "")
            if ns and ns not in ["kube-system", "monitoring"]:
                all_namespaces.add(ns)
    return list(all_namespaces)


# ========== 并行巡检引擎 ==========

def run_single_inspection(task_id: str, region: str, cluster_id: str, ak: str, sk: str,
                         project_id: str = None, aom_instance_id: str = None,
                         cluster_name: str = None, all_pods_map: dict = None,
                         all_namespaces: list = None) -> Tuple[dict, list]:
    """执行单个巡检任务"""
    task = INSPECTION_TASKS.get(task_id)
    if not task:
        return {"name": task_id, "status": "ERROR", "error": "Unknown task"}, []

    try:
        if task_id == "pods":
            return pod_status_inspection(region, cluster_id, ak, sk, project_id)
        elif task_id == "nodes":
            return node_status_inspection(region, cluster_id, ak, sk, project_id)
        elif task_id == "addon_pod_monitoring":
            return addon_pod_monitoring_inspection(
                region, cluster_id, aom_instance_id, cluster_name, ak, sk, project_id, all_pods_map
            )
        elif task_id == "biz_pod_monitoring":
            return biz_pod_monitoring_inspection(
                region, cluster_id, aom_instance_id, cluster_name, ak, sk, project_id, all_pods_map, all_namespaces
            )
        elif task_id == "node_monitoring":
            return node_resource_monitoring_inspection(
                region, cluster_id, aom_instance_id, cluster_name, ak, sk, project_id
            )
        elif task_id == "events":
            return event_inspection(region, cluster_id, ak, sk, project_id)
        elif task_id == "alarms":
            return aom_alarm_inspection(region, cluster_id, cluster_name, ak, sk, project_id)
        elif task_id == "elb_monitoring":
            return elb_monitoring_inspection(
                region, cluster_id, aom_instance_id, cluster_name, ak, sk, project_id
            )
        else:
            return {"name": task["name"], "status": "ERROR", "error": "Unknown task"}, []
    except Exception as e:
        return {"name": task["name"], "status": "ERROR", "error": str(e)}, []


def run_single_inspection_subprocess(args: dict) -> dict:
    """在子进程中执行单个巡检任务"""
    result, issues = run_single_inspection(
        args["task_id"], args["region"], args["cluster_id"], args["ak"], args["sk"],
        args.get("project_id"), args.get("aom_instance_id"), args.get("cluster_name"),
        args.get("all_pods_map"), args.get("all_namespaces")
    )
    return {"task_id": args["task_id"], "check": result, "issues": issues}


def cce_cluster_inspection_parallel(region: str, cluster_id: str, ak: str = None, sk: str = None,
                                    project_id: str = None, max_workers: int = 4) -> Dict[str, Any]:
    """CCE 集群巡检主函数 - 并行版本（线程池）"""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    start_time = time.time()
    inspection_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    inspection = {
        "success": True, "region": region, "cluster_id": cluster_id,
        "inspection_time": inspection_time, "mode": "parallel",
        "max_workers": max_workers,
        "result": {"status": "HEALTHY", "total_issues": 0, "critical_issues": 0, "warning_issues": 0},
        "checks": {}, "issues": [], "sub_reports": {},
        "timing": {"start_time": inspection_time, "duration_seconds": 0, "task_timings": {}}
    }

    all_issues = []

    def add_issues(issues: list):
        nonlocal all_issues
        for issue in issues:
            all_issues.append(issue)
            if issue["severity"] == "CRITICAL":
                inspection["result"]["critical_issues"] += 1
            else:
                inspection["result"]["warning_issues"] += 1
            inspection["result"]["total_issues"] += 1
            if issue["severity"] == "CRITICAL":
                inspection["result"]["status"] = "CRITICAL"
            elif inspection["result"]["status"] == "HEALTHY":
                inspection["result"]["status"] = "WARNING"

    # 预处理
    preprocess_start = time.time()
    cluster_name = cluster_id
    try:
        clusters_result = list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters_result.get("success"):
            for c in clusters_result.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass

    aom_instance_id = None
    aom_instances = list_aom_instances(region, access_key, secret_key, proj_id)
    if aom_instances.get("success"):
        for instance in aom_instances.get("instances", []):
            if instance.get("type") == "CCE":
                test_result = get_aom_prom_metrics_http(region, instance.get("id"), "up",
                                                        ak=access_key, sk=secret_key, project_id=proj_id)
                if test_result.get("success") and test_result.get("result", {}).get("data", {}).get("result"):
                    aom_instance_id = instance.get("id")
                    break

    all_pods_result = get_kubernetes_pods(region, cluster_id, access_key, secret_key, proj_id)
    all_pods_map = {}
    all_namespaces = set()
    if all_pods_result.get("success"):
        for pod in all_pods_result.get("pods", []):
            all_pods_map[pod.get("name", "")] = pod
            ns = pod.get("namespace", "")
            if ns and ns not in ["kube-system", "monitoring"]:
                all_namespaces.add(ns)

    preprocess_duration = time.time() - preprocess_start
    inspection["timing"]["preprocess_seconds"] = round(preprocess_duration, 2)

    # 并行执行
    task_args_list = [{
        "task_id": task_id, "region": region, "cluster_id": cluster_id,
        "ak": access_key, "sk": secret_key, "project_id": proj_id,
        "aom_instance_id": aom_instance_id, "cluster_name": cluster_name,
        "all_pods_map": all_pods_map, "all_namespaces": list(all_namespaces)
    } for task_id in INSPECTION_TASKS.keys()]

    parallel_start = time.time()
    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {
            executor.submit(run_single_inspection_subprocess, args): args["task_id"]
            for args in task_args_list
        }
        for future in concurrent.futures.as_completed(future_to_task):
            task_id = future_to_task[future]
            task_name = INSPECTION_TASKS[task_id]["name"]
            task_start = time.time()
            try:
                result = future.result()
                results[task_id] = result
                task_duration = time.time() - task_start
                inspection["timing"]["task_timings"][task_id] = round(task_duration, 2)
            except Exception as e:
                results[task_id] = {
                    "task_id": task_id,
                    "check": {"name": task_name, "status": "ERROR", "error": str(e)},
                    "issues": []
                }

    parallel_duration = time.time() - parallel_start
    inspection["timing"]["parallel_seconds"] = round(parallel_duration, 2)

    # 汇总结果
    for task_id, result in results.items():
        check_result = result.get("check", {})
        issues = result.get("issues", [])
        inspection["checks"][task_id] = check_result
        add_issues(issues)
        inspection["sub_reports"][task_id] = generate_sub_inspection_report(
            task_id, check_result, issues, inspection_time
        )

    inspection["issues"] = all_issues
    summary_report = generate_summary_report(inspection["sub_reports"], cluster_id, region, inspection_time)
    inspection["report"] = _generate_parallel_text_report(inspection, cluster_id, region)
    inspection["html_report"] = generate_detailed_html_report(summary_report)
    inspection["summary_report"] = summary_report

    total_duration = time.time() - start_time
    inspection["timing"]["duration_seconds"] = round(total_duration, 2)
    inspection["timing"]["total_formatted"] = f"{total_duration:.2f}s"

    return inspection


def _generate_parallel_text_report(inspection: dict, cluster_id: str, region: str) -> str:
    """生成并行模式的详细文本报告"""
    lines = []
    lines.append("=" * 80)
    lines.append("🔍 CCE 集群巡检详细报告 (并行模式)")
    lines.append("=" * 80)
    lines.append(f"集群ID: {cluster_id}")
    lines.append(f"区域: {region}")
    lines.append(f"巡检时间: {inspection['inspection_time']}")
    lines.append(f"巡检模式: 并行 (max_workers={inspection.get('max_workers', 4)})")
    lines.append(f"总耗时: {inspection['timing'].get('total_formatted', 'N/A')}")
    lines.append(f"巡检结果: {inspection['result']['status']}")
    lines.append(f"总问题数: {inspection['result']['total_issues']} "
                 f"(严重: {inspection['result']['critical_issues']}, "
                 f"警告: {inspection['result']['warning_issues']})")
    lines.append("")

    task_timings = inspection.get("timing", {}).get("task_timings", {})
    if task_timings:
        lines.append("📊 各任务耗时:")
        for task_id, duration in task_timings.items():
            task_name = INSPECTION_TASKS.get(task_id, {}).get("name", task_id)
            lines.append(f"   • {task_name}: {duration}s")
        lines.append("")

    sub_reports = inspection.get("sub_reports", {})
    for check_name, sub_report in sub_reports.items():
        lines.append("=" * 80)
        lines.append(f"📋 【{sub_report.get('inspection_name', check_name)}】")
        lines.append(f"   状态: {sub_report.get('status', 'UNKNOWN')}")
        lines.append("-" * 80)
        summary = sub_report.get("summary", {})
        if summary:
            lines.append("📊 检查摘要:")
            for key, value in summary.items():
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value) if value else "无"
                lines.append(f"   • {_format_key(key)}: {value}")
            lines.append("")
        issues = sub_report.get("issues", [])
        if issues:
            lines.append("⚠️ 发现的问题:")
            for issue in issues:
                icon = "🔴" if issue.get("severity") == "CRITICAL" else "🟡"
                lines.append(f"   {icon} [{issue.get('severity')}] {issue.get('category')}")
                lines.append(f"      对象: {issue.get('item')}")
                lines.append(f"      详情: {issue.get('details')}")
            lines.append("")
        lines.append("")

    lines.append("=" * 80)
    lines.append("📋 问题汇总")
    lines.append("=" * 80)
    all_issues = inspection.get("issues", [])
    if all_issues:
        critical = [i for i in all_issues if i.get("severity") == "CRITICAL"]
        warning = [i for i in all_issues if i.get("severity") != "CRITICAL"]
        if critical:
            lines.append("")
            lines.append("🔴 严重问题:")
            for i, issue in enumerate(critical, 1):
                lines.append(f"   {i}. [{issue.get('category')}] {issue.get('item')}")
                lines.append(f"      {issue.get('details')}")
        if warning:
            lines.append("")
            lines.append("🟡 警告问题:")
            for i, issue in enumerate(warning, 1):
                lines.append(f"   {i}. [{issue.get('category')}] {issue.get('item')}")
                lines.append(f"      {issue.get('details')}")
    else:
        lines.append("   ✅ 未发现问题")

    lines.append("")
    lines.append("=" * 80)
    if inspection["result"]["status"] == "HEALTHY":
        lines.append("✅ 集群状态健康，无异常问题")
    elif inspection["result"]["status"] == "WARNING":
        lines.append("⚠️ 集群存在警告问题，建议关注处理")
    else:
        lines.append("❌ 集群存在严重问题，请立即处理！")
    lines.append("=" * 80)
    return "\n".join(lines)


# ========== 串行巡检 ==========

def cce_cluster_inspection(region: str, cluster_id: str, ak: str = None, sk: str = None,
                           project_id: str = None) -> Dict[str, Any]:
    """CCE 集群巡检主函数 - 串行版本"""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    inspection_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    inspection = {
        "success": True, "region": region, "cluster_id": cluster_id,
        "inspection_time": inspection_time,
        "result": {"status": "HEALTHY", "total_issues": 0, "critical_issues": 0, "warning_issues": 0},
        "checks": {}, "issues": [], "sub_reports": {}
    }

    all_issues = []

    def add_issues(issues: list):
        nonlocal all_issues
        for issue in issues:
            all_issues.append(issue)
            if issue["severity"] == "CRITICAL":
                inspection["result"]["critical_issues"] += 1
            else:
                inspection["result"]["warning_issues"] += 1
            inspection["result"]["total_issues"] += 1
            if issue["severity"] == "CRITICAL":
                inspection["result"]["status"] = "CRITICAL"
            elif inspection["result"]["status"] == "HEALTHY":
                inspection["result"]["status"] = "WARNING"

    # 预处理
    cluster_name = cluster_id
    try:
        clusters_result = list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters_result.get("success"):
            for c in clusters_result.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass

    aom_instance_id = None
    aom_instances = list_aom_instances(region, access_key, secret_key, proj_id)
    if aom_instances.get("success"):
        for instance in aom_instances.get("instances", []):
            if instance.get("type") == "CCE":
                test_result = get_aom_prom_metrics_http(region, instance.get("id"), "up",
                                                        ak=access_key, sk=secret_key, project_id=proj_id)
                if test_result.get("success") and test_result.get("result", {}).get("data", {}).get("result"):
                    aom_instance_id = instance.get("id")
                    break

    all_pods_result = get_kubernetes_pods(region, cluster_id, access_key, secret_key, proj_id)
    all_pods_map = {}
    all_namespaces = set()
    if all_pods_result.get("success"):
        for pod in all_pods_result.get("pods", []):
            all_pods_map[pod.get("name", "")] = pod
            ns = pod.get("namespace", "")
            if ns and ns not in ["kube-system", "monitoring"]:
                all_namespaces.add(ns)

    # 9 大巡检项
    checks = [
        ("pods", pod_status_inspection(region, cluster_id, access_key, secret_key, proj_id)),
        ("nodes", node_status_inspection(region, cluster_id, access_key, secret_key, proj_id)),
        ("addon_pod_monitoring", addon_pod_monitoring_inspection(
            region, cluster_id, aom_instance_id, cluster_name, access_key, secret_key, proj_id, all_pods_map)),
        ("biz_pod_monitoring", biz_pod_monitoring_inspection(
            region, cluster_id, aom_instance_id, cluster_name, access_key, secret_key, proj_id, all_pods_map, list(all_namespaces))),
        ("node_monitoring", node_resource_monitoring_inspection(
            region, cluster_id, aom_instance_id, cluster_name, access_key, secret_key, proj_id)),
        ("events", event_inspection(region, cluster_id, access_key, secret_key, proj_id)),
        ("alarms", aom_alarm_inspection(region, cluster_id, cluster_name, access_key, secret_key, proj_id)),
        ("elb_monitoring", elb_monitoring_inspection(
            region, cluster_id, aom_instance_id, cluster_name, access_key, secret_key, proj_id)),
        ("node_vul", node_vul_inspection(region, cluster_id, access_key, secret_key, proj_id)),
    ]

    for task_id, (check_result, issues) in checks:
        inspection["checks"][task_id] = check_result
        add_issues(issues)
        inspection["sub_reports"][task_id] = generate_sub_inspection_report(
            task_id, check_result, issues, inspection_time
        )

    inspection["issues"] = all_issues
    summary_report = generate_summary_report(inspection["sub_reports"], cluster_id, region, inspection_time)
    inspection["report"] = _generate_serial_text_report(inspection, cluster_id, region)
    inspection["html_report"] = generate_detailed_html_report(summary_report)
    inspection["summary_report"] = summary_report

    return inspection


def _generate_serial_text_report(inspection: dict, cluster_id: str, region: str) -> str:
    """生成串行模式的详细文本报告"""
    lines = []
    lines.append("=" * 80)
    lines.append("🔍 CCE 集群巡检详细报告")
    lines.append("=" * 80)
    lines.append(f"集群ID: {cluster_id}")
    lines.append(f"区域: {region}")
    lines.append(f"巡检时间: {inspection['inspection_time']}")
    lines.append(f"巡检结果: {inspection['result']['status']}")
    lines.append(f"总问题数: {inspection['result']['total_issues']} "
                 f"(严重: {inspection['result']['critical_issues']}, "
                 f"警告: {inspection['result']['warning_issues']})")
    lines.append("")

    sub_reports = inspection.get("sub_reports", {})
    for check_name, sub_report in sub_reports.items():
        lines.append("=" * 80)
        lines.append(f"📋 【{sub_report.get('inspection_name', check_name)}】")
        lines.append(f"   状态: {sub_report.get('status', 'UNKNOWN')}")
        lines.append(f"   检查状态: {'已检查' if sub_report.get('checked') else '未检查'}")
        lines.append("-" * 80)
        summary = sub_report.get("summary", {})
        if summary:
            lines.append("📊 检查摘要:")
            for key, value in summary.items():
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value) if value else "无"
                lines.append(f"   • {_format_key(key)}: {value}")
            lines.append("")
        issues = sub_report.get("issues", [])
        if issues:
            lines.append("⚠️ 发现的问题:")
            for issue in issues:
                icon = "🔴" if issue.get("severity") == "CRITICAL" else "🟡"
                lines.append(f"   {icon} [{issue.get('severity')}] {issue.get('category')}")
                lines.append(f"      对象: {issue.get('item')}")
                lines.append(f"      详情: {issue.get('details')}")
            lines.append("")
        recs = sub_report.get("recommendations", [])
        if recs:
            lines.append("💡 处理建议:")
            for i, rec in enumerate(recs[:5], 1):
                lines.append(f"   {i}. {rec.get('target')}")
                lines.append(f"      问题: {rec.get('issue')}")
                lines.append(f"      建议: {rec.get('suggestion')}")
            lines.append("")
        lines.append("")

    lines.append("=" * 80)
    lines.append("📋 问题汇总")
    lines.append("=" * 80)
    all_issues = inspection.get("issues", [])
    if all_issues:
        critical = [i for i in all_issues if i.get("severity") == "CRITICAL"]
        warning = [i for i in all_issues if i.get("severity") != "CRITICAL"]
        if critical:
            lines.append("")
            lines.append("🔴 严重问题:")
            for i, issue in enumerate(critical, 1):
                lines.append(f"   {i}. [{issue.get('category')}] {issue.get('item')}")
                lines.append(f"      {issue.get('details')}")
        if warning:
            lines.append("")
            lines.append("🟡 警告问题:")
            for i, issue in enumerate(warning, 1):
                lines.append(f"   {i}. [{issue.get('category')}] {issue.get('item')}")
                lines.append(f"      {issue.get('details')}")
    else:
        lines.append("   ✅ 未发现问题")

    lines.append("")
    lines.append("=" * 80)
    if inspection["result"]["status"] == "HEALTHY":
        lines.append("✅ 集群状态健康，无异常问题")
    elif inspection["result"]["status"] == "WARNING":
        lines.append("⚠️ 集群存在警告问题，建议关注处理")
    else:
        lines.append("❌ 集群存在严重问题，请立即处理！")
    lines.append("=" * 80)
    return "\n".join(lines)


def _format_key(key: str) -> str:
    """格式化 key 为可读的中文标题"""
    key_map = {
        "total_pods": "Pod总数", "total_nodes": "节点总数",
        "running": "运行中", "pending": "待调度", "failed": "失败",
        "ready": "Ready", "not_ready": "NotReady",
        "restart_pod_count": "重启Pod数", "abnormal_pod_count": "异常Pod数",
        "abnormal_count": "异常节点数",
        "high_cpu_count": "CPU超限数", "high_memory_count": "内存超限数", "high_disk_count": "磁盘超限数",
        "namespaces": "命名空间",
        "total_events": "事件总数", "normal_events": "正常事件", "warning_events": "警告事件",
        "critical_events_count": "关键事件数",
        "total_alarms": "告警总数",
        "critical": "严重", "major": "重要", "minor": "次要", "info": "提示",
        "total_loadbalancers": "负载均衡数",
        "high_connection_count": "高连接数ELB", "high_bandwidth_count": "高带宽ELB",
        "eip_over_limit_count": "EIP超限数",
    }
    return key_map.get(key, key.replace("_", " ").title())


# ========== Subagent 分发与聚合 ==========

def get_preprocess_data(region: str, cluster_id: str, ak: str, sk: str,
                        project_id: str = None) -> dict:
    """获取预处理数据"""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

    cluster_name = cluster_id
    try:
        clusters_result = list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters_result.get("success"):
            for c in clusters_result.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass

    aom_instance_id = None
    try:
        aom_instances = list_aom_instances(region, access_key, secret_key, proj_id)
        if aom_instances.get("success"):
            for instance in aom_instances.get("instances", []):
                if instance.get("type") == "CCE":
                    test_result = get_aom_prom_metrics_http(region, instance.get("id"), "up",
                                                            ak=access_key, sk=secret_key, project_id=proj_id)
                    if test_result.get("success") and test_result.get("result", {}).get("data", {}).get("result"):
                        aom_instance_id = instance.get("id")
                        break
    except Exception:
        pass

    all_pods_map = {}
    all_namespaces = set()
    try:
        all_pods_result = get_kubernetes_pods(region, cluster_id, access_key, secret_key, proj_id)
        if all_pods_result.get("success"):
            for pod in all_pods_result.get("pods", []):
                all_pods_map[pod.get("name", "")] = pod
                ns = pod.get("namespace", "")
                if ns and ns not in ["kube-system", "monitoring"]:
                    all_namespaces.add(ns)
    except Exception:
        pass

    return {
        "cluster_name": cluster_name,
        "aom_instance_id": aom_instance_id,
        "all_pods_map": all_pods_map,
        "all_namespaces": list(all_namespaces)
    }


def generate_subagent_task_list(region: str, cluster_id: str, ak: str, sk: str,
                               project_id: str = None) -> Dict[str, Any]:
    """生成 subagent 任务列表"""
    preprocess_data = get_preprocess_data(region, cluster_id, ak, sk, project_id)
    tasks = []
    for task_id, task in INSPECTION_TASKS.items():
        command = f"cd skills/huawei-cloud/scripts && python3 huawei-cloud.py {task['action']} region={region} cluster_id={cluster_id} ak={ak} sk={sk}"
        if project_id:
            command += f" project_id={project_id}"
        tasks.append({
            "task_id": task_id, "name": task["name"],
            "action": task["action"], "description": task["description"],
            "command": command, "preprocess_data": preprocess_data
        })
    return {
        "success": True, "region": region, "cluster_id": cluster_id,
        "cluster_name": preprocess_data["cluster_name"],
        "aom_instance_id": preprocess_data["aom_instance_id"],
        "task_count": len(tasks), "tasks": tasks, "preprocess_data": preprocess_data
    }


def generate_auto_subagent_info(region: str, cluster_id: str, ak: str, sk: str,
                                 project_id: str = None) -> Dict[str, Any]:
    """生成自动聚合模式的 subagent 信息"""
    preprocess_data = get_preprocess_data(region, cluster_id, ak, sk, project_id)
    tasks = []
    expected_results = []
    for task_id, task in INSPECTION_TASKS.items():
        expected_results.append(task_id)
        command = f"cd skills/huawei-cloud/scripts && python3 huawei-cloud.py {task['action']} region={region} cluster_id={cluster_id} ak={ak} sk={sk}"
        if project_id:
            command += f" project_id={project_id}"
        tasks.append({
            "task_id": task_id, "label": f"inspection-{task_id}",
            "name": task["name"], "action": task["action"],
            "description": task["description"], "command": command
        })
    return {
        "success": True, "mode": "auto",
        "instruction": "启动所有subagent后不要调用sessions_yield，收到结果时累积直到全部完成再输出最终报告",
        "region": region, "cluster_id": cluster_id,
        "cluster_name": preprocess_data["cluster_name"],
        "total_tasks": len(tasks), "expected_results": expected_results,
        "tasks": tasks, "preprocess_data": preprocess_data,
        "start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def execute_single_task(task_id: str, region: str, cluster_id: str, ak: str, sk: str,
                      project_id: str = None, preprocess_data: dict = None) -> Dict[str, Any]:
    """执行单个巡检任务（subagent 内部调用）"""
    task = INSPECTION_TASKS.get(task_id)
    if not task:
        return {"success": False, "error": f"Unknown task: {task_id}"}

    if preprocess_data is None:
        preprocess_data = get_preprocess_data(region, cluster_id, ak, sk, project_id)

    check_result, issues = run_single_inspection(
        task_id, region, cluster_id, ak, sk, project_id,
        preprocess_data.get("aom_instance_id"), preprocess_data.get("cluster_name"),
        preprocess_data.get("all_pods_map"), preprocess_data.get("all_namespaces")
    )
    return {"success": True, "task_id": task_id, "task_name": task["name"],
            "check": check_result, "issues": issues}


def aggregate_subagent_results(results: List[Dict[str, Any]],
                               cluster_info: Dict[str, Any]) -> Dict[str, Any]:
    """聚合所有 subagent 的结果"""
    all_issues = []
    checks = {}
    critical_count = 0
    warning_count = 0

    for result in results:
        if not result.get("success"):
            continue
        task_id = result.get("task_id")
        check = result.get("check", {})
        issues = result.get("issues", [])
        checks[task_id] = check
        for issue in issues:
            all_issues.append(issue)
            if issue.get("severity") == "CRITICAL":
                critical_count += 1
            else:
                warning_count += 1

    if critical_count > 0:
        overall_status = "CRITICAL"
    elif warning_count > 0:
        overall_status = "WARNING"
    else:
        overall_status = "HEALTHY"

    return {
        "success": True, "mode": "subagent_aggregated",
        "cluster_id": cluster_info.get("cluster_id"),
        "cluster_name": cluster_info.get("cluster_name"),
        "region": cluster_info.get("region"),
        "inspection_time": cluster_info.get("start_time", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "result": {"status": overall_status, "total_issues": len(all_issues),
                   "critical_issues": critical_count, "warning_issues": warning_count},
        "checks": checks, "issues": all_issues,
        "summary": {"total_tasks": len(results),
                    "successful_tasks": len([r for r in results if r.get("success")]),
                    "failed_tasks": len([r for r in results if not r.get("success")])}
    }


def get_subagent_tasks() -> List[Dict[str, str]]:
    """获取 subagent 任务列表"""
    return [{"task_id": task_id, "name": task["name"],
             "action": task["action"], "description": task["description"]}
            for task_id, task in INSPECTION_TASKS.items()]


def format_subagent_prompt(task_id: str, region: str, cluster_id: str,
                           ak: str, sk: str, project_id: str = None,
                           extra_params: dict = None) -> str:
    """生成 subagent 执行提示词"""
    task = INSPECTION_TASKS.get(task_id)
    if not task:
        return f"错误：未知任务 {task_id}"
    prompt = f"""执行华为云CCE集群巡检任务：{task['name']}

任务描述：{task['description']}

参数：
- region: {region}
- cluster_id: {cluster_id}
- ak: {ak}
- sk: {sk}
- project_id: {project_id or '未指定'}
"""
    if extra_params:
        prompt += "\n额外参数：\n"
        for key, value in extra_params.items():
            if key in ["ak", "sk"]:
                continue
            prompt += f"- {key}: {value}\n"
    prompt += f"""
执行命令：
cd skills/huawei-cloud/scripts && python3 huawei-cloud.py {task['action']} region={region} cluster_id={cluster_id} ak={ak} sk={sk}

请执行巡检并返回结果JSON。
"""
    return prompt


# ========== 报告导出 ==========

def _generate_html_report(inspection: dict, cluster_id: str, region: str) -> str:
    """生成HTML格式巡检报告"""
    summary_report = inspection.get("summary_report", {})
    if not summary_report:
        summary_report = generate_summary_report(
            inspection.get("sub_reports", {}), cluster_id, region,
            inspection.get("inspection_time", "")
        )
    return generate_detailed_html_report(summary_report)


def generate_inspection_html_report(inspection: dict, cluster_id: str, region: str) -> str:
    """兼容旧入口的 HTML 巡检报告生成函数"""
    return _generate_html_report(inspection, cluster_id, region)


def export_inspection_report(region: str, cluster_id: str, output_file: str = None,
                             ak: str = None, sk: str = None) -> Dict[str, Any]:
    """导出巡检报告到文件"""
    if output_file is None:
        output_file = f"/tmp/cce_inspection_report_{cluster_id[:8]}.html"

    inspection_result = cce_cluster_inspection(region, cluster_id, ak, sk)

    if inspection_result.get("success") and inspection_result.get("html_report"):
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(inspection_result["html_report"])
        return {
            "success": True, "message": "HTML巡检报告已生成", "file": output_file,
            "cluster_id": cluster_id,
            "inspection_time": inspection_result.get("inspection_time"),
            "status": inspection_result.get("result", {}).get("status"),
            "total_issues": inspection_result.get("result", {}).get("total_issues"),
            "critical_issues": inspection_result.get("result", {}).get("critical_issues"),
            "warning_issues": inspection_result.get("result", {}).get("warning_issues")
        }
    return inspection_result
