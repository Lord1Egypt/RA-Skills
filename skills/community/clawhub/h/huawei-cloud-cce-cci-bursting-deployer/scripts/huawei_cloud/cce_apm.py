"""Preview-first APM Java probe injection for CCE workloads."""

from __future__ import annotations

import base64
from typing import Any, Dict, Iterable, Optional

from . import apm, cce_k8s
from .common import K8S_AVAILABLE, K8S_IMPORT_ERROR, _safe_delete_file, get_credentials_with_region, k8s_client


DEFAULT_AGENT_VERSION = "2.5.2"
DEFAULT_VOLUME_NAME = "paas-apm2"
DEFAULT_SECRET_SUFFIX = "apm-credentials"
DEFAULT_MONITOR_GROUP = "default"
SUPPORTED_WORKLOAD_TYPES = {"deployment", "statefulset", "daemonset"}


def _error(message: str, **extra: Any) -> Dict[str, Any]:
    return {"success": False, "error": message, **extra}


def _safe_agent_value(name: str, value: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{name} is required")
    if any(char in text for char in ("\n", "\r", "'", '"')):
        raise ValueError(f"{name} contains unsupported quote or newline characters")
    return text


def _agent_image(region: str, version: str, swr_address: Optional[str]) -> str:
    registry = (swr_address or f"swr.{region}.myhuaweicloud.com").rstrip("/")
    return f"{registry}/op_svc_apm/javaagent:{version}"


def _build_workload_patch(
    cluster_id: str,
    app_name: str,
    business: str,
    env_name: str,
    master_address: str,
    monitor_group: str,
    javaagent_image: str,
    secret_name: str,
    container_names: Iterable[str],
) -> Dict[str, Any]:
    command = (
        "cd /paas-apm2/javaagent/apm-javaagent; "
        "/bin/sh init-config.sh "
        "-master_address \"$APM_MASTER_ADDRESS\" "
        "-app_name \"$APM_APP_NAME\" "
        "-access_key \"$APM_ACCESS_KEY\" "
        "-access_value \"$APM_SECRET_KEY\" "
        "-business \"$APM_BUSINESS\" "
        "-env \"$APM_ENV\""
    )
    target_containers = []
    for name in container_names:
        target_containers.append(
            {
                "name": name,
                "env": [
                    {
                        "name": "JAVA_TOOL_OPTIONS",
                        "value": "-javaagent:/paas-apm2/javaagent/apm-javaagent/apm-javaagent.jar",
                    },
                    {"name": "PAAS_MONITORING_GROUP", "value": monitor_group},
                    {"name": "PAAS_CLUSTER_ID", "value": cluster_id},
                ],
                "volumeMounts": [{"name": DEFAULT_VOLUME_NAME, "mountPath": "/paas-apm2/javaagent/"}],
            }
        )
    return {
        "metadata": {"annotations": {"pressure-test.huawei-cloud/apm-javaagent": "managed"}},
        "spec": {
            "template": {
                "metadata": {"annotations": {"pressure-test.huawei-cloud/apm-javaagent": "managed"}},
                "spec": {
                    "volumes": [{"name": DEFAULT_VOLUME_NAME, "emptyDir": {}}],
                    "initContainers": [
                        {
                            "name": "init-javaagent",
                            "image": javaagent_image,
                            "command": ["/bin/sh", "-c"],
                            "args": [command],
                            "env": [
                                {"name": "APM_MASTER_ADDRESS", "value": master_address},
                                {"name": "APM_APP_NAME", "value": app_name},
                                {"name": "APM_BUSINESS", "value": business},
                                {"name": "APM_ENV", "value": env_name},
                                {
                                    "name": "APM_ACCESS_KEY",
                                    "valueFrom": {
                                        "secretKeyRef": {"name": secret_name, "key": "access-key"}
                                    },
                                },
                                {
                                    "name": "APM_SECRET_KEY",
                                    "valueFrom": {
                                        "secretKeyRef": {"name": secret_name, "key": "secret-key"}
                                    },
                                },
                            ],
                            "resources": {
                                "limits": {"cpu": "250m", "memory": "250Mi"},
                                "requests": {"cpu": "250m", "memory": "250Mi"},
                            },
                            "volumeMounts": [{"name": DEFAULT_VOLUME_NAME, "mountPath": "/var/init/javaagent"}],
                        }
                    ],
                    "containers": target_containers,
                },
            }
        },
    }


def _workload_methods(apps_v1: Any, workload_type: str) -> tuple[Any, Any]:
    methods = {
        "deployment": ("read_namespaced_deployment", "patch_namespaced_deployment"),
        "statefulset": ("read_namespaced_stateful_set", "patch_namespaced_stateful_set"),
        "daemonset": ("read_namespaced_daemon_set", "patch_namespaced_daemon_set"),
    }
    read_name, patch_name = methods[workload_type]
    return getattr(apps_v1, read_name), getattr(apps_v1, patch_name)


def _container_names(workload: Any, container_name: Optional[str]) -> list[str]:
    names = [item.name for item in workload.spec.template.spec.containers or []]
    if container_name:
        if container_name not in names:
            raise ValueError(f"container_name={container_name} was not found in the workload")
        return [container_name]
    if not names:
        raise ValueError("No service containers were found in the workload")
    return names


def _upsert_secret(core_v1: Any, namespace: str, secret_name: str, access_key: str, secret_key: str) -> None:
    body = {
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {"name": secret_name, "namespace": namespace},
        "type": "Opaque",
        "data": {
            "access-key": base64.b64encode(access_key.encode("utf-8")).decode("ascii"),
            "secret-key": base64.b64encode(secret_key.encode("utf-8")).decode("ascii"),
        },
    }
    try:
        core_v1.read_namespaced_secret(secret_name, namespace)
        core_v1.patch_namespaced_secret(secret_name, namespace, body)
    except Exception as exc:
        if getattr(exc, "status", None) != 404:
            raise
        core_v1.create_namespaced_secret(namespace, body)


def inject_cce_apm_javaagent(
    region: str,
    cluster_id: str,
    namespace: str,
    workload_name: str,
    app_name: str,
    business: str,
    env_name: str,
    workload_type: str = "deployment",
    container_name: Optional[str] = None,
    master_address: Optional[str] = None,
    monitor_group: str = DEFAULT_MONITOR_GROUP,
    agent_version: str = DEFAULT_AGENT_VERSION,
    swr_address: Optional[str] = None,
    secret_name: Optional[str] = None,
    apm_access_key: Optional[str] = None,
    apm_secret_key: Optional[str] = None,
    auth_token: Optional[str] = None,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Preview or inject the APM Java agent into a CCE workload."""
    kind = str(workload_type or "").strip().lower()
    if kind not in SUPPORTED_WORKLOAD_TYPES:
        return _error(f"workload_type must be one of: {', '.join(sorted(SUPPORTED_WORKLOAD_TYPES))}")
    try:
        safe_app = _safe_agent_value("app_name", app_name)
        safe_business = _safe_agent_value("business", business)
        safe_env = _safe_agent_value("env_name", env_name)
        safe_group = _safe_agent_value("monitor_group", monitor_group)
        safe_version = _safe_agent_value("agent_version", agent_version)
    except ValueError as exc:
        return _error(str(exc))

    managed_secret = secret_name or f"{workload_name}-{DEFAULT_SECRET_SUFFIX}"
    image = _agent_image(region, safe_version, swr_address)
    placeholder_address = master_address or "<resolve-with-huawei_get_apm_master_address>"
    placeholder_containers = [container_name] if container_name else ["<all-service-containers>"]
    preview_patch = _build_workload_patch(
        cluster_id, safe_app, safe_business, safe_env, placeholder_address, safe_group, image, managed_secret, placeholder_containers
    )
    plan = {
        "operation": "inject_cce_apm_javaagent",
        "region": region,
        "cluster_id": cluster_id,
        "namespace": namespace,
        "workload_type": kind,
        "workload_name": workload_name,
        "container_selection": container_name or "all service containers",
        "master_address_source": "explicit" if master_address else "huawei_get_apm_master_address",
        "secret": {"name": managed_secret, "keys": ["access-key", "secret-key"], "values": "<redacted>"},
        "workload_patch": preview_patch,
        "notes": [
            "This changes the workload pod template and triggers a rollout.",
            "The APM access credentials are stored in a namespace-scoped Kubernetes Secret and are not returned.",
            "Use rollout history or the retained workload manifest to roll back the injection.",
        ],
    }
    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "message": "Preview only. Re-run with confirm=true after explicit approval.",
            "plan": plan,
        }
    if not K8S_AVAILABLE:
        return _error(f"Kubernetes client not installed: {K8S_IMPORT_ERROR}")

    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return _error("Huawei Cloud credentials are required")
    effective_apm_ak = apm_access_key or access_key
    effective_apm_sk = apm_secret_key or secret_key
    effective_master = master_address
    master_resolution = None
    if not effective_master:
        master_resolution = apm.get_apm_master_address(region, auth_token, access_key, secret_key, proj_id)
        if not master_resolution.get("success"):
            return _error(
                "Failed to resolve the APM master address. Pass master_address explicitly or fix APM API access.",
                master_address_resolution=master_resolution,
            )
        effective_master = str(master_resolution["master_address"])

    cert_file = key_file = None
    try:
        _, cert_file, key_file = cce_k8s._setup_k8s_client(
            region, cluster_id, access_key, secret_key, proj_id, "apm_javaagent"
        )
        apps_v1 = k8s_client.AppsV1Api()
        core_v1 = k8s_client.CoreV1Api()
        read_workload, patch_workload = _workload_methods(apps_v1, kind)
        workload = read_workload(workload_name, namespace)
        target_containers = _container_names(workload, container_name)
        patch = _build_workload_patch(
            cluster_id,
            safe_app,
            safe_business,
            safe_env,
            effective_master,
            safe_group,
            image,
            managed_secret,
            target_containers,
        )
        _upsert_secret(core_v1, namespace, managed_secret, effective_apm_ak, effective_apm_sk)
        response = patch_workload(workload_name, namespace, patch)
        return {
            "success": True,
            "action": "inject_cce_apm_javaagent",
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace,
            "workload_type": kind,
            "workload_name": workload_name,
            "target_containers": target_containers,
            "secret": {"name": managed_secret, "keys": ["access-key", "secret-key"], "values": "<redacted>"},
            "master_address": effective_master,
            "master_address_resolution": master_resolution,
            "workload_generation": getattr(getattr(response, "metadata", None), "generation", None),
        }
    except Exception as exc:
        return _error(str(exc), error_type=type(exc).__name__)
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
