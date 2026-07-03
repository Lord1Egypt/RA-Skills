"""CCE to CCI 2.0 bursting setup, smoke deployment, and verification actions."""

from __future__ import annotations

from collections import Counter
import time
from typing import Any, Dict, Iterable, Optional

from huaweicloudsdkcce.v3 import ShowClusterRequest
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkvpc.v2 import ListRouteTablesRequest

from . import cce, cce_addon, cce_k8s, network
from .common import (
    K8S_AVAILABLE,
    K8S_IMPORT_ERROR,
    _safe_delete_file,
    create_cce_client,
    create_vpc_client,
    get_credentials_with_region,
    k8s_client,
)

try:
    from huaweicloudsdkvpcep.v1 import (
        CreateEndpointRequest,
        CreateEndpointRequestBody,
        ListEndpointInfoDetailsRequest,
        ListEndpointsRequest,
        ListServiceDescribeDetailsRequest,
        VpcepClient,
    )

    VPCEP_AVAILABLE = True
    VPCEP_IMPORT_ERROR = None
except ImportError as exc:
    CreateEndpointRequest = None
    CreateEndpointRequestBody = None
    ListEndpointInfoDetailsRequest = None
    ListEndpointsRequest = None
    ListServiceDescribeDetailsRequest = None
    VpcepClient = None
    VPCEP_AVAILABLE = False
    VPCEP_IMPORT_ERROR = str(exc)


DEFAULT_ADDON_VERSION = "1.5.82"
DEFAULT_SMOKE_IMAGE = "swr.cn-north-4.myhuaweicloud.com/paas-perf/perf-nginx:v10.1"
DEFAULT_SMOKE_NAMESPACE = "cci2-burst-lab"
DEFAULT_SMOKE_WORKLOAD = "cci2-burst-demo"
SWR_SERVICE_SUFFIXES = ("swr", "swr-api")
ACTIVE_ENDPOINT_STATUSES = {"accepted", "creating", "pending"}


def _error(message: str, **details: Any) -> Dict[str, Any]:
    return {"success": False, "error": message, **details}


def _credentials(
    region: str,
    ak: Optional[str],
    sk: Optional[str],
    project_id: Optional[str],
) -> tuple[Optional[str], Optional[str], Optional[str], Optional[Dict[str, Any]]]:
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return None, None, None, _error(
            "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        )
    if not proj_id:
        return None, None, None, _error(
            "Project ID not found. Pass project_id or ensure the account can access the region."
        )
    return access_key, secret_key, proj_id, None


def _create_vpcep_client(region: str, ak: str, sk: str, project_id: str):
    if not VPCEP_AVAILABLE:
        raise RuntimeError(f"huaweicloudsdkvpcep is not installed: {VPCEP_IMPORT_ERROR}")
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=project_id)
    return (
        VpcepClient.new_builder()
        .with_credentials(credentials)
        .with_endpoint(f"vpcep.{region}.myhuaweicloud.com")
        .build()
    )


def _cluster_network_context(
    region: str,
    cluster_id: str,
    ak: str,
    sk: str,
    project_id: str,
) -> Dict[str, Any]:
    request = ShowClusterRequest(cluster_id=cluster_id)
    response = create_cce_client(region, ak, sk, project_id).show_cluster(request).to_dict()
    root = response.get("cluster", response)
    spec = root.get("spec", {})
    metadata = root.get("metadata", {})
    host_network = spec.get("host_network") or spec.get("hostNetwork") or {}
    container_network = spec.get("container_network") or spec.get("containerNetwork") or {}
    eni_network = spec.get("eni_network") or spec.get("eniNetwork") or {}
    eni_subnets = eni_network.get("subnets") or []
    first_eni = eni_subnets[0] if eni_subnets else {}
    cci_subnet_id = (
        eni_network.get("eni_subnet_id")
        or eni_network.get("eniSubnetId")
        or first_eni.get("subnet_id")
        or first_eni.get("subnetID")
    )
    return {
        "cluster_id": cluster_id,
        "cluster_name": metadata.get("name"),
        "category": spec.get("category"),
        "container_network_mode": container_network.get("mode"),
        "vpc_id": host_network.get("vpc"),
        "host_vpc_subnet_id": host_network.get("subnet"),
        "cci_neutron_subnet_id": cci_subnet_id,
    }


def _endpoint_summary(endpoint: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": endpoint.get("id"),
        "service_name": endpoint.get("endpoint_service_name") or endpoint.get("service_name"),
        "service_type": endpoint.get("service_type") or endpoint.get("endpoint_service_type"),
        "status": endpoint.get("status"),
        "active_status": endpoint.get("active_status"),
        "vpc_id": endpoint.get("vpc_id"),
        "subnet_id": endpoint.get("subnet_id"),
        "ip": endpoint.get("ip"),
    }


def _list_vpcep_endpoints(client: Any, vpc_id: str) -> list[Dict[str, Any]]:
    request = ListEndpointsRequest(vpc_id=vpc_id, limit=500, offset=0)
    response = client.list_endpoints(request).to_dict()
    return [_endpoint_summary(item) for item in response.get("endpoints", [])]


def _endpoint_detail(client: Any, endpoint_id: str) -> Dict[str, Any]:
    request = ListEndpointInfoDetailsRequest(vpc_endpoint_id=endpoint_id)
    return client.list_endpoint_info_details(request).to_dict()


def _endpoint_is_active(endpoint: Dict[str, Any]) -> bool:
    return str(endpoint.get("status", "")).lower() in ACTIVE_ENDPOINT_STATUSES


def _endpoint_for_service(endpoints: Iterable[Dict[str, Any]], service_name: str) -> Optional[Dict[str, Any]]:
    for endpoint in endpoints:
        if endpoint.get("service_name") == service_name and _endpoint_is_active(endpoint):
            return endpoint
    return None


def _contains_obs_policy(detail: Dict[str, Any]) -> bool:
    for statement in detail.get("policy_statement") or []:
        actions = statement.get("action") or []
        resources = statement.get("resource") or []
        if any("obs:" in str(item).lower() for item in [*actions, *resources]):
            return True
    return False


def _find_obs_endpoint(client: Any, endpoints: Iterable[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for endpoint in endpoints:
        if not _endpoint_is_active(endpoint):
            continue
        text = f"{endpoint.get('service_name', '')} {endpoint.get('service_type', '')}".lower()
        if not any(marker in text for marker in ("obs", "storage", "gateway")):
            continue
        try:
            detail = _endpoint_detail(client, str(endpoint["id"]))
        except Exception:
            detail = {}
        if "obs" in text or _contains_obs_policy(detail):
            return {**endpoint, "obs_policy_verified": _contains_obs_policy(detail)}
    return None


def _describe_public_service(client: Any, service_name: str) -> Dict[str, Any]:
    request = ListServiceDescribeDetailsRequest(endpoint_service_name=service_name)
    return client.list_service_describe_details(request).to_dict()


def _route_table_ids(
    region: str,
    vpc_id: str,
    ak: str,
    sk: str,
    project_id: str,
) -> list[str]:
    request = ListRouteTablesRequest(vpc_id=vpc_id)
    response = create_vpc_client(region, ak, sk, project_id).list_route_tables(request).to_dict()
    return [item["id"] for item in response.get("routetables", []) if item.get("id")]


def _create_endpoint(
    client: Any,
    service_name: str,
    vpc_id: str,
    vpcep_subnet_id: str,
    route_table_ids: Optional[list[str]] = None,
) -> Dict[str, Any]:
    service = _describe_public_service(client, service_name)
    service_id = service.get("id")
    if not service_id:
        raise RuntimeError(f"VPCEP public service was not found: {service_name}")
    service_type = service.get("service_type")
    kwargs: Dict[str, Any] = {
        "endpoint_service_id": service_id,
        "vpc_id": vpc_id,
        "subnet_id": vpcep_subnet_id,
        "enable_dns": True,
        "description": "Created by cce-cci-bursting-deployer",
    }
    if service_type == "gateway":
        kwargs["routetables"] = route_table_ids or []
    request = CreateEndpointRequest(body=CreateEndpointRequestBody(**kwargs))
    response = client.create_endpoint(request).to_dict()
    return {
        "service_name": service_name,
        "service_type": service_type,
        "action": "created",
        "endpoint": _endpoint_summary(response),
    }


def precheck_cce_cci_bursting(
    region: str,
    cluster_id: str,
    vpcep_subnet_id: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Inspect whether a CCE cluster can be configured for CCI 2.0 bursting."""
    access_key, secret_key, proj_id, error = _credentials(region, ak, sk, project_id)
    if error:
        return error
    if not cluster_id:
        return _error("cluster_id is required")

    try:
        context = _cluster_network_context(region, cluster_id, access_key, secret_key, proj_id)
        subnet_result = network.list_vpc_subnets(region, context["vpc_id"], access_key, secret_key, proj_id)
        addons_result = cce_addon.list_cce_addons(region, cluster_id, access_key, secret_key, proj_id)
        installed_addons = addons_result.get("addons", []) if addons_result.get("success") else []
        virtual_kubelet = next(
            (
                item
                for item in installed_addons
                if "virtual-kubelet" in {item.get("name"), item.get("template_name")}
            ),
            None,
        )
        vpc_subnets = subnet_result.get("subnets", []) if subnet_result.get("success") else []
        selected_vpcep_subnet = vpcep_subnet_id or context.get("host_vpc_subnet_id")
        selected_exists = any(item.get("id") == selected_vpcep_subnet for item in vpc_subnets)
        issues = []
        if str(context.get("container_network_mode", "")).lower() != "eni":
            issues.append("CCE to CCI bursting requires a Turbo/ENI cluster.")
        if not context.get("vpc_id"):
            issues.append("Cluster host VPC ID could not be resolved.")
        if not context.get("cci_neutron_subnet_id"):
            issues.append("CCI addon Neutron subnet ID could not be resolved from eni_network.")
        if not selected_vpcep_subnet:
            issues.append("VPCEP VPC subnet ID could not be resolved. Pass vpcep_subnet_id.")
        elif not selected_exists:
            issues.append("vpcep_subnet_id is not a VPC subnet in the cluster VPC.")
        if not VPCEP_AVAILABLE:
            issues.append(f"huaweicloudsdkvpcep is not installed: {VPCEP_IMPORT_ERROR}")

        return {
            "success": not issues,
            "action": "precheck_cce_cci_bursting",
            "region": region,
            "cluster_id": cluster_id,
            "network": context,
            "subnet_roles": {
                "cci_addon_neutron_subnet_id": context.get("cci_neutron_subnet_id"),
                "vpcep_vpc_subnet_id": selected_vpcep_subnet,
                "note": "These are different ID namespaces. Do not swap them.",
            },
            "virtual_kubelet": virtual_kubelet,
            "vpc_subnets": vpc_subnets,
            "issues": issues,
        }
    except Exception as exc:
        return _error(str(exc), error_type=type(exc).__name__)


def ensure_cce_cci_vpcep(
    region: str,
    cluster_id: str,
    vpcep_subnet_id: Optional[str] = None,
    obs_endpoint_service_name: Optional[str] = None,
    route_table_ids: Optional[list[str]] = None,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Ensure SWR and OBS VPCEP dependencies required by CCI image pulling."""
    access_key, secret_key, proj_id, error = _credentials(region, ak, sk, project_id)
    if error:
        return error
    precheck = precheck_cce_cci_bursting(
        region, cluster_id, vpcep_subnet_id, access_key, secret_key, proj_id
    )
    if not precheck.get("success"):
        return _error("CCE to CCI precheck failed.", precheck=precheck)

    context = precheck["network"]
    vpc_id = context["vpc_id"]
    selected_subnet = precheck["subnet_roles"]["vpcep_vpc_subnet_id"]
    try:
        client = _create_vpcep_client(region, access_key, secret_key, proj_id)
        before = _list_vpcep_endpoints(client, vpc_id)
        planned_services = []
        swr_services = [f"com.myhuaweicloud.{region}.{suffix}" for suffix in SWR_SERVICE_SUFFIXES]
        for service_name in swr_services:
            if not _endpoint_for_service(before, service_name):
                planned_services.append(service_name)

        obs_endpoint = _find_obs_endpoint(client, before)
        data_gap = []
        if not obs_endpoint:
            if obs_endpoint_service_name:
                if not _endpoint_for_service(before, obs_endpoint_service_name):
                    planned_services.append(obs_endpoint_service_name)
            else:
                data_gap.append(
                    "No accepted OBS-compatible gateway VPCEP was found. "
                    "Pass the exact obs_endpoint_service_name obtained from the Huawei Cloud service ticket."
                )

        plan = [
            {
                "service_name": name,
                "vpcep_subnet_id": selected_subnet,
                "route_table_ids": route_table_ids or [],
            }
            for name in planned_services
        ]
        if data_gap:
            return _error(
                "OBS VPCEP information is incomplete.",
                action="ensure_cce_cci_vpcep",
                ready=False,
                data_gap=data_gap,
                existing_endpoints=before,
                plan=plan,
            )
        if plan and not confirm:
            return {
                "success": False,
                "requires_confirmation": True,
                "operation": "ensure_cce_cci_vpcep",
                "warning": "VPCEP creation may incur charges. Re-run with confirm=true after explicit user approval.",
                "existing_endpoints": before,
                "plan": plan,
                "obs_endpoint": obs_endpoint,
            }

        effective_route_tables = route_table_ids
        if obs_endpoint_service_name and obs_endpoint_service_name in planned_services and not effective_route_tables:
            effective_route_tables = _route_table_ids(region, vpc_id, access_key, secret_key, proj_id)
            if not effective_route_tables:
                return _error(
                    "OBS gateway VPCEP creation requires at least one route table ID.",
                    action="ensure_cce_cci_vpcep",
                )

        created = []
        for service_name in planned_services:
            created.append(
                _create_endpoint(
                    client,
                    service_name,
                    vpc_id,
                    selected_subnet,
                    effective_route_tables if service_name == obs_endpoint_service_name else None,
                )
            )
        after = _list_vpcep_endpoints(client, vpc_id)
        obs_after = _find_obs_endpoint(client, after)
        missing = [
            service_name for service_name in swr_services if not _endpoint_for_service(after, service_name)
        ]
        if not obs_after:
            missing.append("OBS-compatible gateway VPCEP")
        return {
            "success": not missing,
            "ready": not missing,
            "action": "ensure_cce_cci_vpcep",
            "region": region,
            "cluster_id": cluster_id,
            "vpc_id": vpc_id,
            "vpcep_subnet_id": selected_subnet,
            "created": created,
            "endpoints": after,
            "obs_endpoint": obs_after,
            "missing": missing,
        }
    except Exception as exc:
        return _error(str(exc), action="ensure_cce_cci_vpcep", error_type=type(exc).__name__)


def _find_virtual_kubelet(addons: Iterable[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for addon in addons:
        if "virtual-kubelet" in {addon.get("name"), addon.get("template_name")}:
            return addon
    return None


def _wait_for_virtual_kubelet(
    region: str,
    cluster_id: str,
    ak: str,
    sk: str,
    project_id: str,
    wait_seconds: int,
) -> Optional[Dict[str, Any]]:
    deadline = time.time() + wait_seconds
    while True:
        result = cce_addon.list_cce_addons(region, cluster_id, ak, sk, project_id)
        addon = _find_virtual_kubelet(result.get("addons", []))
        if addon:
            return addon
        if time.time() >= deadline:
            return None
        time.sleep(3)


def setup_cce_cci_bursting(
    region: str,
    cluster_id: str,
    vpcep_subnet_id: Optional[str] = None,
    cci_subnet_id: Optional[str] = None,
    obs_endpoint_service_name: Optional[str] = None,
    route_table_ids: Optional[list[str]] = None,
    addon_version: Optional[str] = None,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Run the idempotent CCE to CCI 2.0 setup workflow."""
    access_key, secret_key, proj_id, error = _credentials(region, ak, sk, project_id)
    if error:
        return error
    precheck = precheck_cce_cci_bursting(
        region, cluster_id, vpcep_subnet_id, access_key, secret_key, proj_id
    )
    if not precheck.get("success"):
        return _error("CCE to CCI precheck failed.", action="setup_cce_cci_bursting", precheck=precheck)

    effective_cci_subnet = cci_subnet_id or precheck["network"].get("cci_neutron_subnet_id")
    if not effective_cci_subnet:
        return _error(
            "CCI Neutron subnet ID is required. Pass cci_subnet_id or configure eni_network on the cluster."
        )
    existing_addon = precheck.get("virtual_kubelet") or {}
    effective_addon_version = addon_version or existing_addon.get("version") or DEFAULT_ADDON_VERSION
    vpcep = ensure_cce_cci_vpcep(
        region=region,
        cluster_id=cluster_id,
        vpcep_subnet_id=vpcep_subnet_id,
        obs_endpoint_service_name=obs_endpoint_service_name,
        route_table_ids=route_table_ids,
        confirm=confirm,
        ak=access_key,
        sk=secret_key,
        project_id=proj_id,
    )
    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "setup_cce_cci_bursting",
            "warning": "This action creates missing VPCEPs and installs or updates virtual-kubelet. Re-run with confirm=true after explicit user approval.",
            "precheck": precheck,
            "vpcep": vpcep,
            "addon_plan": {
                "addon": "virtual-kubelet",
                "addon_version": effective_addon_version,
                "cci_neutron_subnet_id": effective_cci_subnet,
            },
        }
    if not vpcep.get("success"):
        return _error("VPCEP dependencies are not ready.", action="setup_cce_cci_bursting", vpcep=vpcep)

    addons = cce_addon.list_cce_addons(region, cluster_id, access_key, secret_key, proj_id)
    if not addons.get("success"):
        return _error("Failed to list CCE addons.", addons=addons)
    virtual_kubelet = _find_virtual_kubelet(addons.get("addons", []))
    installed = None
    if not virtual_kubelet:
        installed = cce_addon.install_cce_addon(
            region,
            cluster_id,
            "virtual-kubelet",
            effective_addon_version,
            {},
            access_key,
            secret_key,
            proj_id,
        )
        if not installed.get("success"):
            return _error("Failed to install virtual-kubelet.", addon_install=installed)
        virtual_kubelet = _wait_for_virtual_kubelet(
            region, cluster_id, access_key, secret_key, proj_id, wait_seconds=90
        )
        if not virtual_kubelet:
            return _error("virtual-kubelet installation was submitted but the addon instance did not appear in time.")

    configured = cce_addon.configure_cce_bursting_addon(
        region=region,
        cluster_id=cluster_id,
        subnet_id=effective_cci_subnet,
        subnets=[effective_cci_subnet],
        addon_id=str(virtual_kubelet.get("uid") or "virtual-kubelet"),
        addon_version=effective_addon_version,
        enable_schedule_profile_local_surge=True,
        is_install_proxy=False,
        enable_log_collection=False,
        ak=access_key,
        sk=secret_key,
        project_id=proj_id,
    )
    return {
        "success": bool(configured.get("success")),
        "action": "setup_cce_cci_bursting",
        "region": region,
        "cluster_id": cluster_id,
        "subnet_roles": {
            "cci_addon_neutron_subnet_id": effective_cci_subnet,
            "vpcep_vpc_subnet_id": precheck["subnet_roles"]["vpcep_vpc_subnet_id"],
        },
        "vpcep": vpcep,
        "addon_install": installed,
        "addon_configure": configured,
        "next_action": "Run huawei_verify_cce_cci_bursting, then deploy the smoke workload if the virtual node is Ready.",
    }


def deploy_cce_cci_smoke_workload(
    region: str,
    cluster_id: str,
    namespace: str = DEFAULT_SMOKE_NAMESPACE,
    workload_name: str = DEFAULT_SMOKE_WORKLOAD,
    image: Optional[str] = None,
    replicas: int = 2,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create or update a small Deployment that is forced onto CCI bursting capacity."""
    if replicas < 1:
        return _error("replicas must be at least 1")
    effective_image = image or (DEFAULT_SMOKE_IMAGE if region == "cn-north-4" else None)
    if not effective_image:
        return _error("image is required outside cn-north-4. Pass a regional SWR image.")
    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "deploy_cce_cci_smoke_workload",
            "warning": "This action creates or updates a namespace and Deployment. Re-run with confirm=true after explicit user approval.",
            "namespace": namespace,
            "workload_name": workload_name,
            "image": effective_image,
            "replicas": replicas,
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
            region, cluster_id, access_key, secret_key, proj_id, "cci_burst_smoke"
        )
        core_v1 = k8s_client.CoreV1Api()
        apps_v1 = k8s_client.AppsV1Api()
        labels = {"app": workload_name, "bursting.cci.io/burst-to-cci": "enforce"}
        try:
            core_v1.read_namespace(namespace)
            namespace_action = "existing"
        except Exception as exc:
            if getattr(exc, "status", None) != 404:
                raise
            core_v1.create_namespace(k8s_client.V1Namespace(metadata=k8s_client.V1ObjectMeta(name=namespace)))
            namespace_action = "created"

        deployment = k8s_client.V1Deployment(
            metadata=k8s_client.V1ObjectMeta(name=workload_name, labels=labels),
            spec=k8s_client.V1DeploymentSpec(
                replicas=replicas,
                selector=k8s_client.V1LabelSelector(match_labels={"app": workload_name}),
                template=k8s_client.V1PodTemplateSpec(
                    metadata=k8s_client.V1ObjectMeta(labels=labels),
                    spec=k8s_client.V1PodSpec(
                        containers=[
                            k8s_client.V1Container(
                                name="nginx",
                                image=effective_image,
                                image_pull_policy="IfNotPresent",
                                ports=[k8s_client.V1ContainerPort(container_port=80)],
                                resources=k8s_client.V1ResourceRequirements(
                                    requests={"cpu": "250m", "memory": "512Mi"},
                                    limits={"cpu": "250m", "memory": "512Mi"},
                                ),
                            )
                        ]
                    ),
                ),
            ),
        )
        try:
            apps_v1.read_namespaced_deployment(workload_name, namespace)
            response = apps_v1.patch_namespaced_deployment(workload_name, namespace, deployment)
            deployment_action = "patched"
        except Exception as exc:
            if getattr(exc, "status", None) != 404:
                raise
            response = apps_v1.create_namespaced_deployment(namespace, deployment)
            deployment_action = "created"
        return {
            "success": True,
            "action": "deploy_cce_cci_smoke_workload",
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace,
            "namespace_action": namespace_action,
            "workload_name": workload_name,
            "deployment_action": deployment_action,
            "image": effective_image,
            "replicas": replicas,
            "deployment_uid": getattr(response.metadata, "uid", None),
            "next_action": "Run huawei_verify_cce_cci_bursting with the same namespace and workload_name.",
        }
    except Exception as exc:
        return _error(str(exc), action="deploy_cce_cci_smoke_workload", error_type=type(exc).__name__)
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def _node_is_virtual(node: Dict[str, Any]) -> bool:
    labels = node.get("labels") or {}
    return (
        node.get("name") in {"bursting-node", "virtual-kubelet"}
        or labels.get("type") == "virtual-kubelet"
        or labels.get("bursting.cci.io/node-type") == "virtual-kubelet"
    )


def verify_cce_cci_bursting(
    region: str,
    cluster_id: str,
    namespace: Optional[str] = None,
    workload_name: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Verify the addon, virtual node, and optional smoke workload result."""
    access_key, secret_key, proj_id, error = _credentials(region, ak, sk, project_id)
    if error:
        return error
    addons = cce_addon.list_cce_addons(region, cluster_id, access_key, secret_key, proj_id)
    nodes = cce.get_kubernetes_nodes(region, cluster_id, access_key, secret_key, proj_id)
    pods = cce_k8s.get_cce_pods(region, cluster_id, access_key, secret_key, proj_id, namespace)
    deployments = cce_k8s.get_cce_deployments(
        region, cluster_id, access_key, secret_key, proj_id, namespace
    )
    events = cce_k8s.get_cce_events(
        region, cluster_id, access_key, secret_key, proj_id, namespace, limit=100
    )
    if not all(item.get("success") for item in (addons, nodes, pods, deployments, events)):
        return _error(
            "Verification data collection failed.",
            action="verify_cce_cci_bursting",
            data={"addons": addons, "nodes": nodes, "pods": pods, "deployments": deployments, "events": events},
        )

    virtual_kubelet = _find_virtual_kubelet(addons.get("addons", []))
    virtual_nodes = [item for item in nodes.get("nodes", []) if _node_is_virtual(item)]
    ready_virtual_nodes = [item for item in virtual_nodes if str(item.get("ready")).lower() == "true"]
    workload_pods = pods.get("pods", [])
    workload_deployments = deployments.get("deployments", [])
    if workload_name:
        workload_pods = [
            item for item in workload_pods if (item.get("labels") or {}).get("app") == workload_name
        ]
        workload_deployments = [
            item for item in workload_deployments if item.get("name") == workload_name
        ]
    phase_distribution = dict(Counter(item.get("status") for item in workload_pods))
    node_distribution = dict(Counter(item.get("node") for item in workload_pods))
    warning_events = [
        item
        for item in events.get("events", [])
        if str(item.get("type", "")).lower() == "warning"
        and (not workload_name or workload_name in str(item.get("involved_object", {}).get("name", "")))
    ]
    workload_requested = bool(namespace or workload_name)
    virtual_node_names = {item.get("name") for item in virtual_nodes}
    workload_ready = (
        bool(workload_pods)
        and phase_distribution.get("Running", 0) == len(workload_pods)
        and all(item.get("node") in virtual_node_names for item in workload_pods)
    )
    ready = bool(virtual_kubelet and ready_virtual_nodes and (workload_ready or not workload_requested))
    return {
        "success": ready,
        "ready": ready,
        "action": "verify_cce_cci_bursting",
        "region": region,
        "cluster_id": cluster_id,
        "addon": virtual_kubelet,
        "virtual_nodes": virtual_nodes,
        "ready_virtual_node_count": len(ready_virtual_nodes),
        "workload": {
            "namespace": namespace,
            "workload_name": workload_name,
            "deployments": workload_deployments,
            "pod_count": len(workload_pods),
            "phase_distribution": phase_distribution,
            "node_distribution": node_distribution,
            "ready": workload_ready if workload_requested else None,
        },
        "warning_events": warning_events[-20:],
    }
