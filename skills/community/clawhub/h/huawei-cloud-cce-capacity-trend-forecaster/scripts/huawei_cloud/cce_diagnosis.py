#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCE 集群诊断工具

功能：
- 网络诊断：基于告警或工作负载进行诊断，分析链路（Service、Ingress、Nginx-Ingress、ELB、NAT、EIP）
- 节点诊断：批量诊断节点，分析节点状态、事件、监控、告警

使用方式：
    # 网络诊断
    python cce_diagnosis.py network_diagnose region=cn-north-4 cluster_id=xxx workload_name=xxx namespace=default
    python cce_diagnosis.py network_diagnose_by_alarm region=cn-north-4 cluster_id=xxx alarm_info=xxx
    
    # 节点诊断
    python cce_diagnosis.py node_diagnose region=cn-north-4 cluster_id=xxx node_ips=192.168.1.10
    python cce_diagnosis.py node_batch_diagnose region=cn-north-4 cluster_id=xxx
"""

from __future__ import annotations

import os
import sys
import json
import time
import warnings
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List, Tuple

warnings.filterwarnings('ignore')


# ========== 导入 ==========

from .common import create_cce_client, get_credentials_with_region, get_project_id_for_region
from .cce import (
    get_cce_kubeconfig,
    get_kubernetes_deployments,
    get_kubernetes_events,
    get_kubernetes_ingresses,
    get_kubernetes_namespaces,
    get_kubernetes_nodes,
    get_kubernetes_pods,
    get_kubernetes_services,
    list_cce_addons,
    list_cce_cluster_nodes,
    list_cce_clusters,
    list_cce_node_pools,
    scale_cce_workload,
    resize_node_pool,
)
from .aom import get_aom_prom_metrics_http, list_aom_instances
from .elb import get_elb_metrics
from .network import get_eip_metrics, list_eip_addresses, list_nat_gateways, list_security_groups, list_vpc_networks
from .cce_metrics import get_cce_node_metrics, get_cce_pod_metrics_topN


# ========== 配置 ==========

REPORT_DIR = "/root/.openclaw/workspace/report"
BATCH_SIZE = 5
MAX_NODES_ONCE = 10


# ============================================================================
# 第一部分：网络诊断函数
# ============================================================================

def get_aom_instance(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """仅从当前集群的 cie-collector 插件配置中获取 aom_instance_id。拿不到就返回错误。"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        if not access_key or not secret_key:
            return {"success": False, "error": "Credentials are required"}
        if not cluster_id:
            return {"success": False, "error": "cluster_id is required"}

        client = create_cce_client(region, access_key, secret_key, proj_id)
        from huaweicloudsdkcce.v3 import ListAddonInstancesRequest, ShowAddonInstanceRequest

        list_req = ListAddonInstancesRequest()
        list_req.cluster_id = cluster_id
        list_resp = client.list_addon_instances(list_req)

        cie_addon_id = None
        if hasattr(list_resp, 'items') and list_resp.items:
            for addon in list_resp.items:
                addon_name = addon.metadata.name if hasattr(addon, 'metadata') and hasattr(addon.metadata, 'name') else None
                if addon_name == 'cie-collector':
                    cie_addon_id = addon.metadata.uid if hasattr(addon.metadata, 'uid') else None
                    break

        if not cie_addon_id:
            return {"success": False, "error": "cie-collector addon not found in cluster"}

        show_req = ShowAddonInstanceRequest()
        show_req.cluster_id = cluster_id
        show_req.id = cie_addon_id
        show_resp = client.show_addon_instance(show_req)
        addon_detail = show_resp.to_dict() if hasattr(show_resp, 'to_dict') else {}

        detail_root = addon_detail.get('addon_instance', addon_detail) if isinstance(addon_detail, dict) else {}
        spec = detail_root.get('spec', {}) or {}
        custom = spec.get('custom', {}) or {}

        if isinstance(custom, dict):
            aom_instance_id = custom.get('aom_instance_id')
            if aom_instance_id:
                return {"success": True, "aom_instance_id": aom_instance_id, "source": "cie-collector.spec.custom.aom_instance_id"}

        values = spec.get('values')
        if isinstance(values, dict):
            aom_instance_id = values.get('aom_instance_id')
            if aom_instance_id:
                return {"success": True, "aom_instance_id": aom_instance_id, "source": "cie-collector.spec.values.aom_instance_id"}

            nested_custom = values.get('custom') or {}
            if isinstance(nested_custom, dict):
                aom_instance_id = nested_custom.get('aom_instance_id')
                if aom_instance_id:
                    return {"success": True, "aom_instance_id": aom_instance_id, "source": "cie-collector.spec.values.custom.aom_instance_id"}

        return {"success": False, "error": "aom_instance_id not found in cie-collector addon config"}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": type(e).__name__}


def get_cluster_name(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> str:
    """获取集群名称"""
    result = list_cce_clusters(region, ak, sk, project_id)
    if result.get("success") and result.get("clusters"):
        for cluster in result.get("clusters", []):
            if cluster.get("id") == cluster_id:
                return cluster.get("name", cluster_id)
    return cluster_id


# ============================================================================
# 工作负载诊断函数（第一部分补充）
# ============================================================================

def get_workload_pods(region: str, cluster_id: str, workload_name: str, namespace: str,
                      ak: str, sk: str, project_id: str = None) -> List[Dict]:
    """获取工作负载对应的 Pod 列表"""
    pods_result = get_kubernetes_pods(region, cluster_id, ak, sk, project_id, namespace)
    target_pods = []

    if pods_result.get("success") and pods_result.get("pods"):
        for pod in pods_result.get("pods", []):
            if workload_name in pod.get("name", ""):
                target_pods.append(pod)

    return target_pods


def get_namespace_workloads(region: str, cluster_id: str, namespace: str,
                            ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """获取命名空间下的所有工作负载信息"""
    result = {
        "deployments": [],
        "statefulsets": [],
        "pods": []
    }

    # 获取 Deployments
    dep_result = get_kubernetes_deployments(region, cluster_id, ak, sk, project_id, namespace)
    if dep_result.get("success") and dep_result.get("items"):
        for dep in dep_result.get("items", []):
            result["deployments"].append({
                "name": dep.get("name"),
                "replicas": dep.get("replicas"),
                "ready_replicas": dep.get("ready_replicas", 0),
                "available_replicas": dep.get("available_replicas", 0),
                "unavailable_replicas": dep.get("unavailable_replicas", 0),
                "creation_timestamp": dep.get("creation_timestamp"),
                "images": list(set([c.get("image") for c in dep.get("containers", [])]))
            })

    # 获取所有 Pods
    pods_result = get_kubernetes_pods(region, cluster_id, ak, sk, project_id, namespace)
    if pods_result.get("success") and pods_result.get("pods"):
        for pod in pods_result.get("pods", []):
            result["pods"].append({
                "name": pod.get("name"),
                "status": pod.get("status"),
                "ready": pod.get("ready"),
                "restart_count": pod.get("restart_count", 0),
                "node_ip": pod.get("host_ip") or pod.get("node"),
                "pod_ip": pod.get("ip"),
                "age": pod.get("age"),
                "creation_timestamp": pod.get("creation_timestamp")
            })

    return result


def analyze_pod_status(pod: Dict) -> Dict[str, Any]:
    """分析 Pod 状态，返回异常类型和可能的原因"""
    status = pod.get("status", "")
    ready = pod.get("ready", "")
    restart_count = pod.get("restart_count", 0)

    analysis = {
        "status": status,
        "is_abnormal": False,
        "abnormal_type": None,
        "possible_cause": None,
        "suggestion": None
    }

    if "Pending" in status:
        analysis["is_abnormal"] = True
        analysis["abnormal_type"] = "Pending"
        analysis["possible_cause"] = "实例调度失败/存储卷挂载失败/添加存储失败"
        analysis["suggestion"] = "参考: https://support.huaweicloud.com/cce_faq/cce_faq_00098.html"
    elif "ImagePullBackOff" in status or "ErrImagePull" in status:
        analysis["is_abnormal"] = True
        analysis["abnormal_type"] = "ImagePullBackOff"
        analysis["possible_cause"] = "镜像拉取失败"
        analysis["suggestion"] = "参考: https://support.huaweicloud.com/cce_faq/cce_faq_00015.html"
    elif "CrashLoopBackOff" in status:
        analysis["is_abnormal"] = True
        analysis["abnormal_type"] = "CrashLoopBackOff"
        analysis["possible_cause"] = "容器启动失败/健康检查失败/重启"
        analysis["suggestion"] = "参考: https://support.huaweicloud.com/cce_faq/cce_faq_00018.html"
    elif "Evicted" in status:
        analysis["is_abnormal"] = True
        analysis["abnormal_type"] = "Evicted"
        analysis["possible_cause"] = "Pod被驱逐（资源限制导致）"
        analysis["suggestion"] = "参考: https://support.huaweicloud.com/cce_faq/cce_faq_00209.html"
    elif "Creating" in status:
        analysis["is_abnormal"] = True
        analysis["abnormal_type"] = "Creating"
        analysis["possible_cause"] = "实例一直处于创建中"
        analysis["suggestion"] = "参考: https://support.huaweicloud.com/cce_faq/cce_faq_00140.html"
    elif "Terminating" in status:
        analysis["is_abnormal"] = True
        analysis["abnormal_type"] = "Terminating"
        analysis["possible_cause"] = "Pod一直处于结束中"
        analysis["suggestion"] = "参考: https://support.huaweicloud.com/cce_faq/cce_faq_00210.html"
    elif "Stopped" in status:
        analysis["is_abnormal"] = True
        analysis["abnormal_type"] = "Stopped"
        analysis["possible_cause"] = "实例已停止"
        analysis["suggestion"] = "参考: https://support.huaweicloud.com/cce_faq/cce_faq_00012.html"
    elif "Running" in status:
        if ready and "0/" in ready:
            analysis["is_abnormal"] = True
            analysis["abnormal_type"] = "NotReady"
            analysis["possible_cause"] = "容器未就绪"
        elif restart_count > 5:
            analysis["is_abnormal"] = True
            analysis["abnormal_type"] = "FrequentRestart"
            analysis["possible_cause"] = f"容器频繁重启（{restart_count}次）"

    # 检查 Init 容器状态
    init_status = pod.get("init_container_status", [])
    if init_status:
        for init in init_status:
            if "Error" in init.get("state", {}) or "CrashLoopBackOff" in init.get("state", {}):
                analysis["is_abnormal"] = True
                analysis["abnormal_type"] = "InitContainerError"
                analysis["possible_cause"] = "Init容器启动失败"
                analysis["suggestion"] = "参考: https://support.huaweicloud.com/cce_faq/cce_faq_00469.html"

    return analysis


def get_pod_events_for_diagnosis(region: str, cluster_id: str, pod_name: str, namespace: str,
                                  ak: str, sk: str, project_id: str = None) -> List[Dict]:
    """获取 Pod 的事件用于诊断"""
    events_result = get_kubernetes_events(region, cluster_id, ak, sk, project_id, namespace, limit=100)
    target_events = []

    if events_result.get("success") and events_result.get("events"):
        for event in events_result.get("events", []):
            involved = event.get("involved_object", {})
            if pod_name in involved.get("name", ""):
                target_events.append({
                    "type": event.get("type"),
                    "reason": event.get("reason"),
                    "message": event.get("message"),
                    "first_timestamp": event.get("first_timestamp"),
                    "last_timestamp": event.get("last_timestamp"),
                    "count": event.get("count", 1)
                })

    return target_events


def get_workload_alarms(region: str, cluster_name: str, namespace: str, workload_name: str,
                        ak: str, sk: str, project_id: str = None, hours: int = 1) -> List[Dict]:
    """获取工作负载相关的告警信息（近 N 小时）"""
    alarms = []

    aom_instance_id = get_aom_instance(region, "", ak, sk, project_id)
    if aom_instance_id and aom_instance_id.get("success"):
        aom_id = aom_instance_id.get("aom_instance_id")
        query = f'alertmetric{{cluster_name="{cluster_name}",namespace="{namespace}",pod=~"{workload_name}.*"}}'
        try:
            result = get_aom_prom_metrics_http(region, aom_id, query, hours=hours, ak=ak, sk=sk, project_id=project_id)
            if result.get("success") and result.get("data"):
                alarms.extend(result.get("data", []))
        except Exception:
            pass

    return alarms


def analyze_change_correlation(workload_info: Dict, events: List[Dict],
                                fault_time: str = None) -> Dict[str, Any]:
    """分析变更与故障的关联性"""
    correlation = {
        "has_correlation": False,
        "changes": [],
        "analysis": ""
    }

    if not fault_time:
        fault_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        fault_dt = datetime.strptime(fault_time, '%Y-%m-%d %H:%M:%S')
    except Exception:
        fault_dt = datetime.now()

    change_events = []
    for event in events:
        reason = event.get("reason", "")
        message = event.get("message", "")

        if any(keyword in reason.lower() or keyword in message.lower()
               for keyword in ["scaled", "created", "updated", "deleted", "restarted", "scaling", "pull", "kill", "schedule"]):
            change_events.append({
                "reason": reason,
                "message": message,
                "timestamp": event.get("last_timestamp")
            })

    if change_events:
        correlation["has_correlation"] = True
        correlation["changes"] = change_events
        correlation["analysis"] = f"发现{len(change_events)}个变更事件可能与故障相关"

    return correlation


def generate_diagnosis_report(diagnosis_data: Dict) -> Dict[str, Any]:
    """生成综合诊断报告"""
    report = {
        "report_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "region": diagnosis_data.get("region"),
        "cluster_id": diagnosis_data.get("cluster_id"),
        "cluster_name": diagnosis_data.get("cluster_name"),
        "workloads": {},
        "abnormal_pods": [],
        "node_diagnosis": {},
        "network_diagnosis": {},
        "change_correlation": {},
        "alarms": [],
        "operations": [],
        "conclusions": [],
        "recommendations": []
    }

    workloads = diagnosis_data.get("workloads", {})
    report["workloads"] = {
        "total_deployments": len(workloads.get("deployments", [])),
        "total_pods": len(workloads.get("pods", [])),
        "details": workloads
    }

    abnormal_pods = diagnosis_data.get("abnormal_pods", [])
    report["abnormal_pods"] = abnormal_pods

    # 节点诊断结果
    node_diag = diagnosis_data.get("node_diagnosis", {})
    if node_diag.get("success"):
        report["node_diagnosis"] = {
            "status": "completed",
            "abnormal_nodes": node_diag.get("abnormal_nodes", []),
            "summary": node_diag.get("summary", {})
        }

    # 网络诊断结果
    network_diag = diagnosis_data.get("network_diagnosis", {})
    if network_diag.get("success"):
        report["network_diagnosis"] = {
            "status": "completed",
            "chain": network_diag.get("chain", {}),
            "analysis": network_diag.get("analysis", {})
        }

    report["change_correlation"] = diagnosis_data.get("change_correlation", {})
    report["alarms"] = diagnosis_data.get("alarms", [])
    report["operations"] = diagnosis_data.get("operations", [])

    # 生成结论和建议
    if abnormal_pods:
        abnormal_types = [p.get("analysis", {}).get("abnormal_type") for p in abnormal_pods]
        most_common = max(set(abnormal_types), key=abnormal_types.count) if abnormal_types else "Unknown"

        report["conclusions"].append(f"发现{len(abnormal_pods)}个异常Pod，最常见的异常类型为: {most_common}")

        if most_common == "Pending":
            report["recommendations"].append({
                "priority": "HIGH",
                "issue": "Pod调度失败",
                "suggestion": "检查节点资源是否充足，确认节点可用性"
            })
        elif most_common == "CrashLoopBackOff":
            report["recommendations"].append({
                "priority": "HIGH",
                "issue": "容器启动失败",
                "suggestion": "检查容器配置、健康检查、镜像是否正常"
            })
        elif most_common == "ImagePullBackOff":
            report["recommendations"].append({
                "priority": "HIGH",
                "issue": "镜像拉取失败",
                "suggestion": "检查镜像地址、仓库认证、网络连接"
            })

    if node_diag.get("abnormal_nodes"):
        report["recommendations"].append({
            "priority": "MEDIUM",
            "issue": "节点异常",
            "suggestion": f"发现{len(node_diag.get('abnormal_nodes', []))}个异常节点，建议检查节点状态"
        })

    # Top3 根因分析
    report["top3_root_causes"] = []
    if abnormal_pods:
        causes = []
        for pod in abnormal_pods[:5]:
            cause = pod.get("analysis", {}).get("possible_cause")
            if cause:
                causes.append(cause)

        if causes:
            cause_count = {}
            for c in causes:
                cause_count[c] = cause_count.get(c, 0) + 1

            top_causes = sorted(cause_count.items(), key=lambda x: x[1], reverse=True)[:3]
            for cause, count in top_causes:
                report["top3_root_causes"].append({
                    "cause": cause,
                    "affected_count": count
                })

    return report


def get_target_pods(region: str, cluster_id: str, workload_name: str, namespace: str,
                    ak: str, sk: str, project_id: str = None) -> List[Dict]:
    """获取目标工作负载的 Pod 列表"""
    pods_result = get_kubernetes_pods(region, cluster_id, ak, sk, project_id, namespace)
    target_pods = []

    if pods_result.get("success") and pods_result.get("pods"):
        for pod in pods_result.get("pods", []):
            # 匹配工作负载名称（Pod名称通常以deploymentname-xxx格式）
            if workload_name in pod.get("name", ""):
                target_pods.append(pod)

    return target_pods


def get_pod_metrics(pod_name: str, namespace: str, cluster_name: str,
                    aom_instance_id: str, region: str, ak: str, sk: str,
                    project_id: str = None, hours: int = 1) -> Dict[str, Any]:
    """获取Pod的CPU和内存监控数据（近一个小时）"""
    metrics_result = {
        "cpu": {},
        "memory": {}
    }

    try:
        # CPU 使用率查询
        cpu_query = f'sum(rate(container_cpu_usage_seconds_total{{cluster_name="{cluster_name}",namespace="{namespace}",pod=~"{pod_name}.*"}}[5m])) by (pod) * 100'
        cpu_result = get_aom_prom_metrics_http(
            region, aom_instance_id, cpu_query, hours=hours,
            ak=ak, sk=sk, project_id=project_id
        )
        if cpu_result.get("success"):
            metrics_result["cpu"] = cpu_result

        # 内存使用率查询
        mem_query = f'container_memory_working_set_bytes{{cluster_name="{cluster_name}",namespace="{namespace}",pod=~"{pod_name}.*"}}'
        mem_result = get_aom_prom_metrics_http(
            region, aom_instance_id, mem_query, hours=hours,
            ak=ak, sk=sk, project_id=project_id
        )
        if mem_result.get("success"):
            metrics_result["memory"] = mem_result

    except Exception as e:
        metrics_result["error"] = str(e)

    return metrics_result


def get_node_metrics(node_ip: str, region: str, cluster_id: str = "", ak: str = None, sk: str = None,
                    project_id: str = None, hours: int = 1) -> Dict[str, Any]:
    """获取节点监控指标"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
        aom_id = aom_result.get("aom_instance_id", "") if aom_result.get("success") else ""

        cpu_query = f'100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode="idle",instance="{node_ip}"}}[5m])) * 100)'
        memory_query = f'(1 - (node_memory_MemAvailable_bytes{{instance="{node_ip}"}} / node_memory_MemTotal_bytes{{instance="{node_ip}"}})) * 100'
        disk_query = f'(1 - (node_filesystem_avail_bytes{{mountpoint="/",instance="{node_ip}"}} / node_filesystem_size_bytes{{mountpoint="/",instance="{node_ip}"}})) * 100'

        cpu_result = get_aom_prom_metrics_http(region, aom_id, cpu_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
        memory_result = get_aom_prom_metrics_http(region, aom_id, memory_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
        disk_result = get_aom_prom_metrics_http(region, aom_id, disk_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)

        metrics_result = {
            "cpu": cpu_result.get("result", {}).get("data", {}),
            "memory": memory_result.get("result", {}).get("data", {}),
            "disk": disk_result.get("result", {}).get("data", {})
        }

        # 网络流量
        try:
            net_query = f'rate(node_network_receive_bytes_total{{instance="{node_ip}"}}[5m])'
            net_result = get_aom_prom_metrics_http(region, aom_id, net_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
            if net_result.get("success"):
                metrics_result["network"] = net_result
        except Exception:
            pass

        return {
            "success": True,
            **metrics_result
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_service_chain(workload_name: str, namespace: str, region: str, cluster_id: str,
                      ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """获取工作负载的完整服务链路"""
    chain = {
        "workload": {"name": workload_name, "namespace": namespace},
        "pods": [],
        "service": None,
        "ingress": None,
        "nginx_ingress": None,
        "elb": None,
        "eip": None,
        "nat": None,
        "nodes": []
    }

    # 获取Pods
    pods_result = get_kubernetes_pods(region, cluster_id, ak, sk, project_id, namespace)
    if pods_result.get("success") and pods_result.get("pods"):
        for pod in pods_result.get("pods", []):
            if workload_name in pod.get("name", ""):
                chain["pods"].append({
                    "name": pod.get("name"),
                    "status": pod.get("status"),
                    "node_ip": pod.get("host_ip") or pod.get("node"),
                    "ip": pod.get("ip"),
                    "restarts": pod.get("restart_count", 0)
                })
                if (pod.get("host_ip") or pod.get("node")) and (pod.get("host_ip") or pod.get("node")) not in chain["nodes"]:
                    chain["nodes"].append(pod.get("host_ip") or pod.get("node"))

    # 获取Service
    services_result = get_kubernetes_services(region, cluster_id, ak, sk, project_id, namespace)
    if services_result.get("success") and services_result.get("services"):
        for svc in services_result.get("services", []):
            selector = svc.get("selector") or {}
            if (selector and workload_name in selector.values()) or workload_name in svc.get("name", ""):
                chain["service"] = {
                    "name": svc.get("name"),
                    "type": svc.get("type"),
                    "cluster_ip": svc.get("cluster_ip"),
                    "load_balancer_ip": svc.get("load_balancer_ip"),
                    "ports": svc.get("ports", []),
                    "annotations": svc.get("annotations", {})
                }

                # 如果是LoadBalancer类型，获取ELB信息
                if svc.get("type") == "LoadBalancer":
                    annotations = svc.get("annotations", {})
                    elb_id = annotations.get("kubernetes.io/elb.id")
                    if elb_id:
                        chain["elb"] = {
                            "id": elb_id,
                            "ip": svc.get("load_balancer_ip"),
                            "service": svc.get("name")
                        }

    # 获取Ingress
    ingress_result = get_kubernetes_ingresses(region, cluster_id, ak, sk, project_id, namespace)
    if ingress_result.get("success") and ingress_result.get("ingresses"):
        for ing in ingress_result.get("ingresses", []):
            # 检查ingress的backend是否关联到目标service
            http_rules = ing.get("http_rules", [])
            for rule in http_rules:
                backend = rule.get("backend", {})
                service_name = backend.get("service", {}).get("name")
                if service_name == workload_name or service_name == chain["service"]["name"]:
                    chain["ingress"] = {
                        "name": ing.get("name"),
                        "namespace": ing.get("namespace"),
                        "rules": ing.get("rules", []),
                        "tls": ing.get("tls", [])
                    }
                    # 尝试获取nginx-ingress信息
                    annotations = ing.get("annotations", {})
                    if "nginx" in str(annotations).lower():
                        chain["nginx_ingress"] = {
                            "name": ing.get("name"),
                            "annotations": annotations
                        }

    # 如果有ELB，尝试获取EIP信息
    if chain.get("elb") and chain["elb"].get("ip"):
        eip_result = list_eip_addresses(region, ak, sk, project_id)
        if eip_result.get("success") and eip_result.get("eips"):
            for eip in eip_result.get("eips", []):
                if eip.get("ip_address") == chain["elb"].get("ip"):
                    chain["eip"] = {
                        "id": eip.get("id"),
                        "ip_address": eip.get("ip_address"),
                        "bandwidth": eip.get("bandwidth_size"),
                        "type": eip.get("type")
                    }
                    break

    # 检查NAT网关
    if chain.get("service") and chain["service"].get("type") == "LoadBalancer":
        nat_result = list_nat_gateways(region, ak, sk, project_id)
        if nat_result.get("success") and nat_result.get("nat_gateways"):
            chain["nat"] = {
                "count": len(nat_result.get("nat_gateways", [])),
                "note": "NAT网关存在，但无法确定是否与该工作负载直接关联",
                "gateways": [{
                    "id": nat.get("id"),
                    "name": nat.get("name"),
                    "status": nat.get("status")
                } for nat in nat_result.get("nat_gateways", [])[:3]]
            }
        else:
            chain["nat"] = None
    else:
        chain["nat"] = None

    return chain


def analyze_chain_components(chain: Dict, region: str, ak: str, sk: str,
                            project_id: str = None) -> Dict[str, Any]:
    """分析链路所有组件的监控和告警"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

        analysis = {
            "elb": {"status": "N/A", "metrics": {}, "alerts": []},
            "eip": {"status": "N/A", "metrics": {}, "alerts": []},
            "nat": {"status": "N/A", "metrics": {}, "alerts": []},
            "nodes": {},
            "nginx_ingress": {"status": "N/A", "metrics": {}, "alerts": []}
        }

        # 分析 ELB
        elb_data = chain.get("elb")
        if elb_data and elb_data.get("id"):
            elb_id = elb_data.get("id")
            elb_metrics = get_elb_metrics(region, elb_id, access_key, secret_key, proj_id)
            if elb_metrics.get("success"):
                summary = elb_metrics.get("summary", {})
                analysis["elb"] = {
                    "status": "WARNING" if summary.get("l4_bandwidth_usage_percent", 0) > 80 else "OK",
                    "metrics": {
                        "connection_num": summary.get("connection_num"),
                        "bandwidth_usage_percent": summary.get("l4_bandwidth_usage_percent"),
                        "connection_usage_percent": summary.get("l4_connection_usage_percent"),
                        "normal_servers": summary.get("normal_servers"),
                        "abnormal_servers": summary.get("abnormal_servers")
                    },
                    "alerts": []
                }

                # 检查告警阈值
                if summary.get("l4_bandwidth_usage_percent", 0) > 80:
                    analysis["elb"]["alerts"].append(f"ELB带宽使用率已达 {summary.get('l4_bandwidth_usage_percent')}%")
                if summary.get("l4_connection_usage_percent", 0) > 80:
                    analysis["elb"]["alerts"].append(f"ELB连接使用率已达 {summary.get('l4_connection_usage_percent')}%")
                if summary.get("abnormal_servers", 0) > 0:
                    analysis["elb"]["alerts"].append(f"ELB后端有 {summary.get('abnormal_servers')} 个异常服务器")

        # 分析 EIP
        eip_data = chain.get("eip")
        if eip_data and eip_data.get("id"):
            eip_id = eip_data.get("id")
            eip_metrics = get_eip_metrics(region, eip_id, access_key, secret_key, proj_id)
            if eip_metrics.get("success"):
                summary = eip_metrics.get("summary", {})
                analysis["eip"] = {
                    "status": "WARNING" if summary.get("bw_usage_in_percent", 0) > 80 else "OK",
                    "metrics": {
                        "bw_usage_in_percent": summary.get("bw_usage_in_percent"),
                        "bw_usage_out_percent": summary.get("bw_usage_out_percent")
                    },
                    "alerts": []
                }

                if summary.get("bw_usage_in_percent", 0) > 80:
                    analysis["eip"]["alerts"].append(f"EIP入带宽使用率已达 {summary.get('bw_usage_in_percent')}%")
                if summary.get("bw_usage_out_percent", 0) > 80:
                    analysis["eip"]["alerts"].append(f"EIP出带宽使用率已达 {summary.get('bw_usage_out_percent')}%")

        # 分析节点
        for node_ip in chain.get("nodes", []):
            node_metrics = get_node_metrics(node_ip, region, cluster_id, access_key, secret_key, proj_id)
            analysis["nodes"][node_ip] = node_metrics

        return {"success": True, "analysis": analysis}
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_coredns_status(region: str, cluster_id: str, ak: str, sk: str,
                         project_id: str = None) -> Dict[str, Any]:
    """检查 CoreDNS 的状态和监控"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

        result = {
            "status": "OK",
            "pods": [],
            "metrics": {},
            "alerts": [],
            "config": {}
        }

        # 获取kubeconfig
        kubeconfig_result = get_cce_kubeconfig(region, cluster_id, access_key, secret_key, proj_id)
        if not kubeconfig_result.get("success"):
            return {"success": False, "error": "Failed to get kubeconfig"}

        kubeconfig = kubeconfig_result.get("kubeconfig")
        import yaml
        try:
            if "current_context" in kubeconfig:
                kubeconfig["current-context"] = kubeconfig.pop("current_context")
            with open("/tmp/kubeconfig_" + cluster_id[:8] + ".yaml", 'w') as f:
                yaml.dump(kubeconfig, f, default_flow_style=False, allow_unicode=True)
        except Exception:
            pass

        try:
            from kubernetes import client, config
            config.load_kube_config(config_file="/tmp/kubeconfig_" + cluster_id[:8] + ".yaml")
            v1 = client.CoreV1Api()

            coredns_items = []
            seen_pod_uids = set()
            for selector in ("k8s-app=coredns", "k8s-app=kube-dns", "app=coredns"):
                selected_pods = v1.list_namespaced_pod("kube-system", label_selector=selector)
                for pod in selected_pods.items:
                    uid = getattr(pod.metadata, "uid", None) or pod.metadata.name
                    if uid in seen_pod_uids:
                        continue
                    seen_pod_uids.add(uid)
                    coredns_items.append(pod)
            coredns_pods = []
            for pod in coredns_items:
                coredns_pods.append({
                    "name": pod.metadata.name,
                    "ready": str(pod.status.conditions[-1].status if pod.status.conditions else "Unknown"),
                    "restarts": sum(c.restart_count for c in pod.status.container_statuses),
                    "age": str(pod.metadata.creation_timestamp)
                })
                result["pods"].append({
                    "name": pod.metadata.name,
                    "status": pod.status.phase,
                    "ready": str(pod.status.conditions[-1].status if pod.status.conditions else "Unknown"),
                    "restarts": sum(c.restart_count for c in pod.status.container_statuses)
                })

                if "Error" in str(pod.status.phase) or "CrashLoopBackOff" in str(pod.status.phase):
                    result["status"] = "ERROR"
                    result["alerts"].append(f"CoreDNS Pod {pod.metadata.name} 状态异常: {pod.status.phase}")

            result["pods"] = coredns_pods
            result["count"] = len(coredns_pods)
        except Exception as e:
            result["error"] = str(e)

        # 获取CoreDNS addon信息
        addons_result = list_cce_addons(region, cluster_id, access_key, secret_key, proj_id)
        if addons_result.get("success") and addons_result.get("addons"):
            for addon in addons_result.get("addons", []):
                if "coredns" in addon.get("name", "").lower():
                    result["config"] = {
                        "name": addon.get("name"),
                        "version": addon.get("version"),
                        "status": addon.get("status")
                    }

        # 如果有AOM，获取CoreDNS的监控指标
        aom_id_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
        if aom_id_result.get("success"):
            aom_instance_id = aom_id_result.get("aom_instance_id")
            cluster_name = get_cluster_name(region, cluster_id, access_key, secret_key, proj_id)

            # CoreDNS请求监控
            dns_query = 'sum(rate(coredns_dns_requests_total[5m])) by (pod)'
            dns_result = get_aom_prom_metrics_http(region, aom_instance_id, dns_query, hours=1, ak=access_key, sk=secret_key, project_id=proj_id)
            if dns_result.get("success"):
                result["metrics"]["requests"] = dns_result

            # CoreDNS错误监控
            error_query = 'sum(rate(coredns_dns_responses_total{rcode!~"NOERROR|Success"}[5m])) by (pod)'
            error_result = get_aom_prom_metrics_http(region, aom_instance_id, error_query, hours=1, ak=access_key, sk=secret_key, project_id=proj_id)
            if error_result.get("success"):
                result["metrics"]["errors"] = error_result

        return {"success": True, **result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_pod_events(workload_name: str, namespace: str, region: str, cluster_id: str,
                   ak: str, sk: str, project_id: str = None) -> List[Dict]:
    """获取工作负载相关的事件"""
    events_result = get_kubernetes_events(region, cluster_id, ak, sk, project_id, namespace, limit=500)
    target_events = []

    if events_result.get("success") and events_result.get("events"):
        for event in events_result.get("events", []):
            # 匹配相关Pod的事件
            if workload_name in event.get("involved_object", {}).get("name", ""):
                target_events.append({
                    "type": event.get("type"),
                    "reason": event.get("reason"),
                    "message": event.get("message"),
                    "first_timestamp": event.get("first_timestamp"),
                    "last_timestamp": event.get("last_timestamp"),
                    "count": event.get("count", 1)
                })

    return target_events


def generate_network_topology(chain: Dict, analysis: Dict) -> str:
    """生成网络拓扑图（文本格式）"""
    topology = []
    topology.append("=" * 60)
    topology.append("网络链路拓扑图")
    topology.append("=" * 60)

    # 绘制链路
    components = []

    # 用户/外部流量
    topology.append("[外部流量] → ")

    # EIP
    if chain.get("eip"):
        status = "🔴" if analysis.get("eip", {}).get("status") == "WARNING" else "🟢"
        components.append(f"{status}[EIP: {chain['eip'].get('ip_address')}]")

    # ELB
    if chain.get("elb"):
        status = "🔴" if analysis.get("elb", {}).get("status") == "WARNING" else "🟢"
        components.append(f"{status}[ELB: {chain['elb'].get('id')[:8]}...]")

    # NAT (如果有)
    if chain.get("nat") and chain["nat"].get("count", 0) > 0:
        components.append(f"[NAT Gateway]")

    # Nginx Ingress
    if chain.get("nginx_ingress"):
        components.append(f"[Nginx Ingress Controller]")

    # Ingress
    if chain.get("ingress"):
        components.append(f"[Ingress: {chain['ingress'].get('name')}]")

    # Service
    if chain.get("service"):
        svc_type = chain["service"].get("type", "ClusterIP")
        components.append(f"[Service: {chain['service'].get('name')} ({svc_type})]")

    # Workload (Pods)
    pod_count = len(chain.get("pods", []))
    components.append(f"[Workload: {chain['workload'].get('name')}] ({pod_count} pods)")

    # Nodes
    if chain.get("nodes"):
        components.append(f"  └─ 部署节点: {', '.join(chain['nodes'])}")

    topology.append(" → ".join(components))

    # 告警摘要
    all_alerts = []
    if analysis.get("elb", {}).get("alerts"):
        all_alerts.extend(analysis["elb"]["alerts"])
    if analysis.get("eip", {}).get("alerts"):
        all_alerts.extend(analysis["eip"]["alerts"])
    if analysis.get("nodes"):
        for node_ip, node_data in analysis["nodes"].items():
            if node_data.get("error"):
                all_alerts.append(f"节点 {node_ip} 监控获取失败")

    if all_alerts:
        topology.append("\n\n⚠️ 告警摘要:")
        for alert in all_alerts:
            topology.append(f"  - {alert}")

    return "\n".join(topology)


def network_diagnose(region: str, cluster_id: str, workload_name: str = None,
                    namespace: str = "default", ak: str = None, sk: str = None,
                    project_id: str = None) -> Dict[str, Any]:
    """网络诊断主函数"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        if not access_key or not secret_key:
            return {"success": False, "error": "Credentials are required"}

        # 获取集群名称
        cluster_name = get_cluster_name(region, cluster_id, access_key, secret_key, proj_id)

        # 获取 AOM 实例
        aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
        if not aom_result.get("success"):
            return {"success": False, "error": "Failed to get AOM instance", "details": aom_result.get("error")}

        aom_instance_id = aom_result.get("aom_instance_id")

        # 初始化诊断报告
        report = {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "cluster_name": cluster_name,
            "workload_name": workload_name,
            "namespace": namespace,
            "diagnosis_time": datetime.now().isoformat(),
            "steps_completed": [],
            "workload_info": {},
            "chain": {},
            "chain_analysis": {},
            "coredns_status": {},
            "events": [],
            "topology": "",
            "operations": [],
            "recommendations": []
        }

        # ===== 步骤1: 分析工作负载的监控和告警 =====
        if workload_name:
            report["steps_completed"].append("1. 分析工作负载监控和告警")

            # 获取目标Pods
            target_pods = get_target_pods(region, cluster_id, workload_name, namespace, access_key, secret_key, proj_id)
            report["workload_info"]["pods"] = target_pods
            report["workload_info"]["pod_count"] = len(target_pods)

            if target_pods and aom_instance_id:
                # 获取监控数据
                pod_metrics = get_pod_metrics(workload_name, namespace, cluster_name, aom_instance_id,
                                              region, access_key, secret_key, proj_id)
                report["workload_info"]["metrics"] = pod_metrics

                # 分析是否有CPU/内存异常
                cpu_data = pod_metrics.get("cpu", {}).get("data", {}).get("result", [])
                if cpu_data:
                    cpu_values = []
                    for item in cpu_data:
                        values = item.get("values", [])
                        if values:
                            cpu_values.append(float(values[-1][1]) if len(values) > 0 else 0)

                    if cpu_values:
                        avg_cpu = sum(cpu_values) / len(cpu_values)
                        if avg_cpu > 80:
                            report["recommendations"].append({
                                "category": "CPU告警",
                                "issue": f"工作负载平均CPU使用率 {avg_cpu:.1f}%",
                                "suggestion": "建议扩容工作负载实例或增加CPU资源限制"
                            })

            # 获取工作负载的事件
            events = get_pod_events(workload_name, namespace, region, cluster_id, access_key, secret_key, proj_id)
            report["events"] = events

            if events:
                error_events = [e for e in events if e.get("type") in ["Warning", "Error"]]
                if error_events:
                    report["workload_info"]["has_error_events"] = True
                    report["workload_info"]["error_events"] = error_events[:10]

        # ===== 步骤2: 梳理工作负载的链路 =====
        if workload_name:
            report["steps_completed"].append("2. 梳理工作负载链路")

            chain = get_service_chain(workload_name, namespace, region, cluster_id, access_key, secret_key, proj_id)
            report["chain"] = chain

            # ===== 步骤3: 分析链路组件的监控和告警 =====
            report["steps_completed"].append("3. 分析链路组件监控和告警")

            chain_analysis_result = analyze_chain_components(chain, region, access_key, secret_key, proj_id)
            report["chain_analysis"] = chain_analysis_result.get("analysis", {})
            analysis = report["chain_analysis"]

            # 根据分析结果添加建议
            if analysis.get("elb", {}).get("alerts"):
                for alert in analysis["elb"]["alerts"]:
                    report["recommendations"].append({
                        "category": "ELB",
                        "issue": alert,
                        "suggestion": "考虑扩容ELB带宽或规格"
                    })

            if analysis.get("eip", {}).get("alerts"):
                for alert in analysis["eip"]["alerts"]:
                    report["recommendations"].append({
                        "category": "EIP",
                        "issue": alert,
                        "suggestion": "考虑增加EIP带宽或更换高带宽EIP"
                    })

        # ===== 步骤4: 检查CoreDNS状态 =====
        report["steps_completed"].append("4. 检查CoreDNS状态")

        coredns_result = check_coredns_status(region, cluster_id, access_key, secret_key, proj_id)
        report["coredns_status"] = coredns_result

        if coredns_result.get("status") != "OK":
            report["recommendations"].append({
                "category": "CoreDNS",
                "issue": f"CoreDNS状态异常: {coredns_result.get('status')}",
                "suggestion": "检查CoreDNS配置和Pods状态"
            })

        # ===== 生成网络拓扑图 =====
        if workload_name and report.get("chain"):
            report["topology"] = generate_network_topology(report["chain"], report.get("chain_analysis", {}))

        return report

    except Exception as e:
        return {"success": False, "error": str(e)}


def network_diagnose_by_alarm(region: str, cluster_id: str, alarm_info: str,
                              ak: str = None, sk: str = None, project_id: str = None) -> Dict[str, Any]:
    """基于告警进行网络诊断"""
    try:
        alarm_data = {}
        if alarm_info:
            try:
                alarm_data = json.loads(alarm_info)
            except Exception:
                pass

        workload_name = alarm_data.get("workload_name")
        namespace = alarm_data.get("namespace", "default")

        if not workload_name:
            return {"success": False, "error": "workload_name is required in alarm_info"}

        return network_diagnose(region, cluster_id, workload_name, namespace, ak, sk, project_id)
    except Exception as e:
        return {"success": False, "error": str(e)}


def scale_workload(region: str, cluster_id: str, workload_name: str, namespace: str,
                   ak: str = None, sk: str = None, project_id: str = None,
                   replicas: int = 1) -> Dict[str, Any]:
    """扩缩容工作负载"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

        kubeconfig_result = get_cce_kubeconfig(region, cluster_id, access_key, secret_key, proj_id)
        if not kubeconfig_result.get("success"):
            return {"success": False, "error": "Failed to get kubeconfig"}

        kubeconfig = kubeconfig_result.get("kubeconfig")
        import yaml
        # get_cce_kubeconfig 返回的 dict 使用 current_context（python风格）
        # kubernetes client 期望 current-context（yaml风格），需要转换
        if "current_context" in kubeconfig:
            kubeconfig["current-context"] = kubeconfig.pop("current_context")
        with open("/tmp/kubeconfig_" + cluster_id[:8] + ".yaml", 'w') as f:
            yaml.dump(kubeconfig, f, default_flow_style=False, allow_unicode=True)

        from kubernetes import client, config
        config.load_kube_config(config_file="/tmp/kubeconfig_" + cluster_id[:8] + ".yaml")
        apps_v1 = client.AppsV1Api()

        try:
            resp = apps_v1.patch_namespaced_deployment_scale(
                name=workload_name,
                namespace=namespace,
                body={"spec": {"replicas": replicas}}
            )
            return {"success": True, "replicas": resp.spec.replicas, "workload_name": workload_name, "namespace": namespace}
        except Exception as e:
            return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def verify_pod_scheduling_after_scale(region: str, cluster_id: str, workload_name: str,
                                     namespace: str = "default", ak: str = None, sk: str = None,
                                     project_id: str = None) -> Dict[str, Any]:
    """扩缩容后验证 Pod 调度"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

        # 等待片刻让调度完成
        time.sleep(10)

        pods = get_target_pods(region, cluster_id, workload_name, namespace, access_key, secret_key, proj_id)
        running_pods = [p for p in pods if p.get("status") == "Running"]
        pending_pods = [p for p in pods if p.get("status") == "Pending"]
        failed_pods = [p for p in pods if p.get("status") in ["Failed", "Unknown"]]

        return {
            "success": True,
            "total_pods": len(pods),
            "running_pods": len(running_pods),
            "pending_pods": len(pending_pods),
            "failed_pods": len(failed_pods),
            "pending_details": pending_pods,
            "failed_details": failed_pods
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# 第二部分：节点诊断函数
# ============================================================================

def get_nodepool_info(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """获取节点池信息"""
    result = list_cce_node_pools(region, cluster_id, ak, sk, project_id)
    nodepools = {}
    if result.get("nodepools"):
        for np in result["nodepools"]:
            nodepools[np.get("id")] = {"name": np.get("name"), "flavor": np.get("flavor")}
    return {"success": True, "nodepools": nodepools}


def check_npd_installed(region: str, cluster_id: str, ak: str, sk: str, project_id: str = None) -> bool:
    """检查节点问题检测插件是否安装"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        addons_result = list_cce_addons(region, cluster_id, access_key, secret_key, proj_id)
        if addons_result.get("success"):
            for addon in addons_result.get("addons", []):
                if "npd" in addon.get("name", "").lower() or "node-problem" in addon.get("name", "").lower():
                    return True
        return False
    except Exception:
        return False


def get_node_events(node_ip: str, region: str, cluster_id: str, ak: str, sk: str,
                   project_id: str = None, hours: int = 24) -> Dict[str, Any]:
    """获取节点相关事件"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        events_result = get_kubernetes_events(region, cluster_id, access_key, secret_key, proj_id)

        if not events_result.get("success"):
            return {"success": False, "error": "Failed to get events"}

        filtered = []
        cutoff = datetime.now(timezone.utc).timestamp() - hours * 3600

        for event in events_result.get("events", []):
            if node_ip in (event.get("node", "") or "") or node_ip in (event.get("message", "") or ""):
                try:
                    ts = float(event.get("last_timestamp", 0))
                    if ts > cutoff:
                        filtered.append(event)
                except Exception:
                    pass

        return {"success": True, "events": filtered[:50]}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_node_monitoring(node_ip: str, region: str, cluster_id: str, ak: str, sk: str,
                       project_id: str = None, hours: int = 1) -> Dict[str, Any]:
    """获取节点监控数据"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        cluster_name = get_cluster_name(region, cluster_id, access_key, secret_key, proj_id)

        aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
        aom_id = aom_result.get("aom_instance_id", "") if aom_result.get("success") else ""

        queries = {
            "cpu": f'100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode="idle",instance="{node_ip}",cluster_name="{cluster_name}"}}[5m])) * 100)',
            "memory": f'(1 - (node_memory_MemAvailable_bytes{{instance="{node_ip}",cluster_name="{cluster_name}"}} / node_memory_MemTotal_bytes{{instance="{node_ip}",cluster_name="{cluster_name}"}})) * 100',
            "disk": f'(1 - (node_filesystem_avail_bytes{{mountpoint="/",instance="{node_ip}",cluster_name="{cluster_name}"}} / node_filesystem_size_bytes{{mountpoint="/",instance="{node_ip}",cluster_name="{cluster_name}"}})) * 100'
        }

        results = {}
        for key, query in queries.items():
            r = get_aom_prom_metrics_http(region, aom_id, query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
            if r.get("success") and r.get("result", {}).get("data", {}).get("result"):
                try:
                    latest = r["result"]["data"]["result"][0]["values"][-1][1]
                    results[key] = round(float(latest), 2)
                except Exception:
                    results[key] = None
            else:
                results[key] = None

        return {"success": True, "metrics": results}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_workloads_on_node(node_ip: str, region: str, cluster_id: str, ak: str, sk: str,
                         project_id: str = None) -> Dict[str, Any]:
    """获取节点上的工作负载"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        pods_result = get_kubernetes_pods(region, cluster_id, access_key, secret_key, proj_id)

        if not pods_result.get("success"):
            return {"success": False, "error": "Failed to get pods"}

        workloads = []
        for pod in pods_result.get("pods", []):
            if pod.get("node") == node_ip:
                workloads.append({
                    "name": pod.get("name"),
                    "namespace": pod.get("namespace"),
                    "status": pod.get("status"),
                    "workload_type": pod.get("workload_type", "Unknown"),
                    "workload_name": pod.get("workload_name", "Unknown")
                })

        return {"success": True, "workloads": workloads, "count": len(workloads)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_pods_resource_usage(node_ip: str, region: str, cluster_id: str,
                           ak: str, sk: str, project_id: str = None,
                           hours: int = 1) -> Dict[str, Any]:
    """获取节点上所有 Pod 的资源使用"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        cluster_name = get_cluster_name(region, cluster_id, access_key, secret_key, proj_id)
        aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
        aom_id = aom_result.get("aom_instance_id", "") if aom_result.get("success") else ""

        cpu_query = f'sum by (pod, namespace) (rate(container_cpu_usage_seconds_total{{instance="{node_ip}",cluster_name="{cluster_name}"}}[5m])) * 100'
        mem_query = f'sum by (pod, namespace) (container_memory_working_set_bytes{{instance="{node_ip}",cluster_name="{cluster_name}"}}) / 1024 / 1024'

        cpu_result = get_aom_prom_metrics_http(region, aom_id, cpu_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
        mem_result = get_aom_prom_metrics_http(region, aom_id, mem_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)

        pod_metrics = {}

        for r, key in [(cpu_result, "cpu"), (mem_result, "mem")]:
            if r.get("success") and r.get("result", {}).get("data", {}).get("result"):
                for item in r["result"]["data"]["result"]:
                    pod = item.get("metric", {}).get("pod", "")
                    ns = item.get("metric", {}).get("namespace", "")
                    values = item.get("values", [])
                    if values:
                        try:
                            val = round(float(values[-1][1]), 2)
                            k = f"{ns}/{pod}"
                            if k not in pod_metrics:
                                pod_metrics[k] = {}
                            pod_metrics[k][key] = val
                        except Exception:
                            pass

        return {"success": True, "pod_metrics": pod_metrics}
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_vpc_security_group(region: str, cluster_id: str, ak: str, sk: str,
                            project_id: str = None) -> Dict[str, Any]:
    """检查集群安全组配置"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        vpcs_result = list_vpc_networks(region, access_key, secret_key, proj_id)
        sgs_result = list_security_groups(region, access_key, secret_key, proj_id)

        return {
            "success": True,
            "vpcs": vpcs_result.get("vpcs", []),
            "security_groups": sgs_result.get("security_groups", [])
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def diagnose_single_node(node_ip: str, region: str, cluster_id: str,
                        ak: str, sk: str, project_id: str = None) -> Dict[str, Any]:
    """诊断单个节点"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        cluster_name = get_cluster_name(region, cluster_id, access_key, secret_key, proj_id)

        # 并行获取多项数据
        monitoring = get_node_monitoring(node_ip, region, cluster_id, access_key, secret_key, proj_id)
        workloads = get_workloads_on_node(node_ip, region, cluster_id, access_key, secret_key, proj_id)
        events = get_node_events(node_ip, region, cluster_id, access_key, secret_key, proj_id)
        npd_installed = check_npd_installed(region, cluster_id, access_key, secret_key, proj_id)

        return {
            "success": True,
            "node_ip": node_ip,
            "cluster_id": cluster_id,
            "cluster_name": cluster_name,
            "monitoring": monitoring.get("metrics", {}),
            "workloads": workloads.get("workloads", []),
            "events": events.get("events", []),
            "npd_installed": npd_installed
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_abnormal_nodes(region: str, cluster_id: str, ak: str, sk: str,
                     project_id: str = None) -> List[str]:
    """获取异常节点 IP 列表"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        cluster_name = get_cluster_name(region, cluster_id, access_key, secret_key, proj_id)

        abnormal = []
        for node in get_kubernetes_nodes(region, cluster_id, access_key, secret_key, proj_id).get("nodes", []):
            status = node.get("status", "")
            if status not in ["Ready", "ready"]:
                abnormal.append(node.get("ip") or node.get("name"))

        return abnormal
    except Exception:
        return []


def write_abnormal_node_list(region: str, cluster_id: str, session_id: str,
                            abnormal_nodes: List[str]) -> str:
    """写入异常节点列表到文件"""
    os.makedirs(REPORT_DIR, exist_ok=True)
    filepath = os.path.join(REPORT_DIR, f"abnormal_nodes_{cluster_id[:8]}_{session_id}.txt")
    with open(filepath, 'w') as f:
        f.write("\n".join(abnormal_nodes))
    return filepath


def update_node_list_completion(filepath: str, completed_nodes: List[str]):
    """更新已完成节点列表"""
    try:
        if os.path.exists(filepath):
            with open(filepath) as f:
                remaining = [n for n in f.read().strip().split("\n") if n and n not in completed_nodes]
            with open(filepath, 'w') as f:
                f.write("\n".join(remaining))
    except Exception:
        pass


def batch_node_diagnose(region: str, cluster_id: str, node_ips: List[str] = None,
                       ak: str = None, sk: str = None, project_id: str = None) -> Dict[str, Any]:
    """批量诊断节点"""
    try:
        access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
        cluster_name = get_cluster_name(region, cluster_id, access_key, secret_key, proj_id)

        if not node_ips:
            node_ips = get_abnormal_nodes(region, cluster_id, access_key, secret_key, proj_id)

        if not node_ips:
            return {"success": True, "diagnoses": [], "message": "No abnormal nodes found"}

        node_ips = node_ips[:MAX_NODES_ONCE]
        session_id = str(uuid.uuid4())[:8]
        abnormal = get_abnormal_nodes(region, cluster_id, access_key, secret_key, proj_id)
        filepath = write_abnormal_node_list(region, cluster_id, session_id, abnormal)

        diagnoses = []
        batch_results = []

        for i in range(0, len(node_ips), BATCH_SIZE):
            batch = node_ips[i:i + BATCH_SIZE]
            batch_results = []
            for node_ip in batch:
                result = diagnose_single_node(node_ip, region, cluster_id, access_key, secret_key, proj_id)
                batch_results.append(result)
            diagnoses.extend(batch_results)
            update_node_list_completion(filepath, batch)

        try:
            os.remove(filepath)
        except Exception:
            pass

        return {"success": True, "diagnoses": diagnoses, "count": len(diagnoses)}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# 第三部分：工作负载诊断函数
# ============================================================================

def workload_diagnose(region: str, cluster_id: str, workload_name: str = None,
                     namespace: str = "default", ak: str = None, sk: str = None,
                     project_id: str = None, fault_time: str = None,
                     hours: int = 6) -> Dict[str, Any]:
    """
    工作负载异常诊断主函数

    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        workload_name: 工作负载名称（可选，不填则诊断 namespace 下所有工作负载）
        namespace: 命名空间（默认 default）
        ak: Access Key
        sk: Secret Key
        project_id: Project ID
        fault_time: 故障时间点（可选）

    Returns:
        诊断报告
    """
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials are required"}

    project_id = project_id or proj_id

    diagnosis_data = {
        "region": region,
        "cluster_id": cluster_id,
        "workload_name": workload_name,
        "namespace": namespace,
        "fault_time": fault_time,
        "workloads": {},
        "alarms": [],
        "metrics_data": {},
        "monitor_dashboard": None,
        "abnormal_pods": [],
        "node_diagnosis": {},
        "network_diagnosis": {},
        "change_correlation": {},
        "operations": [],
        "conclusions": [],
        "recommendations": [],
        "steps_completed": [],
        "top3_root_causes": []
    }

    cluster_name = get_cluster_name(region, cluster_id, access_key, secret_key, project_id)
    diagnosis_data["cluster_name"] = cluster_name

    # ===== 步骤1: AOM 告警查询 =====
    # 获取工作负载相关的告警，分析是否有资源、网络、系统等相关告警
    # 不管告警是否恢复，都要去查询监控来判断是否有资源瓶颈
    if workload_name and cluster_name:
        alarms = get_workload_alarms(region, cluster_name, namespace, workload_name,
                                     access_key, secret_key, project_id, hours=hours)
        diagnosis_data["alarms"] = alarms
    diagnosis_data["steps_completed"].append("1. AOM告警查询 - 获取工作负载相关告警，分析资源/网络/系统告警")

    # ===== 步骤2: 收集工作负载信息 =====
    namespace_workloads = get_namespace_workloads(region, cluster_id, namespace, access_key, secret_key, project_id)
    diagnosis_data["workloads"] = namespace_workloads

    # 过滤目标 Pods
    target_pods = []
    if workload_name:
        for pod in namespace_workloads.get("pods", []):
            if workload_name in pod.get("name", ""):
                target_pods.append(pod)
    else:
        target_pods = namespace_workloads.get("pods", [])
    diagnosis_data["steps_completed"].append("2. 收集工作负载信息 - 名称/namespace/副本数/Pod状态/异常比例")

    # ===== 步骤3: 收集监控数据 =====
    # CPU/内存使用率、重启次数、事件日志等，绘制监控数据时序图
    metrics_data = {}
    monitor_dashboard_file = None
    try:
        from .chart_generator import generate_monitor_dashboard
        dashboard_result = generate_monitor_dashboard(
            region=region,
            cluster_id=cluster_id,
            ak=access_key, sk=secret_key, project_id=project_id,
            namespace=namespace,
            label_selector=f"app={workload_name}" if workload_name else None,
            hours=hours,
            title=f"{workload_name or namespace} 诊断监控",
            output_file=f"/tmp/cce_diag_{cluster_id[:8]}_{workload_name or namespace}.html"
        )
        if dashboard_result.get("success"):
            monitor_dashboard_file = dashboard_result.get("output_file")
            metrics_data = {
                "cpu_pods": dashboard_result.get("data_summary", {}).get("cpu_pods", 0),
                "memory_pods": dashboard_result.get("data_summary", {}).get("memory_pods", 0),
                "network_pods": dashboard_result.get("data_summary", {}).get("network_pods", 0),
                "dashboard_file": monitor_dashboard_file,
                "file_size_kb": dashboard_result.get("file_size_kb", 0),
            }
    except Exception as e:
        metrics_data["error"] = str(e)

    # 也用 cce_metrics 获取详细时序数据用于分析
    try:
        from .cce_metrics import get_cce_pod_metrics_topN
        topn_result = get_cce_pod_metrics_topN(
            region=region, cluster_id=cluster_id,
            ak=access_key, sk=secret_key, project_id=project_id,
            namespace=namespace,
            label_selector=f"app={workload_name}" if workload_name else None,
            top_n=10, hours=hours
        )
        if topn_result.get("success"):
            cpu_series = topn_result.get("metrics", {}).get("cpu_top_n", [])
            mem_series = topn_result.get("metrics", {}).get("memory_top_n", [])
            # 分析 CPU/内存是否有异常趋势
            for item in cpu_series:
                ts = item.get("time_series", [])
                if ts:
                    vals = [float(t[1]) for t in ts]
                    avg_cpu = sum(vals) / len(vals) if vals else 0
                    max_cpu = max(vals) if vals else 0
                    if avg_cpu > 80 or max_cpu > 95:
                        diagnosis_data["recommendations"].append({
                            "category": "CPU瓶颈",
                            "issue": f"Pod {item.get('pod', '?')} CPU 平均={avg_cpu:.1f}%, 峰值={max_cpu:.1f}%",
                            "suggestion": "建议扩容工作负载实例或增加CPU资源限制"
                        })
            for item in mem_series:
                ts = item.get("time_series", [])
                if ts:
                    vals = [float(t[1]) for t in ts]
                    avg_mem = sum(vals) / len(vals) if vals else 0
                    max_mem = max(vals) if vals else 0
                    if avg_mem > 80 or max_mem > 95:
                        diagnosis_data["recommendations"].append({
                            "category": "内存瓶颈",
                            "issue": f"Pod {item.get('pod', '?')} 内存 平均={avg_mem:.1f}%, 峰值={max_mem:.1f}%",
                            "suggestion": "建议增加内存限制或排查内存泄漏"
                        })
    except Exception:
        pass

    # 如果有告警，查询对应监控数据分析趋势
    if diagnosis_data["alarms"]:
        alarm_keywords = ["cpu", "memory", "内存", "流量", "network", "bandwidth"]
        for alarm in diagnosis_data["alarms"]:
            alarm_name = alarm.get("alarm_name", "").lower() + alarm.get("name", "").lower()
            alarm_desc = alarm.get("alarm_description", "") + alarm.get("description", "")
            for kw in alarm_keywords:
                if kw in alarm_name or kw in alarm_desc.lower():
                    diagnosis_data["recommendations"].append({
                        "category": "告警关联监控",
                        "issue": f"告警 '{alarm.get('alarm_name', alarm.get('name', ''))}' 触发，需关注{kw}相关指标是否有异常趋势",
                        "suggestion": "已通过监控看板采集数据，请查看监控图表分析趋势"
                    })
                    break

    diagnosis_data["metrics_data"] = metrics_data
    diagnosis_data["monitor_dashboard"] = monitor_dashboard_file
    diagnosis_data["steps_completed"].append("3. 收集监控数据 - CPU/内存使用率、重启次数、事件日志，绘制监控时序图")

    # ===== 步骤4: 异常 Pod 诊断 =====
    abnormal_pods = []
    for pod in target_pods:
        analysis = analyze_pod_status(pod)
        pod["analysis"] = analysis

        if analysis.get("is_abnormal"):
            events = get_pod_events_for_diagnosis(
                region, cluster_id, pod.get("name"), namespace,
                access_key, secret_key, project_id
            )
            pod["events"] = events[-5:]
            abnormal_pods.append(pod)

    # 最多取 3 个异常 Pod 做详细诊断
    abnormal_pods_detailed = abnormal_pods[:3]
    diagnosis_data["abnormal_pods"] = abnormal_pods_detailed
    diagnosis_data["abnormal_pods_total"] = len(abnormal_pods)
    diagnosis_data["steps_completed"].append("4. 异常Pod诊断 - 挑选最多3个异常Pod进行诊断")

    # ===== 步骤5: 节点诊断 =====
    all_nodes = list(set([p.get("node_ip") or p.get("node") or p.get("host_ip") for p in target_pods if p.get("node_ip") or p.get("node") or p.get("host_ip")]))
    node_diagnosis_result = {"success": False, "abnormal_nodes": [], "summary": {}}

    if all_nodes:
        try:
            node_diag = batch_node_diagnose(region, cluster_id, all_nodes, access_key, secret_key, project_id)
            if node_diag.get("success"):
                node_diagnosis_result = {
                    "success": True,
                    "abnormal_nodes": [d.get("node_ip") for d in node_diag.get("diagnoses", []) if d.get("monitoring", {}).get("cpu", 0) > 80 or d.get("monitoring", {}).get("memory", 0) > 80],
                    "summary": {},
                    "details": node_diag
                }
        except Exception as e:
            node_diagnosis_result["note"] = str(e)

    diagnosis_data["node_diagnosis"] = node_diagnosis_result
    diagnosis_data["steps_completed"].append("5. 节点诊断 - 分析工作负载所在节点状态")

    # ===== 步骤6: 网络链路诊断 =====
    network_diagnosis_result = {"success": False, "chain": {}, "analysis": {}}

    if workload_name:
        try:
            chain = get_service_chain(workload_name, namespace, region, cluster_id, access_key, secret_key, project_id)
            chain_analysis = analyze_chain_components(chain, region, access_key, secret_key, project_id)
            network_diagnosis_result = {
                "success": True,
                "chain": chain,
                "analysis": chain_analysis.get("analysis", {})
            }
        except Exception as e:
            network_diagnosis_result["note"] = str(e)

    diagnosis_data["network_diagnosis"] = network_diagnosis_result
    diagnosis_data["steps_completed"].append("6. 网络链路诊断 - 分析Service/Ingress/ELB/EIP链路")

    # ===== 步骤7: 变更关联分析 =====
    all_events = []
    events_result = get_kubernetes_events(region, cluster_id, access_key, secret_key, project_id, namespace, limit=500)
    if events_result.get("success") and events_result.get("events"):
        for event in events_result.get("events", []):
            if workload_name and workload_name in event.get("involved_object", {}).get("name", ""):
                all_events.append(event)
            elif not workload_name:
                all_events.append(event)

    change_correlation = analyze_change_correlation(diagnosis_data["workloads"], all_events, fault_time)
    diagnosis_data["change_correlation"] = change_correlation
    diagnosis_data["steps_completed"].append("7. 变更关联分析 - 分析最近1小时内是否有相关配置变更或版本更新")

    # ===== 生成诊断报告 =====
    report = generate_diagnosis_report(diagnosis_data)

    # Top3 根因分析
    top3 = _analyze_top3_root_causes(diagnosis_data)
    diagnosis_data["top3_root_causes"] = top3

    return {
        "success": True,
        "diagnosis": diagnosis_data,
        "report": report
    }


def _analyze_top3_root_causes(diagnosis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """分析 Top3 根因"""
    causes = []

    # 1. 检查告警
    alarms = diagnosis_data.get("alarms", [])
    if alarms:
        alarm_names = [a.get("alarm_name", a.get("name", "未知")) for a in alarms[:3]]
        causes.append({
            "rank": 1,
            "category": "AOM告警",
            "cause": f"发现 {len(alarms)} 条告警: {', '.join(alarm_names)}",
            "confidence": "high",
            "evidence": f"告警数量: {len(alarms)}"
        })

    # 2. 检查异常 Pod
    abnormal_count = diagnosis_data.get("abnormal_pods_total", len(diagnosis_data.get("abnormal_pods", [])))
    if abnormal_count > 0:
        abnormal_pods = diagnosis_data.get("abnormal_pods", [])
        pod_details = [f"{p.get('name', '?')}({p.get('status', '?')})" for p in abnormal_pods[:3]]
        causes.append({
            "rank": 2,
            "category": "Pod异常",
            "cause": f"发现 {abnormal_count} 个异常 Pod: {', '.join(pod_details)}",
            "confidence": "high",
            "evidence": f"异常Pod占比: {abnormal_count}"
        })

    # 3. 检查资源瓶颈
    recommendations = diagnosis_data.get("recommendations", [])
    resource_issues = [r for r in recommendations if r.get("category") in ["CPU瓶颈", "内存瓶颈"]]
    if resource_issues:
        issues_desc = ", ".join(r.get("issue", "") for r in resource_issues[:2])
        causes.append({
            "rank": 3,
            "category": "资源瓶颈",
            "cause": issues_desc,
            "confidence": "medium",
            "evidence": f"资源异常项: {len(resource_issues)}"
        })

    # 4. 检查节点异常
    node_diag = diagnosis_data.get("node_diagnosis", {})
    abnormal_nodes = node_diag.get("abnormal_nodes", [])
    if abnormal_nodes:
        causes.append({
            "rank": len(causes) + 1 if len(causes) < 3 else 3,
            "category": "节点异常",
            "cause": f"发现 {len(abnormal_nodes)} 个节点资源异常: {', '.join(abnormal_nodes[:3])}",
            "confidence": "medium",
            "evidence": f"异常节点: {abnormal_nodes}"
        })

    # 5. 检查变更关联
    change_corr = diagnosis_data.get("change_correlation", {})
    if change_corr.get("has_correlation"):
        causes.append({
            "rank": len(causes) + 1 if len(causes) < 3 else 3,
            "category": "变更关联",
            "cause": f"发现相关变更: {change_corr.get('analysis', '配置变更可能导致问题')}",
            "confidence": "low",
            "evidence": f"变更数量: {len(change_corr.get('changes', []))}"
        })

    # 如果没有发现问题
    if not causes:
        causes.append({
            "rank": 1,
            "category": "健康",
            "cause": "工作负载状态正常，未发现异常根因",
            "confidence": "high",
            "evidence": "所有 Pod Running，无告警，资源正常"
        })

    return causes[:3]


def workload_diagnose_by_alarm(region: str, cluster_id: str, alarm_info: str,
                               ak: str = None, sk: str = None, project_id: str = None,
                               hours: int = 6) -> Dict[str, Any]:
    """基于告警进行工作负载诊断"""
    import re

    workload_name = None
    namespace = "default"
    fault_time = None

    try:
        alarm_data = json.loads(alarm_info)
        resource_id = alarm_data.get("resource_id", "")
        alarm_time = alarm_data.get("alarm_time", "")

        if "namespace=" in resource_id:
            ns_match = re.search(r'namespace:([^,;]+)', resource_id)
            if ns_match:
                namespace = ns_match.group(1)

        if "name=" in resource_id:
            name_match = re.search(r'name:([^,;]+)', resource_id)
            if name_match:
                workload_name = name_match.group(1)

        if alarm_time:
            fault_time = alarm_time

    except Exception:
        # 如果不是 JSON，尝试从名称推断
        if "." in alarm_info:
            parts = alarm_info.split(".")
            workload_name = parts[0]
            namespace = parts[1] if len(parts) > 1 else "default"

    return workload_diagnose(region, cluster_id, workload_name, namespace, ak, sk, project_id, fault_time, hours)


def verify_workload_after_operation(region: str, cluster_id: str, workload_name: str,
                                    namespace: str = "default", ak: str = None, sk: str = None,
                                    project_id: str = None) -> Dict[str, Any]:
    """恢复操作后检查工作负载状态"""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials are required"}

    namespace_workloads = get_namespace_workloads(region, cluster_id, namespace, access_key, secret_key, project_id)

    target_pods = []
    for pod in namespace_workloads.get("pods", []):
        if workload_name and workload_name in pod.get("name", ""):
            target_pods.append(pod)

    abnormal_count = 0
    running_count = 0
    for pod in target_pods:
        analysis = analyze_pod_status(pod)
        if analysis.get("is_abnormal"):
            abnormal_count += 1
        elif "Running" in pod.get("status", ""):
            running_count += 1

    return {
        "success": True,
        "workload_name": workload_name,
        "namespace": namespace,
        "total_pods": len(target_pods),
        "running_pods": running_count,
        "abnormal_pods": abnormal_count,
        "status": "RECOVERED" if abnormal_count == 0 else "STILL_ABNORMAL",
        "check_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "pods": target_pods
    }


def huawei_expand_nodepool(region: str, cluster_id: str, nodepool_id: str,
                           node_count: int, confirm: bool = False,
                           ak: str = None, sk: str = None,
                           project_id: str = None) -> Dict[str, Any]:
    """扩容节点池"""
    return resize_node_pool(region, cluster_id, nodepool_id, node_count, confirm, ak=ak, sk=sk, project_id=project_id)


# ============================================================================
# CLI 入口
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  network_diagnose:       python cce_diagnosis.py network_diagnose region=cn-north-4 cluster_id=xxx workload_name=xxx namespace=default")
        print("  network_diagnose_by_alarm: python cce_diagnosis.py network_diagnose_by_alarm region=cn-north-4 cluster_id=xxx alarm_info=xxx")
        print("  node_diagnose:          python cce_diagnosis.py node_diagnose region=cn-north-4 cluster_id=xxx node_ips=192.168.1.10")
        print("  node_batch_diagnose:    python cce_diagnosis.py node_batch_diagnose region=cn-north-4 cluster_id=xxx")
        print("  workload_diagnose:      python cce_diagnosis.py workload_diagnose region=cn-north-4 cluster_id=xxx workload_name=xxx namespace=default")
        print("  workload_diagnose_by_alarm: python cce_diagnosis.py workload_diagnose_by_alarm region=cn-north-4 cluster_id=xxx alarm_info=xxx")
        print("  verify_workload:        python cce_diagnosis.py verify_workload region=cn-north-4 cluster_id=xxx workload_name=xxx namespace=default")
        print("  expand_nodepool:        python cce_diagnosis.py expand_nodepool region=cn-north-4 cluster_id=xxx nodepool_id=xxx node_count=3 confirm=true")
        sys.exit(1)

    action = sys.argv[1]
    params = dict(p.split("=", 1) for p in sys.argv[2:] if "=" in p)

    region = params.get("region", "")
    cluster_id = params.get("cluster_id", "")
    ak = params.get("ak")
    sk = params.get("sk")
    project_id = params.get("project_id")

    if action == "network_diagnose":
        result = network_diagnose(
            region=region,
            cluster_id=cluster_id,
            workload_name=params.get("workload_name"),
            namespace=params.get("namespace", "default"),
            ak=ak, sk=sk, project_id=project_id
        )
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif action == "network_diagnose_by_alarm":
        result = network_diagnose_by_alarm(
            region=region,
            cluster_id=cluster_id,
            alarm_info=params.get("alarm_info", "{}"),
            ak=ak, sk=sk, project_id=project_id
        )
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif action == "node_diagnose":
        node_ips = params.get("node_ips", "").split(",") if params.get("node_ips") else None
        result = batch_node_diagnose(
            region=region, cluster_id=cluster_id,
            node_ips=node_ips, ak=ak, sk=sk, project_id=project_id
        )
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif action == "node_batch_diagnose":
        result = batch_node_diagnose(
            region=region, cluster_id=cluster_id,
            ak=ak, sk=sk, project_id=project_id
        )
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif action == "workload_diagnose":
        result = workload_diagnose(
            region=region,
            cluster_id=cluster_id,
            workload_name=params.get("workload_name"),
            namespace=params.get("namespace", "default"),
            ak=ak, sk=sk, project_id=project_id,
            fault_time=params.get("fault_time")
        )
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif action == "workload_diagnose_by_alarm":
        result = workload_diagnose_by_alarm(
            region=region,
            cluster_id=cluster_id,
            alarm_info=params.get("alarm_info", "{}"),
            ak=ak, sk=sk, project_id=project_id
        )
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif action == "verify_workload":
        result = verify_workload_after_operation(
            region=region,
            cluster_id=cluster_id,
            workload_name=params.get("workload_name", ""),
            namespace=params.get("namespace", "default"),
            ak=ak, sk=sk, project_id=project_id
        )
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif action == "expand_nodepool":
        try:
            node_count = int(params.get("node_count", 1))
        except Exception:
            node_count = 1
        confirm = params.get("confirm", "false").lower() == "true"
        result = huawei_expand_nodepool(
            region=region,
            cluster_id=cluster_id,
            nodepool_id=params.get("nodepool_id", ""),
            node_count=node_count,
            confirm=confirm,
            ak=ak, sk=sk, project_id=project_id
        )
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
