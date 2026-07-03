"""CCE storage failure diagnosis with Kubernetes evidence and Markdown output."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

from . import network, storage
from .cce_k8s import _setup_k8s_client
from .common import (
    IMPORT_ERROR,
    K8S_AVAILABLE,
    K8S_IMPORT_ERROR,
    SDK_AVAILABLE,
    _safe_delete_file,
    get_credentials_with_region,
    k8s_client,
)


CAPACITY_THRESHOLD = 0.95
INODE_THRESHOLD = 0.95
CSI_LOG_PATTERNS = re.compile(
    r"(?i)(obs|sfs|sfsturbo|nfs|evs|volume|mount|attach|403|forbidden|signaturedoesnotmatch|"
    r"permission denied|i/o error|input/output error|read-only file system|timeout)"
)
SECRET_PATTERNS = [
    re.compile(r"(?i)(authorization:\s*bearer\s+)[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)((?:password|passwd|token|secret|access[_-]?key|secret[_-]?key)\s*[=:]\s*)\S+"),
    re.compile(r"(?i)(x-auth-token\s*[=:]\s*)\S+"),
    re.compile(r"(?i)((?:ak|sk)\s*[=:]\s*)\S+"),
]


def _as_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"0", "false", "no", "off"}


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _k8s_ts(value: Any) -> Optional[str]:
    return str(value) if value else None


def _parse_dt(value: Any) -> Optional[datetime]:
    if not value:
        return None
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if text.endswith("Z"):
            text = f"{text[:-1]}+00:00"
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _md_cell(value: Any, max_len: int = 180) -> str:
    if value is None or value == "":
        return "-"
    text = str(value).replace("\n", " ").replace("|", "\\|").strip()
    if len(text) > max_len:
        return f"{text[: max_len - 3]}..."
    return text


def _mask_secrets(text: str) -> str:
    masked = text or ""
    for pattern in SECRET_PATTERNS:
        masked = pattern.sub(r"\1***", masked)
    return masked


def _log_excerpt(logs: str, max_lines: int = 80, max_chars: int = 8000) -> str:
    selected = [line for line in (logs or "").splitlines() if CSI_LOG_PATTERNS.search(line)]
    if not selected:
        selected = (logs or "").splitlines()[-min(max_lines, 20):]
    excerpt = "\n".join(selected[-max_lines:])
    return _mask_secrets(excerpt[-max_chars:])


def _dict_or_empty(value: Any) -> Dict[str, Any]:
    return dict(value or {})


def _list_or_empty(value: Any) -> List[Any]:
    return list(value or [])


def _resource_to_bytes(value: Any) -> Optional[float]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        pass
    match = re.fullmatch(r"([0-9.]+)\s*([KMGTPE]i?|m)?", text)
    if not match:
        return None
    number = float(match.group(1))
    suffix = match.group(2) or ""
    binary = {"Ki": 1024, "Mi": 1024**2, "Gi": 1024**3, "Ti": 1024**4, "Pi": 1024**5, "Ei": 1024**6}
    decimal = {"K": 1000, "M": 1000**2, "G": 1000**3, "T": 1000**4, "P": 1000**5, "E": 1000**6}
    if suffix == "m":
        return number / 1000
    return number * binary.get(suffix, decimal.get(suffix, 1))


def _quantity_dict(value: Any) -> Dict[str, str]:
    if not value:
        return {}
    try:
        return {key: str(val) for key, val in dict(value).items()}
    except Exception:
        return {}


def _selector_terms_to_dict(node_selector: Any) -> List[Dict[str, Any]]:
    if not node_selector:
        return []
    terms = []
    for term in getattr(node_selector, "node_selector_terms", None) or []:
        expressions = []
        for expr in getattr(term, "match_expressions", None) or []:
            expressions.append({
                "key": getattr(expr, "key", None),
                "operator": getattr(expr, "operator", None),
                "values": list(getattr(expr, "values", None) or []),
            })
        fields = []
        for field in getattr(term, "match_fields", None) or []:
            fields.append({
                "key": getattr(field, "key", None),
                "operator": getattr(field, "operator", None),
                "values": list(getattr(field, "values", None) or []),
            })
        terms.append({"match_expressions": expressions, "match_fields": fields})
    return terms


def _selector_expr_matches(labels: Dict[str, str], expr: Dict[str, Any]) -> bool:
    key = expr.get("key")
    operator = expr.get("operator")
    values = expr.get("values") or []
    current = (labels or {}).get(key)
    if operator == "In":
        return current in values
    if operator == "NotIn":
        return current not in values
    if operator == "Exists":
        return key in labels
    if operator == "DoesNotExist":
        return key not in labels
    if operator == "Gt":
        try:
            return int(current or 0) > int(values[0])
        except (TypeError, ValueError, IndexError):
            return False
    if operator == "Lt":
        try:
            return int(current or 0) < int(values[0])
        except (TypeError, ValueError, IndexError):
            return False
    return False


def _node_matches_terms(node: Dict[str, Any], terms: List[Dict[str, Any]]) -> bool:
    if not terms:
        return True
    labels = node.get("labels") or {}
    for term in terms:
        expressions = term.get("match_expressions") or []
        fields = term.get("match_fields") or []
        if all(_selector_expr_matches(labels, expr) for expr in expressions):
            if not fields:
                return True
            field_ok = True
            for field in fields:
                if field.get("key") == "metadata.name":
                    fake = {"metadata.name": node.get("name")}
                    field_ok = field_ok and _selector_expr_matches(fake, field)
                else:
                    field_ok = False
            if field_ok:
                return True
    return False


def _tolerates_taint(tolerations: List[Dict[str, Any]], taint: Dict[str, Any]) -> bool:
    for tol in tolerations or []:
        effect = tol.get("effect")
        if effect and effect != taint.get("effect"):
            continue
        operator = tol.get("operator") or "Equal"
        if operator == "Exists" and tol.get("key") == taint.get("key"):
            return True
        if operator == "Equal" and tol.get("key") == taint.get("key") and str(tol.get("value")) == str(taint.get("value")):
            return True
    return False


def _blocking_taints(node: Dict[str, Any], pod: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    tolerations = (pod or {}).get("tolerations") or []
    blocked = []
    for taint in node.get("taints") or []:
        if taint.get("effect") not in {"NoSchedule", "NoExecute"}:
            continue
        if not _tolerates_taint(tolerations, taint):
            blocked.append(taint)
    return blocked


def _node_ready(node: Dict[str, Any]) -> bool:
    return str(node.get("ready")) == "True"


def _event_sort_key(event: Dict[str, Any]) -> datetime:
    return (
        _parse_dt(event.get("last_timestamp"))
        or _parse_dt(event.get("event_time"))
        or _parse_dt(event.get("first_timestamp"))
        or datetime.min.replace(tzinfo=timezone.utc)
    )


def _event_text(event: Dict[str, Any]) -> str:
    return " ".join(str(event.get(key) or "") for key in ("reason", "message", "source")).lower()


def _event_to_dict(event: Any) -> Dict[str, Any]:
    involved = getattr(event, "involved_object", None)
    source = getattr(event, "source", None)
    return {
        "name": getattr(getattr(event, "metadata", None), "name", None),
        "namespace": getattr(getattr(event, "metadata", None), "namespace", None),
        "type": getattr(event, "type", None),
        "reason": getattr(event, "reason", None),
        "message": getattr(event, "message", None),
        "source": getattr(source, "component", None) or getattr(event, "reporting_component", None),
        "first_timestamp": _k8s_ts(getattr(event, "first_timestamp", None)),
        "last_timestamp": _k8s_ts(getattr(event, "last_timestamp", None)),
        "event_time": _k8s_ts(getattr(event, "event_time", None)),
        "count": getattr(event, "count", None) or 1,
        "involved_object": {
            "kind": getattr(involved, "kind", None),
            "name": getattr(involved, "name", None),
            "namespace": getattr(involved, "namespace", None),
        } if involved else {},
    }


def _condition_to_dict(condition: Any) -> Dict[str, Any]:
    return {
        "type": getattr(condition, "type", None),
        "status": getattr(condition, "status", None),
        "reason": getattr(condition, "reason", None),
        "message": getattr(condition, "message", None),
        "last_transition_time": _k8s_ts(getattr(condition, "last_transition_time", None)),
    }


def _node_to_dict(node: Any) -> Dict[str, Any]:
    status = getattr(node, "status", None)
    spec = getattr(node, "spec", None)
    metadata = getattr(node, "metadata", None)
    conditions = [_condition_to_dict(item) for item in getattr(status, "conditions", None) or []]
    condition_map = {item.get("type"): item for item in conditions}
    taints = []
    for taint in getattr(spec, "taints", None) or []:
        taints.append({
            "key": getattr(taint, "key", None),
            "value": getattr(taint, "value", None),
            "effect": getattr(taint, "effect", None),
        })
    return {
        "name": getattr(metadata, "name", None),
        "labels": _dict_or_empty(getattr(metadata, "labels", None)),
        "ready": condition_map.get("Ready", {}).get("status", "Unknown"),
        "conditions": conditions,
        "taints": taints,
        "capacity": _quantity_dict(getattr(status, "capacity", None)),
        "allocatable": _quantity_dict(getattr(status, "allocatable", None)),
    }


def _storage_class_to_dict(sc: Any) -> Dict[str, Any]:
    metadata = getattr(sc, "metadata", None)
    return {
        "name": getattr(metadata, "name", None),
        "provisioner": getattr(sc, "provisioner", None),
        "parameters": _dict_or_empty(getattr(sc, "parameters", None)),
        "reclaim_policy": getattr(sc, "reclaim_policy", None),
        "volume_binding_mode": getattr(sc, "volume_binding_mode", None),
        "allow_volume_expansion": getattr(sc, "allow_volume_expansion", None),
        "mount_options": list(getattr(sc, "mount_options", None) or []),
        "annotations": _dict_or_empty(getattr(metadata, "annotations", None)),
    }


def _pvc_to_dict(pvc: Any) -> Dict[str, Any]:
    metadata = getattr(pvc, "metadata", None)
    spec = getattr(pvc, "spec", None)
    status = getattr(pvc, "status", None)
    conditions = [_condition_to_dict(item) for item in getattr(status, "conditions", None) or []]
    resources = getattr(spec, "resources", None)
    requests = _quantity_dict(getattr(resources, "requests", None))
    return {
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "status": getattr(status, "phase", None),
        "volume": getattr(spec, "volume_name", None),
        "storage_class": getattr(spec, "storage_class_name", None),
        "requested": requests,
        "capacity": _quantity_dict(getattr(status, "capacity", None)),
        "access_modes": list(getattr(spec, "access_modes", None) or []),
        "actual_access_modes": list(getattr(status, "access_modes", None) or []),
        "volume_mode": getattr(spec, "volume_mode", None),
        "conditions": conditions,
        "finalizers": list(getattr(metadata, "finalizers", None) or []),
        "deletion_timestamp": _k8s_ts(getattr(metadata, "deletion_timestamp", None)),
        "created": _k8s_ts(getattr(metadata, "creation_timestamp", None)),
        "labels": _dict_or_empty(getattr(metadata, "labels", None)),
        "annotations": _dict_or_empty(getattr(metadata, "annotations", None)),
    }


def _pv_source(pv: Any) -> Dict[str, Any]:
    spec = getattr(pv, "spec", None)
    source = {"type": "unknown"}
    if not spec:
        return source
    csi = getattr(spec, "csi", None)
    if csi:
        return {
            "type": "csi",
            "driver": getattr(csi, "driver", None),
            "volume_handle": getattr(csi, "volume_handle", None),
            "fs_type": getattr(csi, "fs_type", None),
            "volume_attributes": _dict_or_empty(getattr(csi, "volume_attributes", None)),
        }
    if getattr(spec, "cinder", None):
        cinder = spec.cinder
        return {"type": "cinder", "volume_id": getattr(cinder, "volume_id", None), "fs_type": getattr(cinder, "fs_type", None)}
    if getattr(spec, "nfs", None):
        nfs = spec.nfs
        return {"type": "nfs", "server": getattr(nfs, "server", None), "path": getattr(nfs, "path", None)}
    if getattr(spec, "local", None):
        local = spec.local
        return {"type": "local", "path": getattr(local, "path", None)}
    if getattr(spec, "host_path", None):
        host_path = spec.host_path
        return {"type": "host_path", "path": getattr(host_path, "path", None)}
    if getattr(spec, "flex_volume", None):
        flex = spec.flex_volume
        return {
            "type": "flex_volume",
            "driver": getattr(flex, "driver", None),
            "fs_type": getattr(flex, "fs_type", None),
            "options": _dict_or_empty(getattr(flex, "options", None)),
        }
    for attr in ("obs", "nas"):
        if getattr(spec, attr, None):
            item = getattr(spec, attr)
            return {
                "type": attr,
                "server": getattr(item, "server", None),
                "path": getattr(item, "path", None),
                "bucket": getattr(item, "bucket", None),
                "endpoint": getattr(item, "endpoint", None),
            }
    return source


def _pv_to_dict(pv: Any) -> Dict[str, Any]:
    metadata = getattr(pv, "metadata", None)
    spec = getattr(pv, "spec", None)
    status = getattr(pv, "status", None)
    claim_ref = getattr(spec, "claim_ref", None)
    node_affinity = getattr(spec, "node_affinity", None)
    required = getattr(node_affinity, "required", None) if node_affinity else None
    return {
        "name": getattr(metadata, "name", None),
        "status": getattr(status, "phase", None),
        "capacity": _quantity_dict(getattr(spec, "capacity", None)),
        "access_modes": list(getattr(spec, "access_modes", None) or []),
        "storage_class": getattr(spec, "storage_class_name", None),
        "reclaim_policy": getattr(spec, "persistent_volume_reclaim_policy", None),
        "volume_mode": getattr(spec, "volume_mode", None),
        "claim_ref": {
            "namespace": getattr(claim_ref, "namespace", None),
            "name": getattr(claim_ref, "name", None),
        } if claim_ref else None,
        "source": _pv_source(pv),
        "node_affinity": {"required": _selector_terms_to_dict(required)} if required else {},
        "conditions": [_condition_to_dict(item) for item in getattr(status, "conditions", None) or []],
        "finalizers": list(getattr(metadata, "finalizers", None) or []),
        "created": _k8s_ts(getattr(metadata, "creation_timestamp", None)),
        "labels": _dict_or_empty(getattr(metadata, "labels", None)),
        "annotations": _dict_or_empty(getattr(metadata, "annotations", None)),
    }


def _container_status_to_dict(status: Any) -> Dict[str, Any]:
    state = getattr(status, "state", None)
    waiting = getattr(state, "waiting", None) if state else None
    running = getattr(state, "running", None) if state else None
    terminated = getattr(state, "terminated", None) if state else None
    last = getattr(status, "last_state", None)
    last_terminated = getattr(last, "terminated", None) if last else None
    return {
        "name": getattr(status, "name", None),
        "ready": getattr(status, "ready", None),
        "restart_count": getattr(status, "restart_count", 0),
        "waiting_reason": getattr(waiting, "reason", None),
        "waiting_message": getattr(waiting, "message", None),
        "running_started_at": _k8s_ts(getattr(running, "started_at", None)),
        "terminated_reason": getattr(terminated, "reason", None),
        "last_terminated_reason": getattr(last_terminated, "reason", None),
        "last_exit_code": getattr(last_terminated, "exit_code", None),
        "last_started_at": _k8s_ts(getattr(last_terminated, "started_at", None)),
        "last_finished_at": _k8s_ts(getattr(last_terminated, "finished_at", None)),
    }


def _pod_resources(container: Any) -> Dict[str, Any]:
    resources = getattr(container, "resources", None)
    return {
        "requests": _quantity_dict(getattr(resources, "requests", None)),
        "limits": _quantity_dict(getattr(resources, "limits", None)),
    }


def _pod_to_dict(pod: Any) -> Dict[str, Any]:
    metadata = getattr(pod, "metadata", None)
    spec = getattr(pod, "spec", None)
    status = getattr(pod, "status", None)
    volumes = []
    volume_source_by_name = {}
    for volume in getattr(spec, "volumes", None) or []:
        item: Dict[str, Any] = {"name": getattr(volume, "name", None)}
        if getattr(volume, "persistent_volume_claim", None):
            item["pvc"] = getattr(volume.persistent_volume_claim, "claim_name", None)
        if getattr(volume, "config_map", None):
            item["config_map"] = getattr(volume.config_map, "name", None)
        if getattr(volume, "secret", None):
            item["secret"] = getattr(volume.secret, "secret_name", None)
        if getattr(volume, "empty_dir", None) is not None:
            item["empty_dir"] = True
        volume_source_by_name[item["name"]] = item
        volumes.append(item)

    mounts = []
    containers = list(getattr(spec, "init_containers", None) or []) + list(getattr(spec, "containers", None) or [])
    container_specs = {}
    for container in containers:
        container_specs[getattr(container, "name", None)] = {
            "name": getattr(container, "name", None),
            "resources": _pod_resources(container),
        }
        for mount in getattr(container, "volume_mounts", None) or []:
            item = {
                "container": getattr(container, "name", None),
                "name": getattr(mount, "name", None),
                "mount_path": getattr(mount, "mount_path", None),
                "sub_path": getattr(mount, "sub_path", None),
                "read_only": getattr(mount, "read_only", None),
            }
            item["source"] = volume_source_by_name.get(item["name"], {})
            mounts.append(item)

    tolerations = []
    for toleration in getattr(spec, "tolerations", None) or []:
        tolerations.append({
            "key": getattr(toleration, "key", None),
            "operator": getattr(toleration, "operator", None),
            "value": getattr(toleration, "value", None),
            "effect": getattr(toleration, "effect", None),
        })

    conditions = [_condition_to_dict(item) for item in getattr(status, "conditions", None) or []]
    return {
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "phase": getattr(status, "phase", None),
        "reason": getattr(status, "reason", None),
        "message": getattr(status, "message", None),
        "node": getattr(spec, "node_name", None),
        "pod_ip": getattr(status, "pod_ip", None),
        "created": _k8s_ts(getattr(metadata, "creation_timestamp", None)),
        "deletion_timestamp": _k8s_ts(getattr(metadata, "deletion_timestamp", None)),
        "labels": _dict_or_empty(getattr(metadata, "labels", None)),
        "annotations": _dict_or_empty(getattr(metadata, "annotations", None)),
        "node_selector": _dict_or_empty(getattr(spec, "node_selector", None)),
        "tolerations": tolerations,
        "volumes": volumes,
        "volume_mounts": mounts,
        "containers": [_container_status_to_dict(item) for item in getattr(status, "container_statuses", None) or []],
        "init_containers": [_container_status_to_dict(item) for item in getattr(status, "init_container_statuses", None) or []],
        "container_specs": container_specs,
        "conditions": conditions,
    }


def _volume_attachment_to_dict(item: Any) -> Dict[str, Any]:
    metadata = getattr(item, "metadata", None)
    spec = getattr(item, "spec", None)
    status = getattr(item, "status", None)
    source = getattr(spec, "source", None)
    attach_error = getattr(status, "attach_error", None)
    detach_error = getattr(status, "detach_error", None)
    return {
        "name": getattr(metadata, "name", None),
        "attacher": getattr(spec, "attacher", None),
        "node_name": getattr(spec, "node_name", None),
        "volume_name": getattr(source, "persistent_volume_name", None),
        "attached": getattr(status, "attached", None),
        "attach_error": {
            "message": getattr(attach_error, "message", None),
            "time": _k8s_ts(getattr(attach_error, "time", None)),
        } if attach_error else None,
        "detach_error": {
            "message": getattr(detach_error, "message", None),
            "time": _k8s_ts(getattr(detach_error, "time", None)),
        } if detach_error else None,
        "created": _k8s_ts(getattr(metadata, "creation_timestamp", None)),
    }


def _network_policy_to_dict(policy: Any) -> Dict[str, Any]:
    metadata = getattr(policy, "metadata", None)
    spec = getattr(policy, "spec", None)
    return {
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "policy_types": list(getattr(spec, "policy_types", None) or []),
        "pod_selector": getattr(getattr(spec, "pod_selector", None), "match_labels", None) or {},
    }


def _metadata_ref_to_dict(obj: Any, kind: str) -> Dict[str, Any]:
    metadata = getattr(obj, "metadata", None)
    managed_times = [
        _parse_dt(getattr(field, "time", None))
        for field in getattr(metadata, "managed_fields", None) or []
        if getattr(field, "time", None)
    ]
    latest = max([item for item in managed_times if item], default=None)
    return {
        "kind": kind,
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "resource_version": getattr(metadata, "resource_version", None),
        "created": _k8s_ts(getattr(metadata, "creation_timestamp", None)),
        "latest_managed_time": latest.isoformat() if latest else None,
    }


def _safe_call(label: str, fn: Any, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    try:
        result = fn(*args, **kwargs)
        if isinstance(result, dict):
            return result
        return {"success": True, "result": result}
    except Exception as exc:
        return {"success": False, "stage": label, "error": str(exc), "error_type": type(exc).__name__}


def _read_node_stats(v1: Any, node_name: str) -> Dict[str, Any]:
    for path in ("stats/summary", "/stats/summary"):
        try:
            data = v1.connect_get_node_proxy_with_path(node_name, path)
            if isinstance(data, (bytes, bytearray)):
                data = data.decode("utf-8")
            if isinstance(data, str):
                return {"success": True, "node": node_name, "summary": json.loads(data)}
            return {"success": True, "node": node_name, "summary": data}
        except Exception as exc:
            last_error = exc
    return {"success": False, "node": node_name, "error": str(last_error), "error_type": type(last_error).__name__}


def _extract_pvc_volume_stats(node_stats: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    volumes = []
    for node_name, stats in (node_stats or {}).items():
        summary = (stats or {}).get("summary") or {}
        for pod in summary.get("pods") or []:
            pod_ref = pod.get("podRef") or {}
            for volume in pod.get("volume") or []:
                pvc_ref = volume.get("pvcRef") or {}
                if not pvc_ref:
                    continue
                capacity = volume.get("capacityBytes")
                used = volume.get("usedBytes")
                inodes = volume.get("inodes")
                inodes_used = volume.get("inodesUsed")
                volumes.append({
                    "node": node_name,
                    "pod": pod_ref,
                    "name": volume.get("name"),
                    "pvc": {
                        "namespace": pvc_ref.get("namespace") or pod_ref.get("namespace"),
                        "name": pvc_ref.get("name"),
                    },
                    "used_bytes": used,
                    "capacity_bytes": capacity,
                    "usage_ratio": (float(used) / float(capacity)) if used is not None and capacity else None,
                    "inodes_used": inodes_used,
                    "inodes": inodes,
                    "inode_ratio": (float(inodes_used) / float(inodes)) if inodes_used is not None and inodes else None,
                })
    return volumes


def _read_csi_logs(v1: Any, node_name: Optional[str], tail_lines: int) -> Dict[str, Dict[str, Any]]:
    logs: Dict[str, Dict[str, Any]] = {}
    try:
        pods = v1.list_namespaced_pod("kube-system").items
    except Exception as exc:
        return {"kube-system": {"success": False, "error": str(exc)}}

    candidates = []
    for pod in pods:
        name = getattr(getattr(pod, "metadata", None), "name", "") or ""
        labels = _dict_or_empty(getattr(getattr(pod, "metadata", None), "labels", None))
        label_text = " ".join(str(v) for v in labels.values()).lower()
        scheduled_node = getattr(getattr(pod, "spec", None), "node_name", None)
        is_csi = "everest-csi" in name.lower() or ("everest" in label_text and "csi" in label_text)
        if not is_csi:
            continue
        is_controller = "controller" in name.lower() or "provisioner" in name.lower()
        if node_name and scheduled_node != node_name and not is_controller:
            continue
        candidates.append(pod)

    for pod in candidates[:8]:
        name = getattr(getattr(pod, "metadata", None), "name", None)
        containers = getattr(getattr(pod, "spec", None), "containers", None) or []
        for container in containers[:4]:
            container_name = getattr(container, "name", None)
            key = f"kube-system/{name}:{container_name}"
            try:
                raw = v1.read_namespaced_pod_log(
                    name=name,
                    namespace="kube-system",
                    container=container_name,
                    follow=False,
                    tail_lines=tail_lines,
                )
                logs[key] = {"success": True, "excerpt": _log_excerpt(raw, max_lines=tail_lines)}
            except Exception as exc:
                logs[key] = {"success": False, "error": str(exc)}
    return logs


def _collect_config_refs(v1: Any, pods: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    refs: Dict[Tuple[str, str, str], bool] = {}
    for pod in pods:
        for mount in pod.get("volume_mounts") or []:
            if not mount.get("sub_path"):
                continue
            source = mount.get("source") or {}
            if source.get("config_map"):
                refs[(pod["namespace"], "ConfigMap", source["config_map"])] = True
            if source.get("secret"):
                refs[(pod["namespace"], "Secret", source["secret"])] = True

    result: Dict[str, Dict[str, Any]] = {}
    for namespace, kind, name in refs:
        key = f"{namespace}/{kind}/{name}"
        try:
            if kind == "ConfigMap":
                result[key] = _metadata_ref_to_dict(v1.read_namespaced_config_map(name, namespace), kind)
            else:
                result[key] = _metadata_ref_to_dict(v1.read_namespaced_secret(name, namespace), kind)
        except Exception as exc:
            result[key] = {"kind": kind, "name": name, "namespace": namespace, "error": str(exc)}
    return result


def _storage_type(pvc: Dict[str, Any], pv: Optional[Dict[str, Any]], sc: Optional[Dict[str, Any]]) -> str:
    parts = [
        pvc.get("storage_class"),
        (sc or {}).get("name"),
        (sc or {}).get("provisioner"),
        json.dumps((sc or {}).get("parameters") or {}, ensure_ascii=False),
        json.dumps((pv or {}).get("source") or {}, ensure_ascii=False),
    ]
    text = " ".join(str(part or "") for part in parts).lower()
    if "obs" in text:
        return "OBS"
    if "sfsturbo" in text or "sfs-turbo" in text or "sfs_turbo" in text or "turbo" in text:
        return "SFS Turbo"
    if "nfs" in text or "nas" in text or "sfs" in text:
        return "SFS"
    if "local" in text or "host_path" in text:
        return "Local"
    if "evs" in text or "cinder" in text or "csi-disk" in text or "disk.csi" in text or "disk" in text:
        return "EVS"
    return "Unknown"


def _pod_uses_pvc(pod: Dict[str, Any], pvc: Dict[str, Any]) -> bool:
    if pod.get("namespace") != pvc.get("namespace"):
        return False
    return any(volume.get("pvc") == pvc.get("name") for volume in pod.get("volumes") or [])


def _events_for_target(events: Iterable[Dict[str, Any]], target: Dict[str, Any]) -> List[Dict[str, Any]]:
    pvc = target.get("pvc") or {}
    pv = target.get("pv") or {}
    pod_names = {pod.get("name") for pod in target.get("pods") or []}
    names = {pvc.get("name"), pv.get("name"), pvc.get("volume"), *pod_names}
    namespace = pvc.get("namespace")
    selected = []
    for event in events or []:
        involved = event.get("involved_object") or {}
        involved_name = involved.get("name")
        involved_ns = involved.get("namespace")
        if involved_name in names and (not involved_ns or not namespace or involved_ns in {namespace, "kube-system"}):
            selected.append(event)
            continue
        text = _event_text(event)
        if any(name and str(name).lower() in text for name in names):
            selected.append(event)
    return sorted(selected, key=_event_sort_key, reverse=True)


def _build_targets(snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
    inputs = snapshot.get("inputs") or {}
    pvs_by_name = {pv.get("name"): pv for pv in snapshot.get("pvs") or []}
    sc_by_name = {sc.get("name"): sc for sc in snapshot.get("storage_classes") or []}
    requested_pvc = inputs.get("pvc_name")
    namespace = inputs.get("namespace")
    pod_name = inputs.get("pod_name")
    candidate_pvcs = []
    for pvc in snapshot.get("pvcs") or []:
        if requested_pvc and pvc.get("name") != requested_pvc:
            continue
        if namespace and pvc.get("namespace") != namespace:
            continue
        if not requested_pvc and pod_name:
            related = [pod for pod in snapshot.get("pods") or [] if pod.get("name") == pod_name and _pod_uses_pvc(pod, pvc)]
            if not related:
                continue
        candidate_pvcs.append(pvc)

    if not candidate_pvcs:
        candidate_pvcs = [
            pvc for pvc in snapshot.get("pvcs") or []
            if (not namespace or pvc.get("namespace") == namespace)
            and (
                pvc.get("status") != "Bound"
                or pvc.get("deletion_timestamp")
                or (inputs.get("failure_symptom") and any(_pod_uses_pvc(pod, pvc) for pod in snapshot.get("pods") or []))
            )
        ][:10]

    targets = []
    for pvc in candidate_pvcs:
        pv = pvs_by_name.get(pvc.get("volume"))
        sc = sc_by_name.get(pvc.get("storage_class"))
        pods = [pod for pod in snapshot.get("pods") or [] if _pod_uses_pvc(pod, pvc)]
        attachments = [
            attachment for attachment in snapshot.get("volume_attachments") or []
            if pv and attachment.get("volume_name") == pv.get("name")
        ]
        target = {
            "pvc": pvc,
            "pv": pv,
            "storage_class": sc,
            "pods": pods,
            "volume_attachments": attachments,
        }
        target["storage_type"] = _storage_type(pvc, pv, sc)
        target["events"] = _events_for_target(snapshot.get("events") or [], target)
        targets.append(target)
    return targets


def _collect_k8s_snapshot(
    region: str,
    cluster_id: str,
    namespace: Optional[str],
    pvc_name: Optional[str],
    pod_name: Optional[str],
    failure_symptom: Optional[str],
    include_logs: bool,
    include_stats: bool,
    tail_lines: int,
    event_limit: int,
    access_key: str,
    secret_key: str,
    project_id: Optional[str],
) -> Dict[str, Any]:
    _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, project_id, "storage_failure")
    try:
        v1 = k8s_client.CoreV1Api()
        storage_v1 = k8s_client.StorageV1Api()
        networking_v1 = k8s_client.NetworkingV1Api()

        pvcs_raw = v1.list_namespaced_persistent_volume_claim(namespace).items if namespace else v1.list_persistent_volume_claim_for_all_namespaces().items
        pvs_raw = v1.list_persistent_volume().items
        pods_raw = v1.list_namespaced_pod(namespace).items if namespace else v1.list_pod_for_all_namespaces().items
        nodes_raw = v1.list_node().items
        scs_raw = storage_v1.list_storage_class().items
        try:
            vas_raw = storage_v1.list_volume_attachment().items
        except Exception:
            vas_raw = []
        try:
            events_raw = v1.list_namespaced_event(namespace, limit=event_limit).items if namespace else v1.list_event_for_all_namespaces(limit=event_limit).items
        except Exception:
            events_raw = []
        try:
            netpol_raw = networking_v1.list_namespaced_network_policy(namespace).items if namespace else networking_v1.list_network_policy_for_all_namespaces().items
        except Exception:
            netpol_raw = []

        pods = [_pod_to_dict(item) for item in pods_raw]
        nodes = [_node_to_dict(item) for item in nodes_raw]
        snapshot: Dict[str, Any] = {
            "inputs": {
                "region": region,
                "cluster_id": cluster_id,
                "namespace": namespace,
                "pvc_name": pvc_name,
                "pod_name": pod_name,
                "failure_symptom": failure_symptom,
            },
            "collected_at": _now_iso(),
            "pvcs": [_pvc_to_dict(item) for item in pvcs_raw],
            "pvs": [_pv_to_dict(item) for item in pvs_raw],
            "storage_classes": [_storage_class_to_dict(item) for item in scs_raw],
            "pods": pods,
            "nodes": nodes,
            "events": sorted([_event_to_dict(item) for item in events_raw], key=_event_sort_key, reverse=True),
            "volume_attachments": [_volume_attachment_to_dict(item) for item in vas_raw],
            "network_policies": [_network_policy_to_dict(item) for item in netpol_raw],
            "config_refs": _collect_config_refs(v1, pods),
            "node_stats": {},
            "pvc_volume_stats": [],
            "csi_logs": {},
        }
        snapshot["targets"] = _build_targets(snapshot)

        target_nodes = {
            pod.get("node")
            for target in snapshot["targets"]
            for pod in target.get("pods") or []
            if pod.get("node")
        }
        if include_stats:
            for node_name in list(target_nodes)[:5]:
                snapshot["node_stats"][node_name] = _read_node_stats(v1, node_name)
            snapshot["pvc_volume_stats"] = _extract_pvc_volume_stats(snapshot["node_stats"])
        if include_logs:
            node_for_logs = next(iter(target_nodes), None)
            snapshot["csi_logs"] = _read_csi_logs(v1, node_for_logs, tail_lines)
        return snapshot
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def _collect_cloud_storage(
    region: str,
    targets: List[Dict[str, Any]],
    access_key: str,
    secret_key: str,
    project_id: Optional[str],
) -> Dict[str, Any]:
    types = {target.get("storage_type") for target in targets}
    result: Dict[str, Any] = {}
    if "EVS" in types:
        result["evs"] = _safe_call("list_evs", storage.list_evs_volumes, region, ak=access_key, sk=secret_key, project_id=project_id, limit=200)
    if "SFS" in types:
        result["sfs"] = _safe_call("list_sfs", storage.list_sfs, region, ak=access_key, sk=secret_key, project_id=project_id, limit=200)
    if "SFS Turbo" in types:
        result["sfs_turbo"] = _safe_call("list_sfs_turbo", storage.list_sfs_turbo, region, ak=access_key, sk=secret_key, project_id=project_id, limit=200)
    if any(target.get("storage_type") in {"SFS", "SFS Turbo"} for target in targets):
        result["security_groups"] = _safe_call("list_security_groups", network.list_security_groups, region, ak=access_key, sk=secret_key, project_id=project_id)
        result["vpc_acls"] = _safe_call("list_vpc_acls", network.list_vpc_acls, region, ak=access_key, sk=secret_key, project_id=project_id)
    return result


def _add_finding(
    findings: List[Dict[str, Any]],
    stage: str,
    finding_type: str,
    title: str,
    confidence: float,
    severity: str,
    evidence: List[Dict[str, Any]],
    recommendation: List[str],
) -> None:
    findings.append({
        "stage": stage,
        "type": finding_type,
        "title": title,
        "confidence": confidence,
        "severity": severity,
        "evidence": evidence[:12],
        "recommendation": recommendation,
    })


def _events_text(events: Iterable[Dict[str, Any]]) -> str:
    return "\n".join(f"{event.get('reason')}: {event.get('message')}" for event in events or []).lower()


def _csi_log_text(snapshot: Dict[str, Any]) -> str:
    parts = []
    for key, log in (snapshot.get("csi_logs") or {}).items():
        if log.get("success"):
            parts.append(f"{key}\n{log.get('excerpt')}")
    return "\n".join(parts).lower()


def _pod_is_unschedulable(pod: Dict[str, Any], events: List[Dict[str, Any]]) -> bool:
    if pod.get("phase") != "Pending":
        return False
    text = _events_text(events)
    return "failedscheduling" in text or "unschedulable" in text or "0/" in text


def _pod_in_mount_stage(pod: Dict[str, Any], events: List[Dict[str, Any]]) -> bool:
    text = _events_text(events)
    waiting = [
        container.get("waiting_reason")
        for container in [*(pod.get("init_containers") or []), *(pod.get("containers") or [])]
        if container.get("waiting_reason")
    ]
    return (
        "containercreating" in {str(item).lower() for item in waiting}
        or "failedattachvolume" in text
        or "failedmount" in text
    )


def _node_by_name(snapshot: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {node.get("name"): node for node in snapshot.get("nodes") or []}


def _node_names_from_affinity(pv: Dict[str, Any]) -> List[str]:
    names = []
    for term in (pv.get("node_affinity") or {}).get("required") or []:
        for expr in term.get("match_fields") or []:
            if expr.get("key") == "metadata.name" and expr.get("operator") == "In":
                names.extend(expr.get("values") or [])
        for expr in term.get("match_expressions") or []:
            if expr.get("key") in {"kubernetes.io/hostname", "hostname"} and expr.get("operator") == "In":
                names.extend(expr.get("values") or [])
    return list(dict.fromkeys(names))


def _stats_for_pvc(snapshot: Dict[str, Any], pvc: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        stat for stat in snapshot.get("pvc_volume_stats") or []
        if (stat.get("pvc") or {}).get("name") == pvc.get("name")
        and (stat.get("pvc") or {}).get("namespace") == pvc.get("namespace")
    ]


def _check_provisioning(snapshot: Dict[str, Any], target: Dict[str, Any], findings: List[Dict[str, Any]]) -> None:
    pvc = target["pvc"]
    sc = target.get("storage_class") or {}
    storage_type = target.get("storage_type")
    events = target.get("events") or []
    text = _events_text(events)
    if pvc.get("status") != "Pending":
        return

    if sc.get("volume_binding_mode") == "WaitForFirstConsumer" and not target.get("pods"):
        _add_finding(
            findings,
            "一、供应期故障",
            "NormalWaitForFirstConsumer",
            "PVC 使用 WaitForFirstConsumer 且尚无关联 Pod，动态卷创建等待 Pod 调度触发，属于正常行为",
            0.98,
            "info",
            [{"pvc": pvc, "storage_class": sc}],
            [
                "创建或确认引用该 PVC 的 Pod/StatefulSet 后，观察 PVC 是否进入 Bound。",
                "如果已有 Pod 但仍 Pending，再进入调度与供应失败分支继续排查。",
            ],
        )
    if storage_type == "EVS" and "failedprovisioning" in text and "quotaexceeded" in text:
        _add_finding(
            findings,
            "一、供应期故障",
            "EVSQuotaExceeded",
            "PVC 动态创建 EVS 云硬盘失败，事件明确指向华为云账户 EVS 云硬盘配额不足",
            0.98,
            "critical",
            events[:8],
            ["在对应 region/project 检查 EVS 磁盘数量或容量配额，释放无用云硬盘或提交配额提升后重试。"],
        )
    if storage_type in {"SFS", "SFS Turbo"} and (
        "subnet ip insufficiency" in text
        or ("failedprovisioning" in text and (" 400" in text or " 403" in text) and ("subnet" in text or "mount" in text or "ip" in text))
    ):
        _add_finding(
            findings,
            "一、供应期故障",
            "SFSSubnetIPInsufficient",
            "SFS/SFS Turbo 创建挂载点失败，事件指向 VPC 子网可用 IP 不足或挂载点分配被控制面拒绝",
            0.92,
            "critical",
            events[:8],
            ["检查 StorageClass 指向的 VPC/subnet 剩余 IP，扩容子网或更换有可用 IP 的子网后重新创建 PVC。"],
        )
    if storage_type == "OBS" and ("bucketalreadyexists" in text or "invalidbucketname" in text):
        _add_finding(
            findings,
            "一、供应期故障",
            "OBSBucketNameInvalid",
            "OBS 动态创建失败，桶名已存在或不符合 OBS 命名规范",
            0.98,
            "critical",
            events[:8],
            ["修正 StorageClass/参数中的 bucket 名称，避免跨账号/跨区域冲突，并按 OBS 命名规范重试。"],
        )


def _check_scheduling(snapshot: Dict[str, Any], target: Dict[str, Any], findings: List[Dict[str, Any]]) -> None:
    pvc = target["pvc"]
    pv = target.get("pv") or {}
    if pvc.get("status") != "Bound" or not target.get("pods"):
        return
    events = target.get("events") or []
    sched_pods = [pod for pod in target.get("pods") or [] if _pod_is_unschedulable(pod, events)]
    if not sched_pods:
        return

    nodes = snapshot.get("nodes") or []
    nodes_by_name = _node_by_name(snapshot)
    terms = (pv.get("node_affinity") or {}).get("required") or []
    matching_nodes = [node for node in nodes if _node_matches_terms(node, terms)] if terms else nodes
    ready_matching = [node for node in matching_nodes if _node_ready(node)]
    text = _events_text(events)

    if target.get("storage_type") == "Local":
        node_names = _node_names_from_affinity(pv)
        offline = [
            nodes_by_name.get(name) for name in node_names
            if nodes_by_name.get(name) and not _node_ready(nodes_by_name[name])
        ]
        if offline:
            _add_finding(
                findings,
                "二、调度与绑定期故障",
                "LocalPVNodeOffline",
                "Local 本地持久卷绑定的宿主机 NotReady/离线，Pod 无法调度到该节点",
                1.0,
                "critical",
                [{"pv": pv, "offline_nodes": offline, "pods": sched_pods}, *events[:6]],
                ["优先恢复或替换本地卷所属节点；Local PV 数据通常随节点绑定，迁移前需确认数据恢复路径。"],
            )
        return

    if target.get("storage_type") == "EVS":
        blockers = []
        for pod in sched_pods:
            for node in ready_matching:
                taints = _blocking_taints(node, pod)
                if taints:
                    blockers.append({"node": node.get("name"), "taints": taints})
        if "volume node affinity conflict" in text or not ready_matching or blockers or "insufficient cpu" in text or "insufficient memory" in text:
            _add_finding(
                findings,
                "二、调度与绑定期故障",
                "EVSAvailabilityZoneSchedulingConflict",
                "由于 EVS 强单可用区属性，Pod 无法调度到存储所在可用区内可用节点",
                0.94 if ("volume node affinity conflict" in text or not ready_matching) else 0.86,
                "critical",
                [{
                    "pv_node_affinity": pv.get("node_affinity"),
                    "ready_matching_nodes": ready_matching,
                    "blocking_taints": blockers[:8],
                    "pods": sched_pods,
                }, *events[:8]],
                [
                    "在 PV nodeAffinity 指定的 AZ 内恢复或扩容 Ready 节点，并确认节点无 Pod 无法容忍的 NoSchedule/NoExecute 污点。",
                    "若 Pod 侧 nodeSelector/affinity 固定到其他 AZ，需要调整工作负载调度约束或重新规划数据迁移。",
                ],
            )


def _check_attach_mount(snapshot: Dict[str, Any], target: Dict[str, Any], findings: List[Dict[str, Any]]) -> None:
    pvc = target["pvc"]
    pv = target.get("pv") or {}
    events = target.get("events") or []
    text = _events_text(events)
    csi_text = _csi_log_text(snapshot)
    mount_pods = [pod for pod in target.get("pods") or [] if _pod_in_mount_stage(pod, events)]
    if not mount_pods and "failedmount" not in text and "failedattachvolume" not in text:
        return

    storage_type = target.get("storage_type")
    if storage_type == "EVS":
        for pod in mount_pods or target.get("pods") or [{}]:
            node_name = pod.get("node")
            attachments = [
                item for item in target.get("volume_attachments") or []
                if item.get("volume_name") == pv.get("name") and (not node_name or item.get("node_name") == node_name)
            ]
            if not attachments:
                _add_finding(
                    findings,
                    "三、挂载期故障",
                    "VolumeAttachmentNotCreated",
                    "未找到匹配 PV 与目标节点的 VolumeAttachment，Kubernetes 控制面尚未下发 EVS 挂载指令",
                    0.78,
                    "warning",
                    [{"pv": pv.get("name"), "node": node_name, "pod": pod}, *events[:6]],
                    ["检查 attach-detach-controller/CSI controller 是否正常，以及 Pod 是否已经完成调度到目标节点。"],
                )
                continue
            for attachment in attachments:
                attach_error = ((attachment.get("attach_error") or {}).get("message") or "").lower()
                if attachment.get("attached") is False:
                    if any(key in attach_error for key in ("max", "limit", "exceed", "too many")):
                        _add_finding(
                            findings,
                            "三、挂载期故障",
                            "EVSNodeAttachLimitExceeded",
                            "VolumeAttachment Attached=False，错误信息指向 ECS 单节点挂载云硬盘数量达到上限",
                            0.94,
                            "critical",
                            [{"volume_attachment": attachment}, *events[:6]],
                            ["减少该节点挂载盘数量，迁移部分 Pod 到其他节点，或更换满足挂盘需求的节点规格后重试。"],
                        )
                    elif any(key in attach_error for key in ("status", "in-use", "attached", "lock", "another")):
                        _add_finding(
                            findings,
                            "三、挂载期故障",
                            "EVSResidualAttachmentLock",
                            "VolumeAttachment Attached=False，错误信息指向 EVS 状态不正确或被残留节点占用",
                            0.86,
                            "critical",
                            [{"volume_attachment": attachment}, *events[:6]],
                            ["核对 EVS 云盘在云侧的 attachment 状态，确认是否存在旧节点残留挂载；解除残留前需确认文件系统一致性。"],
                        )
                    else:
                        _add_finding(
                            findings,
                            "三、挂载期故障",
                            "EVSAttachFailed",
                            "VolumeAttachment Attached=False，EVS 挂载未完成",
                            0.8,
                            "critical",
                            [{"volume_attachment": attachment}, *events[:6]],
                            ["结合 attach_error、everest-csi-controller 日志和 EVS 云盘状态继续定位控制面或云盘状态异常。"],
                        )
                elif attachment.get("attached") is True and "failedmount" in text:
                    _add_finding(
                        findings,
                        "三、挂载期故障",
                        "HostKernelMountFailed",
                        "EVS 已完成云侧 Attach，但 kubelet FailedMount，问题转入宿主机内核/文件系统挂载阶段",
                        0.84,
                        "critical",
                        [{"volume_attachment": attachment}, *events[:8]],
                        ["检查节点 dmesg/kubelet 日志、文件系统类型、fsck 结果和只读保护；必要时迁移工作负载到健康节点。"],
                    )

    if storage_type in {"SFS", "SFS Turbo"} and "failedmount" in text and ("mount.nfs" in text or "nfs" in text) and "timed out" in text:
        endpoint = (pv.get("source") or {}).get("server") or (pv.get("source") or {}).get("volume_attributes", {}).get("server")
        _add_finding(
            findings,
            "三、挂载期故障",
            "SFSNfsNetworkBlocked",
            "SFS/SFS Turbo NFS 挂载超时，高度疑似网络数据面阻断或安全组未放通 2049",
            0.82,
            "critical",
            [{
                "endpoint": endpoint,
                "network_policies": snapshot.get("network_policies") or [],
                "events": events[:8],
            }],
            [
                "检查节点安全组、SFS/SFS Turbo 安全组和 VPC ACL 是否放通 TCP/UDP 2049。",
                "确认节点到 SFS endpoint 的 VPC 路由正确；Kubernetes NetworkPolicy 通常不拦截 kubelet 主机网络挂载，只作为旁证。",
            ],
        )

    obs_credential_patterns = (
        "403",
        "forbidden",
        "signaturedoesnotmatch",
        "ak size is invalid",
        "sk size is invalid",
        "access key id is invalid",
        "secret access key is invalid",
        "failed to save temporary ak sk file",
        "fuse_opt_parse fail",
    )
    obs_text = f"{text}\n{csi_text}"
    matched_obs_errors = [key for key in obs_credential_patterns if key in obs_text]
    if storage_type == "OBS" and matched_obs_errors:
        annotations = pvc.get("annotations") or {}
        secret_ref = {
            "name": annotations.get("csi.storage.k8s.io/node-publish-secret-name"),
            "namespace": annotations.get("csi.storage.k8s.io/node-publish-secret-namespace"),
        }
        _add_finding(
            findings,
            "三、挂载期故障",
            "OBSCredentialInvalid",
            "OBS 挂载失败，CSI 日志或事件指向 IAM 委托、AK/SK Secret 或桶权限凭据异常",
            0.94,
            "critical",
            [{
                "matched_errors": matched_obs_errors,
                "secret_ref": secret_ref,
                "events": events[:8],
                "csi_logs": snapshot.get("csi_logs") or {},
            }],
            ["核对 CCE 集群 OBS 存储相关 IAM 委托、PVC 注解引用的 Secret、AK/SK 格式和值以及桶权限，修复后重建挂载 Pod 验证。"],
        )

    if "permission denied" in text or ("forbidden" in text and storage_type != "OBS"):
        _add_finding(
            findings,
            "三、挂载期故障",
            "StoragePermissionDenied",
            "存储挂载事件出现权限拒绝，可能是文件系统导出策略、IAM 权限或挂载参数不匹配",
            0.82,
            "critical",
            events[:8],
            ["核对存储侧访问控制、IAM 委托、PV/StorageClass 挂载参数和应用容器运行用户权限。"],
        )


def _check_runtime_teardown(snapshot: Dict[str, Any], target: Dict[str, Any], findings: List[Dict[str, Any]]) -> None:
    pvc = target["pvc"]
    events = target.get("events") or []
    text = _events_text(events)
    symptom = str((snapshot.get("inputs") or {}).get("failure_symptom") or "").lower()
    node_map = _node_by_name(snapshot)

    for stat in _stats_for_pvc(snapshot, pvc):
        if stat.get("usage_ratio") is not None and stat["usage_ratio"] >= CAPACITY_THRESHOLD:
            _add_finding(
                findings,
                "四、运行期与注销期异常",
                "PVCCapacityExhausted",
                "Kubelet stats 显示 PVC 容量使用率超过 95%，应用 IO 异常高度疑似容量耗尽",
                1.0,
                "critical",
                [stat],
                ["扩容 PVC/底层存储或清理数据后，确认 usedBytes/capacityBytes 低于阈值并观察应用写入恢复。"],
            )
        if stat.get("inode_ratio") is not None and stat["inode_ratio"] >= INODE_THRESHOLD:
            _add_finding(
                findings,
                "四、运行期与注销期异常",
                "PVCInodeExhausted",
                "Kubelet stats 显示 PVC inode 使用率超过 95%，小文件过多导致新文件创建失败",
                1.0,
                "critical",
                [stat],
                ["清理小文件、合并碎片文件或迁移到 inode 规模更合适的存储类型，并复查 inodesUsed/inodes。"],
            )

    if "read-only file system" in f"{symptom}\n{text}":
        node_evidence = []
        for pod in target.get("pods") or []:
            node = node_map.get(pod.get("node"))
            if not node:
                continue
            conditions = node.get("conditions") or []
            if any(item.get("type") == "DiskPressure" and item.get("status") == "True" for item in conditions):
                node_evidence.append(node)
        kernel_events = [event for event in events if "kerneloops" in _event_text(event) or "diskpressure" in _event_text(event)]
        _add_finding(
            findings,
            "四、运行期与注销期异常",
            "ReadOnlyFilesystemProtection",
            "应用报 Read-only file system，结合节点事件/压力推断宿主机触发 Linux 文件系统只读保护",
            0.78 if (node_evidence or kernel_events) else 0.62,
            "warning",
            [{"nodes": node_evidence, "events": kernel_events[:6], "symptom": symptom}],
            ["优先迁移工作负载到健康节点，并在节点侧检查内核日志、块设备错误和文件系统一致性。"],
        )

    subpath_mounts = []
    for pod in target.get("pods") or []:
        for mount in pod.get("volume_mounts") or []:
            source = mount.get("source") or {}
            if mount.get("sub_path") and (source.get("config_map") or source.get("secret")):
                subpath_mounts.append({"pod": pod, "mount": mount})
    if subpath_mounts and ("subpath" in f"{text}\n{symptom}" or "not a directory" in text or "stale file handle" in text):
        _add_finding(
            findings,
            "四、运行期与注销期异常",
            "ConfigMapSecretSubPathDeadlock",
            "Pod 使用 ConfigMap/Secret subPath，随后出现挂载失败，符合 subPath 挂载点保护/死锁类问题特征",
            0.86,
            "critical",
            [{"subpath_mounts": subpath_mounts[:5], "config_refs": snapshot.get("config_refs") or {}, "events": events[:8]}],
            ["避免对 ConfigMap/Secret 使用 subPath 热更新；重建 Pod 释放旧挂载点，并改用目录挂载或滚动重启策略。"],
        )

    if pvc.get("deletion_timestamp") and "kubernetes.io/pvc-protection" in (pvc.get("finalizers") or []):
        residual_pods = [pod for pod in snapshot.get("pods") or [] if _pod_uses_pvc(pod, pvc)]
        if residual_pods:
            _add_finding(
                findings,
                "四、运行期与注销期异常",
                "PVCProtectionBlocked",
                "PVC 处于 Terminating 且 pvc-protection finalizer 生效，仍有 Pod 引用该 PVC",
                1.0,
                "critical",
                [{"pvc": pvc, "residual_pods": residual_pods}],
                ["先确认并删除/强制删除残留 Pod，再观察 PVC finalizer 是否自动移除；不要直接手工删除 finalizer，除非已确认无引用和数据风险。"],
            )

    if "i/o error" in f"{symptom}\n{text}" or "input/output error" in f"{symptom}\n{text}":
        _add_finding(
            findings,
            "四、运行期与注销期异常",
            "StorageIOError",
            "应用或事件出现 I/O error，说明运行期存储链路或底层介质存在异常，需要结合云盘/节点日志进一步确认",
            0.72,
            "warning",
            [{"events": events[:8], "symptom": symptom}],
            ["采集节点 dmesg/kubelet 日志和 EVS/SFS/OBS 监控；若错误持续增长，先迁移业务并保护数据一致性。"],
        )


def assess_storage_snapshot(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    """Assess a collected storage snapshot and return findings plus conclusion data."""
    targets = snapshot.get("targets") or _build_targets(snapshot)
    snapshot["targets"] = targets
    findings: List[Dict[str, Any]] = []

    for target in targets:
        _check_provisioning(snapshot, target, findings)
        _check_scheduling(snapshot, target, findings)
        _check_attach_mount(snapshot, target, findings)
        _check_runtime_teardown(snapshot, target, findings)

    severity_order = {"critical": 3, "warning": 2, "info": 1}
    findings.sort(key=lambda item: (severity_order.get(item.get("severity"), 0), item.get("confidence", 0)), reverse=True)
    top_causes = findings[:3]
    if top_causes:
        conclusion = top_causes[0]["title"]
        confidence = "高 (High)" if top_causes[0]["confidence"] >= 0.9 else "中 (Medium)" if top_causes[0]["confidence"] >= 0.75 else "低 (Low)"
    else:
        conclusion = "未命中明确存储根因；当前报告只说明已检查项和证据缺口"
        confidence = "低 (Low)"

    return {
        "findings": findings,
        "top_causes": top_causes,
        "conclusion": conclusion,
        "confidence": confidence,
        "target_count": len(targets),
    }


def _stage_rows(assessment: Dict[str, Any]) -> str:
    stages = [
        "一、供应期故障",
        "二、调度与绑定期故障",
        "三、挂载期故障",
        "四、运行期与注销期异常",
    ]
    rows = ["| 阶段 | 状态 | 命中结论 |", "| :--- | :--- | :--- |"]
    findings = assessment.get("findings") or []
    for stage in stages:
        matched = [item for item in findings if item.get("stage") == stage]
        if matched:
            rows.append(f"| {stage} | {'正常/解释性' if matched[0].get('severity') == 'info' else '异常'} | {_md_cell(matched[0].get('title'), 260)} |")
        else:
            rows.append(f"| {stage} | 已检查 | 未发现强异常 |")
    return "\n".join(rows)


def _target_rows(snapshot: Dict[str, Any]) -> str:
    rows = ["| PVC | PV | StorageClass | 类型 | 关联 Pod | VolumeAttachment |", "| :--- | :--- | :--- | :--- | :--- | :--- |"]
    targets = snapshot.get("targets") or []
    if not targets:
        rows.append("| - | - | - | - | - | - |")
        return "\n".join(rows)
    for target in targets:
        pvc = target.get("pvc") or {}
        pv = target.get("pv") or {}
        sc = target.get("storage_class") or {}
        pods = ", ".join(f"`{pod.get('namespace')}/{pod.get('name')}`({pod.get('phase')})" for pod in (target.get("pods") or [])[:6]) or "-"
        attachments = ", ".join(
            f"`{item.get('name')}` attached={item.get('attached')} node={item.get('node_name')}"
            for item in (target.get("volume_attachments") or [])[:6]
        ) or "-"
        rows.append(
            f"| `{_md_cell(pvc.get('namespace'))}/{_md_cell(pvc.get('name'))}` {pvc.get('status') or '-'} | "
            f"`{_md_cell(pv.get('name'))}` {pv.get('status') or '-'} | "
            f"`{_md_cell(sc.get('name') or pvc.get('storage_class'))}` mode=`{_md_cell(sc.get('volume_binding_mode'))}` | "
            f"{_md_cell(target.get('storage_type'))} | {pods} | {attachments} |"
        )
    return "\n".join(rows)


def _evidence_rows(findings: List[Dict[str, Any]]) -> str:
    rows = ["| 阶段 | 严重度 | 类型 | 置信度 | 证据摘要 |", "| :--- | :--- | :--- | :--- | :--- |"]
    if not findings:
        rows.append("| - | - | - | - | 未命中明确异常证据 |")
        return "\n".join(rows)
    for item in findings:
        evidence = item.get("evidence") or []
        rows.append(
            "| {stage} | {severity} | `{typ}` | {confidence:.0%} | {evidence} |".format(
                stage=_md_cell(item.get("stage")),
                severity=_md_cell(item.get("severity")),
                typ=_md_cell(item.get("type")),
                confidence=float(item.get("confidence") or 0),
                evidence=_md_cell(evidence[0] if evidence else {}, 300),
            )
        )
    return "\n".join(rows)


def _gap_rows(snapshot: Dict[str, Any]) -> str:
    rows = ["| 数据面 | 状态 | 说明 |", "| :--- | :--- | :--- |"]
    rows.append(f"| StorageClass/PV/PVC/Pod/Event | 已采集 | PVC={len(snapshot.get('pvcs') or [])}, PV={len(snapshot.get('pvs') or [])}, Events={len(snapshot.get('events') or [])} |")
    rows.append(f"| VolumeAttachment | {'已采集' if snapshot.get('volume_attachments') is not None else '缺失'} | count={len(snapshot.get('volume_attachments') or [])} |")
    stats_count = len(snapshot.get("pvc_volume_stats") or [])
    rows.append(f"| Kubelet `/stats/summary` | {'已采集' if stats_count else '未采集或无 PVC 统计'} | PVC volume stats={stats_count} |")
    log_count = len(snapshot.get("csi_logs") or {})
    rows.append(f"| Everest CSI 日志 | {'已采集' if log_count else '未采集或未匹配 CSI Pod'} | logs={log_count} |")
    cloud = snapshot.get("cloud_storage") or {}
    rows.append(f"| 华为云存储/网络只读清单 | {'已采集' if cloud else '未启用或无匹配类型'} | keys={list(cloud.keys())} |")
    return "\n".join(rows)


def build_markdown_report(snapshot: Dict[str, Any], assessment: Dict[str, Any]) -> str:
    inputs = snapshot.get("inputs") or {}
    top_causes = assessment.get("top_causes") or []
    findings = assessment.get("findings") or []
    recs = []
    for cause in top_causes:
        for rec in cause.get("recommendation") or []:
            if rec not in recs:
                recs.append(rec)
    if not recs:
        recs = [
            "补充更精确的 PVC/Pod 名称、故障时间窗口和应用报错文本后重新采集。",
            "若是运行期 IO 异常，建议同时采集应用日志、节点 dmesg/kubelet 日志和云侧存储监控。",
        ]

    conclusion_lines = []
    if top_causes:
        for idx, cause in enumerate(top_causes, start=1):
            conclusion_lines.append(f"{idx}. **{cause['title']}** (`{cause['type']}`，置信度 {cause['confidence']:.0%})")
    else:
        conclusion_lines.append("1. 未命中明确根因；当前证据不足以把问题收敛到单一存储故障类型。")

    return "\n".join([
        "# CCE 存储故障自动化诊断报告",
        "",
        "## 1. 诊断总览",
        "| 评估项 | 详细信息 |",
        "| :--- | :--- |",
        f"| 目标集群 | region=`{_md_cell(inputs.get('region'))}` cluster_id=`{_md_cell(inputs.get('cluster_id'))}` |",
        f"| 目标对象 | namespace=`{_md_cell(inputs.get('namespace'))}` pvc=`{_md_cell(inputs.get('pvc_name'))}` pod=`{_md_cell(inputs.get('pod_name'))}` |",
        f"| 故障现象 | {_md_cell(inputs.get('failure_symptom'), 260)} |",
        f"| 诊断结论 | **{_md_cell(assessment.get('conclusion'), 300)}** |",
        f"| 置信度 | **{_md_cell(assessment.get('confidence'))}** |",
        f"| 数据采集时间 | `{_md_cell(snapshot.get('collected_at'))}` |",
        f"| 目标 PVC 数 | {assessment.get('target_count', 0)} |",
        "",
        "## 2. 排查过程",
        _stage_rows(assessment),
        "",
        "## 3. 关键对象关系",
        _target_rows(snapshot),
        "",
        "## 4. 证据矩阵",
        _evidence_rows(findings),
        "",
        "## 5. 诊断结论",
        *conclusion_lines,
        "",
        "## 6. 建议动作与验证标准",
        *[f"{idx}. {rec}" for idx, rec in enumerate(recs, start=1)],
        "恢复验证标准：PVC/PV 状态符合预期；Pod 不再出现 FailedScheduling/FailedAttachVolume/FailedMount；VolumeAttachment attached=True；应用写入成功且容量/inode 使用率回落到安全阈值。",
        "",
        "## 7. 数据缺口与人工确认",
        _gap_rows(snapshot),
        "",
    ])


def diagnose_storage_failure(
    region: str,
    cluster_id: str,
    namespace: Optional[str] = None,
    pvc_name: Optional[str] = None,
    pod_name: Optional[str] = None,
    failure_symptom: Optional[str] = None,
    include_logs: bool = True,
    include_stats: bool = True,
    include_cloud: bool = False,
    tail_lines: int = 160,
    event_limit: int = 500,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Diagnose PVC/PV provisioning, scheduling, attach/mount, runtime and teardown failures."""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided. Set HUAWEI_AK/HUAWEI_SK or pass ak/sk."}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}
    if not K8S_AVAILABLE:
        return {"success": False, "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"}
    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    try:
        snapshot = _collect_k8s_snapshot(
            region,
            cluster_id,
            namespace,
            pvc_name,
            pod_name,
            failure_symptom,
            include_logs,
            include_stats,
            tail_lines,
            event_limit,
            access_key,
            secret_key,
            proj_id,
        )
        if include_cloud:
            snapshot["cloud_storage"] = _collect_cloud_storage(region, snapshot.get("targets") or [], access_key, secret_key, proj_id)
        assessment = assess_storage_snapshot(snapshot)
        report = build_markdown_report(snapshot, assessment)
        return {
            "success": True,
            "action": "huawei_storage_failure_diagnose",
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace or "all",
            "conclusion": assessment["conclusion"],
            "confidence": assessment["confidence"],
            "findings": assessment["findings"],
            "top_causes": assessment["top_causes"],
            "snapshot": snapshot,
            "report_markdown": report,
        }
    except Exception as exc:
        return {"success": False, "stage": "huawei_storage_failure_diagnose", "error": str(exc), "error_type": type(exc).__name__}


def _credentials_or_error(region: str, cluster_id: str, ak: Optional[str], sk: Optional[str], project_id: Optional[str]) -> Tuple[Optional[Tuple[str, str, Optional[str]]], Optional[Dict[str, Any]]]:
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return None, {"success": False, "error": "Credentials not provided. Set HUAWEI_AK/HUAWEI_SK or pass ak/sk."}
    if not cluster_id:
        return None, {"success": False, "error": "cluster_id is required"}
    if not K8S_AVAILABLE:
        return None, {"success": False, "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"}
    if not SDK_AVAILABLE:
        return None, {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}
    return (access_key, secret_key, proj_id), None


def list_storage_classes(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    credentials, error = _credentials_or_error(region, cluster_id, ak, sk, project_id)
    if error:
        return error
    access_key, secret_key, proj_id = credentials
    _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "storageclasses")
    try:
        items = k8s_client.StorageV1Api().list_storage_class().items
        return {
            "success": True,
            "action": "huawei_get_cce_storageclasses",
            "region": region,
            "cluster_id": cluster_id,
            "count": len(items),
            "storage_classes": [_storage_class_to_dict(item) for item in items],
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def list_volume_attachments(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    credentials, error = _credentials_or_error(region, cluster_id, ak, sk, project_id)
    if error:
        return error
    access_key, secret_key, proj_id = credentials
    _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "volumeattachments")
    try:
        items = k8s_client.StorageV1Api().list_volume_attachment().items
        return {
            "success": True,
            "action": "huawei_get_cce_volumeattachments",
            "region": region,
            "cluster_id": cluster_id,
            "count": len(items),
            "volume_attachments": [_volume_attachment_to_dict(item) for item in items],
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def get_node_stats_summary(
    region: str,
    cluster_id: str,
    node_name: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    credentials, error = _credentials_or_error(region, cluster_id, ak, sk, project_id)
    if error:
        return error
    access_key, secret_key, proj_id = credentials
    _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "node_stats")
    try:
        v1 = k8s_client.CoreV1Api()
        node_names = [node_name] if node_name else [getattr(getattr(node, "metadata", None), "name", None) for node in v1.list_node().items]
        stats = {name: _read_node_stats(v1, name) for name in node_names if name}
        return {
            "success": True,
            "action": "huawei_get_cce_node_stats_summary",
            "region": region,
            "cluster_id": cluster_id,
            "node_name": node_name,
            "node_stats": stats,
            "pvc_volume_stats": _extract_pvc_volume_stats(stats),
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def get_everest_csi_logs(
    region: str,
    cluster_id: str,
    node_name: Optional[str] = None,
    tail_lines: int = 160,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    credentials, error = _credentials_or_error(region, cluster_id, ak, sk, project_id)
    if error:
        return error
    access_key, secret_key, proj_id = credentials
    _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "everest_csi_logs")
    try:
        logs = _read_csi_logs(k8s_client.CoreV1Api(), node_name, tail_lines)
        return {
            "success": True,
            "action": "huawei_get_cce_everest_csi_logs",
            "region": region,
            "cluster_id": cluster_id,
            "node_name": node_name,
            "logs": logs,
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def diagnose_storage_failure_action(params: Dict[str, str]) -> Dict[str, Any]:
    return diagnose_storage_failure(
        region=params["region"],
        cluster_id=params["cluster_id"],
        namespace=params.get("namespace"),
        pvc_name=params.get("pvc_name"),
        pod_name=params.get("pod_name"),
        failure_symptom=params.get("failure_symptom"),
        include_logs=_as_bool(params.get("include_logs"), True),
        include_stats=_as_bool(params.get("include_stats"), True),
        include_cloud=_as_bool(params.get("include_cloud"), False),
        tail_lines=_to_int(params.get("tail_lines"), 160),
        event_limit=_to_int(params.get("event_limit"), 500),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )


def list_storage_classes_action(params: Dict[str, str]) -> Dict[str, Any]:
    return list_storage_classes(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))


def list_volume_attachments_action(params: Dict[str, str]) -> Dict[str, Any]:
    return list_volume_attachments(params["region"], params["cluster_id"], params.get("ak"), params.get("sk"), params.get("project_id"))


def get_node_stats_summary_action(params: Dict[str, str]) -> Dict[str, Any]:
    return get_node_stats_summary(params["region"], params["cluster_id"], params.get("node_name"), params.get("ak"), params.get("sk"), params.get("project_id"))


def get_everest_csi_logs_action(params: Dict[str, str]) -> Dict[str, Any]:
    return get_everest_csi_logs(
        params["region"],
        params["cluster_id"],
        params.get("node_name"),
        _to_int(params.get("tail_lines"), 160),
        params.get("ak"),
        params.get("sk"),
        params.get("project_id"),
    )
