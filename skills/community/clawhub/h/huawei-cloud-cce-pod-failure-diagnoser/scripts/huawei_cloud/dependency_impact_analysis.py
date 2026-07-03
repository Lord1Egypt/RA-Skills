"""Service topology based dependency impact analysis for CCE incidents."""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from . import cce


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


def _safe_capture(label: str, collector: Callable[[], Dict[str, Any]]) -> Dict[str, Any]:
    try:
        result = collector()
        if isinstance(result, dict):
            return result
        return {"success": True, "result": result}
    except Exception as exc:  # pragma: no cover - cloud/API boundary
        return {"success": False, "stage": label, "error": str(exc), "error_type": type(exc).__name__}


def _parse_selector(selector: Optional[str]) -> Dict[str, str]:
    parsed: Dict[str, str] = {}
    if not selector:
        return parsed
    for item in selector.split(","):
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key and value:
            parsed[key] = value
    return parsed


def _labels_match(selector: Dict[str, Any], labels: Dict[str, Any]) -> bool:
    if not selector:
        return False
    labels = labels or {}
    return all(str(labels.get(key)) == str(value) for key, value in selector.items())


def _pod_key(pod: Dict[str, Any]) -> str:
    return f"{pod.get('namespace')}/{pod.get('name')}"


def _service_key(service: Dict[str, Any]) -> str:
    return f"{service.get('namespace')}/{service.get('name')}"


def _ingress_key(ingress: Dict[str, Any]) -> str:
    return f"{ingress.get('namespace')}/{ingress.get('name')}"


def _owner_names(pod: Dict[str, Any]) -> List[str]:
    return [
        str(ref.get("name"))
        for ref in (pod.get("owner_references") or [])
        if isinstance(ref, dict) and ref.get("name")
    ]


def _target_pods(
    pods: List[Dict[str, Any]],
    namespace: Optional[str],
    target_name: Optional[str],
    label_selector: Optional[str],
) -> Tuple[List[Dict[str, Any]], str]:
    selector = _parse_selector(label_selector)
    if selector:
        matched = [
            pod for pod in pods
            if (not namespace or pod.get("namespace") == namespace)
            and _labels_match(selector, pod.get("labels") or {})
        ]
        return matched, f"label_selector={label_selector}"

    if target_name:
        matched = []
        for pod in pods:
            if namespace and pod.get("namespace") != namespace:
                continue
            pod_name = str(pod.get("name") or "")
            labels = pod.get("labels") or {}
            owner_names = _owner_names(pod)
            if (
                pod_name == target_name
                or pod_name.startswith(f"{target_name}-")
                or target_name in owner_names
                or any(str(value) == target_name for value in labels.values())
            ):
                matched.append(pod)
        return matched, f"target_name={target_name}"

    matched = [pod for pod in pods if not namespace or pod.get("namespace") == namespace]
    return matched, f"namespace={namespace or 'all'}"


def _services_for_pods(services: List[Dict[str, Any]], pods: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result = []
    for service in services:
        selector = service.get("selector") or {}
        if not selector:
            continue
        for pod in pods:
            if service.get("namespace") != pod.get("namespace"):
                continue
            if _labels_match(selector, pod.get("labels") or {}):
                result.append(service)
                break
    return sorted(result, key=_service_key)


def _services_for_ingress(ingress: Dict[str, Any]) -> List[str]:
    namespace = ingress.get("namespace")
    result = []
    for rule in ingress.get("rules") or []:
        for path in rule.get("paths") or []:
            backend = path.get("backend") or {}
            service_name = backend.get("service_name") or path.get("service_name")
            if service_name:
                result.append(f"{namespace}/{service_name}")
    default_backend = ingress.get("default_backend") or {}
    if default_backend.get("service_name"):
        result.append(f"{namespace}/{default_backend['service_name']}")
    return sorted(set(result))


def _ingresses_for_services(ingresses: List[Dict[str, Any]], services: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    service_keys = {_service_key(service) for service in services}
    result = []
    for ingress in ingresses:
        if service_keys.intersection(_services_for_ingress(ingress)):
            result.append(ingress)
    return sorted(result, key=_ingress_key)


def _pod_ready(pod: Dict[str, Any]) -> bool:
    for condition in pod.get("conditions") or []:
        if condition.get("type") == "Ready":
            return condition.get("status") == "True"
    containers = pod.get("containers") or []
    return bool(containers) and all(container.get("ready") is True for container in containers)


def _pod_health_summary(pods: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(pods)
    ready = sum(1 for pod in pods if _pod_ready(pod))
    abnormal = [
        _pod_key(pod)
        for pod in pods
        if pod.get("status") not in {"Running", "Succeeded"} or not _pod_ready(pod)
    ]
    return {
        "total": total,
        "ready": ready,
        "unready": total - ready,
        "abnormal_pods": abnormal[:20],
        "availability": "available" if total and ready == total else "degraded" if ready else "unavailable",
    }


def _host_entries(ingress: Dict[str, Any]) -> List[str]:
    hosts = []
    for rule in ingress.get("rules") or []:
        host = rule.get("host")
        if host:
            hosts.append(str(host))
    return sorted(set(hosts))


def _propagation_paths(
    target_pods: List[Dict[str, Any]],
    services: List[Dict[str, Any]],
    ingresses: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    paths: List[Dict[str, Any]] = []
    target_pod_keys = [_pod_key(pod) for pod in target_pods]
    for ingress in ingresses:
        for service_key in _services_for_ingress(ingress):
            if service_key not in {_service_key(service) for service in services}:
                continue
            hosts = _host_entries(ingress)
            paths.append({
                "direction": "upstream-to-target",
                "entry": ", ".join(hosts) if hosts else _ingress_key(ingress),
                "path": [f"Ingress:{_ingress_key(ingress)}", f"Service:{service_key}", f"Pods:{', '.join(target_pod_keys[:5])}"],
                "impact": "external traffic to this backend can fail or degrade when target pods are unavailable",
            })
    for service in services:
        paths.append({
            "direction": "cluster-to-target",
            "entry": f"{service.get('name')}.{service.get('namespace')}.svc",
            "path": [f"Service:{_service_key(service)}", f"Pods:{', '.join(target_pod_keys[:5])}"],
            "impact": "in-cluster callers using the service DNS can fail or degrade when endpoints are unhealthy",
        })
    if not paths and target_pods:
        paths.append({
            "direction": "direct-pod",
            "entry": "Pod IP or owner workload",
            "path": [f"Pods:{', '.join(target_pod_keys[:8])}"],
            "impact": "no Service/Ingress was found; blast radius appears limited to direct Pod consumers or batch execution",
        })
    return paths


def _risk_level(health: Dict[str, Any], services: List[Dict[str, Any]], ingresses: List[Dict[str, Any]]) -> Tuple[str, int, str]:
    if not health["total"]:
        return "Unknown", 30, "没有匹配到目标 Pod，无法判断实际可用性。"
    exposure = len(services) + len(ingresses) * 2
    if health["ready"] == 0 and exposure >= 2:
        return "High", 88, "目标 Pod 全部不可用且存在 Service/Ingress 暴露路径。"
    if health["ready"] == 0:
        return "High", 78, "目标 Pod 全部不可用，影响所有直接消费者。"
    if health["unready"] > 0 and exposure >= 2:
        return "Medium", 64, "目标 Pod 部分不可用且存在入口或服务依赖。"
    if health["unready"] > 0:
        return "Medium", 55, "目标 Pod 部分不可用，影响范围取决于副本和流量分布。"
    if exposure >= 2:
        return "Low", 35, "目标 Pod 当前可用，但存在上游依赖路径，后续故障会沿拓扑传播。"
    return "Low", 25, "目标当前可用，且未发现明显外部入口。"


def _topology_mermaid(paths: List[Dict[str, Any]]) -> str:
    lines = ["flowchart LR"]
    if not paths:
        lines.append('  scope["No topology path found"]')
        return "\n".join(lines)
    node_id = 0
    for path in paths[:8]:
        previous = None
        for item in path.get("path") or []:
            node_id += 1
            current = f"N{node_id}"
            label = str(item).replace('"', "'")
            lines.append(f'  {current}["{label}"]')
            if previous:
                lines.append(f"  {previous} --> {current}")
            previous = current
    return "\n".join(lines)


def _capture_status_rows(captures: Dict[str, Dict[str, Any]]) -> List[Tuple[str, str, str]]:
    mapping = {
        "pods": "Pod 快照",
        "services": "Service 快照",
        "ingresses": "Ingress 快照",
        "nodes": "Node 快照",
    }
    rows = []
    for key, label in mapping.items():
        item = captures.get(key) or {}
        rows.append((label, "成功" if item.get("success") else "失败", item.get("error") or f"count={item.get('count', '-')}" ))
    return rows


def build_markdown_report(
    trace_id: str,
    params: Dict[str, str],
    captures: Dict[str, Dict[str, Any]],
    target_pods: List[Dict[str, Any]],
    target_services: List[Dict[str, Any]],
    target_ingresses: List[Dict[str, Any]],
    health: Dict[str, Any],
    paths: List[Dict[str, Any]],
    risk_level: str,
    risk_score: int,
    risk_reason: str,
) -> str:
    target = params.get("target_name") or params.get("workload_name") or params.get("app_name") or params.get("name") or "未指定"
    status_rows = [
        "| 数据源 | 状态 | 说明 |",
        "| --- | --- | --- |",
        *[f"| {_md_cell(source)} | {_md_cell(status)} | {_md_cell(note)} |" for source, status, note in _capture_status_rows(captures)],
    ]
    pod_rows = [
        "| Pod | 状态 | Ready | Node | IP |",
        "| --- | --- | --- | --- | --- |",
    ]
    for pod in target_pods[:20]:
        pod_rows.append(
            f"| {_md_cell(_pod_key(pod))} | {_md_cell(pod.get('status'))} | {_md_cell(_pod_ready(pod))} | "
            f"{_md_cell(pod.get('node'))} | {_md_cell(pod.get('ip'))} |"
        )
    if len(pod_rows) == 2:
        pod_rows.append("| - | - | - | - | - |")

    service_rows = [
        "| Service | Type | ClusterIP | Ports | Selector |",
        "| --- | --- | --- | --- | --- |",
    ]
    for service in target_services[:20]:
        ports = ", ".join(str(port.get("port")) for port in service.get("ports") or [])
        service_rows.append(
            f"| {_md_cell(_service_key(service))} | {_md_cell(service.get('type'))} | {_md_cell(service.get('cluster_ip'))} | "
            f"{_md_cell(ports)} | {_md_cell(json.dumps(service.get('selector') or {}, ensure_ascii=False))} |"
        )
    if len(service_rows) == 2:
        service_rows.append("| - | - | - | - | - |")

    ingress_rows = [
        "| Ingress | Hosts | Backend Services | LB |",
        "| --- | --- | --- | --- |",
    ]
    for ingress in target_ingresses[:20]:
        ingress_rows.append(
            f"| {_md_cell(_ingress_key(ingress))} | {_md_cell(', '.join(_host_entries(ingress)))} | "
            f"{_md_cell(', '.join(_services_for_ingress(ingress)))} | {_md_cell(json.dumps(ingress.get('load_balancer_ingress') or [], ensure_ascii=False))} |"
        )
    if len(ingress_rows) == 2:
        ingress_rows.append("| - | - | - | - |")

    path_lines = []
    for path in paths:
        path_lines.append(f"- **{path.get('direction')}**: {' -> '.join(path.get('path') or [])}。影响: {path.get('impact')}")
    if not path_lines:
        path_lines.append("- 未发现可建模传播路径。")

    return "\n".join(
        [
            "# CCE 依赖影响面分析报告",
            "",
            "## 1. 分析摘要",
            "",
            f"- Analysis-Trace-ID: `{trace_id}`",
            f"- 集群: `{params.get('cluster_id')}`",
            f"- 区域: `{params.get('region')}`",
            f"- 命名空间: `{params.get('namespace') or '全集群'}`",
            f"- 目标对象: `{target}`",
            f"- 风险等级: `{risk_level}`，评分 `{risk_score}/100`",
            f"- 初步结论: {risk_reason}",
            "",
            "## 2. 排查过程",
            "",
            "1. 拉取 Pod、Service、Ingress、Node 当前快照，构建命名空间内服务拓扑。",
            "2. 按目标名称或 label selector 定位目标 Pod，并识别 Ready/异常副本。",
            "3. 用 Service selector 反查上游服务，再从 Ingress backend 反查外部入口。",
            "4. 生成故障传播路径、上下游影响面、证据表和能力缺口。",
            "",
            "## 3. 数据源与采集状态",
            "",
            "\n".join(status_rows),
            "",
            "## 4. 目标健康证据",
            "",
            f"- Pod 总数: `{health['total']}`，Ready: `{health['ready']}`，Unready: `{health['unready']}`，可用性: `{health['availability']}`",
            "\n".join(pod_rows),
            "",
            "## 5. 上游入口与服务暴露",
            "",
            "\n".join(service_rows),
            "",
            "\n".join(ingress_rows),
            "",
            "## 6. 故障传播路径",
            "",
            "\n".join(path_lines),
            "",
            "```mermaid",
            _topology_mermaid(paths),
            "```",
            "",
            "## 7. 影响面结论",
            "",
            f"- 上游入口: `{len(target_ingresses)}` 个 Ingress，`{len(target_services)}` 个 Service。",
            f"- 直接受影响 Pod: `{len(target_pods)}` 个，异常 Pod: `{len(health['abnormal_pods'])}` 个。",
            "- 下游依赖: 当前仅从 Kubernetes Service/Ingress 静态拓扑推断，无法证明应用运行时实际调用链。",
            "- 置信度: 如果无服务网格、APM 或访问日志，服务之间的消费者关系按“可能影响”而非“已观测影响”处理。",
            "",
            "## 8. 能力复用与缺口",
            "",
            "- 已复用 `huawei_get_cce_pods`、`huawei_get_cce_services`、`huawei_get_cce_ingresses`、`huawei_get_kubernetes_nodes`。",
            "- 建议补充 Endpoints/EndpointSlice 原子查询，识别 Service 是否真正有后端地址。",
            "- 建议补充 NetworkPolicy、Gateway API、Service Mesh/APM 调用边数据，提升上下游判断置信度。",
            "",
        ]
    )


def analyze_dependency_impact(params: Dict[str, str]) -> Dict[str, Any]:
    missing = [key for key in ("region", "cluster_id") if not params.get(key)]
    if missing:
        return {"success": False, "error": f"{', '.join(missing)} is required"}

    region = params["region"]
    cluster_id = params["cluster_id"]
    namespace = params.get("namespace")
    ak = params.get("ak")
    sk = params.get("sk")
    project_id = params.get("project_id")
    trace_id = params.get("analysis_trace_id") or f"DIA-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"

    captures = {
        "pods": _safe_capture("pods", lambda: cce.get_kubernetes_pods(region, cluster_id, ak, sk, project_id, namespace, params.get("label_selector"))),
        "services": _safe_capture("services", lambda: cce.get_kubernetes_services(region, cluster_id, ak, sk, project_id, namespace)),
        "ingresses": _safe_capture("ingresses", lambda: cce.get_kubernetes_ingresses(region, cluster_id, ak, sk, project_id, namespace)),
        "nodes": _safe_capture("nodes", lambda: cce.get_kubernetes_nodes(region, cluster_id, ak, sk, project_id)),
    }

    pods = captures["pods"].get("pods", []) if captures["pods"].get("success") else []
    services = captures["services"].get("services", []) if captures["services"].get("success") else []
    ingresses = captures["ingresses"].get("ingresses", []) if captures["ingresses"].get("success") else []

    target_name = params.get("target_name") or params.get("workload_name") or params.get("app_name") or params.get("name")
    target_pods, match_reason = _target_pods(pods, namespace, target_name, params.get("label_selector"))
    target_services = _services_for_pods(services, target_pods)
    if target_name:
        target_services.extend(
            service for service in services
            if service.get("namespace") == namespace and service.get("name") == target_name and service not in target_services
        )
    target_services = sorted({ _service_key(service): service for service in target_services }.values(), key=_service_key)
    target_ingresses = _ingresses_for_services(ingresses, target_services)
    health = _pod_health_summary(target_pods)
    paths = _propagation_paths(target_pods, target_services, target_ingresses)
    risk_level, risk_score, risk_reason = _risk_level(health, target_services, target_ingresses)

    report_markdown = build_markdown_report(
        trace_id,
        params,
        captures,
        target_pods,
        target_services,
        target_ingresses,
        health,
        paths,
        risk_level,
        risk_score,
        risk_reason,
    )
    output_file = params.get("output_file")
    if output_file:
        Path(output_file).write_text(report_markdown, encoding="utf-8")

    return {
        "success": True,
        "analysis_trace_id": trace_id,
        "scope": {
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace,
            "target_name": target_name,
            "match_reason": match_reason,
        },
        "summary": {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risk_reason": risk_reason,
            "pod_health": health,
            "service_count": len(target_services),
            "ingress_count": len(target_ingresses),
            "path_count": len(paths),
        },
        "target": {
            "pods": [_pod_key(pod) for pod in target_pods],
            "services": [_service_key(service) for service in target_services],
            "ingresses": [_ingress_key(ingress) for ingress in target_ingresses],
        },
        "propagation_paths": paths,
        "report_markdown": report_markdown,
        "report_file": output_file,
        "capture_metadata": {
            key: {"success": value.get("success"), "count": value.get("count"), "error": value.get("error")}
            for key, value in captures.items()
        },
    }


def analyze_dependency_impact_action(params: Dict[str, str]) -> Dict[str, Any]:
    return analyze_dependency_impact(params)
