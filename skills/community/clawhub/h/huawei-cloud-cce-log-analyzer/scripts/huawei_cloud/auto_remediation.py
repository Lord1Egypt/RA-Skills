"""Preview-first CCE remediation orchestration."""

from __future__ import annotations

import copy
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from . import cce_k8s, workload_rollout_diagnosis
from .common import (
    IMPORT_ERROR,
    K8S_AVAILABLE,
    K8S_IMPORT_ERROR,
    SDK_AVAILABLE,
    _safe_delete_file,
    get_credentials,
    k8s_client,
)


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value) if value not in (None, "") else default
    except (TypeError, ValueError):
        return default


def _md_cell(value: Any, max_len: int = 180) -> str:
    if value is None or value == "":
        return "-"
    text = str(value).replace("\n", " ").replace("|", "\\|").strip()
    if len(text) > max_len:
        return text[: max_len - 3] + "..."
    return text


def _revision(rs: Any) -> Optional[int]:
    annotations = getattr(getattr(rs, "metadata", None), "annotations", None) or {}
    value = annotations.get("deployment.kubernetes.io/revision")
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _owner_matches(rs: Any, deployment_uid: Optional[str], deployment_name: str) -> bool:
    for ref in getattr(getattr(rs, "metadata", None), "owner_references", None) or []:
        if getattr(ref, "kind", None) != "Deployment":
            continue
        if deployment_uid and getattr(ref, "uid", None) == deployment_uid:
            return True
        if getattr(ref, "name", None) == deployment_name:
            return True
    return False


def _selector_from_deployment(deployment: Any) -> str:
    labels = getattr(getattr(deployment.spec, "selector", None), "match_labels", None) or {}
    return ",".join(f"{key}={labels[key]}" for key in sorted(labels))


def _template_summary(template: Any) -> Dict[str, Any]:
    metadata = getattr(template, "metadata", None)
    spec = getattr(template, "spec", None)
    containers = []
    for container in getattr(spec, "containers", None) or []:
        containers.append({
            "name": getattr(container, "name", None),
            "image": getattr(container, "image", None),
            "command": list(getattr(container, "command", None) or []),
            "args": list(getattr(container, "args", None) or []),
            "env_keys": [getattr(env, "name", None) for env in (getattr(container, "env", None) or []) if getattr(env, "name", None)],
        })
    return {
        "labels": dict(getattr(metadata, "labels", None) or {}),
        "annotations": dict(getattr(metadata, "annotations", None) or {}),
        "service_account": getattr(spec, "service_account_name", None),
        "node_selector": dict(getattr(spec, "node_selector", None) or {}),
        "containers": containers,
    }


def _strip_generated_template_labels(template: Any) -> None:
    metadata = getattr(template, "metadata", None)
    if not metadata:
        return
    labels = getattr(metadata, "labels", None)
    if labels and "pod-template-hash" in labels:
        labels.pop("pod-template-hash", None)


def _list_owned_replicasets(apps_v1: Any, deployment: Any, namespace: str) -> List[Any]:
    selector = _selector_from_deployment(deployment)
    rs_page = apps_v1.list_namespaced_replica_set(namespace, label_selector=selector or None)
    deployment_uid = getattr(getattr(deployment, "metadata", None), "uid", None)
    deployment_name = getattr(getattr(deployment, "metadata", None), "name", "")
    owned = [rs for rs in rs_page.items if _owner_matches(rs, deployment_uid, deployment_name)]
    return sorted(
        [rs for rs in owned if _revision(rs) is not None],
        key=lambda rs: (_revision(rs) or -1, getattr(getattr(rs, "metadata", None), "creation_timestamp", None) or ""),
    )


def _select_revisions(replicasets: List[Any], target_revision: Optional[int]) -> Tuple[Any, Any]:
    if len(replicasets) < 2:
        raise ValueError("at least two Deployment revisions are required for rollback")
    current = max(replicasets, key=lambda rs: _revision(rs) or -1)
    if target_revision is not None:
        target = next((rs for rs in replicasets if _revision(rs) == target_revision), None)
        if target is None:
            raise ValueError(f"target revision {target_revision} was not found")
        if _revision(target) == _revision(current):
            raise ValueError("target revision is already the current revision")
        return current, target
    older = [rs for rs in replicasets if (_revision(rs) or -1) < (_revision(current) or -1)]
    if not older:
        raise ValueError("no previous revision was found")
    target = max(older, key=lambda rs: _revision(rs) or -1)
    return current, target


def _setup_apps_client(region: str, cluster_id: str, ak: Optional[str], sk: Optional[str], project_id: Optional[str], cert_prefix: str) -> Tuple[Any, Optional[str], Optional[str]]:
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        raise ValueError("Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters.")
    if not K8S_AVAILABLE:
        raise RuntimeError(f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}")
    if not SDK_AVAILABLE:
        raise RuntimeError(f"Huawei Cloud SDK not installed: {IMPORT_ERROR}")
    _, cert_file, key_file = cce_k8s._setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, cert_prefix)
    return k8s_client.AppsV1Api(), cert_file, key_file


def rollback_cce_workload(params: Dict[str, str]) -> Dict[str, Any]:
    """Preview or execute Deployment rollback to a previous ReplicaSet template."""
    missing = [key for key in ("region", "cluster_id", "namespace", "workload_type", "name") if not params.get(key)]
    if missing:
        return {"success": False, "error": f"{', '.join(missing)} is required"}
    workload_type = str(params["workload_type"]).strip().lower()
    if workload_type not in {"deployment", "deploy"}:
        return {"success": False, "error": "rollback currently supports Deployment workloads only"}

    region = params["region"]
    cluster_id = params["cluster_id"]
    namespace = params["namespace"]
    name = params["name"]
    confirm = _to_bool(params.get("confirm"), False)
    target_revision = _to_int(params.get("target_revision"), -1)
    target_revision = target_revision if target_revision >= 0 else None
    cert_file = None
    key_file = None

    try:
        apps_v1, cert_file, key_file = _setup_apps_client(
            region, cluster_id, params.get("ak"), params.get("sk"), params.get("project_id"), "rollback"
        )
        deployment = apps_v1.read_namespaced_deployment(name, namespace)
        replicasets = _list_owned_replicasets(apps_v1, deployment, namespace)
        current_rs, target_rs = _select_revisions(replicasets, target_revision)
        current_summary = _template_summary(getattr(current_rs.spec, "template", None))
        target_summary = _template_summary(getattr(target_rs.spec, "template", None))
        revision_summary = [
            {
                "name": getattr(getattr(rs, "metadata", None), "name", None),
                "revision": _revision(rs),
                "replicas": getattr(getattr(rs, "spec", None), "replicas", None),
                "ready_replicas": getattr(getattr(rs, "status", None), "ready_replicas", None),
            }
            for rs in replicasets
        ]

        if not confirm:
            return {
                "success": False,
                "requires_confirmation": True,
                "operation": "rollback_cce_workload",
                "risk_level": "R2",
                "warning": f"即将把 Deployment {namespace}/{name} 回滚到 revision {_revision(target_rs)}。",
                "cluster_id": cluster_id,
                "namespace": namespace,
                "name": name,
                "workload_type": "deployment",
                "current_revision": _revision(current_rs),
                "target_revision": _revision(target_rs),
                "current_template": current_summary,
                "target_template": target_summary,
                "revision_history": revision_summary,
                "hint": "确认执行请再次调用并携带 confirm=true。",
            }

        target_template = copy.deepcopy(target_rs.spec.template)
        _strip_generated_template_labels(target_template)
        deployment.spec.template = target_template
        deployment.metadata.annotations = dict(deployment.metadata.annotations or {})
        deployment.metadata.annotations["codex.openai.com/remediation"] = (
            f"rollback to revision {_revision(target_rs)} at {datetime.utcnow().isoformat()}Z"
        )
        updated = apps_v1.replace_namespaced_deployment(name, namespace, deployment)

        return {
            "success": True,
            "operation": "rollback_cce_workload",
            "risk_level": "R2",
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace,
            "name": name,
            "workload_type": "deployment",
            "from_revision": _revision(current_rs),
            "to_revision": _revision(target_rs),
            "new_generation": getattr(getattr(updated, "metadata", None), "generation", None),
            "message": f"Deployment {namespace}/{name} rollback submitted to revision {_revision(target_rs)}.",
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__, "operation": "rollback_cce_workload"}
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def _rollout_diagnose(params: Dict[str, str], include_logs: bool = False) -> Dict[str, Any]:
    return workload_rollout_diagnosis.workload_rollout_diagnose(
        region=params["region"],
        cluster_id=params["cluster_id"],
        namespace=params["namespace"],
        kind=params.get("kind") or params.get("workload_type") or "deployment",
        name=params.get("workload_name") or params.get("name"),
        include_pod_diagnosis=True,
        include_logs=include_logs,
        include_metrics=False,
        tail_lines=_to_int(params.get("tail_lines"), 80),
        hours=_to_int(params.get("hours"), 1),
        max_pods=_to_int(params.get("max_pods"), 20),
        event_limit=_to_int(params.get("event_limit"), 500),
        label_selector=params.get("label_selector"),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def _safe_rollout_diagnose(params: Dict[str, str], include_logs: bool = False) -> Dict[str, Any]:
    try:
        return _rollout_diagnose(params, include_logs=include_logs)
    except Exception as exc:  # pragma: no cover - cloud/API boundary
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}


def _safe_rollback_preview_or_run(params: Dict[str, str], confirm: bool) -> Dict[str, Any]:
    rollback_params = dict(params)
    rollback_params["workload_type"] = params.get("workload_type") or params.get("kind") or "deployment"
    rollback_params["name"] = params.get("name") or params.get("workload_name") or ""
    rollback_params["confirm"] = "true" if confirm else "false"
    return rollback_cce_workload(rollback_params)


def _top_cause_type(diagnosis: Dict[str, Any]) -> Optional[str]:
    causes = diagnosis.get("top_causes") or []
    if not causes:
        return None
    return causes[0].get("type")


def _rollback_is_suitable(cause_type: Optional[str]) -> bool:
    return cause_type in {"ContainerCommandNotFound", "CrashLoopOrAppExit", "ProbeFailure", "ImagePullBlocked"}


def _wait_for_recovery(params: Dict[str, str], wait_seconds: int, interval_seconds: int) -> Dict[str, Any]:
    deadline = time.time() + max(0, wait_seconds)
    attempts = []
    while True:
        diagnosis = _safe_rollout_diagnose(params, include_logs=False)
        attempts.append({
            "time": datetime.utcnow().isoformat() + "Z",
            "success": diagnosis.get("success"),
            "summary": diagnosis.get("summary"),
        })
        if diagnosis.get("success"):
            summary = diagnosis.get("summary") or {}
            if summary.get("status") == "healthy":
                return {"success": True, "status": "healthy", "attempts": attempts, "diagnosis": diagnosis}
            expected = summary.get("expected_replicas")
            ready = summary.get("ready_replicas")
            available = summary.get("available_replicas")
            if expected is not None and ready is not None and available is not None and int(ready) >= int(expected) and int(available) >= int(expected):
                return {"success": True, "status": "healthy", "attempts": attempts, "diagnosis": diagnosis}
        if time.time() >= deadline:
            return {"success": False, "status": "timeout", "attempts": attempts, "diagnosis": diagnosis}
        time.sleep(max(1, interval_seconds))


def build_markdown_report(
    trace_id: str,
    params: Dict[str, str],
    diagnosis: Dict[str, Any],
    action_result: Dict[str, Any],
    verification: Optional[Dict[str, Any]],
    confirm: bool,
) -> str:
    target = params.get("workload_name") or params.get("name")
    top_cause = _top_cause_type(diagnosis)
    summary = diagnosis.get("summary") or {}
    action_state = "已执行" if confirm and action_result.get("success") else "预览待确认"
    verification_text = "未执行验证"
    if verification:
        verification_text = f"{verification.get('status')}，attempts={len(verification.get('attempts') or [])}"
    return "\n".join(
        [
            "# CCE 自动恢复执行报告",
            "",
            "## 1. 执行摘要",
            "",
            f"- Remediation-Trace-ID: `{trace_id}`",
            f"- 集群: `{params.get('cluster_id')}`",
            f"- 区域: `{params.get('region')}`",
            f"- 命名空间: `{params.get('namespace')}`",
            f"- 目标对象: `{target}`",
            f"- 诊断状态: `{summary.get('status')}`",
            f"- 根因类型: `{top_cause}`",
            f"- 动作: `rollback_previous_revision`，状态: `{action_state}`",
            f"- 验证: `{verification_text}`",
            "",
            "## 2. 恢复决策",
            "",
            f"- 触发依据: 工作负载发布诊断 Top cause = `{top_cause}`。",
            "- 策略: 当启动命令、应用启动、探针或镜像导致新版本不可用时，优先回滚到上一稳定 Deployment revision。",
            "- 风险边界: 回滚会创建新的 Deployment revision 并替换 PodTemplate；必须显式 `confirm=true` 才执行。",
            "",
            "## 3. 动作结果",
            "",
            f"- success: `{action_result.get('success')}`",
            f"- requires_confirmation: `{action_result.get('requires_confirmation')}`",
            f"- from_revision: `{action_result.get('from_revision') or action_result.get('current_revision')}`",
            f"- to_revision: `{action_result.get('to_revision') or action_result.get('target_revision')}`",
            f"- message: {_md_cell(action_result.get('message') or action_result.get('warning') or action_result.get('error'), 360)}",
            "",
            "## 4. 执行后验证",
            "",
            f"- 结果: `{verification_text}`",
            f"- 最新诊断摘要: `{(verification or {}).get('diagnosis', {}).get('summary')}`",
            "",
            "## 5. 后续建议",
            "",
            "- 确认业务入口和 Service endpoints 恢复后，复盘错误 command/args 的发布来源。",
            "- 如果回滚后仍不健康，回到 root-cause-analyzer 继续检查节点、网络、存储和配置变更。",
            "",
        ]
    )


def auto_remediation_run(params: Dict[str, str]) -> Dict[str, Any]:
    missing = [key for key in ("region", "cluster_id", "namespace") if not params.get(key)]
    if missing:
        return {"success": False, "error": f"{', '.join(missing)} is required"}
    if not (params.get("workload_name") or params.get("name")):
        return {"success": False, "error": "workload_name or name is required"}

    trace_id = params.get("remediation_trace_id") or f"ARR-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
    confirm = _to_bool(params.get("confirm"), False)
    strategy = params.get("strategy") or "rollback_previous_revision"
    diagnosis = _safe_rollout_diagnose(params, include_logs=_to_bool(params.get("include_logs"), True))
    cause_type = _top_cause_type(diagnosis)

    if strategy != "rollback_previous_revision":
        return {"success": False, "error": f"unsupported remediation strategy: {strategy}", "diagnosis": diagnosis}
    if diagnosis.get("success") and not _rollback_is_suitable(cause_type):
        report = build_markdown_report(trace_id, params, diagnosis, {"success": False, "error": f"top cause {cause_type} is not safe for automatic rollback"}, None, confirm)
        return {
            "success": False,
            "requires_confirmation": False,
            "remediation_trace_id": trace_id,
            "reason": f"top cause {cause_type} is not suitable for automatic rollback",
            "diagnosis": diagnosis,
            "report_markdown": report,
        }

    action_result = _safe_rollback_preview_or_run(params, confirm=confirm)
    verification = None
    if confirm and action_result.get("success") and _to_bool(params.get("wait"), True):
        verification = _wait_for_recovery(
            params,
            wait_seconds=_to_int(params.get("wait_seconds"), 120),
            interval_seconds=_to_int(params.get("interval_seconds"), 5),
        )

    report_markdown = build_markdown_report(trace_id, params, diagnosis, action_result, verification, confirm)
    output_file = params.get("output_file")
    if output_file:
        Path(output_file).write_text(report_markdown, encoding="utf-8")

    return {
        "success": bool(action_result.get("success")) if confirm else False,
        "requires_confirmation": bool(action_result.get("requires_confirmation")) if not confirm else False,
        "remediation_trace_id": trace_id,
        "strategy": strategy,
        "diagnosis": diagnosis,
        "action_result": action_result,
        "verification": verification,
        "report_markdown": report_markdown,
        "report_file": output_file,
    }


def rollback_cce_workload_action(params: Dict[str, str]) -> Dict[str, Any]:
    return rollback_cce_workload(params)


def auto_remediation_run_action(params: Dict[str, str]) -> Dict[str, Any]:
    return auto_remediation_run(params)
