"""CCE Kubernetes resource functions."""

from typing import Any, Dict, Optional

import base64
import os

from .common import (
    get_credentials,
    create_cce_client,
    SDK_AVAILABLE,
    IMPORT_ERROR,
    K8S_AVAILABLE,
    K8S_IMPORT_ERROR,
    k8s_client,
    _register_cert_file,
    _safe_delete_file,
)

from huaweicloudsdkcce.v3 import CreateKubernetesClusterCertRequest, ClusterCertDuration


def _setup_k8s_client(region: str, cluster_id: str, access_key: str, secret_key: str, proj_id: str, cert_prefix: str):
    """Helper to setup Kubernetes client for CCE cluster.
    
    Returns tuple of (configuration, cert_file, key_file) or raises exception.
    """
    cce_client = create_cce_client(region, access_key, secret_key, proj_id)

    cert_request = CreateKubernetesClusterCertRequest()
    cert_request.cluster_id = cluster_id
    body = ClusterCertDuration()
    body.duration = 1
    cert_request.body = body

    cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
    kubeconfig_data = cert_response.to_dict()

    external_cluster = None
    for c in kubeconfig_data.get('clusters', []):
        if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
            external_cluster = c
            break

    if not external_cluster:
        external_cluster = kubeconfig_data.get('clusters', [{}])[0]

    if not external_cluster:
        raise Exception("Could not find cluster endpoint")

    configuration = k8s_client.Configuration()
    configuration.host = external_cluster.get('cluster', {}).get('server')
    configuration.verify_ssl = False

    user_data = None
    for u in kubeconfig_data.get('users', []):
        if u.get('name') == 'user':
            user_data = u.get('user', {})
            break

    cert_file = None
    key_file = None
    
    if user_data and user_data.get('client_certificate_data'):
        cert_file = f'/tmp/cce_{cert_prefix}_client_{os.getpid()}.crt'
        with open(cert_file, 'wb') as f:
            f.write(base64.b64decode(user_data['client_certificate_data']))
        configuration.cert_file = cert_file

    if user_data and user_data.get('client_key_data'):
        key_file = f'/tmp/cce_{cert_prefix}_client_{os.getpid()}.key'
        with open(key_file, 'wb') as f:
            f.write(base64.b64decode(user_data['client_key_data']))
        configuration.key_file = key_file

    _register_cert_file(cert_file)
    _register_cert_file(key_file)

    k8s_client.Configuration.set_default(configuration)
    
    return configuration, cert_file, key_file


def get_cce_pods(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None, labels: str = None) -> Dict[str, Any]:
    """Get pods in a CCE cluster.

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        namespace: Kubernetes namespace (optional)
        labels: Kubernetes label selector, e.g. "app=nginx,version=v1" (optional)
    """
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    if not K8S_AVAILABLE:
        return {
            "success": False,
            "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "pods")
        v1 = k8s_client.CoreV1Api()

        if namespace:
            pods = v1.list_namespaced_pod(namespace, label_selector=labels)
        else:
            pods = v1.list_pod_for_all_namespaces(label_selector=labels)

        pod_list = []
        for pod in pods.items:
            pod_info = {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "node": pod.spec.node_name,
                "ip": pod.status.pod_ip,
                "created": str(pod.metadata.creation_timestamp) if pod.metadata.creation_timestamp else None,
                "labels": pod.metadata.labels,
            }
            if pod.status.container_statuses:
                containers = []
                for cs in pod.status.container_statuses:
                    containers.append({
                        "name": cs.name,
                        "ready": cs.ready,
                        "restart_count": cs.restart_count,
                        "state": str(cs.state) if cs.state else None
                    })
                pod_info["containers"] = containers
            pod_list.append(pod_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "get_cce_pods",
            "namespace": namespace or "all",
            "count": len(pod_list),
            "pods": pod_list
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def get_cce_namespaces(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get namespaces in a CCE cluster."""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    if not K8S_AVAILABLE:
        return {
            "success": False,
            "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "ns")
        v1 = k8s_client.CoreV1Api()

        namespaces = v1.list_namespace()

        ns_list = []
        for ns in namespaces.items:
            ns_info = {
                "name": ns.metadata.name,
                "status": ns.status.phase,
                "created": str(ns.metadata.creation_timestamp) if ns.metadata.creation_timestamp else None,
                "labels": ns.metadata.labels,
            }
            ns_list.append(ns_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        
        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "get_cce_namespaces",
            "count": len(ns_list),
            "namespaces": ns_list
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def get_cce_deployments(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None) -> Dict[str, Any]:
    """Get deployments in a CCE cluster."""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    if not K8S_AVAILABLE:
        return {
            "success": False,
            "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "dep")
        apps_v1 = k8s_client.AppsV1Api()

        if namespace:
            deployments = apps_v1.list_namespaced_deployment(namespace)
        else:
            deployments = apps_v1.list_deployment_for_all_namespaces()

        dep_list = []
        for dep in deployments.items:
            dep_info = {
                "name": dep.metadata.name,
                "namespace": dep.metadata.namespace,
                "replicas": dep.status.replicas if dep.status else None,
                "ready_replicas": dep.status.ready_replicas if dep.status else None,
                "available_replicas": dep.status.available_replicas if dep.status else None,
                "created": str(dep.metadata.creation_timestamp) if dep.metadata.creation_timestamp else None,
                "labels": dep.metadata.labels,
            }
            if dep.spec:
                dep_info["desired_replicas"] = dep.spec.replicas
                dep_info["strategy"] = dep.spec.strategy.type if dep.spec.strategy else None
            dep_list.append(dep_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        
        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "get_cce_deployments",
            "namespace": namespace or "all",
            "count": len(dep_list),
            "deployments": dep_list
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def get_cce_services(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None) -> Dict[str, Any]:
    """Get services in a CCE cluster"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    if not K8S_AVAILABLE:
        return {
            "success": False,
            "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    cert_file = None
    key_file = None

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "service")
        core_v1 = k8s_client.CoreV1Api()

        if namespace:
            services = core_v1.list_namespaced_service(namespace)
        else:
            services = core_v1.list_service_for_all_namespaces()

        service_list = []
        for svc in services.items:
            svc_info = {
                "name": svc.metadata.name,
                "namespace": svc.metadata.namespace,
                "type": svc.spec.type if svc.spec.type else "ClusterIP",
                "cluster_ip": svc.spec.cluster_ip if hasattr(svc.spec, 'cluster_ip') else None,
                "cluster_ips": list(svc.spec.cluster_ips) if hasattr(svc.spec, 'cluster_ips') and svc.spec.cluster_ips else [],
                "external_ips": list(svc.spec.external_ips) if hasattr(svc.spec, 'external_ips') and svc.spec.external_ips else [],
                "external_name": svc.spec.external_name if hasattr(svc.spec, 'external_name') else None,
                "load_balancer_ip": None,
                "load_balancer_ingress": [],
                "ports": [],
                "selector": dict(svc.spec.selector) if svc.spec.selector else None,
                "session_affinity": svc.spec.session_affinity if hasattr(svc.spec, 'session_affinity') else None,
                "created": svc.metadata.creation_timestamp.isoformat() if svc.metadata.creation_timestamp else None,
                "labels": dict(svc.metadata.labels) if svc.metadata.labels else {},
                "annotations": dict(svc.metadata.annotations) if svc.metadata.annotations else {}
            }

            if svc.spec.type == "LoadBalancer":
                if svc.status.load_balancer and svc.status.load_balancer.ingress:
                    for ingress in svc.status.load_balancer.ingress:
                        svc_info["load_balancer_ingress"].append({
                            "ip": ingress.ip,
                            "hostname": ingress.hostname
                        })
                    if svc_info["load_balancer_ingress"]:
                        svc_info["load_balancer_ip"] = svc_info["load_balancer_ingress"][0].get("ip")

            if svc.spec.ports:
                for port in svc.spec.ports:
                    port_info = {
                        "name": port.name,
                        "protocol": port.protocol,
                        "port": port.port,
                        "target_port": port.target_port,
                        "node_port": port.node_port
                    }
                    svc_info["ports"].append(port_info)

            service_list.append(svc_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace,
            "count": len(service_list),
            "services": service_list
        }

    except Exception as e:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def get_cce_ingresses(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None) -> Dict[str, Any]:
    """Get ingresses in a CCE cluster"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    if not K8S_AVAILABLE:
        return {
            "success": False,
            "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    cert_file = None
    key_file = None

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "ingress")
        networking_v1 = k8s_client.NetworkingV1Api()

        if namespace:
            ingresses = networking_v1.list_namespaced_ingress(namespace)
        else:
            ingresses = networking_v1.list_ingress_for_all_namespaces()

        ingress_list = []
        for ingress in ingresses.items:
            ingress_info = {
                "name": ingress.metadata.name,
                "namespace": ingress.metadata.namespace,
                "ingress_class_name": ingress.spec.ingress_class_name,
                "default_backend": None,
                "rules": [],
                "tls": [],
                "load_balancer_ingress": [],
                "created": ingress.metadata.creation_timestamp.isoformat() if ingress.metadata.creation_timestamp else None,
                "labels": dict(ingress.metadata.labels) if ingress.metadata.labels else {},
                "annotations": dict(ingress.metadata.annotations) if ingress.metadata.annotations else {}
            }

            if ingress.spec.default_backend:
                ingress_info["default_backend"] = {
                    "service_name": ingress.spec.default_backend.service.name if ingress.spec.default_backend.service else None,
                    "service_port": ingress.spec.default_backend.service.port.number if ingress.spec.default_backend.service and ingress.spec.default_backend.service.port else None
                }

            if ingress.spec.rules:
                for rule in ingress.spec.rules:
                    rule_info = {
                        "host": rule.host,
                        "paths": []
                    }
                    if rule.http and rule.http.paths:
                        for path in rule.http.paths:
                            path_info = {
                                "path": path.path,
                                "path_type": path.path_type,
                                "backend": {
                                    "service_name": path.backend.service.name if path.backend.service else None,
                                    "service_port": path.backend.service.port.number if path.backend.service and path.backend.service.port else None
                                }
                            }
                            rule_info["paths"].append(path_info)
                    ingress_info["rules"].append(rule_info)

            if ingress.spec.tls:
                for tls in ingress.spec.tls:
                    tls_info = {
                        "hosts": tls.hosts,
                        "secret_name": tls.secret_name
                    }
                    ingress_info["tls"].append(tls_info)

            if ingress.status.load_balancer and ingress.status.load_balancer.ingress:
                for lb_ingress in ingress.status.load_balancer.ingress:
                    ingress_info["load_balancer_ingress"].append({
                        "ip": lb_ingress.ip,
                        "hostname": lb_ingress.hostname
                    })

            ingress_list.append(ingress_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace,
            "count": len(ingress_list),
            "ingresses": ingress_list
        }

    except Exception as e:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def get_cce_events(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None, limit: int = 500) -> Dict[str, Any]:
    """Get events in a CCE cluster with pagination support"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    if not K8S_AVAILABLE:
        return {
            "success": False,
            "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "event")
        v1 = k8s_client.CoreV1Api()

        all_events = []
        continue_token = None
        total_fetched = 0
        max_events = limit

        while total_fetched < max_events:
            page_size = min(500, max_events - total_fetched)

            if namespace:
                events = v1.list_namespaced_event(namespace, limit=page_size, _continue=continue_token)
            else:
                events = v1.list_event_for_all_namespaces(limit=page_size, _continue=continue_token)

            if not events.items:
                break

            for e in events.items:
                event_info = {
                    "name": e.metadata.name,
                    "namespace": e.metadata.namespace if e.metadata else None,
                    "type": e.type,
                    "reason": e.reason,
                    "message": e.message,
                    "first_timestamp": str(e.first_timestamp) if e.first_timestamp else None,
                    "last_timestamp": str(e.last_timestamp) if e.last_timestamp else None,
                    "count": e.count if hasattr(e, 'count') and e.count else 1,
                    "involved_object": {
                        "kind": e.involved_object.kind if e.involved_object else None,
                        "name": e.involved_object.name if e.involved_object else None,
                        "namespace": e.involved_object.namespace if e.involved_object else None,
                    } if e.involved_object else None,
                }
                all_events.append(event_info)

            total_fetched += len(events.items)

            if hasattr(events.metadata, 'continue_') and events.metadata._continue:
                continue_token = events.metadata._continue
            else:
                break

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "get_cce_events",
            "namespace": namespace or "all",
            "count": len(all_events),
            "limit": limit,
            "events": all_events
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def get_cce_pvcs(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None) -> Dict[str, Any]:
    """Get PVCs (PersistentVolumeClaims) in a CCE cluster"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    if not K8S_AVAILABLE:
        return {
            "success": False,
            "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "pvc")
        v1 = k8s_client.CoreV1Api()

        if namespace:
            pvcs = v1.list_namespaced_persistent_volume_claim(namespace)
        else:
            pvcs = v1.list_persistent_volume_claim_for_all_namespaces()

        pvc_list = []
        for pvc in pvcs.items:
            pvc_info = {
                "name": pvc.metadata.name,
                "namespace": pvc.metadata.namespace,
                "status": pvc.status.phase,
                "volume": pvc.spec.volume_name,
                "storage_class": pvc.spec.storage_class_name,
                "capacity": pvc.status.capacity if pvc.status.capacity else {},
                "access_modes": pvc.spec.access_modes,
                "created": str(pvc.metadata.creation_timestamp) if pvc.metadata.creation_timestamp else None,
                "labels": pvc.metadata.labels,
                "annotations": pvc.metadata.annotations,
            }
            if pvc.spec.volume_mode:
                pvc_info["volume_mode"] = pvc.spec.volume_mode
            if pvc.status.access_modes:
                pvc_info["actual_access_modes"] = pvc.status.access_modes
            if pvc.status.conditions:
                conditions = []
                for c in pvc.status.conditions:
                    conditions.append({
                        "type": c.type,
                        "status": c.status,
                        "message": c.message,
                        "reason": c.reason,
                    })
                pvc_info["conditions"] = conditions
            pvc_list.append(pvc_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        
        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "get_cce_pvcs",
            "namespace": namespace or "all",
            "count": len(pvc_list),
            "pvcs": pvc_list
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def get_cce_pvs(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get PVs (PersistentVolumes) in a CCE cluster"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    if not K8S_AVAILABLE:
        return {
            "success": False,
            "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "pv")
        v1 = k8s_client.CoreV1Api()

        pvs = v1.list_persistent_volume()

        pv_list = []
        for pv in pvs.items:
            capacity = {}
            if hasattr(pv.status, 'capacity'):
                for k, v in dict(pv.status.capacity).items():
                    capacity[k] = v

            pv_info = {
                "name": pv.metadata.name,
                "status": pv.status.phase,
                "capacity": capacity,
                "access_modes": pv.spec.access_modes,
                "storage_class": pv.spec.storage_class_name,
                "created": str(pv.metadata.creation_timestamp) if pv.metadata.creation_timestamp else None,
                "labels": pv.metadata.labels,
                "annotations": pv.metadata.annotations,
            }
            if pv.spec.claim_ref:
                pv_info["claim_ref"] = {
                    "namespace": pv.spec.claim_ref.namespace,
                    "name": pv.spec.claim_ref.name,
                }
            pv_info["source"] = {"type": "unknown"}
            if hasattr(pv.spec, 'host_path') and pv.spec.host_path:
                pv_info["source"] = {"type": "host_path", "path": pv.spec.host_path.path}
            elif hasattr(pv.spec, 'gce_persistent_disk') and pv.spec.gce_persistent_disk:
                pv_info["source"] = {"type": "gce_pd", "pd_name": pv.spec.gce_persistent_disk.pd_name}
            elif hasattr(pv.spec, 'aws_elastic_block_store') and pv.spec.aws_elastic_block_store:
                pv_info["source"] = {"type": "aws_ebs", "volume_id": pv.spec.aws_elastic_block_store.volume_id}
            elif hasattr(pv.spec, 'nfs') and pv.spec.nfs:
                pv_info["source"] = {"type": "nfs", "server": pv.spec.nfs.server, "path": pv.spec.nfs.path}
            elif hasattr(pv.spec, 'cinder') and pv.spec.cinder:
                pv_info["source"] = {"type": "cinder", "volume_id": pv.spec.cinder.volume_id}
            elif hasattr(pv.spec, 'obs') and pv.spec.obs:
                pv_info["source"] = {"type": "obs", "bucket": pv.spec.obs.bucket, "endpoint": pv.spec.obs.endpoint}
            elif hasattr(pv.spec, 'nas') and pv.spec.nas:
                pv_info["source"] = {"type": "nas", "server": pv.spec.nas.server, "path": pv.spec.nas.path}

            if hasattr(pv.spec, 'volume_mode') and pv.spec.volume_mode:
                pv_info["volume_mode"] = pv.spec.volume_mode
            if hasattr(pv.status, 'conditions') and pv.status.conditions:
                conditions = []
                for c in pv.status.conditions:
                    conditions.append({
                        "type": c.type,
                        "status": c.status,
                        "message": c.message,
                        "reason": c.reason,
                    })
                pv_info["conditions"] = conditions
            pv_list.append(pv_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        
        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "get_cce_pvs",
            "count": len(pv_list),
            "pvs": pv_list
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def list_cce_configmaps(region: str, cluster_id: str, namespace: Optional[str] = None, limit: int = 100, offset: int = 0, include_data: bool = False, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """List ConfigMaps in a CCE cluster"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "configmaps")
        core_v1 = k8s_client.CoreV1Api()
        
        if namespace:
            configmaps = core_v1.list_namespaced_config_map(namespace, limit=limit)
        else:
            configmaps = core_v1.list_config_map_for_all_namespaces(limit=limit)

        configmap_list = []
        for cm in configmaps.items:
            cm_info = {
                "name": cm.metadata.name,
                "namespace": cm.metadata.namespace,
                "created": str(cm.metadata.creation_timestamp) if cm.metadata.creation_timestamp else None,
                "labels": cm.metadata.labels,
                "annotations": cm.metadata.annotations,
                "data_keys": list(cm.data.keys()) if cm.data else []
            }
            if include_data and cm.data:
                cm_info["data"] = cm.data
            configmap_list.append(cm_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        
        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "list_cce_configmaps",
            "namespace": namespace or "all",
            "count": len(configmap_list),
            "configmaps": configmap_list
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def list_cce_secrets(region: str, cluster_id: str, namespace: Optional[str] = None, limit: int = 100, include_data: bool = False, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """List Secrets in a CCE Kubernetes cluster"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "secrets")
        core_v1 = k8s_client.CoreV1Api()
        
        if namespace:
            secrets = core_v1.list_namespaced_secret(namespace, limit=limit)
        else:
            secrets = core_v1.list_secret_for_all_namespaces(limit=limit)

        secret_list = []
        for secret in secrets.items:
            secret_info = {
                "name": secret.metadata.name,
                "namespace": secret.metadata.namespace,
                "type": secret.type,
                "created": str(secret.metadata.creation_timestamp) if secret.metadata.creation_timestamp else None,
                "labels": secret.metadata.labels,
                "annotations": secret.metadata.annotations,
                "data_keys": list(secret.data.keys()) if secret.data else []
            }
            if include_data and secret.data:
                secret_info["data"] = secret.data
            secret_list.append(secret_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        
        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "list_cce_secrets",
            "namespace": namespace or "all",
            "count": len(secret_list),
            "secrets": secret_list
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def list_cce_daemonsets(region: str, cluster_id: str, namespace: Optional[str] = None, limit: int = 100, include_data: bool = False, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """List DaemonSets in a CCE Kubernetes cluster"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "daemonsets")
        apps_v1 = k8s_client.AppsV1Api()
        
        if namespace:
            daemonsets = apps_v1.list_namespaced_daemon_set(namespace, limit=limit)
        else:
            daemonsets = apps_v1.list_daemon_set_for_all_namespaces(limit=limit)

        daemonset_list = []
        for ds in daemonsets.items:
            images = []
            if hasattr(ds.spec, 'template') and hasattr(ds.spec.template, 'spec') and hasattr(ds.spec.template.spec, 'containers'):
                for container in ds.spec.template.spec.containers:
                    images.append(container.image)
            
            ds_info = {
                "name": ds.metadata.name,
                "namespace": ds.metadata.namespace,
                "desired_replicas": ds.status.desired_number_scheduled if hasattr(ds.status, 'desired_number_scheduled') else 0,
                "current_replicas": ds.status.current_number_scheduled if hasattr(ds.status, 'current_number_scheduled') else 0,
                "ready_replicas": ds.status.number_ready if hasattr(ds.status, 'number_ready') else 0,
                "available_replicas": ds.status.number_available if hasattr(ds.status, 'number_available') else 0,
                "updated_replicas": ds.status.updated_number_scheduled if hasattr(ds.status, 'updated_number_scheduled') else 0,
                "created": str(ds.metadata.creation_timestamp) if ds.metadata.creation_timestamp else None,
                "images": images,
                "update_strategy": ds.spec.update_strategy.type if hasattr(ds.spec, 'update_strategy') and hasattr(ds.spec.update_strategy, 'type') else "RollingUpdate",
            }
            if include_data:
                ds_info["spec"] = ds.spec
            daemonset_list.append(ds_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        
        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "list_cce_daemonsets",
            "namespace": namespace or "all",
            "count": len(daemonset_list),
            "daemonsets": daemonset_list
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def list_cce_statefulsets(region: str, cluster_id: str, namespace: Optional[str] = None, limit: int = 100, include_data: bool = False, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """List StatefulSets in a CCE Kubernetes cluster"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "statefulsets")
        apps_v1 = k8s_client.AppsV1Api()
        
        if namespace:
            statefulsets = apps_v1.list_namespaced_stateful_set(namespace, limit=limit)
        else:
            statefulsets = apps_v1.list_stateful_set_for_all_namespaces(limit=limit)

        statefulset_list = []
        for sts in statefulsets.items:
            images = []
            if hasattr(sts.spec, 'template') and hasattr(sts.spec.template, 'spec') and hasattr(sts.spec.template.spec, 'containers'):
                for container in sts.spec.template.spec.containers:
                    images.append(container.image)
            
            volume_claim_templates = []
            if hasattr(sts.spec, 'volume_claim_templates') and sts.spec.volume_claim_templates:
                for vct in sts.spec.volume_claim_templates:
                    volume_claim_templates.append({
                        "name": vct.metadata.name if hasattr(vct.metadata, 'name') else None,
                        "storage": vct.spec.resources.requests.get("storage", "") if hasattr(vct.spec, 'resources') and hasattr(vct.spec.resources, 'requests') else "",
                        "storage_class": vct.spec.storage_class_name if hasattr(vct.spec, 'storage_class_name') else None
                    })
            
            sts_info = {
                "name": sts.metadata.name,
                "namespace": sts.metadata.namespace,
                "desired_replicas": sts.spec.replicas if hasattr(sts.spec, 'replicas') and sts.spec.replicas is not None else 0,
                "current_replicas": sts.status.current_replicas if hasattr(sts.status, 'current_replicas') and sts.status.current_replicas is not None else 0,
                "ready_replicas": sts.status.ready_replicas if hasattr(sts.status, 'ready_replicas') and sts.status.ready_replicas is not None else 0,
                "available_replicas": sts.status.available_replicas if hasattr(sts.status, 'available_replicas') and sts.status.available_replicas is not None else 0,
                "updated_replicas": sts.status.updated_replicas if hasattr(sts.status, 'updated_replicas') and sts.status.updated_replicas is not None else 0,
                "created": str(sts.metadata.creation_timestamp) if sts.metadata.creation_timestamp else None,
                "images": images,
                "volume_claim_templates": volume_claim_templates,
                "service_name": sts.spec.service_name if hasattr(sts.spec, 'service_name') else None,
                "update_strategy": sts.spec.update_strategy.type if hasattr(sts.spec, 'update_strategy') and hasattr(sts.spec.update_strategy, 'type') else "RollingUpdate",
            }
            if include_data:
                sts_info["spec"] = sts.spec
            statefulset_list.append(sts_info)

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        
        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "list_cce_statefulsets",
            "namespace": namespace or "all",
            "count": len(statefulset_list),
            "statefulsets": statefulset_list
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def list_cce_cronjobs(region: str, cluster_id: str, namespace: str = None, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """List CronJobs in a CCE cluster"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    if not K8S_AVAILABLE:
        return {
            "success": False,
            "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "cronjob")
        batch_v1 = k8s_client.BatchV1Api()

        if namespace:
            cronjobs = batch_v1.list_namespaced_cron_job(namespace)
        else:
            cronjobs = batch_v1.list_cron_job_for_all_namespaces()

        result = []
        for cj in cronjobs.items:
            result.append({
                "name": cj.metadata.name,
                "namespace": cj.metadata.namespace,
                "schedule": cj.spec.schedule,
                "concurrency_policy": cj.spec.concurrency_policy,
                "suspend": cj.spec.suspend,
                "successful_jobs_history_limit": cj.spec.successful_jobs_history_limit,
                "failed_jobs_history_limit": cj.spec.failed_jobs_history_limit,
                "last_schedule_time": str(cj.status.last_schedule_time) if cj.status.last_schedule_time else None,
                "active_jobs": len(cj.status.active) if cj.status.active else 0,
                "creation_timestamp": str(cj.metadata.creation_timestamp) if cj.metadata.creation_timestamp else None,
            })

        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "list_cce_cronjobs",
            "namespace": namespace or "all",
            "count": len(result),
            "cronjobs": result,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }