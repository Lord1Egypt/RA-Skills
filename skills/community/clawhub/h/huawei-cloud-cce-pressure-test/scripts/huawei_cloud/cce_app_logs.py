"""Application log discovery and query helpers."""

from __future__ import annotations

import base64
import json
import os
import re
import tempfile
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from . import lts
from .common import _register_cert_file, _safe_delete_file, create_cce_client, get_credentials_with_region, k8s_client


def _get_policy_name(params: Dict[str, str]) -> Optional[str]:
    return params.get("logconfig_name") or params.get("policy_name")


def _to_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    return str(value).lower() in {"1", "true", "yes", "y", "on"}


def _to_int(value: Optional[str], default: int) -> int:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _parse_text_list(value: Optional[str], default: List[str]) -> List[str]:
    if not value:
        return default
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return default
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(item) for item in parsed if str(item).strip()]
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in text.split(",") if item.strip()]


def _parse_json_value(value: Optional[str], default: Any) -> Any:
    if value is None or value == "":
        return default
    if isinstance(value, (dict, list)):
        return value
    return json.loads(str(value))


def _format_ts(timestamp_ms: Optional[int]) -> Optional[str]:
    if timestamp_ms is None:
        return None
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")


def _content_of(log: Dict[str, Any]) -> str:
    content = log.get("content")
    if isinstance(content, dict):
        return json.dumps(content, ensure_ascii=False)
    if content is None:
        return ""
    return str(content)


def _json_content_of(log: Dict[str, Any]) -> Dict[str, Any]:
    content = log.get("content")
    if isinstance(content, dict):
        return content
    if not content:
        return {}
    text = str(content).strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            for nested_key in ("log", "message", "content"):
                nested = parsed.get(nested_key)
                if isinstance(nested, str) and nested.strip().startswith("{"):
                    try:
                        nested_parsed = json.loads(nested)
                        if isinstance(nested_parsed, dict):
                            merged = dict(parsed)
                            merged.update(nested_parsed)
                            return merged
                    except json.JSONDecodeError:
                        pass
            return parsed
        return {}
    except json.JSONDecodeError:
        pass
    match = re.search(r"(\{.*\})", text)
    if match:
        try:
            parsed = json.loads(match.group(1))
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def _deep_get(data: Dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _extract_log_time_ms(log: Dict[str, Any]) -> Optional[int]:
    timestamp = log.get("timestamp")
    if timestamp not in (None, ""):
        try:
            value = int(timestamp)
            if value < 10_000_000_000:
                value *= 1000
            return value
        except (TypeError, ValueError):
            pass

    content = _content_of(log)
    nginx_match = re.search(r"\[(\d{1,2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\]", content)
    if nginx_match:
        try:
            parsed = datetime.strptime(nginx_match.group(1), "%d/%b/%Y:%H:%M:%S %z")
            return int(parsed.timestamp() * 1000)
        except ValueError:
            pass

    iso_match = re.search(r"\b(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})(?:[.,]\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b", content)
    if iso_match:
        try:
            parsed = datetime.strptime(iso_match.group(1).replace("T", " "), "%Y-%m-%d %H:%M:%S")
            return int(parsed.timestamp() * 1000)
        except ValueError:
            pass

    epoch_match = re.search(r"\b(1[6-9]\d{8}(?:\d{3})?)\b", content)
    if epoch_match:
        value = int(epoch_match.group(1))
        if value < 10_000_000_000:
            value *= 1000
        return value
    return None


def _extract_audit_time_ms(log: Dict[str, Any], audit: Dict[str, Any]) -> Optional[int]:
    for path in ("stageTimestamp", "requestReceivedTimestamp", "timestamp", "time"):
        value = _deep_get(audit, path)
        if not value:
            continue
        if isinstance(value, (int, float)):
            numeric = int(value)
            return numeric * 1000 if numeric < 10_000_000_000 else numeric
        text = str(value).replace("T", " ").replace("Z", "").split(".")[0]
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S%z"):
            try:
                return int(datetime.strptime(text, fmt).timestamp() * 1000)
            except ValueError:
                continue
    return _extract_log_time_ms(log)


def _extract_http_status(content: str) -> Optional[int]:
    match = re.search(r'"\S+\s+\S+\s+HTTP/[^"]+"\s+(\d{3})\b', content)
    if not match:
        match = re.search(r"\bstatus(?:=|:|\s)(\d{3})\b", content, flags=re.IGNORECASE)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def _classify_log(
    content: str,
    error_patterns: List[str],
    warning_patterns: List[str],
    http_error_status_threshold: int,
    include_http_4xx: bool,
) -> Tuple[bool, str, List[str], Optional[int]]:
    reasons = []
    lower_content = content.lower()
    severity = "normal"

    for pattern in error_patterns:
        try:
            if re.search(pattern, content, flags=re.IGNORECASE):
                reasons.append(pattern)
        except re.error:
            if pattern.lower() in lower_content:
                reasons.append(pattern)

    warning_reasons = []
    for pattern in warning_patterns:
        try:
            if re.search(pattern, content, flags=re.IGNORECASE):
                warning_reasons.append(pattern)
        except re.error:
            if pattern.lower() in lower_content:
                warning_reasons.append(pattern)

    status_code = _extract_http_status(content)
    if status_code is not None:
        if status_code >= http_error_status_threshold:
            reasons.append(f"http_{status_code}")
        elif include_http_4xx and status_code >= 400:
            warning_reasons.append(f"http_{status_code}")

    if reasons:
        if re.search(r"\b(fatal|panic|oom|out of memory|segmentation fault|traceback)\b", content, flags=re.IGNORECASE):
            severity = "critical"
        else:
            severity = "error"
        return True, severity, reasons, status_code
    if warning_reasons:
        return True, "warning", warning_reasons, status_code
    return False, severity, [], status_code


def _build_incident_windows(anomalies: List[Dict[str, Any]], gap_minutes: int) -> List[Dict[str, Any]]:
    if not anomalies:
        return []
    gap_ms = max(gap_minutes, 1) * 60 * 1000
    sorted_items = sorted(anomalies, key=lambda item: (item.get("timestamp_ms") is None, item.get("timestamp_ms") or 0, item["index"]))
    windows = []
    current = None
    for item in sorted_items:
        item_ts = item.get("timestamp_ms")
        if current is None:
            current = {
                "start_time": item.get("time"),
                "end_time": item.get("time"),
                "start_timestamp": item_ts,
                "end_timestamp": item_ts,
                "count": 1,
                "severities": {item["severity"]: 1},
                "reasons": {},
            }
        elif item_ts is not None and current.get("end_timestamp") is not None and item_ts - current["end_timestamp"] <= gap_ms:
            current["end_time"] = item.get("time")
            current["end_timestamp"] = item_ts
            current["count"] += 1
            current["severities"][item["severity"]] = current["severities"].get(item["severity"], 0) + 1
        elif item_ts is None and current.get("end_timestamp") is None:
            current["count"] += 1
            current["severities"][item["severity"]] = current["severities"].get(item["severity"], 0) + 1
        else:
            windows.append(current)
            current = {
                "start_time": item.get("time"),
                "end_time": item.get("time"),
                "start_timestamp": item_ts,
                "end_timestamp": item_ts,
                "count": 1,
                "severities": {item["severity"]: 1},
                "reasons": {},
            }
        for reason in item.get("reasons", []):
            current["reasons"][reason] = current["reasons"].get(reason, 0) + 1
    if current:
        windows.append(current)
    for window in windows:
        if window.get("start_timestamp") is not None and window.get("end_timestamp") is not None:
            window["duration_seconds"] = max(0, int((window["end_timestamp"] - window["start_timestamp"]) / 1000))
        else:
            window["duration_seconds"] = None
        window["top_reasons"] = sorted(window.pop("reasons").items(), key=lambda item: item[1], reverse=True)[:10]
    return windows


def _logconfig_cr_combinations() -> List[Tuple[str, str, str]]:
    return [
        ("logging.openvessel.io", "v1", "logconfigs"),
        ("lts.opentelekomcloud.com", "v1", "logconfigs"),
        ("lts.huaweicloud.com", "v1", "logconfigs"),
        ("lts.io", "v1", "logconfigs"),
        ("logging.huaweicloud.com", "v1", "logconfigs"),
        ("lts.opentelekomcloud.com", "v1alpha1", "logconfigs"),
        ("lts.opentelekomcloud.com", "v1beta1", "logconfigs"),
    ]


def _get_cce_custom_objects_api(params: Dict[str, str]) -> Tuple[Any, List[str]]:
    region = params["region"]
    cluster_id = params["cluster_id"]
    ak, sk, project_id = get_credentials_with_region(region, params.get("ak"), params.get("sk"), params.get("project_id"))

    from huaweicloudsdkcce.v3.model.cluster_cert_duration import ClusterCertDuration
    from huaweicloudsdkcce.v3.model.create_kubernetes_cluster_cert_request import CreateKubernetesClusterCertRequest

    cce_client = create_cce_client(region, ak, sk, project_id)
    cert_request = CreateKubernetesClusterCertRequest()
    cert_request.cluster_id = cluster_id
    body = ClusterCertDuration()
    body.duration = 1
    cert_request.body = body
    cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
    kubeconfig_data = cert_response.to_dict()

    external_cluster = None
    for cluster in kubeconfig_data.get("clusters", []):
        if "external" in cluster.get("name", "") and "TLS" not in cluster.get("name", ""):
            external_cluster = cluster
            break
    if not external_cluster:
        external_cluster = kubeconfig_data.get("clusters", [{}])[0]
    if not external_cluster:
        raise RuntimeError("Could not find cluster endpoint")

    temp_files = []
    configuration = k8s_client.Configuration()
    configuration.host = external_cluster.get("cluster", {}).get("server")
    configuration.verify_ssl = False

    user_data = None
    for user in kubeconfig_data.get("users", []):
        if user.get("name") == "user":
            user_data = user.get("user", {})
            break

    if user_data and user_data.get("client_certificate_data"):
        cert_file = tempfile.mktemp(suffix=".crt")
        with open(cert_file, "wb") as handle:
            handle.write(base64.b64decode(user_data["client_certificate_data"]))
        configuration.cert_file = cert_file
        temp_files.append(cert_file)
        _register_cert_file(cert_file)

    if user_data and user_data.get("client_key_data"):
        key_file = tempfile.mktemp(suffix=".key")
        with open(key_file, "wb") as handle:
            handle.write(base64.b64decode(user_data["client_key_data"]))
        configuration.key_file = key_file
        temp_files.append(key_file)
        _register_cert_file(key_file)

    k8s_client.Configuration.set_default(configuration)
    return k8s_client.CustomObjectsApi(), temp_files


def _query_logs_with_pagination(
    params: Dict[str, str],
    log_group_id: str,
    log_stream_id: str,
    start_time: Optional[str],
    end_time: Optional[str],
    labels: Dict[str, str],
) -> Dict[str, Any]:
    auto_paginate = _to_bool(params.get("auto_paginate"), False)
    page_limit = _to_int(params.get("limit"), 1000)
    max_pages = _to_int(params.get("max_pages"), 10 if auto_paginate else 1)
    max_pages = max(max_pages, 1)
    is_desc = _to_bool(params.get("is_desc"), True)
    is_iterative = _to_bool(params.get("is_iterative"), auto_paginate)

    all_logs = []
    page_results = []
    scroll_id = params.get("scroll_id")
    seen_scroll_ids = set()
    last_result: Dict[str, Any] = {}
    stopped_reason = "completed"

    for page_index in range(max_pages):
        page = lts.query_logs(
            region=params["region"],
            log_group_id=log_group_id,
            log_stream_id=log_stream_id,
            start_time=start_time,
            end_time=end_time,
            keywords=params.get("keywords"),
            limit=page_limit,
            scroll_id=scroll_id,
            is_desc=is_desc,
            is_iterative=is_iterative,
            labels=labels,
            ak=params.get("ak"),
            sk=params.get("sk"),
            project_id=params.get("project_id"),
        )
        if not page.get("success"):
            if not all_logs:
                return page
            page["partial_logs"] = all_logs
            page["partial_total"] = len(all_logs)
            page["pages_fetched"] = len(page_results)
            return page

        page_logs = page.get("logs", [])
        all_logs.extend(page_logs)
        next_scroll_id = page.get("scroll_id")
        page_results.append(
            {
                "page": page_index + 1,
                "count": len(page_logs),
                "scroll_id": next_scroll_id,
            }
        )
        last_result = page

        if not auto_paginate:
            stopped_reason = "auto_paginate_disabled"
            break
        if not next_scroll_id:
            stopped_reason = "no_more_pages"
            break
        if next_scroll_id in seen_scroll_ids:
            stopped_reason = "repeated_scroll_id"
            break

        seen_scroll_ids.add(next_scroll_id)
        scroll_id = next_scroll_id
    else:
        stopped_reason = "max_pages_reached"

    result = dict(last_result)
    result["logs"] = all_logs
    result["total"] = len(all_logs)
    result["auto_paginate"] = auto_paginate
    result["page_limit"] = page_limit
    result["max_pages"] = max_pages
    result["pages_fetched"] = len(page_results)
    result["page_results"] = page_results
    result["stopped_reason"] = stopped_reason
    result["has_more"] = stopped_reason == "max_pages_reached" and bool(result.get("scroll_id"))
    return result


def get_cce_logconfigs_action(params: Dict[str, str]) -> Dict[str, Any]:
    cluster_id = params["cluster_id"]
    namespace = params.get("namespace")

    temp_files = []
    try:
        custom_api, temp_files = _get_cce_custom_objects_api(params)

        logconfigs = []
        tried = []
        for group, version, plural in _logconfig_cr_combinations():
            tried.append(f"{group}/{version}/{plural}")
            try:
                if namespace:
                    api_result = custom_api.list_namespaced_custom_object(group=group, version=version, namespace=namespace, plural=plural)
                else:
                    api_result = custom_api.list_cluster_custom_object(group=group, version=version, plural=plural)
                for item in api_result.get("items", []):
                    metadata = item.get("metadata", {})
                    spec = item.get("spec", {})
                    input_detail = spec.get("inputDetail", {})
                    output_detail = spec.get("outputDetail", {})
                    logconfigs.append(
                        {
                            "name": metadata.get("name"),
                            "logconfig_name": metadata.get("name"),
                            "policy_name": metadata.get("name"),
                            "namespace": metadata.get("namespace"),
                            "creation_time": str(metadata.get("creationTimestamp")),
                            "input_type": input_detail.get("type"),
                            "output_type": output_detail.get("type"),
                            "spec": spec,
                            "status": item.get("status", {}),
                            "api_version": f"{group}/{version}",
                        }
                    )
                if logconfigs:
                    break
            except Exception:
                continue

        return {
            "success": True,
            "cluster_id": cluster_id,
            "namespace": namespace or "all",
            "count": len(logconfigs),
            "tried_api_combinations": tried,
            "logconfigs": logconfigs,
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    finally:
        for file_path in temp_files:
            _safe_delete_file(file_path)


def _build_logconfig_workloads(params: Dict[str, str], source_type: str) -> List[Dict[str, Any]]:
    workloads = _parse_json_value(params.get("workloads"), None)
    if workloads is not None:
        if not isinstance(workloads, list):
            raise ValueError("workloads must be a JSON array")
        return workloads

    workload_namespace = params.get("workload_namespace") or params.get("namespace") or "default"
    workload_name = params.get("workload_name") or params.get("app_name")
    if not workload_name:
        raise ValueError("workload_name or app_name is required when workloads is not provided")
    workload = {
        "namespace": workload_namespace,
        "kind": params.get("workload_kind", "Deployment"),
        "name": workload_name,
    }
    container_name = params.get("container")
    if container_name:
        workload["container"] = container_name

    if source_type == "container_file":
        log_path = params.get("log_path")
        file_pattern = params.get("file_pattern", "*.log")
        if not log_path:
            raise ValueError("log_path is required for container_file LogConfig")
        workload["files"] = _parse_json_value(
            params.get("files"),
            [{"logPath": log_path, "filePattern": file_pattern}],
        )
    return [workload]


def _build_logconfig_body(params: Dict[str, str]) -> Dict[str, Any]:
    name = params.get("logconfig_name") or params.get("name")
    if not name:
        raise ValueError("logconfig_name or name is required")
    source_type = params.get("source_type") or params.get("input_type") or "container_stdout"
    if source_type not in {"container_stdout", "container_file"}:
        raise ValueError("source_type must be container_stdout or container_file")

    log_group_id = params.get("log_group_id")
    log_stream_id = params.get("log_stream_id")
    if not log_group_id or not log_stream_id:
        raise ValueError("log_group_id and log_stream_id are required")

    all_containers = _to_bool(params.get("all_containers"), source_type == "container_stdout" and not params.get("workload_name") and not params.get("app_name") and not params.get("workloads"))
    input_detail: Dict[str, Any] = {
        "containerFile": {"discoveredForwardSize": params.get("discovered_forward_size", "1MB" if source_type == "container_file" else "")},
        "containerStdout": {},
        "event": {
            "normalEvents": {"enable": False},
            "warningEvents": {"enable": False},
        },
        "hostFile": {"file": {}},
        "processors": _parse_json_value(params.get("processors"), {"fluentBitConfig": {}, "type": params.get("processor_type", "singleline")}),
        "type": source_type,
    }

    if source_type == "container_stdout":
        if all_containers:
            input_detail["containerStdout"] = {"allContainers": True}
            namespaces = _parse_text_list(params.get("namespaces"), [])
            if namespaces:
                input_detail["containerStdout"]["namespaces"] = namespaces
        else:
            input_detail["containerStdout"] = {"allContainers": False, "workloads": _build_logconfig_workloads(params, source_type)}
    else:
        input_detail["containerFile"]["workloads"] = _build_logconfig_workloads(params, source_type)

    return {
        "apiVersion": f"{params.get('api_group', 'logging.openvessel.io')}/{params.get('api_version', 'v1')}",
        "kind": "LogConfig",
        "metadata": {
            "name": name,
            "namespace": params.get("logconfig_namespace", "kube-system"),
        },
        "spec": {
            "inputDetail": input_detail,
            "logConfigStatus": {
                "LTS": {},
                "conditions": [],
            },
            "outputDetail": {
                "AOM": {},
                "LTS": {
                    "isCustomised": _to_bool(params.get("is_customised"), False),
                    "ltsGroupCreateParam": _parse_json_value(params.get("lts_group_create_param"), {}),
                    "ltsGroupID": log_group_id,
                    "ltsStreamCreateParam": _parse_json_value(params.get("lts_stream_create_param"), {}),
                    "ltsStreamID": log_stream_id,
                },
                "kafka": {},
                "type": "LTS",
            },
        },
    }


def create_cce_logconfig_action(params: Dict[str, str]) -> Dict[str, Any]:
    temp_files = []
    try:
        body = _build_logconfig_body(params)
        group = params.get("api_group", "logging.openvessel.io")
        version = params.get("api_version", "v1")
        plural = params.get("plural", "logconfigs")
        namespace = body["metadata"]["namespace"]

        if not _to_bool(params.get("confirm"), False):
            return {
                "success": False,
                "requires_confirmation": True,
                "message": "创建CCE LogConfig会修改集群日志采集配置。如确认创建，请带 confirm=true 重新调用。",
                "cluster_id": params["cluster_id"],
                "logconfig_name": body["metadata"]["name"],
                "logconfig_namespace": namespace,
                "api_version": body["apiVersion"],
                "request_body": body,
            }

        custom_api, temp_files = _get_cce_custom_objects_api(params)
        response = custom_api.create_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            body=body,
        )
        metadata = response.get("metadata", {}) if isinstance(response, dict) else {}
        return {
            "success": True,
            "cluster_id": params["cluster_id"],
            "logconfig_name": metadata.get("name", body["metadata"]["name"]),
            "logconfig_namespace": metadata.get("namespace", namespace),
            "api_version": body["apiVersion"],
            "source_type": body["spec"]["inputDetail"]["type"],
            "log_group_id": body["spec"]["outputDetail"]["LTS"]["ltsGroupID"],
            "log_stream_id": body["spec"]["outputDetail"]["LTS"]["ltsStreamID"],
            "response": response,
        }
    except Exception as exc:
        status = getattr(exc, "status", None)
        reason = getattr(exc, "reason", None)
        body_text = getattr(exc, "body", None)
        return {
            "success": False,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "status": status,
            "reason": reason,
            "response_body": body_text,
        }
    finally:
        for file_path in temp_files:
            _safe_delete_file(file_path)


def delete_cce_logconfig_action(params: Dict[str, str]) -> Dict[str, Any]:
    temp_files = []
    try:
        name = params.get("logconfig_name") or params.get("name")
        if not name:
            raise ValueError("logconfig_name or name is required")
        namespace = params.get("logconfig_namespace") or params.get("namespace") or "kube-system"
        group = params.get("api_group", "logging.openvessel.io")
        version = params.get("api_version", "v1")
        plural = params.get("plural", "logconfigs")

        custom_api, temp_files = _get_cce_custom_objects_api(params)
        existing = custom_api.get_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=name,
        )
        metadata = existing.get("metadata", {}) if isinstance(existing, dict) else {}
        spec = existing.get("spec", {}) if isinstance(existing, dict) else {}
        input_detail = spec.get("inputDetail", {})
        output_detail = spec.get("outputDetail", {})

        if not _to_bool(params.get("confirm"), False):
            return {
                "success": False,
                "requires_confirmation": True,
                "message": "删除CCE LogConfig会停止对应日志采集。如确认删除，请带 confirm=true 重新调用。",
                "cluster_id": params["cluster_id"],
                "logconfig_name": metadata.get("name", name),
                "logconfig_namespace": metadata.get("namespace", namespace),
                "api_version": f"{group}/{version}",
                "source_type": input_detail.get("type"),
                "output_type": output_detail.get("type"),
                "target": {
                    "group": group,
                    "version": version,
                    "namespace": namespace,
                    "plural": plural,
                    "name": name,
                },
                "existing": {
                    "name": metadata.get("name", name),
                    "namespace": metadata.get("namespace", namespace),
                    "creation_time": metadata.get("creationTimestamp"),
                    "input_type": input_detail.get("type"),
                    "output_type": output_detail.get("type"),
                    "log_group_id": output_detail.get("LTS", {}).get("ltsGroupID"),
                    "log_stream_id": output_detail.get("LTS", {}).get("ltsStreamID"),
                },
            }

        response = custom_api.delete_namespaced_custom_object(
            group=group,
            version=version,
            namespace=namespace,
            plural=plural,
            name=name,
        )
        return {
            "success": True,
            "cluster_id": params["cluster_id"],
            "logconfig_name": name,
            "logconfig_namespace": namespace,
            "api_version": f"{group}/{version}",
            "response": response,
        }
    except Exception as exc:
        status = getattr(exc, "status", None)
        reason = getattr(exc, "reason", None)
        body_text = getattr(exc, "body", None)
        return {
            "success": False,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "status": status,
            "reason": reason,
            "response_body": body_text,
        }
    finally:
        for file_path in temp_files:
            _safe_delete_file(file_path)


def _discover_audit_log_stream(params: Dict[str, str]) -> Dict[str, Any]:
    if params.get("log_group_id") and params.get("log_stream_id"):
        return {
            "success": True,
            "log_group_id": params["log_group_id"],
            "log_stream_id": params["log_stream_id"],
            "match_type": "explicit_ids",
        }

    group_name_filter = (params.get("log_group_name") or "").lower()
    stream_name_filter = (params.get("log_stream_name") or "").lower()
    audit_terms = [term.lower() for term in _parse_text_list(params.get("audit_stream_keywords"), ["audit", "apiserver", "api-server", "kube-apiserver"])]
    cluster_hint = (params.get("cluster_id") or "").lower()

    groups_result = lts.list_log_groups(params["region"], params.get("ak"), params.get("sk"), params.get("project_id"))
    if not groups_result.get("success"):
        return groups_result

    candidates = []
    for group in groups_result.get("log_groups", []):
        group_name = str(group.get("log_group_name") or "").lower()
        group_id = group.get("log_group_id")
        if params.get("log_group_id") and group_id != params["log_group_id"]:
            continue
        if group_name_filter and group_name_filter not in group_name:
            continue
        if not group_name_filter and cluster_hint and cluster_hint not in group_name and not any(term in group_name for term in audit_terms):
            # Keep scanning other groups, but avoid opening every unrelated group when names give no hint.
            continue

        streams_result = lts.list_log_streams(params["region"], group_id, params.get("ak"), params.get("sk"), params.get("project_id"))
        if not streams_result.get("success"):
            continue
        for stream in streams_result.get("log_streams", []):
            stream_name = str(stream.get("log_stream_name") or "").lower()
            if stream_name_filter and stream_name_filter not in stream_name:
                continue
            score = 0
            if cluster_hint and cluster_hint in stream_name:
                score += 6
            elif cluster_hint and cluster_hint in group_name:
                score += 2
            for term in audit_terms:
                if term in stream_name:
                    score += 5
                if term in group_name:
                    score += 2
            if stream_name_filter:
                score += 10
            if group_name_filter:
                score += 4
            if score > 0:
                candidates.append({"score": score, "log_group": group, "log_stream": stream})

    candidates.sort(key=lambda item: item["score"], reverse=True)
    if not candidates:
        return {
            "success": False,
            "error": "未自动发现CCE审计日志流",
            "note": "请传入 log_group_id/log_stream_id，或使用 log_group_name/log_stream_name/audit_stream_keywords 指定审计日志流名称特征。",
            "searched_group_count": len(groups_result.get("log_groups", [])),
        }
    selected = candidates[0]
    return {
        "success": True,
        "log_group_id": selected["log_group"].get("log_group_id"),
        "log_stream_id": selected["log_stream"].get("log_stream_id"),
        "log_group_name": selected["log_group"].get("log_group_name"),
        "log_stream_name": selected["log_stream"].get("log_stream_name"),
        "match_type": "auto_discovered",
        "candidates": [
            {
                "score": item["score"],
                "log_group_id": item["log_group"].get("log_group_id"),
                "log_group_name": item["log_group"].get("log_group_name"),
                "log_stream_id": item["log_stream"].get("log_stream_id"),
                "log_stream_name": item["log_stream"].get("log_stream_name"),
            }
            for item in candidates[:10]
        ],
    }


def _audit_filters(params: Dict[str, str]) -> Dict[str, Any]:
    audit_type = params.get("audit_type") or params.get("scenario")
    resource_name = params.get("resource_name") or params.get("pod_name") or params.get("workload_name") or params.get("app_name")
    content_keywords = _parse_text_list(params.get("content_keywords"), [])
    for keyword in (
        resource_name,
        params.get("namespace"),
        params.get("user"),
        params.get("status_code"),
        params.get("verb"),
        params.get("resource"),
        *(_parse_text_list(params.get("verbs"), [])),
        *(_parse_text_list(params.get("resources"), [])),
    ):
        if keyword and keyword not in content_keywords:
            content_keywords.append(keyword)
    if audit_type == "pod_delete":
        for keyword in ("delete", "pods"):
            if keyword not in content_keywords:
                content_keywords.append(keyword)
    elif audit_type in {"workload_change", "application_change", "app_change"}:
        for keyword in ("create", "update", "patch", "delete"):
            if keyword not in content_keywords:
                content_keywords.append(keyword)
    filters: Dict[str, Any] = {
        "audit_type": audit_type,
        "resource_name": resource_name,
        "content_keywords": content_keywords,
    }
    return filters


def _extract_audit_event(log: Dict[str, Any]) -> Dict[str, Any]:
    content = _content_of(log)
    audit = _json_content_of(log)
    object_ref = audit.get("objectRef", {}) if isinstance(audit.get("objectRef"), dict) else {}
    user_info = audit.get("user", {}) if isinstance(audit.get("user"), dict) else {}
    response_status = audit.get("responseStatus", {}) if isinstance(audit.get("responseStatus"), dict) else {}
    timestamp_ms = _extract_audit_time_ms(log, audit)
    return {
        "timestamp_ms": timestamp_ms,
        "time": _format_ts(timestamp_ms),
        "verb": audit.get("verb"),
        "user": user_info.get("username") or audit.get("username"),
        "resource": object_ref.get("resource"),
        "subresource": object_ref.get("subresource"),
        "namespace": object_ref.get("namespace"),
        "name": object_ref.get("name"),
        "api_group": object_ref.get("apiGroup"),
        "api_version": object_ref.get("apiVersion"),
        "request_uri": audit.get("requestURI"),
        "source_ips": audit.get("sourceIPs"),
        "user_agent": audit.get("userAgent"),
        "stage": audit.get("stage"),
        "status_code": response_status.get("code"),
        "status_reason": response_status.get("reason"),
        "content": content[:1000],
        "raw": audit,
    }


def _audit_event_matches(event: Dict[str, Any], filters: Dict[str, Any]) -> bool:
    content_lower = re.sub(r"</?highlighttag>", "", str(event.get("content") or ""), flags=re.IGNORECASE).lower()
    keywords = [item.lower() for item in filters.get("content_keywords", [])]
    if keywords and not all(keyword in content_lower for keyword in keywords):
        return False
    return True


def query_cce_audit_logs_action(params: Dict[str, str]) -> Dict[str, Any]:
    stream_result = _discover_audit_log_stream(params)
    if not stream_result.get("success"):
        return stream_result

    filters = _audit_filters(params)
    query_params = dict(params)
    query_params.setdefault("auto_paginate", "true")
    query_params.setdefault("max_pages", "5")
    query_params.setdefault("limit", "500")
    if not query_params.get("keywords") and filters.get("content_keywords"):
        query_params["keywords"] = " ".join(filters["content_keywords"])
    if not query_params.get("start_time") and not query_params.get("end_time"):
        hours = _to_int(query_params.get("hours"), 1)
        end_time_dt = datetime.now()
        start_time_dt = end_time_dt - timedelta(hours=hours)
        query_params["start_time"] = start_time_dt.strftime("%Y-%m-%d %H:%M:%S")
        query_params["end_time"] = end_time_dt.strftime("%Y-%m-%d %H:%M:%S")

    labels = _parse_labels(query_params.get("labels")) or {}
    if query_params.get("cluster_id") and _to_bool(query_params.get("add_cluster_label"), False):
        labels.setdefault("clusterId", query_params["cluster_id"])

    query_result = _query_logs_with_pagination(
        params=query_params,
        log_group_id=stream_result["log_group_id"],
        log_stream_id=stream_result["log_stream_id"],
        start_time=query_params.get("start_time"),
        end_time=query_params.get("end_time"),
        labels=labels,
    )
    if not query_result.get("success"):
        return query_result

    events = [_extract_audit_event(log) for log in query_result.get("logs", [])]
    matched_events = [event for event in events if _audit_event_matches(event, filters)]
    sample_limit = _to_int(params.get("sample_limit"), 50)

    def _count_by(key: str) -> List[Dict[str, Any]]:
        counts: Dict[str, int] = {}
        for event in matched_events:
            value = event.get(key)
            if value is None or value == "":
                value = "unknown"
            value = str(value)
            counts[value] = counts.get(value, 0) + 1
        return [{"value": value, "count": count} for value, count in sorted(counts.items(), key=lambda item: item[1], reverse=True)[:20]]

    return {
        "success": True,
        "cluster_id": params["cluster_id"],
        "log_group_id": stream_result["log_group_id"],
        "log_stream_id": stream_result["log_stream_id"],
        "log_group_name": stream_result.get("log_group_name"),
        "log_stream_name": stream_result.get("log_stream_name"),
        "stream_match_type": stream_result.get("match_type"),
        "analysis_window": {
            "start_time": query_result.get("start_time"),
            "end_time": query_result.get("end_time"),
        },
        "filters": filters,
        "summary": {
            "queried_logs": len(query_result.get("logs", [])),
            "parsed_audit_events": len(events),
            "matched_events": len(matched_events),
            "matched_ratio": round(len(matched_events) / len(events), 6) if events else 0.0,
        },
        "top_users": _count_by("user"),
        "top_verbs": _count_by("verb"),
        "top_resources": _count_by("resource"),
        "top_namespaces": _count_by("namespace"),
        "top_status_codes": _count_by("status_code"),
        "events": matched_events[:sample_limit],
        "query_summary": {
            "auto_paginate": query_result.get("auto_paginate"),
            "page_limit": query_result.get("page_limit"),
            "max_pages": query_result.get("max_pages"),
            "pages_fetched": query_result.get("pages_fetched"),
            "stopped_reason": query_result.get("stopped_reason"),
            "labels": labels,
            "lts_keywords": query_params.get("keywords"),
        },
        "discovery_candidates": stream_result.get("candidates"),
    }


def get_application_logconfigs_action(params: Dict[str, str]) -> Dict[str, Any]:
    cluster_id = params["cluster_id"]
    app_name = params["app_name"]
    namespace = params.get("namespace")  # 不设置默认值，用于匹配逻辑
    requested_policy_name = _get_policy_name(params)

    # 去掉 namespace 参数，让 get_cce_logconfigs_action 搜索所有命名空间
    search_params = {k: v for k, v in params.items() if k != "namespace"}
    logconfig_result = get_cce_logconfigs_action(search_params)
    if not logconfig_result.get("success"):
        return logconfig_result

    logconfigs = logconfig_result.get("logconfigs", [])
    if not logconfigs:
        return {"success": False, "error": "集群中未找到任何LogConfig采集规则", "note": "请先配置日志采集规则或确认日志采集组件已安装"}

    def _extract_lts_stream(logconfig: Dict[str, Any]) -> Dict[str, Optional[str]]:
        lts_config = logconfig.get("spec", {}).get("outputDetail", {}).get("LTS", {})
        log_group_id = lts_config.get("ltsGroupID")
        log_stream_id = lts_config.get("ltsStreamID", lts_config.get("streamID"))
        if not log_stream_id:
            log_stream_id = logconfig.get("spec", {}).get("logConfigStatus", {}).get("LTS", {}).get("streamID")
        return {"log_group_id": log_group_id, "log_stream_id": log_stream_id}

    matched_streams = []
    stdout_primary = None

    # 1) container_stdout: 精确工作负载匹配
    for logconfig in logconfigs:
        try:
            if logconfig.get("spec", {}).get("inputDetail", {}).get("type") != "container_stdout":
                continue
            workloads = logconfig.get("spec", {}).get("inputDetail", {}).get("containerStdout", {}).get("workloads", [])
            for workload in workloads:
                if workload.get("namespace") == namespace and workload.get("name") == app_name:
                    stream = _extract_lts_stream(logconfig)
                    if stream.get("log_group_id") and stream.get("log_stream_id"):
                        entry = {
                            "source_type": "container_stdout",
                            "match_type": "精确匹配应用LogConfig",
                            "logconfig_name": logconfig.get("name"),
                            "policy_name": logconfig.get("name"),
                            "log_group_id": stream["log_group_id"],
                            "log_stream_id": stream["log_stream_id"],
                        }
                        matched_streams.append(entry)
                        stdout_primary = stdout_primary or entry
                    break
        except Exception:
            continue

    # 2) container_stdout: 全容器规则匹配
    if not stdout_primary:
        for logconfig in logconfigs:
            try:
                if logconfig.get("spec", {}).get("inputDetail", {}).get("type") != "container_stdout":
                    continue
                container_stdout = logconfig.get("spec", {}).get("inputDetail", {}).get("containerStdout", {})
                if container_stdout.get("allContainers") is not True:
                    continue
                allowed_namespaces = container_stdout.get("namespaces", [])
                if allowed_namespaces and namespace not in allowed_namespaces:
                    continue
                stream = _extract_lts_stream(logconfig)
                if stream.get("log_group_id") and stream.get("log_stream_id"):
                    entry = {
                        "source_type": "container_stdout",
                        "match_type": "命名空间全局LogConfig匹配",
                        "logconfig_name": logconfig.get("name"),
                        "policy_name": logconfig.get("name"),
                        "log_group_id": stream["log_group_id"],
                        "log_stream_id": stream["log_stream_id"],
                    }
                    matched_streams.append(entry)
                    stdout_primary = entry
                    break
            except Exception:
                continue

    # 3) container_stdout: default-stdout 兜底
    if not stdout_primary:
        for logconfig in logconfigs:
            try:
                if logconfig.get("name") != "default-stdout":
                    continue
                if logconfig.get("spec", {}).get("inputDetail", {}).get("type") != "container_stdout":
                    continue
                stream = _extract_lts_stream(logconfig)
                if stream.get("log_group_id") and stream.get("log_stream_id"):
                    entry = {
                        "source_type": "container_stdout",
                        "match_type": "默认default-stdout LogConfig匹配",
                        "logconfig_name": logconfig.get("name"),
                        "policy_name": logconfig.get("name"),
                        "log_group_id": stream["log_group_id"],
                        "log_stream_id": stream["log_stream_id"],
                    }
                    matched_streams.append(entry)
                    stdout_primary = entry
                    break
            except Exception:
                continue

    # 4) container_file: workloads匹配（补充返回文件日志采集策略）
    for logconfig in logconfigs:
        try:
            if logconfig.get("spec", {}).get("inputDetail", {}).get("type") != "container_file":
                continue
            workloads = logconfig.get("spec", {}).get("inputDetail", {}).get("containerFile", {}).get("workloads", [])
            for workload in workloads:
                if workload.get("namespace") == namespace and workload.get("name") == app_name:
                    stream = _extract_lts_stream(logconfig)
                    if stream.get("log_group_id") and stream.get("log_stream_id"):
                        matched_streams.append(
                            {
                                "source_type": "container_file",
                                "match_type": "容器文件采集策略匹配",
                                "logconfig_name": logconfig.get("name"),
                                "policy_name": logconfig.get("name"),
                                "log_group_id": stream["log_group_id"],
                                "log_stream_id": stream["log_stream_id"],
                                "workload": workload,
                            }
                        )
                    break
        except Exception:
            continue

    if not matched_streams:
        return {
            "success": False,
            "error": "未匹配到任何日志采集规则",
            "note": "请检查应用是否配置了stdout/container_file采集规则，或集群是否存在default-stdout默认采集规则",
        }

    primary = stdout_primary or matched_streams[0]
    if requested_policy_name:
        primary = next(
            (
                stream
                for stream in matched_streams
                if stream.get("logconfig_name") == requested_policy_name or stream.get("policy_name") == requested_policy_name
            ),
            None,
        )
        if not primary:
            return {
                "success": False,
                "error": f"未找到名称为 {requested_policy_name} 的日志采集策略",
                "available_policies": [stream.get("policy_name") for stream in matched_streams],
                "matched_streams": matched_streams,
            }
    return {
        "success": True,
        "match_type": primary.get("match_type"),
        "logconfig_name": primary.get("logconfig_name"),
        "policy_name": primary.get("policy_name"),
        "source_type": primary.get("source_type"),
        "app_name": app_name,
        "namespace": namespace,
        "log_group_id": primary.get("log_group_id"),
        "log_stream_id": primary.get("log_stream_id"),
        "cluster_id": cluster_id,
        "matched_streams": matched_streams,
    }


def query_application_logs_action(params: Dict[str, str]) -> Dict[str, Any]:
    namespace = params.get("namespace", "default")
    app_name = params["app_name"]
    policy_name = _get_policy_name(params)
    custom_labels = _parse_labels(params.get("labels"))
    stream_result = get_application_logconfigs_action(params)
    if not stream_result.get("success"):
        return stream_result

    # CCE/LTS uses nameSpace and logconfig as label keys in collected container logs.
    system_labels = {"clusterId": params["cluster_id"], "appName": app_name, "nameSpace": namespace}
    if policy_name:
        system_labels["logconfig"] = policy_name
    final_labels = system_labels.copy()
    if custom_labels:
        final_labels.update(custom_labels)

    result = _query_logs_with_pagination(
        params=params,
        log_group_id=stream_result["log_group_id"],
        log_stream_id=stream_result["log_stream_id"],
        start_time=params.get("start_time"),
        end_time=params.get("end_time"),
        labels=final_labels,
    )
    result.update(
        {
            "cluster_id": params["cluster_id"],
            "namespace": namespace,
            "app_name": app_name,
            "match_type": stream_result.get("match_type"),
            "logconfig_name": stream_result.get("logconfig_name"),
            "policy_name": stream_result.get("policy_name"),
            "source_type": stream_result.get("source_type"),
            "auto_label_filter": system_labels,
            "custom_labels": custom_labels,
            "final_labels": final_labels,
            "matched_streams": stream_result.get("matched_streams"),
        }
    )
    return result


def query_application_recent_logs_action(params: Dict[str, str]) -> Dict[str, Any]:
    namespace = params.get("namespace", "default")
    app_name = params["app_name"]
    policy_name = _get_policy_name(params)
    custom_labels = _parse_labels(params.get("labels"))
    stream_result = get_application_logconfigs_action(params)
    if not stream_result.get("success"):
        return stream_result

    # CCE/LTS uses nameSpace and logconfig as label keys in collected container logs.
    system_labels = {"clusterId": params["cluster_id"], "appName": app_name, "nameSpace": namespace}
    if policy_name:
        system_labels["logconfig"] = policy_name
    final_labels = system_labels.copy()
    if custom_labels:
        final_labels.update(custom_labels)

    hours = _to_int(params.get("hours"), 1)
    end_time_dt = datetime.now()
    start_time_dt = end_time_dt - timedelta(hours=hours)
    result = _query_logs_with_pagination(
        params=params,
        log_group_id=stream_result["log_group_id"],
        log_stream_id=stream_result["log_stream_id"],
        start_time=start_time_dt.strftime("%Y-%m-%d %H:%M:%S"),
        end_time=end_time_dt.strftime("%Y-%m-%d %H:%M:%S"),
        labels=final_labels,
    )
    result["hours"] = hours
    result.update(
        {
            "cluster_id": params["cluster_id"],
            "namespace": namespace,
            "app_name": app_name,
            "match_type": stream_result.get("match_type"),
            "logconfig_name": stream_result.get("logconfig_name"),
            "policy_name": stream_result.get("policy_name"),
            "source_type": stream_result.get("source_type"),
            "auto_label_filter": system_labels,
            "custom_labels": custom_labels,
            "final_labels": final_labels,
            "matched_streams": stream_result.get("matched_streams"),
        }
    )
    return result


def analyze_application_logs_action(params: Dict[str, str]) -> Dict[str, Any]:
    query_params = dict(params)
    query_params.setdefault("auto_paginate", "true")
    query_params.setdefault("max_pages", "10")
    query_params.setdefault("limit", "1000")
    query_params.setdefault("is_desc", "false")

    if params.get("start_time") or params.get("end_time"):
        query_result = query_application_logs_action(query_params)
    else:
        query_params.setdefault("hours", "1")
        query_result = query_application_recent_logs_action(query_params)
    if not query_result.get("success"):
        return query_result

    default_error_patterns = [
        r"\berror\b",
        r"\bexception\b",
        r"\btraceback\b",
        r"\bpanic\b",
        r"\bfatal\b",
        r"\bfailed?\b",
        r"\bfailure\b",
        r"\btimeout\b",
        r"\btimed out\b",
        r"\bconnection refused\b",
        r"\bunavailable\b",
        r"\boom\b",
        r"out of memory",
        r"segmentation fault",
        r"stacktrace",
    ]
    default_warning_patterns = [r"\bwarn(?:ing)?\b", r"\bdeprecated\b", r"\bretry(?:ing)?\b", r"\bslow\b"]
    error_patterns = _parse_text_list(params.get("error_patterns"), default_error_patterns)
    warning_patterns = _parse_text_list(params.get("warning_patterns"), default_warning_patterns)
    http_error_status_threshold = _to_int(params.get("http_error_status_threshold"), 500)
    include_http_4xx = _to_bool(params.get("include_http_4xx"), False)
    incident_gap_minutes = _to_int(params.get("incident_gap_minutes"), 5)
    sample_limit = _to_int(params.get("sample_limit"), 20)

    logs = query_result.get("logs", [])
    analyzed_logs = []
    anomalies = []
    status_code_counts: Dict[str, int] = {}
    reason_counts: Dict[str, int] = {}
    severity_counts = {"critical": 0, "error": 0, "warning": 0, "normal": 0}
    timestamped_logs = []

    for index, log in enumerate(logs):
        content = _content_of(log)
        timestamp_ms = _extract_log_time_ms(log)
        is_abnormal, severity, reasons, status_code = _classify_log(
            content,
            error_patterns,
            warning_patterns,
            http_error_status_threshold,
            include_http_4xx,
        )
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
        if status_code is not None:
            key = str(status_code)
            status_code_counts[key] = status_code_counts.get(key, 0) + 1
        for reason in reasons:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

        analyzed = {
            "index": index,
            "timestamp_ms": timestamp_ms,
            "time": _format_ts(timestamp_ms),
            "is_abnormal": is_abnormal,
            "severity": severity,
            "reasons": reasons,
            "status_code": status_code,
        }
        analyzed_logs.append(analyzed)
        if timestamp_ms is not None:
            timestamped_logs.append(analyzed)
        if is_abnormal:
            sample = dict(analyzed)
            sample["content"] = content[:500]
            anomalies.append(sample)

    total_logs = len(logs)
    abnormal_logs = len(anomalies)
    abnormal_ratio = round(abnormal_logs / total_logs, 6) if total_logs else 0.0
    timestamped_sorted = sorted(timestamped_logs, key=lambda item: item["timestamp_ms"])
    anomalies_sorted = sorted(anomalies, key=lambda item: (item.get("timestamp_ms") is None, item.get("timestamp_ms") or 0, item["index"]))
    first_abnormal = anomalies_sorted[0] if anomalies_sorted else None
    last_abnormal = anomalies_sorted[-1] if anomalies_sorted else None
    recovery = None
    if last_abnormal and last_abnormal.get("timestamp_ms") is not None:
        for item in timestamped_sorted:
            if item["timestamp_ms"] > last_abnormal["timestamp_ms"] and not item["is_abnormal"]:
                recovery = item
                break

    http_4xx_count = sum(count for code, count in status_code_counts.items() if 400 <= int(code) < 500)
    http_5xx_count = sum(count for code, count in status_code_counts.items() if int(code) >= 500)
    top_status_codes = sorted(status_code_counts.items(), key=lambda item: item[1], reverse=True)[:10]
    top_patterns = sorted(reason_counts.items(), key=lambda item: item[1], reverse=True)[:20]
    window_start = query_result.get("start_time")
    window_end = query_result.get("end_time")
    window_duration_minutes = None
    if isinstance(window_start, int) and isinstance(window_end, int) and window_end > window_start:
        window_duration_minutes = round((window_end - window_start) / 60000, 4)
    logs_per_minute = round(total_logs / window_duration_minutes, 6) if window_duration_minutes else None
    abnormal_logs_per_minute = round(abnormal_logs / window_duration_minutes, 6) if window_duration_minutes else None

    return {
        "success": True,
        "cluster_id": query_result.get("cluster_id"),
        "namespace": query_result.get("namespace"),
        "app_name": query_result.get("app_name"),
        "logconfig_name": query_result.get("logconfig_name"),
        "policy_name": query_result.get("policy_name"),
        "source_type": query_result.get("source_type"),
        "log_group_id": query_result.get("log_group_id"),
        "log_stream_id": query_result.get("log_stream_id"),
        "analysis_window": {
            "start_time": _format_ts(window_start) if isinstance(window_start, int) else window_start,
            "end_time": _format_ts(window_end) if isinstance(window_end, int) else window_end,
            "start_timestamp": window_start,
            "end_timestamp": window_end,
            "duration_minutes": window_duration_minutes,
        },
        "summary": {
            "total_logs": total_logs,
            "timestamped_logs": len(timestamped_logs),
            "abnormal_logs": abnormal_logs,
            "normal_logs": total_logs - abnormal_logs,
            "abnormal_ratio": abnormal_ratio,
            "abnormal_percent": round(abnormal_ratio * 100, 4),
            "critical_logs": severity_counts.get("critical", 0),
            "error_logs": severity_counts.get("error", 0),
            "warning_logs": severity_counts.get("warning", 0),
            "http_4xx_count": http_4xx_count,
            "http_5xx_count": http_5xx_count,
            "logs_per_minute": logs_per_minute,
            "abnormal_logs_per_minute": abnormal_logs_per_minute,
            "is_recovered": bool(recovery) if abnormal_logs else True,
        },
        "timeline": {
            "first_abnormal_time": first_abnormal.get("time") if first_abnormal else None,
            "first_abnormal_timestamp": first_abnormal.get("timestamp_ms") if first_abnormal else None,
            "last_abnormal_time": last_abnormal.get("time") if last_abnormal else None,
            "last_abnormal_timestamp": last_abnormal.get("timestamp_ms") if last_abnormal else None,
            "recovery_time": recovery.get("time") if recovery else None,
            "recovery_timestamp": recovery.get("timestamp_ms") if recovery else None,
            "recovery_observed": bool(recovery) if abnormal_logs else True,
        },
        "incident_windows": _build_incident_windows(anomalies, incident_gap_minutes),
        "top_patterns": [{"pattern": pattern, "count": count} for pattern, count in top_patterns],
        "top_status_codes": [{"status_code": code, "count": count} for code, count in top_status_codes],
        "abnormal_samples": anomalies_sorted[:sample_limit],
        "query_summary": {
            "auto_paginate": query_result.get("auto_paginate"),
            "page_limit": query_result.get("page_limit"),
            "max_pages": query_result.get("max_pages"),
            "pages_fetched": query_result.get("pages_fetched"),
            "stopped_reason": query_result.get("stopped_reason"),
            "final_labels": query_result.get("final_labels"),
            "keywords": params.get("keywords"),
            "keywords_scope_note": "When keywords is set, ratios are calculated only over logs matched by that keyword filter." if params.get("keywords") else None,
        },
    }


def _parse_labels(labels: Optional[str]) -> Optional[Dict[str, str]]:
    if not labels:
        return None
    if isinstance(labels, dict):
        return labels
    return json.loads(labels)
