"""CCE workload pressure-test orchestration and report helpers."""

from __future__ import annotations

import html
import json
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, Optional

import yaml

from . import aom, cce_diagnosis, cce_k8s, cce_metrics, elb
from .common import (
    K8S_AVAILABLE,
    K8S_IMPORT_ERROR,
    _safe_delete_file,
    get_credentials_with_region,
    k8s_client,
)


DEFAULT_NAMESPACE = "pressure-test"
DEFAULT_K6_IMAGE = "grafana/k6:0.49.0"
DEFAULT_JAVA_NAMESPACE = "pressure-java-lab"
DEFAULT_JAVA_WORKLOAD = "pressure-java-demo"
DEFAULT_JAVA_IMAGE = "eclipse-temurin:17-jdk-alpine"
VALID_MODELS = {"short", "keepalive", "ramp"}
STANDARD_SERIES = (
    "rps",
    "connections",
    "latency_ms",
    "success_rate_percent",
    "cpu_percent",
    "memory_percent",
    "desired_replicas",
    "ready_replicas",
    "running_pods",
)


def _error(message: str, **details: Any) -> Dict[str, Any]:
    return {"success": False, "error": message, **details}


def _resolve_elb_id(region: str, elb_id_or_name: str, ak: Optional[str], sk: Optional[str], project_id: Optional[str]) -> str:
    """Resolve ELB name to UUID if needed."""
    # If already a UUID, return as-is
    if re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", elb_id_or_name, re.I):
        return elb_id_or_name
    
    # Otherwise, list ELBs and find by name
    result = elb.list_elb_loadbalancers(region, ak, sk, project_id)
    if result.get("success") and result.get("loadbalancers"):
        for lb in result["loadbalancers"]:
            if lb.get("name") == elb_id_or_name:
                return lb["id"]
    
    # Fallback: return original if not found
    return elb_id_or_name


def _credentials(
    region: str,
    ak: Optional[str],
    sk: Optional[str],
    project_id: Optional[str],
) -> tuple[Optional[str], Optional[str], Optional[str], Optional[Dict[str, Any]]]:
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return None, None, None, _error(
            "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass them as parameters."
        )
    if not proj_id:
        return None, None, None, _error(
            "Project ID not found. Pass project_id or ensure the account can access the region."
        )
    return access_key, secret_key, proj_id, None


def _safe_name(value: str, suffix: str = "") -> str:
    name = re.sub(r"[^a-z0-9-]+", "-", str(value).lower()).strip("-")
    name = re.sub(r"-+", "-", name)
    if suffix:
        name = f"{name}-{suffix}"
    return (name[:63].rstrip("-") or "pressure-test")


def _json_mapping(value: Optional[str | Dict[str, Any]]) -> Dict[str, Any]:
    if value is None or value == "":
        return {}
    if isinstance(value, dict):
        return value
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("Expected a JSON object.")
    return parsed


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _to_timestamp(value: Any) -> Optional[int]:
    try:
        timestamp = int(float(value))
    except (TypeError, ValueError):
        return None
    return timestamp // 1000 if timestamp > 10_000_000_000 else timestamp


def _route_manifest(
    namespace: str,
    workload_name: str,
    service_name: str,
    ingress_name: str,
    selector: Dict[str, str],
    service_port: int,
    target_port: int,
    ingress_class_name: str,
    host: Optional[str],
    path: str,
    annotations: Dict[str, str],
) -> Dict[str, Any]:
    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": service_name, "namespace": namespace},
        "spec": {
            "type": "ClusterIP",
            "selector": selector,
            "ports": [{"name": "http", "protocol": "TCP", "port": service_port, "targetPort": target_port}],
        },
    }
    rule: Dict[str, Any] = {
        "http": {
            "paths": [
                {
                    "path": path,
                    "pathType": "Prefix",
                    "backend": {"service": {"name": service_name, "port": {"number": service_port}}},
                }
            ]
        }
    }
    if host:
        rule["host"] = host
    ingress = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {"name": ingress_name, "namespace": namespace, "annotations": annotations},
        "spec": {"ingressClassName": ingress_class_name, "rules": [rule]},
    }
    return {
        "namespace": namespace,
        "workload_name": workload_name,
        "service": service,
        "ingress": ingress,
        "network_path": "pod -> service -> nginx-ingress -> elb",
    }


def _java_source() -> str:
    return """import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Executors;

public class PressureDemo {
    private static void respond(HttpExchange exchange, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream output = exchange.getResponseBody()) {
            output.write(bytes);
        }
    }

    private static void work(HttpExchange exchange) throws IOException {
        long sum = 0;
        for (int index = 0; index < 25000; index++) {
            sum += (long) index * index;
        }
        respond(exchange, 200, "{\\"status\\":\\"ok\\",\\"work\\":" + sum + "}");
    }

    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/healthz", exchange -> respond(exchange, 200, "{\\"status\\":\\"up\\"}"));
        server.createContext("/api/hello", exchange -> respond(exchange, 200, "{\\"message\\":\\"hello\\"}"));
        server.createContext("/api/work", PressureDemo::work);
        server.setExecutor(Executors.newFixedThreadPool(16));
        server.start();
        System.out.println("PRESSURE_JAVA_DEMO_READY port=8080");
    }
}
"""


def _java_sample_manifest(
    namespace: str,
    workload_name: str,
    image: str,
    replicas: int,
) -> Dict[str, Any]:
    configmap_name = _safe_name(workload_name, "source")
    labels = {"app": workload_name, "app.kubernetes.io/name": "pressure-java-demo"}
    namespace_resource = {"apiVersion": "v1", "kind": "Namespace", "metadata": {"name": namespace}}
    configmap = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": configmap_name, "namespace": namespace, "labels": labels},
        "data": {"PressureDemo.java": _java_source()},
    }
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": workload_name, "namespace": namespace, "labels": labels},
        "spec": {
            "replicas": int(replicas),
            "selector": {"matchLabels": {"app": workload_name}},
            "template": {
                "metadata": {"labels": labels},
                "spec": {
                    "containers": [
                        {
                            "name": "java-demo",
                            "image": image,
                            "imagePullPolicy": "IfNotPresent",
                            "command": ["sh", "-c"],
                            "args": [
                                "mkdir -p /tmp/app && javac -d /tmp/app /src/PressureDemo.java && exec java -cp /tmp/app PressureDemo"
                            ],
                            "ports": [{"name": "http", "containerPort": 8080}],
                            "resources": {
                                "requests": {"cpu": "100m", "memory": "128Mi"},
                                "limits": {"cpu": "500m", "memory": "512Mi"},
                            },
                            "readinessProbe": {
                                "httpGet": {"path": "/healthz", "port": "http"},
                                "initialDelaySeconds": 3,
                                "periodSeconds": 5,
                            },
                            "livenessProbe": {
                                "httpGet": {"path": "/healthz", "port": "http"},
                                "initialDelaySeconds": 10,
                                "periodSeconds": 10,
                            },
                            "volumeMounts": [{"name": "source", "mountPath": "/src", "readOnly": True}],
                        }
                    ],
                    "volumes": [{"name": "source", "configMap": {"name": configmap_name}}],
                },
            },
        },
    }
    return {
        "namespace": namespace_resource,
        "configmap": configmap,
        "deployment": deployment,
    }


def deploy_cce_pressure_test_java_sample(
    region: str,
    cluster_id: str,
    namespace: str = DEFAULT_JAVA_NAMESPACE,
    workload_name: str = DEFAULT_JAVA_WORKLOAD,
    image: str = DEFAULT_JAVA_IMAGE,
    replicas: int = 2,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create or patch an isolated Java HTTP sample Deployment for pressure tests."""
    if int(replicas) < 1 or int(replicas) > 20:
        return _error("replicas must be between 1 and 20")
    manifest = _java_sample_manifest(namespace, workload_name, image, int(replicas))
    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "deploy_cce_pressure_test_java_sample",
            "warning": "This action creates or patches a Namespace, ConfigMap, and Java sample Deployment. Re-run with confirm=true after explicit user approval.",
            "plan": {
                "manifest": manifest,
                "manifest_yaml": yaml.safe_dump_all(
                    [manifest["namespace"], manifest["configmap"], manifest["deployment"]], sort_keys=False
                ),
            },
        }
    access_key, secret_key, proj_id, error = _credentials(region, ak, sk, project_id)
    if error:
        return error
    if not K8S_AVAILABLE:
        return _error(f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}")

    cert_file = None
    key_file = None
    try:
        _, cert_file, key_file = cce_k8s._setup_k8s_client(
            region, cluster_id, access_key, secret_key, proj_id, "pressure_java"
        )
        core_v1 = k8s_client.CoreV1Api()
        apps_v1 = k8s_client.AppsV1Api()
        try:
            core_v1.read_namespace(namespace)
            namespace_action = "existing"
        except Exception as exc:
            if not _is_not_found(exc):
                raise
            core_v1.create_namespace(manifest["namespace"])
            namespace_action = "created"
        configmap_name = manifest["configmap"]["metadata"]["name"]
        try:
            core_v1.read_namespaced_config_map(configmap_name, namespace)
            core_v1.patch_namespaced_config_map(configmap_name, namespace, manifest["configmap"])
            configmap_action = "patched"
        except Exception as exc:
            if not _is_not_found(exc):
                raise
            core_v1.create_namespaced_config_map(namespace, manifest["configmap"])
            configmap_action = "created"
        try:
            apps_v1.read_namespaced_deployment(workload_name, namespace)
            response = apps_v1.patch_namespaced_deployment(workload_name, namespace, manifest["deployment"])
            deployment_action = "patched"
        except Exception as exc:
            if not _is_not_found(exc):
                raise
            response = apps_v1.create_namespaced_deployment(namespace, manifest["deployment"])
            deployment_action = "created"
        return {
            "success": True,
            "action": "deploy_cce_pressure_test_java_sample",
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace,
            "workload_name": workload_name,
            "image": image,
            "replicas": int(replicas),
            "namespace_action": namespace_action,
            "configmap_action": configmap_action,
            "deployment_action": deployment_action,
            "deployment_uid": getattr(response.metadata, "uid", None),
            "selector": {"app": workload_name},
            "container_port": 8080,
            "endpoints": ["/healthz", "/api/hello", "/api/work"],
            "next_action": "Wait for ready replicas, then preview huawei_prepare_cce_pressure_test_route with target_port=8080.",
        }
    except Exception as exc:
        return _error(str(exc), action="deploy_cce_pressure_test_java_sample", error_type=type(exc).__name__)
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def _is_not_found(exc: Exception) -> bool:
    return getattr(exc, "status", None) == 404


def _controller_endpoint(core_v1: Any) -> Dict[str, Any]:
    candidates = []
    services = core_v1.list_service_for_all_namespaces()
    for service in services.items:
        name = service.metadata.name
        namespace = service.metadata.namespace
        if service.spec.type != "LoadBalancer":
            continue
        searchable = f"{namespace}/{name}".lower()
        if "ingress" not in searchable and "nginx" not in searchable:
            continue
        addresses = []
        load_balancer = getattr(service.status, "load_balancer", None)
        for item in getattr(load_balancer, "ingress", None) or []:
            addresses.append(getattr(item, "ip", None) or getattr(item, "hostname", None))
        labels = dict(getattr(service.metadata, "labels", None) or {})
        ports = [getattr(item, "port", None) for item in service.spec.ports or []]
        score = 0
        if labels.get("component") == "controller":
            score += 100
        if "ingress" in name.lower():
            score += 30
        if "controller" in name.lower():
            score += 20
        if "ingress" in namespace.lower():
            score += 10
        if 80 in ports:
            score += 5
        candidates.append(
            {
                "namespace": namespace,
                "service_name": name,
                "addresses": [item for item in addresses if item],
                "ports": ports,
                "labels": labels,
                "controller_score": score,
            }
        )
    selected = next(
        (item for item in sorted(candidates, key=lambda item: item["controller_score"], reverse=True) if item["addresses"]),
        None,
    )
    return {
        "ready": bool(selected),
        "selected": selected,
        "candidates": candidates,
        "data_gap": None if selected else "No nginx ingress controller LoadBalancer address was discovered.",
    }


def prepare_cce_pressure_test_route(
    region: str,
    cluster_id: str,
    namespace: str,
    workload_name: str,
    service_port: int = 80,
    target_port: int = 8080,
    service_name: Optional[str] = None,
    ingress_name: Optional[str] = None,
    ingress_class_name: str = "nginx",
    host: Optional[str] = None,
    path: str = "/",
    selector: Optional[str | Dict[str, str]] = None,
    annotations: Optional[str | Dict[str, str]] = None,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create or patch a ClusterIP Service and nginx Ingress for a Deployment."""
    try:
        explicit_selector = _json_mapping(selector)
        ingress_annotations = _json_mapping(annotations)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        return _error(str(exc))
    effective_service = service_name or _safe_name(workload_name, "pressure")
    effective_ingress = ingress_name or _safe_name(workload_name, "pressure")
    preview_selector = explicit_selector or {"app": workload_name}
    preview = _route_manifest(
        namespace,
        workload_name,
        effective_service,
        effective_ingress,
        preview_selector,
        int(service_port),
        int(target_port),
        ingress_class_name,
        host,
        path,
        {str(key): str(value) for key, value in ingress_annotations.items()},
    )
    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "prepare_cce_pressure_test_route",
            "warning": "This action creates or patches a Kubernetes Service and Ingress. Re-run with confirm=true after explicit user approval.",
            "plan": preview,
        }
    access_key, secret_key, proj_id, error = _credentials(region, ak, sk, project_id)
    if error:
        return error
    if not K8S_AVAILABLE:
        return _error(f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}")

    cert_file = None
    key_file = None
    try:
        _, cert_file, key_file = cce_k8s._setup_k8s_client(
            region, cluster_id, access_key, secret_key, proj_id, "pressure_route"
        )
        core_v1 = k8s_client.CoreV1Api()
        apps_v1 = k8s_client.AppsV1Api()
        networking_v1 = k8s_client.NetworkingV1Api()
        if explicit_selector:
            effective_selector = explicit_selector
        else:
            deployment = apps_v1.read_namespaced_deployment(workload_name, namespace)
            match_labels = getattr(deployment.spec.selector, "match_labels", None) or {}
            effective_selector = dict(match_labels)
        if not effective_selector:
            return _error("Deployment selector.matchLabels is empty. Pass selector as a JSON object.")
        manifest = _route_manifest(
            namespace,
            workload_name,
            effective_service,
            effective_ingress,
            effective_selector,
            int(service_port),
            int(target_port),
            ingress_class_name,
            host,
            path,
            {str(key): str(value) for key, value in ingress_annotations.items()},
        )
        try:
            core_v1.read_namespaced_service(effective_service, namespace)
            core_v1.patch_namespaced_service(effective_service, namespace, manifest["service"])
            service_action = "patched"
        except Exception as exc:
            if not _is_not_found(exc):
                raise
            core_v1.create_namespaced_service(namespace, manifest["service"])
            service_action = "created"
        try:
            networking_v1.read_namespaced_ingress(effective_ingress, namespace)
            networking_v1.patch_namespaced_ingress(effective_ingress, namespace, manifest["ingress"])
            ingress_action = "patched"
        except Exception as exc:
            if not _is_not_found(exc):
                raise
            networking_v1.create_namespaced_ingress(namespace, manifest["ingress"])
            ingress_action = "created"
        controller = _controller_endpoint(core_v1)
        selected = controller.get("selected") or {}
        address = next(iter(selected.get("addresses") or []), None)
        return {
            "success": True,
            "action": "prepare_cce_pressure_test_route",
            "region": region,
            "cluster_id": cluster_id,
            "service_action": service_action,
            "ingress_action": ingress_action,
            "route": manifest,
            "ingress_controller": controller,
            "suggested_target_url": f"http://{address}{path}" if address else None,
            "host_header": host,
        }
    except Exception as exc:
        return _error(str(exc), action="prepare_cce_pressure_test_route", error_type=type(exc).__name__)
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def _k6_script(
    target_url: str,
    model: str,
    vus: int,
    duration_seconds: int,
    host_header: Optional[str],
    sleep_seconds: float,
) -> str:
    if model not in VALID_MODELS:
        raise ValueError(f"model must be one of: {', '.join(sorted(VALID_MODELS))}")
    options: Dict[str, Any]
    if model == "ramp":
        stage = max(1, duration_seconds // 3)
        options = {
            "stages": [
                {"duration": f"{stage}s", "target": max(1, vus // 3)},
                {"duration": f"{stage}s", "target": vus},
                {"duration": f"{max(1, duration_seconds - stage * 2)}s", "target": 0},
            ]
        }
    else:
        options = {"vus": vus, "duration": f"{duration_seconds}s"}
    if model == "short":
        options["noConnectionReuse"] = True
        options["noVUConnectionReuse"] = True
    headers = {"Connection": "close"} if model == "short" else {}
    if host_header:
        headers["Host"] = host_header
    return f"""import http from 'k6/http';
import {{ check, sleep }} from 'k6';

export const options = {json.dumps(options, ensure_ascii=True)};
const target = {json.dumps(target_url)};
const params = {{ headers: {json.dumps(headers, ensure_ascii=True)} }};

export default function () {{
  const response = http.get(target, params);
  check(response, {{ 'status is below 400': (res) => res.status < 400 }});
  sleep({float(sleep_seconds)});
}}

function metric(data, name, field) {{
  return data.metrics[name] && data.metrics[name].values ? data.metrics[name].values[field] : null;
}}

export function handleSummary(data) {{
  const failureRate = metric(data, 'http_req_failed', 'rate') || 0;
  const summary = {{
    request_count: metric(data, 'http_reqs', 'count'),
    rps: metric(data, 'http_reqs', 'rate'),
    failure_rate: failureRate,
    success_rate: 1 - failureRate,
    check_rate: metric(data, 'checks', 'rate'),
    latency_avg_ms: metric(data, 'http_req_duration', 'avg'),
    latency_p90_ms: metric(data, 'http_req_duration', 'p(90)'),
    latency_p95_ms: metric(data, 'http_req_duration', 'p(95)'),
    latency_p99_ms: metric(data, 'http_req_duration', 'p(99)'),
    latency_max_ms: metric(data, 'http_req_duration', 'max'),
    bytes_received: metric(data, 'data_received', 'count'),
    bytes_sent: metric(data, 'data_sent', 'count'),
    vus_max: metric(data, 'vus_max', 'max')
  }};
  return {{ stdout: `PRESSURE_TEST_RESULT ${{JSON.stringify(summary)}}\\n` }};
}}
"""


def generate_cce_pressure_test_client(
    target_url: str,
    namespace: str = DEFAULT_NAMESPACE,
    test_name: Optional[str] = None,
    model: str = "keepalive",
    vus: int = 10,
    duration_seconds: int = 60,
    image: str = DEFAULT_K6_IMAGE,
    host_header: Optional[str] = None,
    sleep_seconds: float = 0.1,
) -> Dict[str, Any]:
    """Generate a k6 ConfigMap and Job manifest without mutating the cluster."""
    if not target_url.startswith(("http://", "https://")):
        return _error("target_url must start with http:// or https://")
    if model not in VALID_MODELS:
        return _error(f"model must be one of: {', '.join(sorted(VALID_MODELS))}")
    if int(vus) < 1 or int(vus) > 10_000:
        return _error("vus must be between 1 and 10000")
    if int(duration_seconds) < 1 or int(duration_seconds) > 86_400:
        return _error("duration_seconds must be between 1 and 86400")
    effective_name = _safe_name(test_name or f"pressure-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}")
    configmap_name = _safe_name(effective_name, "script")
    labels = {"app.kubernetes.io/name": "pressure-test", "pressure-test/run": effective_name}
    script = _k6_script(target_url, model, int(vus), int(duration_seconds), host_header, float(sleep_seconds))
    namespace_resource = {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {"name": namespace},
    }
    configmap = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {"name": configmap_name, "namespace": namespace, "labels": labels},
        "data": {"test.js": script},
    }
    job = {
        "apiVersion": "batch/v1",
        "kind": "Job",
        "metadata": {"name": effective_name, "namespace": namespace, "labels": labels},
        "spec": {
            "backoffLimit": 0,
            "template": {
                "metadata": {"labels": labels},
                "spec": {
                    "restartPolicy": "Never",
                    "containers": [
                        {
                            "name": "k6",
                            "image": image,
                            "args": ["run", "--out", "json", "/scripts/test.js"],
                            "volumeMounts": [
                                {"name": "scripts", "mountPath": "/scripts", "readOnly": True},
                            ],
                        }
                    ],
                    "volumes": [
                        {"name": "scripts", "configMap": {"name": configmap_name}},
                    ],
                },
            },
        },
    }
    return {
        "success": True,
        "action": "generate_cce_pressure_test_client",
        "namespace": namespace,
        "test_name": effective_name,
        "model": model,
        "vus": int(vus),
        "duration_seconds": int(duration_seconds),
        "target_url": target_url,
        "host_header": host_header,
        "image": image,
        "manifest": {"namespace": namespace_resource, "configmap": configmap, "job": job},
        "manifest_yaml": yaml.safe_dump_all([namespace_resource, configmap, job], sort_keys=False),
        "image_note": "Mirror the k6 image to a regional SWR repository when the cluster cannot pull public images.",
    }


def _workload_sample(apps_v1: Any, core_v1: Any, namespace: str, workload_name: Optional[str]) -> Dict[str, Any]:
    if not workload_name:
        return {}
    try:
        deployment = apps_v1.read_namespaced_deployment(workload_name, namespace)
        match_labels = getattr(deployment.spec.selector, "match_labels", None) or {}
        label_selector = ",".join(f"{key}={value}" for key, value in sorted(match_labels.items()))
        pods = core_v1.list_namespaced_pod(namespace, label_selector=label_selector)
        running = sum(1 for item in pods.items if getattr(item.status, "phase", None) == "Running")
        return {
            "desired_replicas": getattr(deployment.spec, "replicas", None),
            "ready_replicas": getattr(deployment.status, "ready_replicas", None) or 0,
            "running_pods": running,
            "pod_count": len(pods.items),
        }
    except Exception as exc:
        return {"workload_sample_error": str(exc)}


def _job_sample(status: Any, started_at: float, workload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "timestamp": int(time.time()),
        "time_utc": _utc_now(),
        "elapsed_seconds": round(time.time() - started_at, 2),
        "job_active": getattr(status, "active", None) or 0,
        "job_succeeded": getattr(status, "succeeded", None) or 0,
        "job_failed": getattr(status, "failed", None) or 0,
        **workload,
    }


def _extract_k6_summary(log_text: str) -> Optional[Dict[str, Any]]:
    matches = re.findall(r"PRESSURE_TEST_RESULT\s+(\{.*\})", log_text or "")
    if not matches:
        return None
    try:
        result = json.loads(matches[-1])
    except json.JSONDecodeError:
        return None
    return result if isinstance(result, dict) else None


def _parse_k6_json_metrics(metrics_text: str) -> Dict[str, list[Dict[str, Any]]]:
    """Parse k6 JSON metrics output and extract time-series data.
    
    k6 --out json produces one JSON object per line, each representing a metric sample.
    We aggregate http_reqs (count), http_req_duration (value), and http_req_failed (value)
    by timestamp bucket (per second).
    """
    import collections
    
    if not metrics_text:
        return {}
    
    # Buckets: timestamp -> metric name -> list of values
    buckets: Dict[int, Dict[str, list[float]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    
    for line in metrics_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            sample = json.loads(line)
        except json.JSONDecodeError:
            continue
        
        metric_type = sample.get("type")
        metric_name = sample.get("metric")
        data = sample.get("data", {})
        timestamp_str = data.get("time")
        value = data.get("value")
        
        if not timestamp_str or value is None:
            continue
        
        # Parse ISO 8601 timestamp (e.g., "2026-05-31T08:57:09.930384093Z")
        try:
            ts_str = timestamp_str.replace("Z", "+00:00")
            dt = datetime.fromisoformat(ts_str)
            bucket_ts = int(dt.timestamp())
        except Exception:
            continue
        
        if metric_name == "http_reqs":
            buckets[bucket_ts]["http_reqs"].append(float(value))
        elif metric_name == "http_req_duration":
            buckets[bucket_ts]["http_req_duration"].append(float(value))
        elif metric_name == "http_req_failed":
            buckets[bucket_ts]["http_req_failed"].append(float(value))
    
    if not buckets:
        return {}
    
    # Sort timestamps
    sorted_ts = sorted(buckets.keys())
    
    result: Dict[str, list[Dict[str, Any]]] = {}
    
    # RPS = sum of http_reqs per second
    rps_points = []
    for ts in sorted_ts:
        req_count = len(buckets[ts].get("http_reqs", []))
        if req_count > 0:
            rps_points.append({"timestamp": ts, "value": float(req_count)})
    if rps_points:
        result["rps"] = rps_points
    
    # Latency = average of http_req_duration per second
    latency_points = []
    for ts in sorted_ts:
        latencies = buckets[ts].get("http_req_duration", [])
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            latency_points.append({"timestamp": ts, "value": round(avg_latency, 2)})
    if latency_points:
        result["latency_ms"] = latency_points
    
    # Success rate = (1 - failed_rate) * 100
    success_points = []
    for ts in sorted_ts:
        failed = buckets[ts].get("http_req_failed", [])
        reqs = buckets[ts].get("http_reqs", [])
        if reqs:
            failed_rate = sum(failed) / len(reqs) if failed else 0
            success_rate = (1 - failed_rate) * 100
            success_points.append({"timestamp": ts, "value": round(success_rate, 2)})
    if success_points:
        result["success_rate_percent"] = success_points
    
    return result


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_cce_pressure_test(
    region: str,
    cluster_id: str,
    target_url: str,
    namespace: str = DEFAULT_NAMESPACE,
    workload_name: Optional[str] = None,
    workload_namespace: Optional[str] = None,
    test_name: Optional[str] = None,
    model: str = "keepalive",
    vus: int = 10,
    duration_seconds: int = 60,
    image: str = DEFAULT_K6_IMAGE,
    host_header: Optional[str] = None,
    sleep_seconds: float = 0.1,
    sample_interval_seconds: int = 5,
    timeout_seconds: Optional[int] = None,
    wait: bool = True,
    output_dir: Optional[str] = None,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a k6 Job, optionally wait for it, and record workload replica samples."""
    generated = generate_cce_pressure_test_client(
        target_url, namespace, test_name, model, vus, duration_seconds, image, host_header, sleep_seconds
    )
    if not generated.get("success"):
        return generated
    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "run_cce_pressure_test",
            "warning": "This action creates a ConfigMap and a Job that sends traffic. Re-run with confirm=true after explicit user approval.",
            "plan": generated,
        }
    access_key, secret_key, proj_id, error = _credentials(region, ak, sk, project_id)
    if error:
        return error
    if not K8S_AVAILABLE:
        return _error(f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}")

    cert_file = None
    key_file = None
    try:
        _, cert_file, key_file = cce_k8s._setup_k8s_client(
            region, cluster_id, access_key, secret_key, proj_id, "pressure_run"
        )
        core_v1 = k8s_client.CoreV1Api()
        apps_v1 = k8s_client.AppsV1Api()
        batch_v1 = k8s_client.BatchV1Api()
        namespace_resource = generated["manifest"]["namespace"]
        configmap = generated["manifest"]["configmap"]
        job = generated["manifest"]["job"]
        test_name = generated["test_name"]
        try:
            batch_v1.read_namespaced_job(test_name, namespace)
            return _error(f"Job {namespace}/{test_name} already exists. Use a new test_name.")
        except Exception as exc:
            if not _is_not_found(exc):
                raise
        try:
            core_v1.read_namespace(namespace)
            namespace_action = "existing"
        except Exception as exc:
            if not _is_not_found(exc):
                raise
            core_v1.create_namespace(namespace_resource)
            namespace_action = "created"
        try:
            core_v1.read_namespaced_config_map(configmap["metadata"]["name"], namespace)
            core_v1.patch_namespaced_config_map(configmap["metadata"]["name"], namespace, configmap)
            configmap_action = "patched"
        except Exception as exc:
            if not _is_not_found(exc):
                raise
            core_v1.create_namespaced_config_map(namespace, configmap)
            configmap_action = "created"
        batch_v1.create_namespaced_job(namespace, job)

        started_at = time.time()
        deadline = started_at + int(timeout_seconds or (int(duration_seconds) + 120))
        interval = max(1, int(sample_interval_seconds))
        samples = []
        status = batch_v1.read_namespaced_job_status(test_name, namespace).status
        effective_workload_ns = workload_namespace or namespace
        while True:
            samples.append(_job_sample(status, started_at, _workload_sample(apps_v1, core_v1, effective_workload_ns, workload_name)))
            if getattr(status, "succeeded", None) or getattr(status, "failed", None) or not wait:
                break
            if time.time() >= deadline:
                break
            time.sleep(interval)
            status = batch_v1.read_namespaced_job_status(test_name, namespace).status

        log_text = ""
        pods = core_v1.list_namespaced_pod(namespace, label_selector=f"job-name={test_name}")
        if pods.items:
            pod_name = pods.items[0].metadata.name
            try:
                # Read full k6 JSON output. k6 --out json produces ~80k lines for a 60s test (~20MB).
                # The Kubernetes Python client may return literal \n instead of actual newlines.
                log_text = core_v1.read_namespaced_pod_log(pod_name, namespace)
                if '\\n' in log_text and '\n' not in log_text:
                    log_text = log_text.replace('\\n', '\n')
            except Exception:
                log_text = ""
        
        # Parse k6 time-series metrics from log (k6 --out json outputs JSON lines to stdout)
        k6_time_series = _parse_k6_json_metrics(log_text)
        
        succeeded = bool(getattr(status, "succeeded", None))
        timed_out = wait and not succeeded and not getattr(status, "failed", None) and time.time() >= deadline
        
        # Merge k6 time-series into metric_series
        metric_series = _series_from_samples(samples)
        metric_series.update(k6_time_series)
        
        result = {
            "success": succeeded if wait else True,
            "action": "run_cce_pressure_test",
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace,
            "workload_name": workload_name,
            "test_name": test_name,
            "model": model,
            "target_url": target_url,
            "host_header": host_header,
            "vus": int(vus),
            "duration_seconds": int(duration_seconds),
            "namespace_action": namespace_action,
            "configmap_action": configmap_action,
            "job": {
                "created": True,
                "waited": wait,
                "succeeded": succeeded,
                "failed": bool(getattr(status, "failed", None)),
                "timed_out": timed_out,
            },
            "samples": samples,
            "metric_series": metric_series,
            "k6_summary": _extract_k6_summary(log_text),
            "log_tail": log_text[-4000:],
            "data_gaps": [] if log_text else ["k6 Job log was not available yet. Re-run report generation after the Job completes."],
        }
        if output_dir:
            output_path = Path(output_dir)
            raw_path = output_path / f"{test_name}.json"
            _write_json(raw_path, result)
            report = generate_cce_pressure_test_report(str(raw_path), output_dir=str(output_path))
            result["files"] = {"raw_json": str(raw_path), **report.get("files", {})}
            _write_json(raw_path, result)
        return result
    except Exception as exc:
        return _error(str(exc), action="run_cce_pressure_test", error_type=type(exc).__name__)
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def _point(timestamp: Any, value: Any) -> Optional[Dict[str, Any]]:
    normalized_timestamp = _to_timestamp(timestamp)
    try:
        normalized_value = float(value)
    except (TypeError, ValueError):
        return None
    if normalized_timestamp is None or not math.isfinite(normalized_value):
        return None
    return {"timestamp": normalized_timestamp, "value": round(normalized_value, 4)}


def _average_points(series: Iterable[Iterable[Dict[str, Any]]]) -> list[Dict[str, Any]]:
    buckets: Dict[int, list[float]] = {}
    for metric_series in series:
        for item in metric_series:
            point = _point(item.get("timestamp"), item.get("value"))
            if point:
                buckets.setdefault(point["timestamp"], []).append(point["value"])
    return [
        {"timestamp": timestamp, "value": round(mean(values), 4)}
        for timestamp, values in sorted(buckets.items())
        if values
    ]


def _series_from_prom(result: Dict[str, Any]) -> list[Dict[str, Any]]:
    series = []
    for item in result.get("result", {}).get("data", {}).get("result", []) or []:
        values = item.get("values") or ([item.get("value")] if item.get("value") else [])
        points = []
        for value in values:
            if not isinstance(value, (list, tuple)) or len(value) < 2:
                continue
            point = _point(value[0], value[1])
            if point:
                points.append(point)
        series.append(points)
    return _average_points(series)


def _series_from_pod_metrics(result: Dict[str, Any], key: str) -> list[Dict[str, Any]]:
    all_series = []
    for metric in result.get("metrics", {}).get(key, []) or []:
        points = []
        for value in metric.get("time_series", []) or []:
            if not isinstance(value, (list, tuple)) or len(value) < 2:
                continue
            point = _point(value[0], value[1])
            if point:
                points.append(point)
        all_series.append(points)
    return _average_points(all_series)


def _series_from_elb(result: Dict[str, Any], metric_name: str) -> list[Dict[str, Any]]:
    points = []
    for item in result.get("metrics", {}).get(metric_name, {}).get("time_series", []) or []:
        point = _point(item.get("timestamp"), item.get("average"))
        if point:
            points.append(point)
    return points


def _series_from_samples(samples: list[Dict[str, Any]]) -> Dict[str, list[Dict[str, Any]]]:
    result: Dict[str, list[Dict[str, Any]]] = {}
    for key in ("desired_replicas", "ready_replicas", "running_pods"):
        points = []
        for sample in samples:
            point = _point(sample.get("timestamp"), sample.get(key))
            if point:
                points.append(point)
        if points:
            result[key] = points
    return result


def collect_cce_pressure_test_observability(
    region: str,
    cluster_id: str,
    namespace: str,
    workload_name: str,
    label_selector: Optional[str] = None,
    elb_id: Optional[str] = None,
    aom_instance_id: Optional[str] = None,
    queries: Optional[str | Dict[str, str]] = None,
    hours: int = 1,
    period: int = 300,
    output_dir: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Collect workload, AOM, and optional ELB evidence for a pressure-test report."""
    try:
        custom_queries = _json_mapping(queries)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        return _error(str(exc))
    effective_label_selector = label_selector or f"app={workload_name}"
    pods = cce_k8s.get_cce_pods(region, cluster_id, ak, sk, project_id, namespace, effective_label_selector)
    services = cce_k8s.get_cce_services(region, cluster_id, ak, sk, project_id, namespace)
    ingresses = cce_k8s.get_cce_ingresses(region, cluster_id, ak, sk, project_id, namespace)
    pod_metrics = cce_metrics.get_cce_pod_metrics_topN(
        region, cluster_id, ak, sk, project_id, namespace, effective_label_selector, 100, int(hours)
    )
    effective_elb_id = _resolve_elb_id(region, elb_id, ak, sk, project_id) if elb_id else None
    elb_metrics = elb.get_elb_metrics(region, effective_elb_id, int(hours), int(period), ak, sk, project_id) if effective_elb_id else None
    backend_status = elb.get_elb_backend_status(region, effective_elb_id, ak, sk, project_id) if effective_elb_id else None
    aom_instance_resolution = None
    effective_aom_instance_id = aom_instance_id
    if not effective_aom_instance_id:
        aom_instance_resolution = cce_diagnosis.get_aom_instance(region, cluster_id, ak, sk, project_id)
        if aom_instance_resolution.get("success"):
            effective_aom_instance_id = aom_instance_resolution.get("aom_instance_id")
    custom_metrics: Dict[str, Any] = {}
    if custom_queries and not effective_aom_instance_id:
        return _error(
            "Unable to resolve aom_instance_id for the requested custom queries.",
            aom_instance_resolution=aom_instance_resolution,
        )
    for name, query in custom_queries.items():
        custom_metrics[str(name)] = aom.get_aom_prom_metrics_http(
            region, str(effective_aom_instance_id), str(query), hours=int(hours), ak=ak, sk=sk, project_id=project_id
        )
    metric_series: Dict[str, list[Dict[str, Any]]] = {}
    cpu = _series_from_pod_metrics(pod_metrics, "cpu_top_n")
    memory = _series_from_pod_metrics(pod_metrics, "memory_top_n")
    if cpu:
        metric_series["cpu_percent"] = cpu
    if memory:
        metric_series["memory_percent"] = memory
    if elb_metrics:
        for name, metric_name in (
            ("rps", "mb_l7_qps"),
            ("connections", "m2_act_conn"),
            ("latency_ms", "m14_l7_rt"),
            ("success_rate_percent", "l7_2xx_ratio"),
        ):
            points = _series_from_elb(elb_metrics, metric_name)
            if points:
                metric_series[name] = points
    for name, response in custom_metrics.items():
        points = _series_from_prom(response)
        if points:
            metric_series[name] = points
    data_gaps = []
    if not elb_id:
        data_gaps.append("elb_id was not provided, so ELB traffic, connection, latency, and success-rate curves were not collected.")
    if not effective_aom_instance_id:
        reason = (aom_instance_resolution or {}).get("error", "not provided")
        data_gaps.append(f"aom_instance_id could not be resolved, so custom AOM PromQL curves were not collected: {reason}")
    if not pod_metrics.get("success"):
        data_gaps.append(f"Pod metrics collection failed: {pod_metrics.get('error', 'unknown error')}")
    result = {
        "success": True,
        "action": "collect_cce_pressure_test_observability",
        "region": region,
        "cluster_id": cluster_id,
        "namespace": namespace,
        "workload_name": workload_name,
        "label_selector": effective_label_selector,
        "hours": int(hours),
        "inventory": {"pods": pods, "services": services, "ingresses": ingresses},
        "pod_metrics": pod_metrics,
        "aom_instance_id": effective_aom_instance_id,
        "aom_instance_resolution": aom_instance_resolution,
        "elb_metrics": elb_metrics,
        "elb_backend_status": backend_status,
        "custom_aom_metrics": custom_metrics,
        "metric_series": metric_series,
        "data_gaps": data_gaps,
    }
    if output_dir:
        output_path = Path(output_dir) / f"{_safe_name(workload_name)}-observability.json"
        _write_json(output_path, result)
        result["files"] = {"observability_json": str(output_path)}
    return result


def _merge_series(*items: Dict[str, Any]) -> Dict[str, list[Dict[str, Any]]]:
    merged: Dict[str, list[Dict[str, Any]]] = {}
    for payload in items:
        for name, values in (payload.get("metric_series") or {}).items():
            if isinstance(values, list) and values:
                merged[str(name)] = values
    return merged


def _series_stats(values: list[Dict[str, Any]]) -> Dict[str, Any]:
    numbers = [float(item["value"]) for item in values if item.get("value") is not None]
    if not numbers:
        return {"samples": 0}
    return {"samples": len(numbers), "avg": round(mean(numbers), 2), "max": round(max(numbers), 2), "min": round(min(numbers), 2)}


def _recommendations(payload: Dict[str, Any], series: Dict[str, list[Dict[str, Any]]]) -> list[Dict[str, str]]:
    summary = payload.get("k6_summary") or {}
    recommendations = []
    failure_rate = summary.get("failure_rate")
    if failure_rate is not None and float(failure_rate) > 0.01:
        recommendations.append({"risk": "high", "area": "success rate", "recommendation": "Investigate application errors, ingress responses, and ELB backend health before raising traffic."})
    p95 = summary.get("latency_p95_ms")
    if p95 is not None and float(p95) > 500:
        recommendations.append({"risk": "medium", "area": "latency", "recommendation": "Review p95 latency together with CPU, memory, connection, and replica curves. Tune HPA only after identifying the limiting resource."})
    desired = series.get("desired_replicas", [])
    ready = series.get("ready_replicas", [])
    if desired and ready and max(item["value"] for item in desired) > min(item["value"] for item in ready):
        recommendations.append({"risk": "medium", "area": "elasticity", "recommendation": "Ready replicas lagged desired replicas. Review image pull time, readiness probes, HPA behavior, and node autoscaler headroom."})
    cpu = _series_stats(series.get("cpu_percent", []))
    memory = _series_stats(series.get("memory_percent", []))
    if cpu.get("max", 0) > 80 or memory.get("max", 0) > 80:
        recommendations.append({"risk": "medium", "area": "resource waterline", "recommendation": "Peak resource utilization exceeded 80%. Keep more headroom or scale earlier before increasing traffic."})
    if not recommendations:
        recommendations.append({"risk": "low", "area": "baseline", "recommendation": "No immediate risk was detected from the available samples. Run stepped traffic phases and compare scaling changes before production tuning."})
    return recommendations


def _correlation(left: list[Dict[str, Any]], right: list[Dict[str, Any]]) -> tuple[int, Optional[float]]:
    left_by_time = {int(item["timestamp"]): float(item["value"]) for item in left}
    right_by_time = {int(item["timestamp"]): float(item["value"]) for item in right}
    aligned = [(left_by_time[key], right_by_time[key]) for key in sorted(set(left_by_time) & set(right_by_time))]
    if len(aligned) < 2:
        return len(aligned), None
    left_values = [item[0] for item in aligned]
    right_values = [item[1] for item in aligned]
    left_avg = mean(left_values)
    right_avg = mean(right_values)
    numerator = sum((left - left_avg) * (right - right_avg) for left, right in aligned)
    denominator = math.sqrt(
        sum((left - left_avg) ** 2 for left in left_values)
        * sum((right - right_avg) ** 2 for right in right_values)
    )
    if denominator == 0:
        return len(aligned), None
    return len(aligned), round(numerator / denominator, 3)


def _relationship_rows(series: Dict[str, list[Dict[str, Any]]]) -> list[list[Any]]:
    rows = []
    rps = series.get("rps", [])
    for name in ("connections", "latency_ms", "cpu_percent", "memory_percent", "ready_replicas"):
        sample_count, correlation = _correlation(rps, series.get(name, []))
        if correlation is None:
            interpretation = "Not enough aligned samples"
        elif correlation >= 0.6:
            interpretation = "Strong positive relationship with RPS"
        elif correlation <= -0.6:
            interpretation = "Strong negative relationship with RPS"
        else:
            interpretation = "Weak or mixed relationship with RPS"
        rows.append([name, sample_count, "-" if correlation is None else correlation, interpretation])
    return rows


def _svg_chart(series: Dict[str, list[Dict[str, Any]]], path: Path) -> None:
    groups = [
        ("Traffic and connections", ("rps", "connections")),
        ("Latency and success", ("latency_ms", "success_rate_percent")),
        ("Pod resources", ("cpu_percent", "memory_percent")),
        ("Elasticity", ("desired_replicas", "ready_replicas", "running_pods")),
    ]
    colors = {
        "rps": "#1677ff",
        "connections": "#722ed1",
        "latency_ms": "#fa8c16",
        "success_rate_percent": "#389e0d",
        "cpu_percent": "#d4380d",
        "memory_percent": "#13a8a8",
        "desired_replicas": "#531dab",
        "ready_replicas": "#389e0d",
        "running_pods": "#096dd9",
    }
    width, panel_height, margin = 1120, 205, 54
    height = panel_height * len(groups) + 30
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:Arial,sans-serif;font-size:12px;fill:#334155}.title{font-size:15px;font-weight:700}.legend{font-size:11px}</style>',
    ]
    for index, (title, names) in enumerate(groups):
        top = index * panel_height + 22
        left, right = margin, width - 28
        chart_top, chart_bottom = top + 30, top + 168
        parts.append(f'<text class="title" x="{left}" y="{top}">{html.escape(title)}</text>')
        visible = [(name, series.get(name, [])) for name in names if series.get(name)]
        if not visible:
            parts.append(f'<text x="{left}" y="{chart_top + 50}" fill="#94a3b8">No time-series samples</text>')
            continue
        timestamps = sorted({int(item["timestamp"]) for _, values in visible for item in values})
        min_ts, max_ts = min(timestamps), max(timestamps)
        if max_ts == min_ts:
            max_ts += 1
        parts.append(f'<line x1="{left}" y1="{chart_bottom}" x2="{right}" y2="{chart_bottom}" stroke="#cbd5e1"/>')
        parts.append(f'<line x1="{left}" y1="{chart_top}" x2="{left}" y2="{chart_bottom}" stroke="#cbd5e1"/>')
        legend_x = left + 220
        for legend_index, (name, values) in enumerate(visible):
            numbers = [float(item["value"]) for item in values]
            low, high = min(numbers), max(numbers)
            if high == low:
                high += 1
            coords = []
            for item in values:
                x = left + (int(item["timestamp"]) - min_ts) / (max_ts - min_ts) * (right - left)
                y = chart_bottom - (float(item["value"]) - low) / (high - low) * (chart_bottom - chart_top)
                coords.append(f"{x:.1f},{y:.1f}")
            color = colors.get(name, "#475569")
            parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.5" points="{" ".join(coords)}"/>')
            label = f"{name} [{min(numbers):.1f}, {max(numbers):.1f}]"
            parts.append(f'<line x1="{legend_x + legend_index * 210}" y1="{top - 5}" x2="{legend_x + 20 + legend_index * 210}" y2="{top - 5}" stroke="{color}" stroke-width="3"/>')
            parts.append(f'<text class="legend" x="{legend_x + 26 + legend_index * 210}" y="{top - 1}">{html.escape(label)}</text>')
        parts.append(f'<text x="{left}" y="{chart_bottom + 18}">{datetime.fromtimestamp(min_ts, timezone.utc).strftime("%H:%M:%S")} UTC</text>')
        parts.append(f'<text x="{right - 70}" y="{chart_bottom + 18}">{datetime.fromtimestamp(max_ts, timezone.utc).strftime("%H:%M:%S")} UTC</text>')
    parts.append("</svg>")
    path.write_text("\n".join(parts) + "\n", encoding="utf-8")


def _risk_label(value: str) -> str:
    color = {"high": "#cf1322", "medium": "#d48806", "low": "#389e0d"}.get(value, "#64748b")
    return f'<span style="display:inline-block;padding:2px 8px;color:#fff;background:{color};border-radius:4px">{html.escape(value)}</span>'


def _html_table(headers: list[str], rows: list[list[Any]]) -> str:
    body = "".join("<tr>" + "".join(f"<td>{item}</td>" for item in row) + "</tr>" for row in rows)
    return "<table><thead><tr>" + "".join(f"<th>{html.escape(header)}</th>" for header in headers) + f"</tr></thead><tbody>{body}</tbody></table>"


def _generate_network_topology(observations: Dict[str, Any]) -> str:
    """Generate network topology ASCII diagram."""
    elb_info = observations.get("elb_metrics", {})
    backend_status = observations.get("elb_backend_status", {})
    
    # Extract ELB name from backend status or metrics
    elb_name = "ELB"
    if backend_status.get("success"):
        lb_status = backend_status.get("loadbalancer_status", {})
        if lb_status.get("statuses"):
            elb_name = lb_status["statuses"].get("loadbalancer", {}).get("name", "ELB")
    if elb_name == "ELB" and elb_info.get("elb_name"):
        elb_name = elb_info["elb_name"]
    
    elb_type = elb_info.get("elb_type", "Unknown")
    
    # Count healthy backends
    healthy_members = []
    if backend_status.get("success"):
        for member in backend_status.get("members", []):
            if member.get("operating_status") == "ONLINE":
                healthy_members.append(f"{member.get('address')}:{member.get('protocol_port')}")
    
    # Extract ELB ID
    elb_id = elb_info.get("elb_id", "N/A")
    if elb_id == "N/A" and backend_status.get("elb_id"):
        elb_id = backend_status["elb_id"]
    
    topology = f"""
    ┌─────────────────────────────────────────────────────────────┐
    │                    Network Topology                         │
    └─────────────────────────────────────────────────────────────┘
    
        k6 Client (10 VUs)
              │
              ▼
    ┌─────────────────────┐
    │   {html.escape(elb_name):<17} │  Type: {html.escape(elb_type)}
    │  {html.escape(elb_id):<19} │  IP: 192.168.135.155
    └──────────┬──────────┘
              │ TCP 80/443
              ▼
    ┌─────────────────────┐
    │  nginx-ingress      │  
    │  (2 replicas)       │
    └──────────┬──────────┘
              │ HTTP
              ▼
    ┌─────────────────────┐
    │   pressure-java     │
    │   demo (2 pods)     │
    └─────────────────────┘
    
    Healthy Backends: {len(healthy_members)}
    {chr(10).join('    • ' + m for m in healthy_members) if healthy_members else '    • No backend data'}
    """
    return topology


def _generate_elb_metrics_table(observations: Dict[str, Any]) -> tuple[list[list[str]], list[list[str]]]:
    """Generate ELB metrics table rows."""
    elb_metrics = observations.get("elb_metrics", {})
    if not elb_metrics.get("success"):
        return [], []
    
    rows_en = []
    rows_cn = []
    
    # Layer 4 metrics
    l4_metrics = {
        "m2_act_conn": "Active Connections",
        "m4_ncps": "New Connections/sec",
        "m7_in_Bps": "Inbound Bytes/sec",
        "m8_out_Bps": "Outbound Bytes/sec",
        "ma_normal_servers": "Healthy Backends",
        "m9_abnormal_servers": "Unhealthy Backends",
    }
    
    l4_metrics_cn = {
        "m2_act_conn": "活跃连接数",
        "m4_ncps": "新建连接数/秒",
        "m7_in_Bps": "入站字节/秒",
        "m8_out_Bps": "出站字节/秒",
        "ma_normal_servers": "健康后端数",
        "m9_abnormal_servers": "异常后端数",
    }
    
    metrics_data = elb_metrics.get("metrics", {})
    
    for key, name_en in l4_metrics.items():
        name_cn = l4_metrics_cn.get(key, key)
        metric = metrics_data.get(key, {})
        value = metric.get("latest_value", "N/A")
        unit = metric.get("unit", "")
        
        if value is not None and value != "N/A":
            rows_en.append([name_en, f"{value} {unit}"])
            rows_cn.append([name_cn, f"{value} {unit}"])
    
    return rows_en, rows_cn


def generate_cce_pressure_test_report(
    result_path: str,
    observations_path: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate Markdown, HTML, and SVG artifacts from a pressure-test result (CN + EN)."""
    try:
        payload = json.loads(Path(result_path).read_text(encoding="utf-8"))
        observations = json.loads(Path(observations_path).read_text(encoding="utf-8")) if observations_path else {}
    except (OSError, json.JSONDecodeError) as exc:
        return _error(str(exc))
    series = _merge_series(payload, observations)
    data_gaps = list(payload.get("data_gaps") or []) + list(observations.get("data_gaps") or [])
    
    # Smart data gap analysis
    k6_summary = payload.get("k6_summary") or {}
    elb_metrics = observations.get("elb_metrics", {})
    elb_support_l7 = elb_metrics.get("support_protocol", {}).get("layer7", False) if elb_metrics.get("success") else False
    
    for name in STANDARD_SERIES:
        if series.get(name):
            continue
            
        if name in ("rps", "latency_ms", "success_rate_percent"):
            # k6 metrics: aggregate values available, time-series not critical
            if k6_summary:
                data_gaps.append(f"{name}: k6 aggregate metrics available (time-series curve requires k6 JSON output or stepped traffic model)")
            else:
                data_gaps.append(f"{name}: No k6 metrics collected. Check if the Job completed successfully.")
                
        elif name == "connections":
            if elb_metrics.get("success"):
                data_gaps.append(f"{name}: ELB returned zero or no connection data (keepalive model may show low connection counts)")
            else:
                data_gaps.append(f"{name}: No ELB metrics available. Pass elb_id to collect connection data.")
                
        elif name in ("desired_replicas", "ready_replicas", "running_pods"):
            # Check if workload sampling had errors
            samples = payload.get("samples", [])
            has_workload_error = any("workload_sample_error" in s for s in samples)
            if has_workload_error:
                data_gaps.append(f"{name}: Workload sampling failed. Use workload_namespace=<target-ns> if workload is in a different namespace from the k6 client.")
            else:
                data_gaps.append(f"{name}: No workload replica data collected.")
        else:
            data_gaps.append(f"{name}: No time-series data available.")
    
    # Add ELB L7 limitation note
    if elb_metrics.get("success") and not elb_support_l7:
        data_gaps.append("ELB is Layer-4 only (no l7_flavor_id), so Layer-7 metrics (QPS, HTTP status codes, response time) are not available from ELB. These are handled by nginx-ingress internally.")
    
    data_gaps = list(dict.fromkeys(data_gaps))
    recommendations = _recommendations(payload, series)
    output_path = Path(output_dir) if output_dir else Path(result_path).parent
    output_path.mkdir(parents=True, exist_ok=True)
    base = _safe_name(payload.get("test_name") or Path(result_path).stem)
    chart_path = output_path / f"{base}-curves.svg"
    
    # Generate both CN and EN reports
    md_path_cn = output_path / f"{base}-report-zh.md"
    html_path_cn = output_path / f"{base}-report-zh.html"
    md_path_en = output_path / f"{base}-report-en.md"
    html_path_en = output_path / f"{base}-report-en.html"
    
    _svg_chart(series, chart_path)

    summary = payload.get("k6_summary") or {}
    stats = {name: _series_stats(values) for name, values in series.items()}
    stats_rows = [[name, item.get("samples", 0), item.get("avg", "-"), item.get("max", "-"), item.get("min", "-")] for name, item in sorted(stats.items())]
    recommendation_rows = [[item["risk"], item["area"], item["recommendation"]] for item in recommendations]
    relationship_rows = _relationship_rows(series)
    
    # Get ELB metrics
    elb_rows_en, elb_rows_cn = _generate_elb_metrics_table(observations)
    topology = _generate_network_topology(observations)
    
    # ==================== Chinese Report ====================
    md_cn = [
        "# CCE 压力测试报告",
        "",
        f"- **测试名称**: `{payload.get('test_name', '-')}`",
        f"- **工作负载**: `{payload.get('namespace', '-')}/{payload.get('workload_name', '-')}`",
        f"- **流量模型**: `{payload.get('model', '-')}`",
        f"- **目标地址**: `{payload.get('target_url', '-')}`",
        "",
        "## 网络拓扑",
        "",
        "```",
        topology,
        "```",
        "",
        "## 性能曲线",
        "",
        f"![pressure-test curves]({chart_path.name})",
        "",
        "## k6 压测摘要",
        "",
        "| 指标 | 数值 |",
        "|------|------|",
        f"| 请求总数 | {summary.get('request_count', '-')} |",
        f"| RPS | {summary.get('rps', '-'):.2f} |",
        f"| 成功率 | {summary.get('success_rate', '-')*100:.1f}% |",
        f"| 平均延迟 | {summary.get('latency_avg_ms', '-'):.2f} ms |",
        f"| P95延迟 | {summary.get('latency_p95_ms', '-'):.2f} ms |",
        f"| 最大延迟 | {summary.get('latency_max_ms', '-'):.2f} ms |",
        f"| 最大VUs | {summary.get('vus_max', '-')} |",
        "",
        "## 时序统计",
        "",
        "| 指标 | 样本数 | 平均值 | 最大值 | 最小值 |",
        "|------|--------|--------|--------|--------|",
    ]
    for row in stats_rows:
        md_cn.append("| " + " | ".join(str(item) for item in row) + " |")
    
    # Add ELB metrics
    if elb_rows_cn:
        md_cn.extend(["", "## ELB 指标", "", "| 指标 | 数值 |", "|------|------|"])
        for row in elb_rows_cn:
            md_cn.append(f"| {row[0]} | {row[1]} |")
    
    md_cn.extend(["", "## 建议", "", "| 风险 | 领域 | 建议 |", "|------|------|------|"])
    for row in recommendation_rows:
        md_cn.append("| " + " | ".join(str(item) for item in row) + " |")
    
    md_cn.extend(["", "## 数据缺口", "", "| 风险 | 数据缺口 |", "|------|----------|"])
    for gap in data_gaps:
        md_cn.append(f"| medium | {gap} |")
    
    md_path_cn.write_text("\n".join(md_cn) + "\n", encoding="utf-8")
    
    # ==================== English Report ====================
    md_en = [
        "# CCE Pressure Test Report",
        "",
        f"- **Test Name**: `{payload.get('test_name', '-')}`",
        f"- **Workload**: `{payload.get('namespace', '-')}/{payload.get('workload_name', '-')}`",
        f"- **Traffic Model**: `{payload.get('model', '-')}`",
        f"- **Target URL**: `{payload.get('target_url', '-')}`",
        "",
        "## Network Topology",
        "",
        "```",
        topology,
        "```",
        "",
        "## Performance Curves",
        "",
        f"![pressure-test curves]({chart_path.name})",
        "",
        "## k6 Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Request Count | {summary.get('request_count', '-')} |",
        f"| RPS | {summary.get('rps', '-'):.2f} |",
        f"| Success Rate | {summary.get('success_rate', '-')*100:.1f}% |",
        f"| Avg Latency | {summary.get('latency_avg_ms', '-'):.2f} ms |",
        f"| P95 Latency | {summary.get('latency_p95_ms', '-'):.2f} ms |",
        f"| Max Latency | {summary.get('latency_max_ms', '-'):.2f} ms |",
        f"| Max VUs | {summary.get('vus_max', '-')} |",
        "",
        "## Time-Series Summary",
        "",
        "| Metric | Samples | Average | Maximum | Minimum |",
        "|--------|---------|---------|---------|---------|",
    ]
    for row in stats_rows:
        md_en.append("| " + " | ".join(str(item) for item in row) + " |")
    
    # Add ELB metrics
    if elb_rows_en:
        md_en.extend(["", "## ELB Metrics", "", "| Metric | Value |", "|--------|-------|"])
        for row in elb_rows_en:
            md_en.append(f"| {row[0]} | {row[1]} |")
    
    md_en.extend(["", "## Recommendations", "", "| Risk | Area | Recommendation |", "|------|------|----------------|"])
    for row in recommendation_rows:
        md_en.append("| " + " | ".join(str(item) for item in row) + " |")
    
    md_en.extend(["", "## Data Gaps", "", "| Risk | Data Gap |", "|------|----------|"])
    for gap in data_gaps:
        md_en.append(f"| medium | {gap} |")
    
    md_path_en.write_text("\n".join(md_en) + "\n", encoding="utf-8")
    
    # ==================== Chinese HTML ====================
    k6_rows = [[html.escape(name), html.escape(str(summary.get(name, "-")))] for name in ("request_count", "rps", "success_rate", "latency_avg_ms", "latency_p95_ms", "latency_p99_ms", "latency_max_ms", "vus_max")]
    
    elb_html_cn = _html_table(["指标", "数值"], [[html.escape(str(r[0])), html.escape(str(r[1]))] for r in elb_rows_cn]) if elb_rows_cn else "<p>无ELB数据</p>"
    elb_html_en = _html_table(["Metric", "Value"], [[html.escape(str(r[0])), html.escape(str(r[1]))] for r in elb_rows_en]) if elb_rows_en else "<p>No ELB data available</p>"
    
    html_cn = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>CCE 压力测试报告</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#1e293b;margin:28px;max-width:1180px;line-height:1.6}}
h1,h2{{color:#0f172a;border-bottom:2px solid #e2e8f0;padding-bottom:8px}}
table{{border-collapse:collapse;width:100%;margin:12px 0 24px;font-size:14px}}th,td{{border:1px solid #cbd5e1;padding:10px;text-align:left}}th{{background:#f1f5f9;font-weight:600}}
img{{max-width:100%;border:1px solid #e2e8f0;border-radius:4px}}
code{{background:#f1f5f9;padding:2px 6px;border-radius:3px;font-size:13px}}
.topology{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:20px;font-family:"Courier New",monospace;font-size:13px;line-height:1.5;overflow-x:auto}}
.metric-card{{background:#f0fdf4;border-left:4px solid #389e0d;padding:12px;margin:8px 0;border-radius:4px}}
.warning{{background:#fffbeb;border-left:4px solid #d48806}}
.danger{{background:#fef2f2;border-left:4px solid #cf1322}}
</style></head><body>
<h1> CCE 压力测试报告</h1>
<p><strong>测试名称:</strong> <code>{html.escape(str(payload.get("test_name", "-")))}</code><br>
<strong>工作负载:</strong> <code>{html.escape(str(payload.get("namespace", "-")))}/{html.escape(str(payload.get("workload_name", "-")))}</code><br>
<strong>流量模型:</strong> <code>{html.escape(str(payload.get("model", "-")))}</code><br>
<strong>目标地址:</strong> <code>{html.escape(str(payload.get("target_url", "-")))}</code></p>

<h2> 网络拓扑</h2>
<div class="topology"><pre>{html.escape(topology)}</pre></div>

<h2> 性能曲线</h2>
<img src="{html.escape(chart_path.name)}" alt="pressure-test curves">

<h2> k6 压测摘要</h2>
{_html_table(["指标", "数值"], k6_rows)}

<h2> 时序统计</h2>
{_html_table(["指标", "样本数", "平均值", "最大值", "最小值"], [[html.escape(str(item)) for item in row] for row in stats_rows])}

<h2> ELB 指标</h2>
{elb_html_cn}

<h2> 关联分析</h2>
{_html_table(["指标", "对齐样本数", "与RPS相关性", "解读"], [[html.escape(str(item)) for item in row] for row in relationship_rows])}

<h2> 建议</h2>
{_html_table(["风险", "领域", "建议"], [[_risk_label(row[0]), html.escape(row[1]), html.escape(row[2])] for row in recommendation_rows])}

<h2> 数据缺口</h2>
{_html_table(["风险", "数据缺口"], [[_risk_label("medium"), html.escape(gap)] for gap in data_gaps])}
</body></html>
"""
    html_path_cn.write_text(html_cn, encoding="utf-8")
    
    # ==================== English HTML ====================
    html_en = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>CCE Pressure Test Report</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#1e293b;margin:28px;max-width:1180px;line-height:1.6}}
h1,h2{{color:#0f172a;border-bottom:2px solid #e2e8f0;padding-bottom:8px}}
table{{border-collapse:collapse;width:100%;margin:12px 0 24px;font-size:14px}}th,td{{border:1px solid #cbd5e1;padding:10px;text-align:left}}th{{background:#f1f5f9;font-weight:600}}
img{{max-width:100%;border:1px solid #e2e8f0;border-radius:4px}}
code{{background:#f1f5f9;padding:2px 6px;border-radius:3px;font-size:13px}}
.topology{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:20px;font-family:"Courier New",monospace;font-size:13px;line-height:1.5;overflow-x:auto}}
.metric-card{{background:#f0fdf4;border-left:4px solid #389e0d;padding:12px;margin:8px 0;border-radius:4px}}
.warning{{background:#fffbeb;border-left:4px solid #d48806}}
.danger{{background:#fef2f2;border-left:4px solid #cf1322}}
</style></head><body>
<h1> CCE Pressure Test Report</h1>
<p><strong>Test Name:</strong> <code>{html.escape(str(payload.get("test_name", "-")))}</code><br>
<strong>Workload:</strong> <code>{html.escape(str(payload.get("namespace", "-")))}/{html.escape(str(payload.get("workload_name", "-")))}</code><br>
<strong>Traffic Model:</strong> <code>{html.escape(str(payload.get("model", "-")))}</code><br>
<strong>Target URL:</strong> <code>{html.escape(str(payload.get("target_url", "-")))}</code></p>

<h2> Network Topology</h2>
<div class="topology"><pre>{html.escape(topology)}</pre></div>

<h2> Performance Curves</h2>
<img src="{html.escape(chart_path.name)}" alt="pressure-test curves">

<h2> k6 Summary</h2>
{_html_table(["Metric", "Value"], k6_rows)}

<h2> Time-Series Summary</h2>
{_html_table(["Metric", "Samples", "Average", "Maximum", "Minimum"], [[html.escape(str(item)) for item in row] for row in stats_rows])}

<h2> ELB Metrics</h2>
{elb_html_en}

<h2> Relationship Assessment</h2>
{_html_table(["Metric", "Aligned Samples", "Correlation vs RPS", "Interpretation"], [[html.escape(str(item)) for item in row] for row in relationship_rows])}

<h2> Recommendations</h2>
{_html_table(["Risk", "Area", "Recommendation"], [[_risk_label(row[0]), html.escape(row[1]), html.escape(row[2])] for row in recommendation_rows])}

<h2> Data Gaps</h2>
{_html_table(["Risk", "Data Gap"], [[_risk_label("medium"), html.escape(gap)] for gap in data_gaps])}
</body></html>
"""
    html_path_en.write_text(html_en, encoding="utf-8")
    
    return {
        "success": True,
        "action": "generate_cce_pressure_test_report",
        "files": {
            "markdown_cn": str(md_path_cn),
            "html_cn": str(html_path_cn),
            "markdown_en": str(md_path_en),
            "html_en": str(html_path_en),
            "chart_svg": str(chart_path)
        },
        "recommendations": recommendations,
        "data_gaps": data_gaps,
        "metric_series": series,
    }
