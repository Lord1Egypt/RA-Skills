"""Pod failure diagnosis helpers for CCE clusters."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict, List, Optional

from . import cce, cce_metrics


CRASH_REASONS = {"CrashLoopBackOff"}
IMAGE_PULL_REASONS = {"ImagePullBackOff", "ErrImagePull", "InvalidImageName"}
OOM_REASONS = {"OOMKilled"}
PENDING_EVENT_REASONS = {
    "FailedScheduling",
    "FailedMount",
    "FailedAttachVolume",
    "FailedCreatePodSandBox",
    "FailedCreate",
}
IMAGE_PULL_KEYWORDS = (
    "failed to pull image",
    "errimagepull",
    "imagepullbackoff",
    "back-off pulling image",
    "manifest unknown",
    "unauthorized",
    "no basic auth credentials",
    "repository does not exist",
    "invalid image name",
)
SCHEDULING_KEYWORDS = (
    "insufficient",
    "didn't match",
    "did not match",
    "node(s) had taint",
    "node affinity",
    "pod affinity",
    "node selector",
    "preemption",
    "max node group size",
)
VOLUME_KEYWORDS = (
    "mount",
    "attach",
    "volume",
    "pvc",
    "persistentvolumeclaim",
    "timeout",
    "permission denied",
)
SECRET_PATTERNS = [
    re.compile(r"(?i)(authorization:\s*bearer\s+)[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)((?:password|passwd|token|secret|access[_-]?key|secret[_-]?key)\s*[=:]\s*)\S+"),
    re.compile(r"(?i)(x-auth-token\s*[=:]\s*)\S+"),
]


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _lower_text(*parts: Any) -> str:
    return " ".join(str(part or "") for part in parts).lower()


def _mask_secrets(text: str) -> str:
    masked = text or ""
    for pattern in SECRET_PATTERNS:
        masked = pattern.sub(r"\1***", masked)
    return masked


def _log_excerpt(logs: str, max_lines: int = 40, max_chars: int = 6000) -> str:
    lines = (logs or "").splitlines()
    excerpt = "\n".join(lines[-max_lines:])
    return _mask_secrets(excerpt[-max_chars:])


def _state_detail(container: Dict[str, Any], key: str = "state_detail") -> Dict[str, Any]:
    value = container.get(key)
    return value if isinstance(value, dict) else {}


def _state_reason(container: Dict[str, Any]) -> Optional[str]:
    for key in ("state_detail", "last_state_detail"):
        detail = _state_detail(container, key)
        reason = detail.get("reason")
        if reason:
            return reason
    state_text = _lower_text(container.get("state"), container.get("last_state"))
    for reason in sorted(CRASH_REASONS | IMAGE_PULL_REASONS | OOM_REASONS):
        if reason.lower() in state_text:
            return reason
    return None


def _last_termination(container: Dict[str, Any]) -> Dict[str, Any]:
    for key in ("last_state_detail", "state_detail"):
        detail = _state_detail(container, key)
        if detail.get("type") == "terminated":
            return detail
    return {}


def _all_containers(pod: Dict[str, Any]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for container in pod.get("init_containers") or []:
        item = dict(container)
        item["container_type"] = "init"
        result.append(item)
    for container in pod.get("containers") or []:
        item = dict(container)
        item["container_type"] = "app"
        result.append(item)
    return result


def _event_summary(event: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "type": event.get("type"),
        "reason": event.get("reason"),
        "message": event.get("message"),
        "last_timestamp": event.get("last_timestamp"),
        "count": event.get("count", 1),
    }


def _event_text(event: Dict[str, Any]) -> str:
    return _lower_text(event.get("reason"), event.get("message"))


def _events_for_pod(events: List[Dict[str, Any]], pod: Dict[str, Any]) -> List[Dict[str, Any]]:
    pod_name = pod.get("name")
    namespace = pod.get("namespace")
    selected = []
    for event in events:
        involved = event.get("involved_object") or {}
        if involved.get("kind") != "Pod":
            continue
        if involved.get("name") != pod_name:
            continue
        if namespace and involved.get("namespace") and involved.get("namespace") != namespace:
            continue
        selected.append(event)
    return selected


def _condition(pod: Dict[str, Any], condition_type: str) -> Dict[str, Any]:
    for condition in pod.get("conditions") or []:
        if condition.get("type") == condition_type:
            return condition
    return {}


def _matches_workload(pod: Dict[str, Any], workload_name: Optional[str]) -> bool:
    if not workload_name:
        return True
    name = pod.get("name") or ""
    if name == workload_name or name.startswith(f"{workload_name}-") or workload_name in name:
        return True
    for ref in pod.get("owner_references") or []:
        ref_name = ref.get("name") or ""
        if ref_name == workload_name or ref_name.startswith(f"{workload_name}-"):
            return True
    return False


def _has_abnormal_signal(pod: Dict[str, Any]) -> bool:
    status_text = _lower_text(pod.get("status"), pod.get("phase"), pod.get("reason"), pod.get("message"))
    if any(key.lower() in status_text for key in ["pending", "failed", "evicted", "unknown"]):
        return True
    for container in _all_containers(pod):
        reason = _state_reason(container)
        if reason in CRASH_REASONS | IMAGE_PULL_REASONS | OOM_REASONS:
            return True
        if _to_int(container.get("restart_count"), 0) >= 3:
            return True
        if container.get("ready") is False:
            return True
    return False


def _add_issue(
    issues: List[Dict[str, Any]],
    issue_type: str,
    title: str,
    confidence: float,
    evidence: List[Dict[str, Any]],
    recommendation: List[str],
    container: Optional[str] = None,
) -> None:
    issues.append({
        "type": issue_type,
        "title": title,
        "confidence": confidence,
        "container": container,
        "evidence": evidence[:8],
        "recommendation": recommendation,
    })


def _diagnose_pod(pod: Dict[str, Any], events: List[Dict[str, Any]]) -> Dict[str, Any]:
    pod_events = _events_for_pod(events, pod)
    event_evidence = [_event_summary(event) for event in pod_events[:10]]
    issues: List[Dict[str, Any]] = []
    status = pod.get("status") or pod.get("phase")
    reason = pod.get("reason")
    message = pod.get("message")
    status_text = _lower_text(status, reason, message)

    if "evicted" in status_text:
        _add_issue(
            issues,
            "Evicted",
            "Pod 已被驱逐，优先确认节点资源压力或节点不可用",
            0.92,
            [{"pod_status": status, "reason": reason, "message": message}, *event_evidence],
            [
                "查看驱逐消息中的 MemoryPressure、DiskPressure、ephemeral-storage 或 NodeNotReady 线索。",
                "检查节点资源水位、Pod requests/limits 和临时存储用量。",
                "需要迁移或隔离节点时转交 auto-remediation-runner 预览。"
            ],
        )

    scheduled = _condition(pod, "PodScheduled")
    pending_reason_events = [
        event for event in pod_events
        if event.get("reason") in PENDING_EVENT_REASONS
    ]
    is_pending = status == "Pending" or scheduled.get("status") == "False" or bool(pending_reason_events)
    if is_pending:
        pending_events = [
            event for event in pod_events
            if event.get("reason") in PENDING_EVENT_REASONS
            or any(keyword in _event_text(event) for keyword in SCHEDULING_KEYWORDS + VOLUME_KEYWORDS)
        ]
        lower_events = " ".join(_event_text(event) for event in pending_events)
        if any(keyword in lower_events for keyword in VOLUME_KEYWORDS):
            title = "Pod Pending 与存储挂载/绑定异常相关"
            recommendations = [
                "检查 PVC/PV 绑定状态、StorageClass、Everest 插件和后端 EVS/SFS 资源。",
                "查看 FailedMount/FailedAttachVolume 事件中的卷名、超时和权限信息。"
            ]
            issue_type = "PendingStorage"
            confidence = 0.86
        else:
            title = "Pod Pending 与调度条件不满足相关"
            recommendations = [
                "检查 FailedScheduling 事件中的资源不足、亲和性、污点容忍、节点选择器和配额原因。",
                "关联节点 Ready 状态和 CPU/内存/Pod 数量可分配资源。"
            ]
            issue_type = "PendingScheduling"
            confidence = 0.84
        _add_issue(
            issues,
            issue_type,
            title,
            confidence,
            [
                {"pod_status": status, "pod_scheduled": scheduled},
                *[_event_summary(event) for event in pending_events[:8]],
            ],
            recommendations,
        )

    image_events = [
        event for event in pod_events
        if event.get("reason") in IMAGE_PULL_REASONS
        or any(keyword in _event_text(event) for keyword in IMAGE_PULL_KEYWORDS)
    ]
    crash_events = [
        event for event in pod_events
        if "back-off restarting failed container" in _event_text(event)
        or "crashloopbackoff" in _event_text(event)
    ]

    for container in _all_containers(pod):
        container_name = container.get("name")
        state = _state_detail(container)
        last_terminated = _last_termination(container)
        state_reason = _state_reason(container)
        restart_count = _to_int(container.get("restart_count"), 0)

        if state_reason in IMAGE_PULL_REASONS or (
            image_events
            and container.get("ready") is False
            and state.get("reason") not in CRASH_REASONS
        ):
            _add_issue(
                issues,
                "ImagePullBackOff",
                "镜像拉取失败或正在退避重试",
                0.9 if state_reason in IMAGE_PULL_REASONS else 0.78,
                [
                    {
                        "container": container_name,
                        "image": container.get("image"),
                        "state": state,
                        "image_pull_secrets": pod.get("image_pull_secrets"),
                    },
                    *[_event_summary(event) for event in image_events[:8]],
                ],
                [
                    "确认镜像地址、tag、命名空间和仓库是否存在。",
                    "确认 imagePullSecrets、SWR/第三方仓库权限和节点到镜像仓库网络连通性。",
                    "如果是临时网络或仓库限流，观察事件 count 和 last_timestamp 是否仍在增长。"
                ],
                container_name,
            )

        if state_reason in CRASH_REASONS or (crash_events and restart_count > 0):
            terminated_reason = last_terminated.get("reason")
            _add_issue(
                issues,
                "CrashLoopBackOff",
                "容器反复启动失败并进入退避重试",
                0.92 if state_reason in CRASH_REASONS else 0.8,
                [
                    {
                        "container": container_name,
                        "restart_count": restart_count,
                        "state": state,
                        "last_termination": last_terminated,
                    },
                    *[_event_summary(event) for event in crash_events[:8]],
                ],
                [
                    "优先查看 previous 日志、退出码、启动命令和应用配置。",
                    "核对 ConfigMap/Secret、环境变量、挂载路径和依赖服务可达性。",
                    "如果事件包含 probe failed，检查 startupProbe/livenessProbe 阈值和应用启动耗时。"
                ],
                container_name,
            )
            if terminated_reason in OOM_REASONS or last_terminated.get("exit_code") == 137:
                state_reason = "OOMKilled"

        if state_reason in OOM_REASONS or last_terminated.get("reason") in OOM_REASONS or last_terminated.get("exit_code") == 137:
            _add_issue(
                issues,
                "OOMKilled",
                "容器被 OOM Killer 终止",
                0.93,
                [
                    {
                        "container": container_name,
                        "restart_count": restart_count,
                        "last_termination": last_terminated,
                        "resources": container.get("resources"),
                    },
                    *event_evidence,
                ],
                [
                    "对比容器 memory limit/request 与故障前内存曲线，判断是限额过低还是内存泄漏。",
                    "检查是否有突增流量、批处理任务或缓存膨胀导致工作集飙升。",
                    "需要调大资源规格时转交 auto-remediation-runner 预览 resize_cce_workload。"
                ],
                container_name,
            )

        if restart_count >= 3 and not any(issue.get("container") == container_name for issue in issues):
            _add_issue(
                issues,
                "FrequentRestart",
                "容器存在多次重启但未命中特定等待原因",
                0.65,
                [
                    {
                        "container": container_name,
                        "restart_count": restart_count,
                        "state": state,
                        "last_termination": last_terminated,
                    },
                    *event_evidence,
                ],
                [
                    "查看 current/previous 日志和退出码，确认是否为应用异常、探针失败或节点重启。",
                    "关联同节点其他 Pod 是否同时重启，排除节点级故障。"
                ],
                container_name,
            )

    if not issues:
        ready = _condition(pod, "Ready")
        containers_ready = _condition(pod, "ContainersReady")
        if ready.get("status") == "False" or containers_ready.get("status") == "False":
            _add_issue(
                issues,
                "PodNotReady",
                "Pod 未就绪但未命中特定故障类型",
                0.55,
                [{"ready": ready, "containers_ready": containers_ready}, *event_evidence],
                [
                    "检查 readinessProbe、容器端口监听、依赖服务和 Service endpoint。",
                    "继续查看事件、日志和业务健康检查结果收敛根因。"
                ],
            )

    return {
        "pod": {
            "name": pod.get("name"),
            "namespace": pod.get("namespace"),
            "status": status,
            "reason": reason,
            "message": message,
            "node": pod.get("node"),
            "pod_ip": pod.get("ip"),
            "host_ip": pod.get("host_ip"),
            "qos_class": pod.get("qos_class"),
            "owner_references": pod.get("owner_references") or [],
        },
        "issues": issues,
        "events": event_evidence,
        "containers": _all_containers(pod),
    }


def _choose_log_container(pod_diag: Dict[str, Any]) -> Optional[str]:
    for issue in pod_diag.get("issues") or []:
        if issue.get("container"):
            return issue["container"]
    containers = pod_diag.get("containers") or []
    if containers:
        return containers[0].get("name")
    return None


def _need_previous_logs(pod_diag: Dict[str, Any]) -> bool:
    return any(
        issue.get("type") in {"CrashLoopBackOff", "OOMKilled", "FrequentRestart"}
        for issue in pod_diag.get("issues") or []
    )


def _fetch_pod_logs(
    region: str,
    cluster_id: str,
    pod_diag: Dict[str, Any],
    ak: Optional[str],
    sk: Optional[str],
    project_id: Optional[str],
    tail_lines: int,
) -> Dict[str, Any]:
    pod = pod_diag.get("pod") or {}
    pod_name = pod.get("name")
    namespace = pod.get("namespace") or "default"
    container = _choose_log_container(pod_diag)
    result = {"container": container, "current": None, "previous": None}
    if not pod_name or not container:
        return result

    current = cce.get_pod_logs(
        region, cluster_id, pod_name, ak, sk, project_id,
        namespace=namespace, container=container, previous=False, tail_lines=tail_lines,
    )
    result["current"] = {
        "success": current.get("success", False),
        "error": current.get("error"),
        "excerpt": _log_excerpt(current.get("logs", ""), max_lines=tail_lines) if current.get("success") else None,
    }

    if _need_previous_logs(pod_diag):
        previous = cce.get_pod_logs(
            region, cluster_id, pod_name, ak, sk, project_id,
            namespace=namespace, container=container, previous=True, tail_lines=tail_lines,
        )
        result["previous"] = {
            "success": previous.get("success", False),
            "error": previous.get("error"),
            "excerpt": _log_excerpt(previous.get("logs", ""), max_lines=tail_lines) if previous.get("success") else None,
        }
    return result


def _fetch_pod_metrics(
    region: str,
    cluster_id: str,
    pod_diag: Dict[str, Any],
    ak: Optional[str],
    sk: Optional[str],
    project_id: Optional[str],
    hours: int,
) -> Dict[str, Any]:
    pod = pod_diag.get("pod") or {}
    pod_name = pod.get("name")
    namespace = pod.get("namespace")
    if not pod_name:
        return {"success": False, "error": "pod name is missing"}
    return cce_metrics.get_cce_pod_metrics(
        region, cluster_id, pod_name, ak, sk, project_id, namespace=namespace, hours=hours,
    )


def _aggregate_causes(pod_diags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}
    for pod_diag in pod_diags:
        pod_name = f"{pod_diag['pod'].get('namespace')}/{pod_diag['pod'].get('name')}"
        for issue in pod_diag.get("issues") or []:
            issue_type = issue["type"]
            if issue_type not in grouped:
                grouped[issue_type] = {
                    "type": issue_type,
                    "title": issue["title"],
                    "confidence": issue["confidence"],
                    "affected_pods": [],
                    "evidence": [],
                    "recommendation": [],
                }
            item = grouped[issue_type]
            item["confidence"] = max(item["confidence"], issue["confidence"])
            item["affected_pods"].append(pod_name)
            item["evidence"].extend(issue.get("evidence") or [])
            item["recommendation"].extend(issue.get("recommendation") or [])

    causes = []
    for item in grouped.values():
        recommendations = []
        for rec in item["recommendation"]:
            if rec not in recommendations:
                recommendations.append(rec)
        item["recommendation"] = recommendations[:6]
        item["evidence"] = item["evidence"][:10]
        item["affected_count"] = len(set(item["affected_pods"]))
        item["affected_pods"] = sorted(set(item["affected_pods"]))
        causes.append(item)

    causes.sort(key=lambda cause: (cause["confidence"], cause["affected_count"]), reverse=True)
    for index, cause in enumerate(causes, start=1):
        cause["rank"] = index
    return causes[:3]


def _recommended_actions(top_causes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    action_map = {
        "CrashLoopBackOff": [
            "读取 previous 日志并结合退出码定位应用启动失败点。",
            "核对 ConfigMap/Secret、启动命令、探针配置和依赖服务。"
        ],
        "ImagePullBackOff": [
            "校验镜像地址/tag、SWR 权限、imagePullSecrets 和节点出网能力。",
            "确认仓库是否限流或镜像是否被删除。"
        ],
        "OOMKilled": [
            "拉取故障窗口内存曲线，判断是否需要调整 memory limit/request。",
            "排查内存泄漏、缓存膨胀和突发任务。"
        ],
        "PendingScheduling": [
            "检查节点可用资源、污点容忍、亲和性、节点选择器和命名空间配额。",
            "如需扩容节点池，转交 auto-remediation-runner 生成预览。"
        ],
        "PendingStorage": [
            "检查 PVC/PV/StorageClass/Everest 和底层 EVS/SFS 状态。",
            "确认挂载路径、权限和后端存储容量。"
        ],
        "Evicted": [
            "检查被驱逐节点的 MemoryPressure/DiskPressure/ephemeral-storage 压力。",
            "清理或迁移高消耗 Pod，必要时转交 auto-remediation-runner 预览隔离动作。"
        ],
    }
    actions = []
    seen = set()
    for cause in top_causes:
        for action in action_map.get(cause["type"], cause.get("recommendation") or []):
            if action in seen:
                continue
            actions.append({
                "action": action,
                "source_cause": cause["type"],
                "requires_confirmation": False,
            })
            seen.add(action)
    return actions


def pod_failure_diagnose(
    region: str,
    cluster_id: str,
    namespace: Optional[str] = None,
    pod_name: Optional[str] = None,
    workload_name: Optional[str] = None,
    labels: Optional[str] = None,
    include_logs: bool = True,
    include_metrics: bool = False,
    tail_lines: int = 80,
    hours: int = 1,
    max_pods: int = 20,
    event_limit: int = 500,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Diagnose common Pod failures from Kubernetes Pod status, events, logs, and optional metrics."""
    pods_result = cce.get_kubernetes_pods(
        region, cluster_id, ak, sk, project_id, namespace=namespace, labels=labels,
    )
    if not pods_result.get("success"):
        return {**pods_result, "stage": "get_cce_pods"}

    all_pods = pods_result.get("pods") or []
    selected = [
        pod for pod in all_pods
        if (not pod_name or pod.get("name") == pod_name)
        and _matches_workload(pod, workload_name)
    ]
    explicit_target = bool(pod_name or workload_name or labels)
    if not explicit_target:
        selected = [pod for pod in selected if _has_abnormal_signal(pod)]
    selected = selected[:max_pods]

    if not selected:
        return {
            "success": True,
            "action": "pod_failure_diagnose",
            "region": region,
            "cluster_id": cluster_id,
            "target": {
                "namespace": namespace,
                "pod_name": pod_name,
                "workload_name": workload_name,
                "labels": labels,
            },
            "summary": {
                "diagnosis_status": "no_matching_abnormal_pods",
                "message": "未找到匹配的异常 Pod；如果要诊断正常或指定 Pod，请提供 pod_name/workload_name/labels。",
                "total_pods_seen": len(all_pods),
            },
            "pods": [],
            "top_causes": [],
            "recommended_actions": [],
            "warnings": [],
        }

    warnings = []
    events_result = cce.get_kubernetes_events(
        region, cluster_id, ak, sk, project_id, namespace=namespace, limit=event_limit,
    )
    if events_result.get("success"):
        events = events_result.get("events") or []
    else:
        events = []
        warnings.append({
            "stage": "get_cce_events",
            "error": events_result.get("error"),
            "error_type": events_result.get("error_type"),
        })

    pod_diags = [_diagnose_pod(pod, events) for pod in selected]

    log_budget = 5
    if include_logs:
        for pod_diag in pod_diags:
            if log_budget <= 0:
                break
            if not pod_diag.get("issues"):
                continue
            if any(issue.get("type") == "ImagePullBackOff" for issue in pod_diag.get("issues") or []):
                continue
            pod_diag["logs"] = _fetch_pod_logs(
                region, cluster_id, pod_diag, ak, sk, project_id, tail_lines,
            )
            log_budget -= 1

    if include_metrics:
        for pod_diag in pod_diags:
            try:
                pod_diag["metrics"] = _fetch_pod_metrics(
                    region, cluster_id, pod_diag, ak, sk, project_id, hours,
                )
            except Exception as exc:
                pod_diag["metrics"] = {
                    "success": False,
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                }

    top_causes = _aggregate_causes(pod_diags)
    status_counts = Counter(pod.get("status") or pod.get("phase") or "Unknown" for pod in selected)
    issue_counts = Counter(
        issue.get("type")
        for pod_diag in pod_diags
        for issue in (pod_diag.get("issues") or [])
    )

    diagnosis_status = "abnormal" if top_causes else "no_known_failure_detected"
    return {
        "success": True,
        "action": "pod_failure_diagnose",
        "region": region,
        "cluster_id": cluster_id,
        "target": {
            "namespace": namespace,
            "pod_name": pod_name,
            "workload_name": workload_name,
            "labels": labels,
            "include_logs": include_logs,
            "include_metrics": include_metrics,
        },
        "summary": {
            "diagnosis_status": diagnosis_status,
            "diagnosed_pods": len(pod_diags),
            "total_pods_seen": len(all_pods),
            "status_counts": dict(status_counts),
            "issue_counts": dict(issue_counts),
        },
        "pods": pod_diags,
        "top_causes": top_causes,
        "recommended_actions": _recommended_actions(top_causes),
        "warnings": warnings,
        "next_skill": "auto-remediation-runner" if any(
            cause["type"] in {"OOMKilled", "PendingScheduling", "Evicted"}
            for cause in top_causes
        ) else None,
    }
