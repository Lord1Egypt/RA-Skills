"""CCE HorizontalPodAutoscaler helpers."""

from __future__ import annotations

import base64
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from huaweicloudsdkcce.v3 import ClusterCertDuration, CreateKubernetesClusterCertRequest

from .common import (
    IMPORT_ERROR,
    K8S_AVAILABLE,
    K8S_IMPORT_ERROR,
    SDK_AVAILABLE,
    _register_cert_file,
    _safe_delete_file,
    create_cce_client,
    get_credentials,
    k8s_client,
)

try:
    from kubernetes.client.rest import ApiException
except Exception:
    ApiException = None


SYSTEM_NAMESPACES = {"kube-system"}


def _validate_common(region: str, cluster_id: Optional[str], ak: Optional[str], sk: Optional[str], project_id: Optional[str]):
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return None, {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters.",
        }
    if not cluster_id:
        return None, {"success": False, "error": "cluster_id is required"}
    if not K8S_AVAILABLE:
        return None, {"success": False, "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"}
    if not SDK_AVAILABLE:
        return None, {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}
    return (access_key, secret_key, proj_id), None


def _write_cert_file(payload: str, suffix: str) -> str:
    fd, path = tempfile.mkstemp(prefix=f"cce_hpa_{os.getpid()}_", suffix=suffix)
    with os.fdopen(fd, "wb") as handle:
        handle.write(base64.b64decode(payload))
    _register_cert_file(path)
    return path


def _setup_k8s_client(region: str, cluster_id: str, access_key: str, secret_key: str, project_id: str):
    cce_client = create_cce_client(region, access_key, secret_key, project_id)

    cert_request = CreateKubernetesClusterCertRequest()
    cert_request.cluster_id = cluster_id
    body = ClusterCertDuration()
    body.duration = 1
    cert_request.body = body

    cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
    kubeconfig_data = cert_response.to_dict()

    external_cluster = None
    for cluster in kubeconfig_data.get("clusters", []):
        name = cluster.get("name", "")
        if "external" in name and "TLS" not in name:
            external_cluster = cluster
            break
    if not external_cluster:
        external_cluster = kubeconfig_data.get("clusters", [{}])[0]
    if not external_cluster:
        raise RuntimeError("Could not find cluster endpoint")

    configuration = k8s_client.Configuration()
    configuration.host = external_cluster.get("cluster", {}).get("server")
    configuration.verify_ssl = False

    user_data = {}
    for user in kubeconfig_data.get("users", []):
        if user.get("name") == "user":
            user_data = user.get("user", {})
            break

    cert_file = None
    key_file = None
    if user_data.get("client_certificate_data"):
        cert_file = _write_cert_file(user_data["client_certificate_data"], ".crt")
        configuration.cert_file = cert_file
    if user_data.get("client_key_data"):
        key_file = _write_cert_file(user_data["client_key_data"], ".key")
        configuration.key_file = key_file

    k8s_client.Configuration.set_default(configuration)
    return cert_file, key_file


def _to_plain(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_to_plain(item) for item in value]
    if isinstance(value, tuple):
        return [_to_plain(item) for item in value]
    if isinstance(value, dict):
        return {key: _to_plain(item) for key, item in value.items()}
    if hasattr(value, "to_dict"):
        return _to_plain(value.to_dict())
    return str(value)


def _normalize_kind(workload_type: str) -> str:
    normalized = (workload_type or "deployment").strip().lower()
    if normalized in {"deployment", "deploy"}:
        return "Deployment"
    if normalized in {"statefulset", "sts"}:
        return "StatefulSet"
    raise ValueError("workload_type must be 'deployment' or 'statefulset'")


def _coerce_behavior(behavior: Any) -> Optional[Dict[str, Any]]:
    if not behavior:
        return None
    if isinstance(behavior, dict):
        return behavior
    if isinstance(behavior, str):
        return json.loads(behavior)
    raise ValueError("behavior must be a JSON object")


def build_hpa_manifest(
    workload_name: str,
    namespace: str,
    min_replicas: int,
    max_replicas: int,
    workload_type: str = "deployment",
    hpa_name: Optional[str] = None,
    target_cpu_utilization: Optional[int] = 60,
    target_memory_utilization: Optional[int] = None,
    behavior: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if not workload_name:
        raise ValueError("workload_name is required")
    if not namespace:
        raise ValueError("namespace is required")
    if namespace in SYSTEM_NAMESPACES:
        raise ValueError("kube-system workloads are excluded from cost optimization HPA actions")
    if min_replicas < 1:
        raise ValueError("min_replicas must be greater than or equal to 1")
    if max_replicas < min_replicas:
        raise ValueError("max_replicas must be greater than or equal to min_replicas")

    metrics = []
    if target_cpu_utilization is not None:
        if target_cpu_utilization < 1 or target_cpu_utilization > 100:
            raise ValueError("target_cpu_utilization must be between 1 and 100")
        metrics.append({
            "type": "Resource",
            "resource": {
                "name": "cpu",
                "target": {"type": "Utilization", "averageUtilization": target_cpu_utilization},
            },
        })
    if target_memory_utilization is not None:
        if target_memory_utilization < 1 or target_memory_utilization > 100:
            raise ValueError("target_memory_utilization must be between 1 and 100")
        metrics.append({
            "type": "Resource",
            "resource": {
                "name": "memory",
                "target": {"type": "Utilization", "averageUtilization": target_memory_utilization},
            },
        })
    if not metrics:
        raise ValueError("At least one HPA metric target is required")

    manifest = {
        "apiVersion": "autoscaling/v2",
        "kind": "HorizontalPodAutoscaler",
        "metadata": {
            "name": hpa_name or f"{workload_name}-hpa",
            "namespace": namespace,
        },
        "spec": {
            "scaleTargetRef": {
                "apiVersion": "apps/v1",
                "kind": _normalize_kind(workload_type),
                "name": workload_name,
            },
            "minReplicas": min_replicas,
            "maxReplicas": max_replicas,
            "metrics": metrics,
        },
    }
    if behavior:
        manifest["spec"]["behavior"] = behavior
    return manifest


def generate_cce_hpa_manifest(
    workload_name: str,
    namespace: str,
    min_replicas: int,
    max_replicas: int,
    workload_type: str = "deployment",
    hpa_name: Optional[str] = None,
    target_cpu_utilization: Optional[int] = 60,
    target_memory_utilization: Optional[int] = None,
    behavior: Any = None,
    output_file: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        manifest = build_hpa_manifest(
            workload_name=workload_name,
            namespace=namespace,
            min_replicas=min_replicas,
            max_replicas=max_replicas,
            workload_type=workload_type,
            hpa_name=hpa_name,
            target_cpu_utilization=target_cpu_utilization,
            target_memory_utilization=target_memory_utilization,
            behavior=_coerce_behavior(behavior),
        )
        manifest_yaml = yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True)
        result = {
            "success": True,
            "action": "generate_cce_hpa_manifest",
            "hpa_name": manifest["metadata"]["name"],
            "namespace": namespace,
            "workload_name": workload_name,
            "workload_type": manifest["spec"]["scaleTargetRef"]["kind"],
            "manifest": manifest,
            "manifest_yaml": manifest_yaml,
        }
        if output_file:
            Path(output_file).write_text(manifest_yaml, encoding="utf-8")
            result["output_file"] = output_file
        return result
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}


def list_cce_hpas(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    namespace: Optional[str] = None,
    include_system: bool = False,
) -> Dict[str, Any]:
    credentials, error = _validate_common(region, cluster_id, ak, sk, project_id)
    if error:
        return error

    cert_file = None
    key_file = None
    try:
        access_key, secret_key, proj_id = credentials
        cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id)
        autoscaling_v2 = k8s_client.AutoscalingV2Api()

        if namespace:
            hpas = autoscaling_v2.list_namespaced_horizontal_pod_autoscaler(namespace)
        else:
            hpas = autoscaling_v2.list_horizontal_pod_autoscaler_for_all_namespaces()

        result = []
        for hpa in hpas.items:
            hpa_namespace = hpa.metadata.namespace
            if not include_system and hpa_namespace in SYSTEM_NAMESPACES:
                continue
            result.append({
                "name": hpa.metadata.name,
                "namespace": hpa_namespace,
                "created": str(hpa.metadata.creation_timestamp) if hpa.metadata.creation_timestamp else None,
                "labels": dict(hpa.metadata.labels) if hpa.metadata.labels else {},
                "annotations": dict(hpa.metadata.annotations) if hpa.metadata.annotations else {},
                "scale_target_ref": _to_plain(hpa.spec.scale_target_ref if hpa.spec else None),
                "min_replicas": hpa.spec.min_replicas if hpa.spec else None,
                "max_replicas": hpa.spec.max_replicas if hpa.spec else None,
                "metrics": _to_plain(hpa.spec.metrics if hpa.spec else None),
                "current_replicas": hpa.status.current_replicas if hpa.status else None,
                "desired_replicas": hpa.status.desired_replicas if hpa.status else None,
                "current_metrics": _to_plain(hpa.status.current_metrics if hpa.status else None),
                "conditions": _to_plain(hpa.status.conditions if hpa.status else None),
            })

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "list_cce_hpas",
            "namespace": namespace or "all-business",
            "include_system": include_system,
            "count": len(result),
            "hpas": result,
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def configure_cce_hpa(
    region: str,
    cluster_id: str,
    workload_name: str,
    namespace: str,
    min_replicas: int,
    max_replicas: int,
    workload_type: str = "deployment",
    hpa_name: Optional[str] = None,
    target_cpu_utilization: Optional[int] = 60,
    target_memory_utilization: Optional[int] = None,
    behavior: Any = None,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    generated = generate_cce_hpa_manifest(
        workload_name=workload_name,
        namespace=namespace,
        min_replicas=min_replicas,
        max_replicas=max_replicas,
        workload_type=workload_type,
        hpa_name=hpa_name,
        target_cpu_utilization=target_cpu_utilization,
        target_memory_utilization=target_memory_utilization,
        behavior=behavior,
    )
    if not generated.get("success"):
        return generated

    manifest = generated["manifest"]
    manifest_yaml = generated["manifest_yaml"]
    effective_hpa_name = manifest["metadata"]["name"]

    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "configure_cce_hpa",
            "warning": "This will create or replace a HorizontalPodAutoscaler. Review the manifest and run again with confirm=true to apply it.",
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace,
            "hpa_name": effective_hpa_name,
            "workload_name": workload_name,
            "manifest": manifest,
            "manifest_yaml": manifest_yaml,
            "hint": "Add confirm=true after explicit user approval.",
        }

    credentials, error = _validate_common(region, cluster_id, ak, sk, project_id)
    if error:
        return error

    cert_file = None
    key_file = None
    try:
        access_key, secret_key, proj_id = credentials
        cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id)
        autoscaling_v2 = k8s_client.AutoscalingV2Api()

        exists = True
        try:
            autoscaling_v2.read_namespaced_horizontal_pod_autoscaler(effective_hpa_name, namespace)
        except Exception as exc:
            if ApiException is not None and isinstance(exc, ApiException) and getattr(exc, "status", None) == 404:
                exists = False
            else:
                raise

        if exists:
            response = autoscaling_v2.replace_namespaced_horizontal_pod_autoscaler(effective_hpa_name, namespace, manifest)
            operation = "replace"
        else:
            response = autoscaling_v2.create_namespaced_horizontal_pod_autoscaler(namespace, manifest)
            operation = "create"

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "configure_cce_hpa",
            "operation": operation,
            "namespace": namespace,
            "hpa_name": effective_hpa_name,
            "workload_name": workload_name,
            "manifest": manifest,
            "response": _to_plain(response),
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
