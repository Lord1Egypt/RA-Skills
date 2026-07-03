#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCE 集群自动巡检模块 —— 快检 + 诊断分离架构

设计理念：
  快检（Quick Check）: 3 个 API 串行，<30s，判断是否有异常
  诊断（Deep Diagnosis）: 异常时才执行，6+ 个 API 串行/并行，生成完整诊断报告

使用方式：
  # 快检（用于 cron 高频调用）
  huawei_cce_quick_check region=cn-north-4 cluster_id=xxx

  # 深度诊断（快检发现异常后调用）
  huawei_cce_deep_diagnosis region=cn-north-4 cluster_id=xxx check_result=<快检结果JSON>

  # 自动巡检（快检 + 判断 + 诊断，一步到位）
  huawei_cce_auto_inspection region=cn-north-4 cluster_id=xxx

cron 配置建议：
  - 每 5 分钟执行 huawei_cce_auto_inspection，超时设 60s（无异常时 <30s 直接返回）
  - 发现异常时由 agent 自行 spawn 诊断子任务，不占巡检超时

异常判断阈值（可配置）：
  - CPU 告警 > 80%（不管是否恢复）
  - 业务 Pod CPU 平均 > 60%
  - ELB 最近 5min QPS > 1500
  - ELB 最近 5min P99 时延 > 100ms
  - 可用副本 ≠ 期望副本
  - Pod CrashLoopBackOff / OOMKilled
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional

from .common import get_credentials_with_region
from .aom import list_aom_alarms, get_aom_prom_metrics_http, list_aom_instances
from .cce import (
    get_kubernetes_deployments,
    get_kubernetes_pods,
    list_cce_clusters,
)
from .cce_metrics import get_cce_pod_metrics_topN
from .elb import get_elb_metrics
from .cce_inspection import (
    aom_alarm_inspection,
    node_status_inspection,
    pod_status_inspection,
    event_inspection,
    node_resource_monitoring_inspection,
    addon_pod_monitoring_inspection,
    biz_pod_monitoring_inspection,
)
from .cce_diagnosis import workload_diagnose, network_diagnose
from .report_generator import generate_detailed_html_report


# ========== 默认阈值配置 ==========

DEFAULT_THRESHOLDS = {
    "cpu_alarm_percent": 80,           # CPU 告警阈值
    "pod_cpu_avg_percent": 60,         # 业务 Pod CPU 平均值阈值
    "elb_qps": 1500,                   # ELB QPS 阈值
    "elb_p99_ms": 100,                 # ELB P99 时延阈值 (ms)
    "elb_recent_minutes": 5,           # ELB 只看最近 N 分钟数据
    "alarm_hours": 0.5,                # 告警查询时间窗口 (小时)
    "replica_mismatch": True,          # 是否检查副本数不匹配
    "pod_crashloop": True,             # 是否检查 CrashLoopBackOff
}


# ========== 快检：3 个 API，< 30s ==========

def cce_quick_check(
    region: str,
    cluster_id: str,
    ak: str = None,
    sk: str = None,
    project_id: str = None,
    thresholds: Dict[str, Any] = None,
    elb_ids: List[str] = None,
    business_labels: List[str] = None,
) -> Dict[str, Any]:
    """CCE 集群快速巡检（<30s）

    只做 3 件事：
    1. 查 AOM 告警（active+history，近 30 分钟）
    2. 查 Pod CPU TopN
    3. 查 ELB 监控（最近 5 分钟）

    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
        thresholds: 自定义阈值（覆盖 DEFAULT_THRESHOLDS）
        elb_ids: 需要检查的 ELB ID 列表（默认自动发现）
        business_labels: 业务 Pod 标签列表，如 ["app=nginx", "app=api"]

    Returns:
        {
            "success": True,
            "has_anomaly": True/False,
            "anomaly_details": [...],
            "normal_details": [...],
            "duration_seconds": 12.3,
            "metrics": {
                "alarms": {...},
                "cpu_topn": {...},
                "elb_metrics": {...},
            }
        }
    """
    start_time = time.time()
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

    cfg = {**DEFAULT_THRESHOLDS}
    if thresholds:
        cfg.update(thresholds)

    result = {
        "success": True,
        "has_anomaly": False,
        "anomaly_details": [],
        "normal_details": [],
        "metrics": {},
        "duration_seconds": 0,
        "cluster_id": cluster_id,
        "region": region,
        "check_time": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S CST"),
    }

    # ---- 获取集群名称 ----
    cluster_name = cluster_id
    try:
        clusters = list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters.get("success"):
            for c in clusters.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass

    # ---- Step 1: AOM 告警查询 (active + history) ----
    alarm_data = {}
    try:
        alarm_result = list_aom_alarms(
            region=region,
            ak=access_key,
            sk=secret_key,
            project_id=proj_id,
            cluster_name=cluster_name,
            hours=cfg["alarm_hours"],
            limit=200,
        )
        alarm_data = alarm_result if alarm_result.get("success") else {"error": alarm_result.get("error", "Unknown")}
        result["metrics"]["alarms"] = alarm_data

        # 检查是否有 CPU/内存/磁盘类告警
        if alarm_result.get("success"):
            resource_keywords = ["CPU", "cpu", "Memory", "memory", "内存", "磁盘", "Disk", "OOM", "oom",
                                 "Pressure", "pressure", "压力", "CrashLoopBackOff"]
            for alarm in alarm_result.get("events", []):
                alarm_text = alarm.get("event_name", "") + " " + alarm.get("message", "")
                severity = alarm.get("event_severity", "Info")

                # 资源类告警检查
                if any(kw in alarm_text for kw in resource_keywords):
                    if severity in ("Critical", "Major"):
                        result["has_anomaly"] = True
                        result["anomaly_details"].append({
                            "type": "resource_alarm",
                            "severity": severity,
                            "name": alarm.get("event_name"),
                            "status": alarm.get("status"),
                            "message": alarm.get("message", "")[:200],
                        })

                # 严重告警不管类型都标记
                if severity == "Critical" and alarm.get("status") == "firing":
                    result["has_anomaly"] = True
                    result["anomaly_details"].append({
                        "type": "critical_alarm",
                        "severity": severity,
                        "name": alarm.get("event_name"),
                        "status": "firing",
                        "message": alarm.get("message", "")[:200],
                    })

            if not result["anomaly_details"]:
                result["normal_details"].append(
                    f"AOM 告警正常：{alarm_result.get('firing_count', 0)} firing, "
                    f"{alarm_result.get('resolved_count', 0)} resolved，无资源类严重告警"
                )
    except Exception as e:
        result["metrics"]["alarms"] = {"error": str(e)}

    # ---- Step 2: Pod CPU TopN ----
    cpu_data = {}
    try:
        cpu_result = get_cce_pod_metrics_topN(
            region=region,
            cluster_id=cluster_id,
            ak=access_key,
            sk=secret_key,
            project_id=proj_id,
            metric_type="cpu",
            top_n=10,
            hours=0.25,  # 只看最近 15 分钟，加快查询
        )
        cpu_data = cpu_result if cpu_result.get("success") else {"error": cpu_result.get("error", "Unknown")}
        result["metrics"]["cpu_topn"] = cpu_data

        # 检查业务 Pod CPU 是否超阈值
        if cpu_result.get("success"):
            high_cpu_pods = []
            for pod in cpu_result.get("pods", [])[:10]:
                pod_name = pod.get("name", "")
                values = pod.get("metric", {}).get("values", [])
                if values:
                    latest_cpu = float(values[-1][1])
                    if latest_cpu > cfg["pod_cpu_avg_percent"]:
                        high_cpu_pods.append({"name": pod_name, "cpu_percent": latest_cpu})

            if high_cpu_pods:
                result["has_anomaly"] = True
                result["anomaly_details"].append({
                    "type": "high_pod_cpu",
                    "threshold": cfg["pod_cpu_avg_percent"],
                    "pods": high_cpu_pods,
                    "message": f"{len(high_cpu_pods)} 个 Pod CPU > {cfg['pod_cpu_avg_percent']}%: "
                               + ", ".join(f"{p['name']}({p['cpu_percent']:.1f}%)" for p in high_cpu_pods[:5]),
                })
            else:
                result["normal_details"].append(f"Pod CPU 正常：Top 10 均 < {cfg['pod_cpu_avg_percent']}%")
    except Exception as e:
        result["metrics"]["cpu_topn"] = {"error": str(e)}

    # ---- Step 3: ELB 监控（自动发现或指定 ID） ----
    elb_data = {}
    elb_anomalies = []

    # 如果未指定 ELB ID，从 Service 列表自动发现
    if not elb_ids:
        try:
            from .cce import get_kubernetes_services
            svc_result = get_kubernetes_services(region, cluster_id, access_key, secret_key, proj_id)
            if svc_result.get("success"):
                elb_ids = []
                for svc in svc_result.get("services", []):
                    if svc.get("type") == "LoadBalancer":
                        elb_id = svc.get("annotations", {}).get("kubernetes.io/elb.id", "")
                        if elb_id and elb_id not in elb_ids:
                            elb_ids.append(elb_id)
        except Exception:
            elb_ids = []

    if elb_ids:
        for eid in elb_ids:
            try:
                elb_result = get_elb_metrics(region, eid, access_key, secret_key, proj_id)
                elb_data[eid] = elb_result if elb_result.get("success") else {"error": elb_result.get("error", "Unknown")}

                # 只看最近 N 分钟数据判断异常
                if elb_result.get("success"):
                    metrics = elb_result.get("metrics", {})
                    recent_min = cfg["elb_recent_minutes"]

                    # 检查新建连接数 (NCPS)
                    ncps_data = metrics.get("m4_ncps", {})
                    if isinstance(ncps_data, dict) and "time_series" in ncps_data:
                        recent_ncps = _get_recent_values(ncps_data["time_series"], recent_min)
                        if recent_ncps and max(recent_ncps) > cfg["elb_qps"]:
                            peak_ncps = max(recent_ncps)
                            elb_anomalies.append({
                                "type": "elb_high_qps",
                                "elb_id": eid,
                                "value": peak_ncps,
                                "threshold": cfg["elb_qps"],
                                "message": f"ELB {eid} 最近 {recent_min}min NCPS: {peak_ncps:.0f}/s > {cfg['elb_qps']}",
                            })

                    # 检查并发连接数
                    cps_data = metrics.get("m1_cps", {})
                    if isinstance(cps_data, dict) and "time_series" in cps_data:
                        recent_cps = _get_recent_values(cps_data["time_series"], recent_min)
                        if recent_cps and max(recent_cps) > 10000:
                            peak_cps = max(recent_cps)
                            elb_anomalies.append({
                                "type": "elb_high_connections",
                                "elb_id": eid,
                                "value": peak_cps,
                                "message": f"ELB {eid} 并发连接数: {peak_cps:.0f}",
                            })

                    # 检查带宽使用率
                    for bw_key, bw_name in [("m22_in_bandwidth", "入带宽"), ("m23_out_bandwidth", "出带宽")]:
                        bw_data = metrics.get(bw_key, {})
                        if isinstance(bw_data, dict) and "latest_value" in bw_data:
                            if bw_data["latest_value"] and bw_data["latest_value"] > 100_000_000:  # > 100Mbps
                                elb_anomalies.append({
                                    "type": "elb_high_bandwidth",
                                    "elb_id": eid,
                                    "direction": bw_name,
                                    "value_bps": bw_data["latest_value"],
                                    "message": f"ELB {eid} {bw_name}: {bw_data['latest_value']/1_000_000:.1f} Mbps",
                                })

            except Exception as e:
                elb_data[eid] = {"error": str(e)}

    result["metrics"]["elb_metrics"] = elb_data

    if elb_anomalies:
        result["has_anomaly"] = True
        result["anomaly_details"].extend(elb_anomalies)
    elif elb_ids:
        result["normal_details"].append(f"ELB 正常：{len(elb_ids)} 个 ELB 最近 {cfg['elb_recent_minutes']}分钟内无异常")
    else:
        result["normal_details"].append("ELB：未发现 LoadBalancer Service")

    # ---- 附加检查：副本数不匹配 / CrashLoop ----
    try:
        pods_result = get_kubernetes_pods(region, cluster_id, access_key, secret_key, proj_id)
        if pods_result.get("success"):
            pods = pods_result.get("pods", [])
            crashloop_pods = []
            for p in pods:
                if p.get("state_reason") == "CrashLoopBackOff":
                    crashloop_pods.append(p.get("name"))
            if crashloop_pods and cfg.get("pod_crashloop"):
                result["has_anomaly"] = True
                result["anomaly_details"].append({
                    "type": "pod_crashloop",
                    "pods": crashloop_pods[:10],
                    "message": f"{len(crashloop_pods)} 个 Pod CrashLoopBackOff: "
                               + ", ".join(crashloop_pods[:5]),
                })
    except Exception:
        pass

    # ---- 副本数检查 ----
    if cfg.get("replica_mismatch"):
        try:
            deploys_result = get_kubernetes_deployments(region, cluster_id, access_key, secret_key, proj_id)
            if deploys_result.get("success"):
                mismatched = []
                for dep in deploys_result.get("deployments", []):
                    ready = dep.get("ready_replicas", 0)
                    desired = dep.get("replicas", 0)
                    if ready != desired and desired > 0:
                        mismatched.append({"name": dep.get("name"), "ready": ready, "desired": desired})
                if mismatched:
                    result["has_anomaly"] = True
                    result["anomaly_details"].append({
                        "type": "replica_mismatch",
                        "deployments": mismatched,
                        "message": f"{len(mismatched)} 个 Deployment 副本不匹配: "
                                   + ", ".join(f"{d['name']}({d['ready']}/{d['desired']})" for d in mismatched[:5]),
                    })
        except Exception:
            pass

    result["duration_seconds"] = round(time.time() - start_time, 2)

    return result


# ========== 深度诊断：异常后执行 ==========

def cce_deep_diagnosis(
    region: str,
    cluster_id: str,
    quick_check_result: Dict[str, Any] = None,
    ak: str = None,
    sk: str = None,
    project_id: str = None,
    notify_email: str = None,
    report_file: str = None,
) -> Dict[str, Any]:
    """CCE 集群深度诊断（快检发现异常后调用）

    执行 6+ 个 API 获取完整诊断数据：
    1. 告警智能分类 (analyze_aom_alarms)
    2. Pod 内存 TopN
    3. 工作负载详情
    4. 节点状态
    5. 集群事件
    6. 根因定位
    7. 生成恢复方案
    8. （可选）生成 HTML 报告 + 发邮件

    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        quick_check_result: 快检结果（用于提取异常上下文，可选）
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
        notify_email: 通知邮箱（可选）
        report_file: HTML 报告输出路径（默认 /tmp/cce_diag_report.html）

    Returns:
        完整诊断结果
    """
    start_time = time.time()
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

    result = {
        "success": True,
        "cluster_id": cluster_id,
        "region": region,
        "diagnosis_time": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S CST"),
        "quick_check_anomalies": [],
        "diagnosis": {},
        "root_cause": None,
        "recovery_plan": [],
        "duration_seconds": 0,
    }

    # 提取快检异常上下文
    if quick_check_result and quick_check_result.get("anomaly_details"):
        result["quick_check_anomalies"] = quick_check_result["anomaly_details"]

    # ---- 获取集群名称 & AOM 实例 ----
    cluster_name = cluster_id
    aom_instance_id = None
    try:
        clusters = list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters.get("success"):
            for c in clusters.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass

    try:
        aom_result = list_aom_instances(region, access_key, secret_key, proj_id)
        if aom_result.get("success"):
            for inst in aom_result.get("instances", []):
                if inst.get("cluster_id") == cluster_id or inst.get("cluster_name") == cluster_name:
                    aom_instance_id = inst.get("id")
                    break
    except Exception:
        pass

    # ---- 诊断 Step 1: AOM 告警智能分类 ----
    try:
        from .aom import analyze_aom_alarms
        alarm_analysis = analyze_aom_alarms(
            region=region,
            ak=access_key,
            sk=secret_key,
            project_id=proj_id,
            hours=1,
        )
        result["diagnosis"]["alarm_analysis"] = alarm_analysis
    except Exception as e:
        result["diagnosis"]["alarm_analysis"] = {"error": str(e)}

    # ---- 诊断 Step 2: Pod 内存 TopN ----
    try:
        mem_result = get_cce_pod_metrics_topN(
            region=region,
            cluster_id=cluster_id,
            ak=access_key,
            sk=secret_key,
            project_id=proj_id,
            metric_type="memory",
            top_n=10,
            hours=0.5,
        )
        result["diagnosis"]["memory_topn"] = mem_result
    except Exception as e:
        result["diagnosis"]["memory_topn"] = {"error": str(e)}

    # ---- 诊断 Step 3: 工作负载详情 ----
    try:
        deploys_result = get_kubernetes_deployments(region, cluster_id, access_key, secret_key, proj_id)
        result["diagnosis"]["deployments"] = deploys_result
    except Exception as e:
        result["diagnosis"]["deployments"] = {"error": str(e)}

    # ---- 诊断 Step 4: 节点状态 ----
    try:
        from .cce import get_kubernetes_nodes
        nodes_result = get_kubernetes_nodes(region, cluster_id, access_key, secret_key, proj_id)
        result["diagnosis"]["nodes"] = nodes_result
    except Exception as e:
        result["diagnosis"]["nodes"] = {"error": str(e)}

    # ---- 诊断 Step 5: 集群事件 ----
    try:
        from .cce import get_kubernetes_events
        events_result = get_kubernetes_events(region, cluster_id, access_key, secret_key, proj_id)
        result["diagnosis"]["events"] = events_result
    except Exception as e:
        result["diagnosis"]["events"] = {"error": str(e)}

    # ---- 诊断 Step 6: 根因定位 ----
    root_cause = _analyze_root_cause(quick_check_result, result["diagnosis"])
    result["root_cause"] = root_cause

    # ---- 诊断 Step 7: 恢复方案 ----
    recovery_plan = _generate_recovery_plan(root_cause, result["diagnosis"])
    result["recovery_plan"] = recovery_plan

    result["duration_seconds"] = round(time.time() - start_time, 2)

    return result


# ========== 自动巡检：快检 + 判断 + 诊断 ==========

def cce_auto_inspection(
    region: str,
    cluster_id: str,
    ak: str = None,
    sk: str = None,
    project_id: str = None,
    thresholds: Dict[str, Any] = None,
    elb_ids: List[str] = None,
    notify_email: str = None,
) -> Dict[str, Any]:
    """CCE 集群自动巡检（快检 + 诊断一步到位）

    流程：
    1. 执行快速巡检
    2. 有异常 → 自动执行深度诊断 → 返回诊断结果
    3. 无异常 → 返回 HEARTBEAT_OK

    适合 cron 调用：
    - 无异常时 <30s 返回，不浪费资源
    - 有异常时自动深诊，但建议 cron 超时设 300s
    - 更好的做法：cron 只调快检，异常时由 agent spawn 诊断子任务

    Args:
        region: 华为云区域
        cluster_id: CCE 集群 ID
        ak: Access Key ID
        sk: Secret Access Key
        project_id: Project ID
        thresholds: 自定义阈值
        elb_ids: ELB ID 列表
        notify_email: 通知邮箱

    Returns:
        快检结果（无异常） 或 深诊结果（有异常）
    """
    # Step 1: 快检
    check_result = cce_quick_check(
        region=region,
        cluster_id=cluster_id,
        ak=ak,
        sk=sk,
        project_id=project_id,
        thresholds=thresholds,
        elb_ids=elb_ids,
    )

    if not check_result.get("has_anomaly"):
        # 无异常，直接返回
        check_result["auto_inspection"] = "HEARTBEAT_OK"
        check_result["message"] = (
            f"✅ 巡检正常 ({check_result['duration_seconds']}s) | "
            + " | ".join(check_result.get("normal_details", []))
        )
        return check_result

    # Step 2: 有异常，执行深度诊断
    diag_result = cce_deep_diagnosis(
        region=region,
        cluster_id=cluster_id,
        quick_check_result=check_result,
        ak=ak,
        sk=sk,
        project_id=project_id,
        notify_email=notify_email,
    )

    diag_result["auto_inspection"] = "ANOMALY_DETECTED"
    diag_result["quick_check"] = check_result
    diag_result["message"] = _format_diagnosis_summary(diag_result)

    return diag_result


# ========== 辅助函数 ==========

def _get_recent_values(time_series: list, recent_minutes: int) -> List[float]:
    """从 time_series 中提取最近 N 分钟的值"""
    if not time_series:
        return []

    now = time.time()
    cutoff = now - recent_minutes * 60
    values = []

    for point in time_series:
        if isinstance(point, (list, tuple)) and len(point) >= 2:
            ts = point[0]
            val = point[1]
            if isinstance(ts, (int, float)) and ts >= cutoff:
                try:
                    values.append(float(val))
                except (ValueError, TypeError):
                    pass
    return values


def _analyze_root_cause(quick_check: Dict, diagnosis: Dict) -> Dict[str, Any]:
    """根据快检 + 诊断数据自动定位根因"""
    root_cause = {
        "type": "unknown",
        "chain": [],
        "summary": "",
        "confidence": "low",
    }

    anomalies = quick_check.get("anomaly_details", []) if quick_check else []
    anomaly_types = {a.get("type") for a in anomalies}

    # 场景1: 流量突发 → CPU 饱和
    if "elb_high_qps" in anomaly_types and "high_pod_cpu" in anomaly_types:
        # 检查是否有 CPU limit 瓶颈
        deployments = diagnosis.get("deployments", {})
        low_cpu_pods = []
        if deployments.get("success"):
            for dep in deployments.get("deployments", []):
                for c in dep.get("containers", []):
                    cpu_limit = c.get("resources", {}).get("limits", {}).get("cpu", "")
                    if cpu_limit and _parse_cpu(cpu_limit) <= 1:
                        low_cpu_pods.append({
                            "deployment": dep.get("name"),
                            "container": c.get("name"),
                            "cpu_limit": cpu_limit,
                        })

        root_cause = {
            "type": "traffic_spike_cpu_bottleneck",
            "chain": [
                "外部流量突增",
                "ELB 连接数暴增",
                "Pod CPU 饱和",
                "CPU limit 成为 throttle 瓶颈" if low_cpu_pods else "CPU 资源不足",
                "响应时延增大",
            ],
            "summary": (
                f"流量突发导致 CPU 饱和"
                + (f"，{len(low_cpu_pods)} 个容器 CPU limit ≤ 1 核成为 throttle 瓶颈" if low_cpu_pods else "")
            ),
            "low_cpu_pods": low_cpu_pods,
            "confidence": "high",
        }

    # 场景2: 纯 CPU 高（无 ELB 异常）
    elif "high_pod_cpu" in anomaly_types and "elb_high_qps" not in anomaly_types:
        root_cause = {
            "type": "cpu_high",
            "chain": ["Pod CPU 使用率高", "可能是业务逻辑问题或内部调用增加"],
            "summary": "Pod CPU 使用率偏高，需进一步确认是业务增长还是代码问题",
            "confidence": "medium",
        }

    # 场景3: 纯告警异常
    elif "resource_alarm" in anomaly_types or "critical_alarm" in anomaly_types:
        root_cause = {
            "type": "alarm_triggered",
            "chain": ["AOM 告警触发", "需检查具体告警内容"],
            "summary": "存在资源类严重告警，需关注",
            "confidence": "medium",
        }

    # 场景4: 副本数不匹配
    elif "replica_mismatch" in anomaly_types:
        mismatch = [a for a in anomalies if a.get("type") == "replica_mismatch"]
        root_cause = {
            "type": "replica_mismatch",
            "chain": ["Pod 副本数不足", "可能是节点资源不够或调度失败"],
            "summary": mismatch[0].get("message", "") if mismatch else "副本数不匹配",
            "confidence": "medium",
        }

    # 场景5: CrashLoop
    elif "pod_crashloop" in anomaly_types:
        crash = [a for a in anomalies if a.get("type") == "pod_crashloop"]
        root_cause = {
            "type": "pod_crashloop",
            "chain": ["Pod 崩溃循环", "需要检查容器日志和配置"],
            "summary": crash[0].get("message", "") if crash else "Pod CrashLoopBackOff",
            "confidence": "medium",
        }

    return root_cause


def _generate_recovery_plan(root_cause: Dict, diagnosis: Dict) -> List[Dict[str, Any]]:
    """根据根因生成恢复方案"""
    plan = []
    rc_type = root_cause.get("type", "unknown")

    if rc_type == "traffic_spike_cpu_bottleneck":
        # 流量突发场景
        target_deploys = set()
        for p in root_cause.get("low_cpu_pods", []):
            target_deploys.add(p["deployment"])

        if target_deploys:
            for dep_name in target_deploys:
                plan.append({
                    "step": len(plan) + 1,
                    "action": "scale_cce_workload",
                    "description": f"扩容 {dep_name} 副本（建议 2-3x）",
                    "params": {"name": dep_name, "namespace": "default"},
                    "effect": "增加处理能力，降低单 Pod CPU 压力",
                    "risk": "low",
                })
                plan.append({
                    "step": len(plan) + 1,
                    "action": "resize_cce_workload",
                    "description": f"提升 {dep_name} CPU limit 到 4 核",
                    "params": {"name": dep_name, "namespace": "default", "cpu_limit": "4"},
                    "effect": "解除 cgroup throttle 瓶颈",
                    "risk": "medium",
                })

    elif rc_type == "cpu_high":
        plan.append({
            "step": 1,
            "action": "check_logs",
            "description": "检查高 CPU Pod 的业务日志",
            "effect": "确认 CPU 高的根因（业务增长/代码问题/异常流量）",
            "risk": "none",
        })

    elif rc_type == "replica_mismatch":
        for dep in root_cause.get("deployments", []):
            plan.append({
                "step": len(plan) + 1,
                "action": "investigate_scheduling",
                "description": f"排查 {dep.get('name')} 调度失败原因",
                "effect": "找到 Pod 无法调度的根因并解决",
                "risk": "none",
            })

    elif rc_type == "pod_crashloop":
        plan.append({
            "step": 1,
            "action": "check_crashloop_logs",
            "description": "查看 CrashLoop Pod 的容器日志和退出码",
            "effect": "确认崩溃原因",
            "risk": "none",
        })

    # 通用收尾步骤
    if rc_type != "unknown":
        plan.append({
            "step": len(plan) + 1,
            "action": "verify_recovery",
            "description": "恢复操作后等待 2-5 分钟，验证指标是否恢复正常",
            "effect": "确认恢复效果",
            "risk": "none",
        })

    return plan


def _parse_cpu(cpu_str: str) -> float:
    """解析 CPU 字符串为核心数"""
    if not cpu_str:
        return 0
    cpu_str = str(cpu_str).strip()
    if cpu_str.endswith("m"):
        return int(cpu_str[:-1]) / 1000
    try:
        return float(cpu_str)
    except ValueError:
        return 0


def _format_diagnosis_summary(diag: Dict) -> str:
    """格式化诊断结果为人类可读摘要"""
    qc = diag.get("quick_check", {})
    anomalies = qc.get("anomaly_details", [])
    root_cause = diag.get("root_cause", {})
    recovery = diag.get("recovery_plan", [])

    lines = ["🚨 CCE集群异常 - 自动诊断完成", ""]

    # 异常摘要
    lines.append("📊 异常摘要")
    for a in anomalies[:6]:
        msg = a.get("message", a.get("type", ""))
        lines.append(f"  - {msg}")

    # 根因
    if root_cause.get("summary"):
        lines.append("")
        lines.append(f"🔍 根因：{root_cause['summary']}")
        if root_cause.get("chain"):
            lines.append("  链路: " + " → ".join(root_cause["chain"]))

    # 恢复方案
    if recovery:
        lines.append("")
        lines.append("📋 恢复方案（待确认）")
        for step in recovery:
            lines.append(f"  {step['step']}. {step['description']}")
            lines.append(f"     效果: {step.get('effect', '')} | 风险: {step.get('risk', '?')}")

    # 耗时
    lines.append(f"\n⏱️ 快检 {qc.get('duration_seconds', 0)}s + 诊断 {diag.get('duration_seconds', 0)}s")

    return "\n".join(lines)
