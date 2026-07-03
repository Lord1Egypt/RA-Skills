from .common import *
from .common import _register_cert_file, _safe_delete_file
from huaweicloudsdkcore.exceptions.exceptions import ClientRequestException


def get_cce_addon_detail(region: str, cluster_id: str, addon_name: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get detailed information of a specific CCE addon."""
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

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        from huaweicloudsdkcce.v3 import ShowAddonInstanceRequest
        request = ShowAddonInstanceRequest()
        request.cluster_id = cluster_id
        request.id = addon_name

        response = client.show_addon_instance(request)

        addon_info = {}
        if hasattr(response, 'spec') and response.spec:
            spec = response.spec
            addon_info["name"] = getattr(spec, 'name', None)
            addon_info["version"] = getattr(spec, 'version', None)
            addon_info["status"] = getattr(spec, 'status', None)
            addon_info["description"] = getattr(spec, 'description', None)

            if hasattr(spec, 'custom') and spec.custom:
                custom = spec.custom
                addon_info["custom_params"] = {}

                if hasattr(custom, 'aom_id'):
                    addon_info["custom_params"]["aom_id"] = custom.aom_id
                if hasattr(custom, 'aom_instance_id'):
                    addon_info["custom_params"]["aom_instance_id"] = custom.aom_instance_id
                if hasattr(custom, 'prom_instance_id'):
                    addon_info["custom_params"]["prom_instance_id"] = custom.prom_instance_id
                if hasattr(custom, 'remote_write_url'):
                    addon_info["custom_params"]["remote_write_url"] = custom.remote_write_url
                if hasattr(custom, 'remote_read_url'):
                    addon_info["custom_params"]["remote_read_url"] = custom.remote_read_url

                if isinstance(custom, dict):
                    addon_info["custom_params"] = custom
                    if 'aom_id' in custom:
                        addon_info["aom_id"] = custom['aom_id']
                    if 'aom_instance_id' in custom:
                        addon_info["aom_instance_id"] = custom['aom_instance_id']
                    if 'prom_instance_id' in custom:
                        addon_info["aom_instance_id"] = custom['prom_instance_id']

        if hasattr(response, 'metadata') and response.metadata:
            metadata = response.metadata
            addon_info["uid"] = getattr(metadata, 'uid', None)
            addon_info["creation_timestamp"] = str(getattr(metadata, 'creation_timestamp', None))

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "get_cce_addon_detail",
            "addon": addon_info
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def list_cce_clusters(region: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """List CCE clusters in the specified region with pagination"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        request = ListClustersRequest()

        response = client.list_clusters(request)

        clusters = []
        if hasattr(response, 'items') and response.items:
            for cluster in response.items:
                cluster_info = {
                    "id": cluster.metadata.uid,
                    "name": cluster.metadata.name,
                    "status": cluster.status.phase if hasattr(cluster, 'status') and hasattr(cluster.status, 'phase') else 'Unknown',
                    "type": cluster.spec.type if hasattr(cluster, 'spec') and hasattr(cluster.spec, 'type') else 'Unknown',
                    "version": cluster.spec.version if hasattr(cluster, 'spec') and hasattr(cluster.spec, 'version') else 'Unknown',
                    "created_at": str(cluster.metadata.creation_timestamp) if hasattr(cluster, 'metadata') and hasattr(cluster.metadata, 'creation_timestamp') else None,
                }
                # Network configuration
                if hasattr(cluster, 'spec') and hasattr(cluster.spec, 'network'):
                    cluster_info["network"] = {
                        "vpc_id": getattr(cluster.spec.network, 'vpc_id', None),
                        "subnet_id": getattr(cluster.spec.network, 'subnet_id', None),
                    }
                # Node configuration
                if hasattr(cluster, 'spec') and hasattr(cluster.spec, 'node'):
                    cluster_info["node_config"] = {
                        "flavor": getattr(cluster.spec.node, 'flavor', None),
                        "count": getattr(cluster.spec.node, 'initial_node_count', None),
                    }
                clusters.append(cluster_info)

        return {
            "success": True,
            "region": region,
            "action": "list_cce_clusters",
            "count": len(clusters),
            "clusters": clusters
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def delete_cce_cluster(region: str, cluster_id: str, confirm: bool = False, delete_evs: bool = False, delete_net: bool = False, delete_obs: bool = False, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Delete a CCE cluster

    IMPORTANT: This operation will delete the cluster and all its resources.
    User confirmation is required before deletion.

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID to delete
        confirm: Must be set to True to confirm deletion (required)
        delete_evs: Whether to delete associated EVS volumes (default: False)
        delete_net: Whether to delete associated network resources (default: False)
        delete_obs: Whether to delete associated OBS buckets (default: False)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with deletion result
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

    # Require explicit confirmation
    if not confirm:
        return {
            "success": False,
            "error": "Deletion not confirmed. To delete the cluster, please set confirm=true parameter.",
            "warning": "This operation will delete the cluster and all its resources (nodes, workloads, etc.). Are you sure you want to delete this cluster?",
            "hint": "Add confirm=true parameter to confirm deletion. Example: delete_cce_cluster region=cn-north-4 cluster_id=xxx confirm=true"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        # Build the delete request
        request = DeleteClusterRequest()
        request.cluster_id = cluster_id
        request.delete_evs = delete_evs
        request.delete_net = delete_net
        request.delete_obs = delete_obs

        # Execute the delete
        response = client.delete_cluster(request)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "delete_cce_cluster",
            "message": f"Cluster deletion request submitted successfully",
            "delete_evs": delete_evs,
            "delete_net": delete_net,
            "delete_obs": delete_obs,
            "response": response.to_dict() if hasattr(response, 'to_dict') else str(response)
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def list_cce_cluster_nodes(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """List nodes in a CCE cluster with pagination"""
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

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        request = ListNodesRequest()
        request.cluster_id = cluster_id

        response = client.list_nodes(request)

        nodes = []
        if hasattr(response, 'items') and response.items:
            for node in response.items:
                node_info = {
                    "id": node.metadata.uid,
                    "name": node.metadata.name,
                    "status": node.status.phase if hasattr(node, 'status') and hasattr(node.status, 'phase') else 'Unknown',
                    "created_at": str(node.metadata.creation_timestamp) if hasattr(node, 'metadata') and hasattr(node.metadata, 'creation_timestamp') else None,
                    "labels": dict(node.metadata.labels) if hasattr(node.metadata, 'labels') and node.metadata.labels else {},
                }
                # Node spec
                if hasattr(node, 'spec'):
                    node_info["flavor"] = getattr(node.spec, 'flavor', None)
                    node_info["server_id"] = getattr(node.status, 'server_id', None)  # ECS服务器ID = HSS host_id
                    node_info["availability_zone"] = getattr(node.spec, 'az', None)  # 可用区
                # Node conditions
                if hasattr(node, 'status') and hasattr(node.status, 'conditions'):
                    conditions = []
                    for cond in node.status.conditions:
                        conditions.append({
                            "type": cond.type,
                            "status": cond.status,
                            "reason": getattr(cond, 'reason', None),
                        })
                    node_info["conditions"] = conditions
                nodes.append(node_info)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "list_cce_nodes",
            "count": len(nodes),
            "nodes": nodes
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def get_cce_nodes(region: str, cluster_id: str, node_name: Optional[str] = None, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get detailed information about CCE cluster nodes
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        node_name: Node name (optional, if not provided, returns all nodes)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with node details
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

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        request = ListNodesRequest()
        request.cluster_id = cluster_id

        response = client.list_nodes(request)

        nodes = []
        if hasattr(response, 'items') and response.items:
            for node in response.items:
                # If node_name is provided, filter by name
                if node_name and node.metadata.name != node_name:
                    continue
                
                node_info = {
                    "id": node.metadata.uid,
                    "name": node.metadata.name,
                    "status": node.status.phase if hasattr(node, 'status') and hasattr(node.status, 'phase') else 'Unknown',
                    "created_at": str(node.metadata.creation_timestamp) if hasattr(node, 'metadata') and hasattr(node.metadata, 'creation_timestamp') else None,
                }
                # Node spec
                if hasattr(node, 'spec'):
                    node_info["flavor"] = getattr(node.spec, 'flavor', None)
                    node_info["server_id"] = getattr(node.status, 'server_id', None)  # ECS服务器ID = HSS host_id
                    node_info["availability_zone"] = getattr(node.spec, 'az', None)  # 可用区
                # Node conditions
                if hasattr(node, 'status') and hasattr(node.status, 'conditions'):
                    conditions = []
                    for cond in node.status.conditions:
                        conditions.append({
                            "type": cond.type,
                            "status": cond.status,
                            "reason": getattr(cond, 'reason', None),
                            "message": getattr(cond, 'message', None),
                        })
                    node_info["conditions"] = conditions
                # Node allocatable and capacity
                if hasattr(node, 'status'):
                    node_info["allocatable"] = getattr(node.status, 'allocatable', None)
                    node_info["capacity"] = getattr(node.status, 'capacity', None)
                nodes.append(node_info)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "get_cce_nodes",
            "node_name": node_name,
            "count": len(nodes),
            "nodes": nodes
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def delete_cce_node(region: str, cluster_id: str, node_id: str, confirm: bool = False, scale_down: bool = True, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Delete a node from CCE cluster

    IMPORTANT: This operation will delete the node and all its pods.
    User confirmation is required before deletion.

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        node_id: Node ID to delete
        confirm: Must be set to True to confirm deletion (required)
        scale_down: Whether to scale down pods before deleting (default: True)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with deletion result
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

    if not node_id:
        return {
            "success": False,
            "error": "node_id is required"
        }

    # Require explicit confirmation
    if not confirm:
        return {
            "success": False,
            "error": "Deletion not confirmed. To delete the node, please set confirm=true parameter.",
            "warning": f"This operation will delete the node '{node_id}' from cluster '{cluster_id}'. All pods on this node will be terminated. Are you sure?",
            "hint": "Add confirm=true parameter to confirm deletion. Example: delete_cce_node region=cn-north-4 cluster_id=xxx node_id=yyy confirm=true"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        # Build the delete request
        request = DeleteNodeRequest()
        request.cluster_id = cluster_id
        request.node_id = node_id
        request.nodepool_scale_down = scale_down

        # Execute the delete
        response = client.delete_node(request)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "node_id": node_id,
            "action": "delete_cce_node",
            "message": f"Node deletion request submitted successfully",
            "scale_down": scale_down,
            "response": response.to_dict() if hasattr(response, 'to_dict') else str(response)
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def list_cce_node_pools(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """List node pools in a CCE cluster with pagination"""
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

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        request = ListNodePoolsRequest()
        request.cluster_id = cluster_id

        response = client.list_node_pools(request)

        nodepools = []
        if hasattr(response, 'items') and response.items:
            for nodepool in response.items:
                # Get scale groups (default + extension)
                scale_groups = []
                
                # Add default scale group (from spec.nodeTemplate)
                if hasattr(nodepool, 'spec'):
                    default_sg_info = {
                        "name": "default",
                        "type": "default",
                        "initial_node_count": nodepool.spec.initial_node_count if hasattr(nodepool.spec, 'initial_node_count') else None,
                    }
                    
                    # Get info from nodeTemplate
                    if hasattr(nodepool.spec, 'node_template'):
                        node_template = nodepool.spec.node_template
                        default_sg_info["flavor"] = node_template.flavor if hasattr(node_template, 'flavor') else None
                        default_sg_info["availability_zone"] = node_template.az if hasattr(node_template, 'az') else None
                        # Add other nodeTemplate fields if available
                        if hasattr(node_template, 'root_volume'):
                            default_sg_info["root_volume"] = node_template.root_volume.to_dict() if hasattr(node_template.root_volume, 'to_dict') else str(node_template.root_volume)
                        if hasattr(node_template, 'data_volumes'):
                            default_sg_info["data_volumes"] = [dv.to_dict() if hasattr(dv, 'to_dict') else str(dv) for dv in node_template.data_volumes]
                    
                    # Get autoscaling info
                    if hasattr(nodepool.spec, 'autoscaling'):
                        default_sg_info["autoscaling"] = {
                            "enable": nodepool.spec.autoscaling.enable if hasattr(nodepool.spec.autoscaling, 'enable') else None,
                            "min_node_count": nodepool.spec.autoscaling.min_node_count if hasattr(nodepool.spec.autoscaling, 'min_node_count') else None,
                            "max_node_count": nodepool.spec.autoscaling.max_node_count if hasattr(nodepool.spec.autoscaling, 'max_node_count') else None,
                            "scale_down_cooldown_time": nodepool.spec.autoscaling.scale_down_cooldown_time if hasattr(nodepool.spec.autoscaling, 'scale_down_cooldown_time') else None,
                            "priority": nodepool.spec.autoscaling.priority if hasattr(nodepool.spec.autoscaling, 'priority') else None,
                        }
                    
                    scale_groups.append(default_sg_info)
                
                # Add extension scale groups
                extension_scale_groups = []
                if hasattr(nodepool, 'spec') and hasattr(nodepool.spec, 'extension_scale_groups'):
                    extension_scale_groups = nodepool.spec.extension_scale_groups or []
                for sg in extension_scale_groups:
                    sg_info = {
                        "type": "extension",
                    }
                    if hasattr(sg, 'metadata'):
                        sg_info["name"] = sg.metadata.name if hasattr(sg.metadata, 'name') else None
                        sg_info["uid"] = sg.metadata.uid if hasattr(sg.metadata, 'uid') else None
                    if hasattr(sg, 'spec'):
                        sg_spec = sg.spec
                        sg_info["flavor"] = sg_spec.flavor if hasattr(sg_spec, 'flavor') else None
                        sg_info["availability_zone"] = sg_spec.az if hasattr(sg_spec, 'az') else None
                        sg_info["initial_node_count"] = sg_spec.initial_node_count if hasattr(sg_spec, 'initial_node_count') else None
                        sg_info["min_node_count"] = sg_spec.min_node_count if hasattr(sg_spec, 'min_node_count') else None
                        sg_info["max_node_count"] = sg_spec.max_node_count if hasattr(sg_spec, 'max_node_count') else None
                        if hasattr(sg_spec, 'autoscaling'):
                            sg_info["autoscaling"] = {
                                "enable": sg_spec.autoscaling.enable if hasattr(sg_spec.autoscaling, 'enable') else None,
                                "extension_priority": sg_spec.autoscaling.extension_priority if hasattr(sg_spec.autoscaling, 'extension_priority') else None,
                            }
                    scale_groups.append(sg_info)
                
                # Get scale group statuses
                scale_group_statuses = []
                raw_scale_group_statuses = []
                if hasattr(nodepool, 'status') and hasattr(nodepool.status, 'scale_group_statuses'):
                    raw_scale_group_statuses = nodepool.status.scale_group_statuses or []
                for sgs in raw_scale_group_statuses:
                    sgs_info = {}
                    if hasattr(sgs, 'name'):
                        sgs_info["name"] = sgs.name
                    if hasattr(sgs, 'current_node_count'):
                        sgs_info["current_node_count"] = sgs.current_node_count
                    if hasattr(sgs, 'status'):
                        sgs_info["status"] = sgs.status
                    scale_group_statuses.append(sgs_info)
                
                pool_info = {
                    "id": nodepool.metadata.uid,
                    "name": nodepool.metadata.name,
                    "flavor": nodepool.spec.flavor if hasattr(nodepool, 'spec') and hasattr(nodepool.spec, 'flavor') else None,
                    "initial_node_count": nodepool.spec.initial_node_count if hasattr(nodepool, 'spec') and hasattr(nodepool.spec, 'initial_node_count') else None,
                    "autoscaling_enabled": nodepool.spec.autoscaling.enabled if hasattr(nodepool, 'spec') and hasattr(nodepool.spec, 'autoscaling') and hasattr(nodepool.spec.autoscaling, 'enabled') else False,
                    "scale_groups": scale_groups,  # 详细的伸缩组信息
                    "scale_group_statuses": scale_group_statuses,  # 伸缩组状态
                    "created_at": str(nodepool.metadata.creation_timestamp) if hasattr(nodepool, 'metadata') and hasattr(nodepool.metadata, 'creation_timestamp') else None,
                }
                nodepools.append(pool_info)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "list_cce_nodepools",
            "count": len(nodepools),
            "nodepools": nodepools
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def get_cce_kubeconfig(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, duration: int = 30) -> Dict[str, Any]:
    """Get kubeconfig for a CCE cluster

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        duration: Certificate validity duration in days (default: 30)

    Returns:
        Dictionary with kubeconfig content
    """
    # Auto-fetch project_id if not provided
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not proj_id:
        return {
            "success": False,
            "error": "Project ID not found. Please provide project_id parameter."
        }

    if not cluster_id:
        return {
            "success": False,
            "error": "cluster_id is required"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        from huaweicloudsdkcce.v3 import CreateKubernetesClusterCertRequest, ClusterCertDuration
        
        client = create_cce_client(region, access_key, secret_key, proj_id)
        
        # Create certificate request
        cert_duration = ClusterCertDuration(duration=duration)
        request = CreateKubernetesClusterCertRequest(cluster_id=cluster_id)
        request.body = cert_duration
        
        response = client.create_kubernetes_cluster_cert(request)
        
        result = {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "get_cce_kubeconfig",
            "duration_days": duration,
        }
        
        # Parse response
        if hasattr(response, 'to_dict'):
            resp_dict = response.to_dict()
            
            # Extract kubeconfig
            result["kubeconfig"] = resp_dict
            
            # Extract key information
            if 'clusters' in resp_dict:
                result["cluster_endpoints"] = []
                for cluster in resp_dict['clusters']:
                    endpoint_info = {
                        "name": cluster.get('name'),
                        "server": cluster.get('cluster', {}).get('server')
                    }
                    result["cluster_endpoints"].append(endpoint_info)
            
            if 'current_context' in resp_dict:
                result["current_context"] = resp_dict['current_context']
            
            # Generate YAML format kubeconfig
            import yaml
            result["kubeconfig_yaml"] = yaml.dump(resp_dict, default_flow_style=False, allow_unicode=True)
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def list_cce_addons(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """List addons (plugins) in a CCE cluster

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with addon list
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

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        from huaweicloudsdkcce.v3 import ListAddonInstancesRequest
        request = ListAddonInstancesRequest()
        request.cluster_id = cluster_id

        response = client.list_addon_instances(request)

        addons = []
        if hasattr(response, 'items') and response.items:
            for addon in response.items:
                addon_info = {
                    "name": addon.metadata.name if hasattr(addon, 'metadata') and hasattr(addon.metadata, 'name') else None,
                    "uid": addon.metadata.uid if hasattr(addon, 'metadata') and hasattr(addon.metadata, 'uid') else None,
                    "template_name": addon.spec.template_name if hasattr(addon, 'spec') and hasattr(addon.spec, 'template_name') else None,
                    "version": addon.spec.version if hasattr(addon, 'spec') and hasattr(addon.spec, 'version') else None,
                    "status": addon.status.status if hasattr(addon, 'status') and hasattr(addon.status, 'status') else None,
                    "description": addon.spec.description if hasattr(addon, 'spec') and hasattr(addon.spec, 'description') else None,
                    "created_at": str(addon.metadata.creation_timestamp) if hasattr(addon, 'metadata') and hasattr(addon.metadata, 'creation_timestamp') else None,
                }
                addons.append(addon_info)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "list_cce_addons",
            "count": len(addons),
            "addons": addons
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def resize_node_pool(region: str, cluster_id: str, nodepool_id: str, node_count: int, confirm: bool = False, scale_group_names: Optional[List[str]] = None, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Resize (scale up or down) a CCE node pool to the specified number of nodes

    ⚠️ 二次确认机制：
    - 第一步：不带 confirm 参数调用，返回确认提示
    - 第二步：带 confirm=true 再次调用，执行操作

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        nodepool_id: Node pool ID to resize
        node_count: Target node count (desired number of nodes)
        confirm: True to confirm and execute (default: False)
        scale_group_names: List of scale group names to use (default: ["default"])
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with operation result
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

    if not nodepool_id:
        return {
            "success": False,
            "error": "nodepool_id is required"
        }

    if node_count is None or node_count < 0:
        return {
            "success": False,
            "error": "node_count must be a non-negative integer"
        }

    # ========== 二次确认机制 ==========
    if not confirm:
        sg_note = f" (using scale groups: {', '.join(scale_group_names)})" if scale_group_names else ""
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "resize_nodepool",
            "warning": f"⚠️ 危险操作：即将调整节点池 '{nodepool_id}' 的节点数为 {node_count}{sg_note}",
            "cluster_id": cluster_id,
            "nodepool_id": nodepool_id,
            "target_node_count": node_count,
            "scale_group_names": scale_group_names,
            "hint": "确认操作请添加 confirm=true 参数",
            "note": "⚠️ 此操作会影响集群资源和计费！",
            "example": f"resize_node_pool region={region} cluster_id={cluster_id} nodepool_id={nodepool_id} node_count={node_count} scale_group_names={','.join(scale_group_names)} confirm=true" if scale_group_names else f"resize_node_pool region={region} cluster_id={cluster_id} nodepool_id={nodepool_id} node_count={node_count} confirm=true"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        # For testing, try both nodepool name and uid
        # First, get the nodepool details to get both name and uid
        nodepool_result = list_cce_node_pools(region, cluster_id, ak, sk, project_id)
        if not nodepool_result.get("success"):
            return nodepool_result
        
        # Find the target nodepool and get both name and uid
        target_nodepool = None
        nodepool_name = None
        nodepool_uid = None
        for np in nodepool_result.get("nodepools", []):
            np_id = np.get("id")
            np_name = np.get("name")
            if (np_id and np_id.strip() == nodepool_id.strip()) or (np_name and np_name.strip() == nodepool_id.strip()):
                target_nodepool = np
                nodepool_name = np_name
                nodepool_uid = np_id
                break
        if not target_nodepool:
            return {
                "success": False,
                "error": f"Node pool {nodepool_id} not found in cluster {cluster_id}"
            }
        
        # Use specified scale group names, default to ["default"]
        if not scale_group_names:
            scale_group_names = ["default"]

        client = create_cce_client(region, access_key, secret_key, proj_id)

        # Build the scale request using ScaleNodePool API
        # First try with nodepool_uid, then with nodepool_name
        request = ScaleNodePoolRequest()
        request.cluster_id = cluster_id
        request.nodepool_id = nodepool_uid
        
        # Create the scale body - using correct format from API
        scale_body = ScaleNodePoolRequestBody()
        scale_body.node_num = node_count
        scale_body.kind = 'NodePool'
        scale_body.api_version = 'v3'
        
        # Create spec with scale_groups
        spec = ScaleNodePoolSpec()
        spec.desired_node_count = node_count
        
        # Use dynamically retrieved scale_group_names
        spec.scale_groups = scale_group_names
        
        scale_body.spec = spec
        request.body = scale_body
        
        # First try with nodepool_uid
        try:
            response = client.scale_node_pool(request)
        except ClientRequestException as e:
            # If failed with uid, try with name
            if "Nodepool not found" in str(e) or "Invalid nodepool uuid" in str(e):
                request.nodepool_id = nodepool_name
                response = client.scale_node_pool(request)
            else:
                raise

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "nodepool_id": nodepool_id,
            "action": "resize_node_pool",
            "target_node_count": node_count,
            "scale_group_names_used": scale_group_names,
            "message": f"Node pool resize request submitted successfully",
            "response": response.to_dict() if hasattr(response, 'to_dict') else str(response)
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None),
            "hint": "Check if the target node count is valid for the node pool"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def _k8s_ts(value: Any) -> Optional[str]:
    return str(value) if value else None


def _k8s_resource_requirements(container: Any) -> Dict[str, Any]:
    resources = getattr(container, "resources", None)
    if not resources:
        return {}
    return {
        "requests": dict(getattr(resources, "requests", None) or {}),
        "limits": dict(getattr(resources, "limits", None) or {}),
    }


def _k8s_container_state(state: Any) -> Dict[str, Any]:
    if not state:
        return {}
    waiting = getattr(state, "waiting", None)
    running = getattr(state, "running", None)
    terminated = getattr(state, "terminated", None)
    if waiting:
        return {
            "type": "waiting",
            "reason": getattr(waiting, "reason", None),
            "message": getattr(waiting, "message", None),
        }
    if running:
        return {
            "type": "running",
            "started_at": _k8s_ts(getattr(running, "started_at", None)),
        }
    if terminated:
        return {
            "type": "terminated",
            "reason": getattr(terminated, "reason", None),
            "message": getattr(terminated, "message", None),
            "exit_code": getattr(terminated, "exit_code", None),
            "signal": getattr(terminated, "signal", None),
            "started_at": _k8s_ts(getattr(terminated, "started_at", None)),
            "finished_at": _k8s_ts(getattr(terminated, "finished_at", None)),
        }
    return {}


def _k8s_container_status(cs: Any, spec_by_name: Dict[str, Any]) -> Dict[str, Any]:
    spec = spec_by_name.get(getattr(cs, "name", ""))
    state_detail = _k8s_container_state(getattr(cs, "state", None))
    last_state_detail = _k8s_container_state(getattr(cs, "last_state", None))
    return {
        "name": getattr(cs, "name", None),
        "image": getattr(cs, "image", None) or getattr(spec, "image", None),
        "image_id": getattr(cs, "image_id", None),
        "container_id": getattr(cs, "container_id", None),
        "ready": getattr(cs, "ready", None),
        "started": getattr(cs, "started", None),
        "restart_count": getattr(cs, "restart_count", 0),
        "state": str(getattr(cs, "state", None)) if getattr(cs, "state", None) else None,
        "state_detail": state_detail,
        "last_state": str(getattr(cs, "last_state", None)) if getattr(cs, "last_state", None) else None,
        "last_state_detail": last_state_detail,
        "resources": _k8s_resource_requirements(spec),
    }


def _k8s_pod_conditions(conditions: Any) -> List[Dict[str, Any]]:
    result = []
    for condition in conditions or []:
        result.append({
            "type": getattr(condition, "type", None),
            "status": getattr(condition, "status", None),
            "reason": getattr(condition, "reason", None),
            "message": getattr(condition, "message", None),
            "last_transition_time": _k8s_ts(getattr(condition, "last_transition_time", None)),
        })
    return result


def _k8s_owner_references(owner_refs: Any) -> List[Dict[str, Any]]:
    result = []
    for ref in owner_refs or []:
        result.append({
            "kind": getattr(ref, "kind", None),
            "name": getattr(ref, "name", None),
            "uid": getattr(ref, "uid", None),
            "controller": getattr(ref, "controller", None),
        })
    return result


def get_kubernetes_pods(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None, labels: str = None) -> Dict[str, Any]:
    """Get pods in a CCE cluster

    Args:
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

    cert_file = None
    key_file = None

    try:
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint (accessible from public network)
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            # Fallback to internal cluster
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False  # Skip SSL verification for CCE

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = tempfile.mktemp(prefix="cce_pod_client_", suffix=".crt")
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = tempfile.mktemp(prefix="cce_pod_client_", suffix=".key")
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration and get pods
        k8s_client.Configuration.set_default(configuration)
        v1 = k8s_client.CoreV1Api()

        if namespace:
            # Get pods in specific namespace
            pods = v1.list_namespaced_pod(namespace, label_selector=labels)
        else:
            # Get pods in all namespaces
            pods = v1.list_pod_for_all_namespaces(label_selector=labels)

        pod_list = []
        for pod in pods.items:
            spec_containers = {c.name: c for c in (pod.spec.containers or [])}
            init_spec_containers = {c.name: c for c in (pod.spec.init_containers or [])} if pod.spec.init_containers else {}
            pod_info = {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "phase": pod.status.phase,
                "reason": pod.status.reason,
                "message": pod.status.message,
                "node": pod.spec.node_name,
                "ip": pod.status.pod_ip,
                "host_ip": pod.status.host_ip,
                "qos_class": pod.status.qos_class,
                "created": str(pod.metadata.creation_timestamp) if pod.metadata.creation_timestamp else None,
                "labels": pod.metadata.labels,
                "annotation_keys": sorted((pod.metadata.annotations or {}).keys()),
                "owner_references": _k8s_owner_references(pod.metadata.owner_references),
                "conditions": _k8s_pod_conditions(pod.status.conditions),
                "restart_policy": pod.spec.restart_policy,
                "service_account": pod.spec.service_account_name,
                "image_pull_secrets": [
                    item.name for item in (pod.spec.image_pull_secrets or []) if getattr(item, "name", None)
                ],
            }
            # Container info
            if pod.status.container_statuses:
                pod_info["containers"] = [
                    _k8s_container_status(cs, spec_containers)
                    for cs in pod.status.container_statuses
                ]
            else:
                pod_info["containers"] = []

            if pod.status.init_container_statuses:
                pod_info["init_containers"] = [
                    _k8s_container_status(cs, init_spec_containers)
                    for cs in pod.status.init_container_statuses
                ]
            else:
                pod_info["init_containers"] = []
            pod_list.append(pod_info)

        # 清理临时证书文件
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
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)

def get_kubernetes_namespaces(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get namespaces in a CCE cluster"""
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
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_ns_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_ns_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration and get namespaces
        k8s_client.Configuration.set_default(configuration)
        v1 = k8s_client.CoreV1Api()

        # Get all namespaces
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

        # 清理临时证书文件
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

def get_kubernetes_deployments(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None) -> Dict[str, Any]:
    """Get deployments in a CCE cluster"""
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
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_dep_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_dep_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration and get deployments
        k8s_client.Configuration.set_default(configuration)
        apps_v1 = k8s_client.AppsV1Api()

        # Get all deployments
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
            # 获取spec中的副本数
            if dep.spec:
                dep_info["desired_replicas"] = dep.spec.replicas
                dep_info["strategy"] = dep.spec.strategy.type if dep.spec.strategy else None
            dep_list.append(dep_info)

        # 清理临时证书文件
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

def scale_cce_workload(region: str, cluster_id: str, workload_type: str, name: str, namespace: str, replicas: int, confirm: bool = False, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Scale a CCE workload (Deployment or StatefulSet) to the specified number of replicas

    ⚠️ 二次确认机制：
    - 第一步：不带 confirm 参数调用，返回确认提示
    - 第二步：带 confirm=true 再次调用，执行操作
    
    Example:
        # 第一步：预览操作
        scale_cce_workload region=xxx cluster_id=xxx workload_type=deployment name=my-app namespace=default replicas=3
        
        # 第二步：确认执行
        scale_cce_workload region=xxx cluster_id=xxx workload_type=deployment name=my-app namespace=default replicas=3 confirm=true

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        workload_type: Type of workload - 'deployment' or 'statefulset'
        name: Name of the workload
        namespace: Kubernetes namespace
        replicas: Target number of replicas
        confirm: True to confirm and execute (default: False)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with scaling result
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

    if not name or not namespace:
        return {
            "success": False,
            "error": "name and namespace are required"
        }

    if workload_type not in ['deployment', 'statefulset']:
        return {
            "success": False,
            "error": "workload_type must be 'deployment' or 'statefulset'"
        }

    if replicas is None or replicas < 0:
        return {
            "success": False,
            "error": "replicas must be a non-negative integer"
        }

    # ========== 二次确认机制 ==========
    if not confirm:
        # 第一步：返回确认提示
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "scale_workload",
            "warning": f"⚠️ 危险操作：即将修改 {workload_type} '{name}' (命名空间: {namespace}) 的副本数为 {replicas}",
            "cluster_id": cluster_id,
            "namespace": namespace,
            "name": name,
            "workload_type": workload_type,
            "target_replicas": replicas,
            "hint": "确认操作请添加 confirm=true 参数",
            "example": f"scale_cce_workload region={region} cluster_id={cluster_id} workload_type={workload_type} name={name} namespace={namespace} replicas={replicas} confirm=true"
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
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_scale_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_scale_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration
        k8s_client.Configuration.set_default(configuration)

        # Scale the workload
        if workload_type == 'deployment':
            apps_v1 = k8s_client.AppsV1Api()
            # Get current deployment
            deployment = apps_v1.read_namespaced_deployment(name, namespace)
            old_replicas = deployment.spec.replicas

            # Update replicas
            deployment.spec.replicas = replicas
            apps_v1.replace_namespaced_deployment(name, namespace, deployment)

            return {
                "success": True,
                "region": region,
                "cluster_id": cluster_id,
                "action": "scale_deployment",
                "workload_type": "deployment",
                "name": name,
                "namespace": namespace,
                "old_replicas": old_replicas,
                "new_replicas": replicas,
                "message": f"Deployment '{name}' scaled from {old_replicas} to {replicas} replicas"
            }

        elif workload_type == 'statefulset':
            apps_v1 = k8s_client.AppsV1Api()
            # Get current statefulset
            statefulset = apps_v1.read_namespaced_stateful_set(name, namespace)
            old_replicas = statefulset.spec.replicas

            # Update replicas
            statefulset.spec.replicas = replicas
            apps_v1.replace_namespaced_stateful_set(name, namespace, statefulset)

            return {
                "success": True,
                "region": region,
                "cluster_id": cluster_id,
                "action": "scale_statefulset",
                "workload_type": "statefulset",
                "name": name,
                "namespace": namespace,
                "old_replicas": old_replicas,
                "new_replicas": replicas,
                "message": f"StatefulSet '{name}' scaled from {old_replicas} to {replicas} replicas"
            }

        # 清理临时证书文件
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def resize_cce_workload(region: str, cluster_id: str, workload_type: str, name: str, namespace: str,
                       replicas: Optional[int] = None,
                       cpu_limit: Optional[str] = None, memory_limit: Optional[str] = None,
                       cpu_request: Optional[str] = None, memory_request: Optional[str] = None,
                       confirm: bool = False,
                       ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Resize a CCE workload: adjust replicas and/or resource limits (CPU/memory)

    ⚠️ 二次确认机制：
    - 第一步：不带 confirm 参数调用，返回当前配置和变更预览
    - 第二步：带 confirm=true 再次调用，执行操作

    支持的参数（均可选，至少提供一个）：
    - replicas: 副本数
    - cpu_limit: CPU limit（如 "4", "2", "500m"）
    - memory_limit: 内存 limit（如 "1Gi", "512Mi"）
    - cpu_request: CPU request（如 "100m", "500m"）
    - memory_request: 内存 request（如 "512Mi", "1Gi"）

    Example:
        # 第一步：预览操作
        resize_cce_workload region=xxx cluster_id=xxx workload_type=deployment name=nginx namespace=default cpu_limit=4

        # 第二步：确认执行
        resize_cce_workload region=xxx cluster_id=xxx workload_type=deployment name=nginx namespace=default cpu_limit=4 confirm=true

    Args:
        region: Huawei Cloud region (e.g. cn-north-4)
        cluster_id: CCE cluster ID
        workload_type: 'deployment' or 'statefulset'
        name: Workload name
        namespace: Kubernetes namespace
        replicas: Target replicas (optional)
        cpu_limit: CPU limit string (optional)
        memory_limit: Memory limit string (optional)
        cpu_request: CPU request string (optional)
        memory_request: Memory request string (optional)
        confirm: True to confirm and execute (default: False)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with resize result
    """
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    if not name or not namespace:
        return {"success": False, "error": "name and namespace are required"}

    if workload_type not in ['deployment', 'statefulset']:
        return {"success": False, "error": "workload_type must be 'deployment' or 'statefulset'"}

    # 至少需要一个变更参数
    change_params = {k: v for k, v in [('replicas', replicas), ('cpu_limit', cpu_limit),
                                        ('memory_limit', memory_limit), ('cpu_request', cpu_request),
                                        ('memory_request', memory_request)] if v is not None}
    if not change_params:
        return {"success": False, "error": "At least one of replicas/cpu_limit/memory_limit/cpu_request/memory_request must be specified"}

    if not K8S_AVAILABLE:
        return {"success": False, "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"}

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    cert_file = None
    key_file = None

    try:
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break
        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]
        if not external_cluster:
            return {"success": False, "error": "Could not find cluster endpoint"}

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = f'/tmp/cce_resize_client_{os.getpid()}.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = f'/tmp/cce_resize_client_{os.getpid()}.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        k8s_client.Configuration.set_default(configuration)
        apps_v1 = k8s_client.AppsV1Api()

        # 读取当前工作负载
        if workload_type == 'deployment':
            workload_obj = apps_v1.read_namespaced_deployment(name, namespace)
        else:
            workload_obj = apps_v1.read_namespaced_stateful_set(name, namespace)

        # 收集当前配置
        old_replicas = workload_obj.spec.replicas
        containers = workload_obj.spec.template.spec.containers
        old_resources = {}
        for c in containers:
            res = c.resources
            old_limits = dict(res.limits) if res and res.limits else {}
            old_requests = dict(res.requests) if res and res.requests else {}
            old_resources[c.name] = {
                'limits': old_limits,
                'requests': old_requests
            }

        # ========== 二次确认机制 ==========
        if not confirm:
            changes_desc = []
            if replicas is not None:
                changes_desc.append(f"replicas: {old_replicas} → {replicas}")
            if cpu_limit is not None:
                old_val = old_resources.get(containers[0].name, {}).get('limits', {}).get('cpu', 'unset')
                changes_desc.append(f"cpu_limit: {old_val} → {cpu_limit}")
            if memory_limit is not None:
                old_val = old_resources.get(containers[0].name, {}).get('limits', {}).get('memory', 'unset')
                changes_desc.append(f"memory_limit: {old_val} → {memory_limit}")
            if cpu_request is not None:
                old_val = old_resources.get(containers[0].name, {}).get('requests', {}).get('cpu', 'unset')
                changes_desc.append(f"cpu_request: {old_val} → {cpu_request}")
            if memory_request is not None:
                old_val = old_resources.get(containers[0].name, {}).get('requests', {}).get('memory', 'unset')
                changes_desc.append(f"memory_request: {old_val} → {memory_request}")

            return {
                "success": False,
                "requires_confirmation": True,
                "operation": "resize_workload",
                "warning": f"⚠️ 危险操作：即将修改 {workload_type} '{name}' (命名空间: {namespace}) 的资源配置",
                "cluster_id": cluster_id,
                "namespace": namespace,
                "name": name,
                "workload_type": workload_type,
                "current_config": {
                    "replicas": old_replicas,
                    "containers": old_resources
                },
                "changes": changes_desc,
                "hint": "确认操作请添加 confirm=true 参数",
                "example": f"resize_cce_workload region={region} cluster_id={cluster_id} workload_type={workload_type} name={name} namespace={namespace} " + " ".join(f"{k}={v}" for k, v in change_params.items()) + " confirm=true"
            }

        # ========== 执行变更 ==========
        # 修改副本数
        if replicas is not None:
            workload_obj.spec.replicas = replicas

        # 修改容器资源 (应用到第一个容器，如需指定可用 container_name 参数扩展)
        for container in containers:
            if container.resources is None:
                container.resources = k8s_client.V1ResourceRequirements()
            if container.resources.limits is None:
                container.resources.limits = {}
            if container.resources.requests is None:
                container.resources.requests = {}

            if cpu_limit is not None:
                container.resources.limits['cpu'] = cpu_limit
            if memory_limit is not None:
                container.resources.limits['memory'] = memory_limit
            if cpu_request is not None:
                container.resources.requests['cpu'] = cpu_request
            if memory_request is not None:
                container.resources.requests['memory'] = memory_request

        # 提交更新
        if workload_type == 'deployment':
            apps_v1.replace_namespaced_deployment(name, namespace, workload_obj)
        else:
            apps_v1.replace_namespaced_stateful_set(name, namespace, workload_obj)

        # 读取更新后的配置
        if workload_type == 'deployment':
            new_obj = apps_v1.read_namespaced_deployment(name, namespace)
        else:
            new_obj = apps_v1.read_namespaced_stateful_set(name, namespace)

        new_resources = {}
        for c in new_obj.spec.template.spec.containers:
            res = c.resources
            new_limits = dict(res.limits) if res and res.limits else {}
            new_requests = dict(res.requests) if res and res.requests else {}
            new_resources[c.name] = {
                'limits': new_limits,
                'requests': new_requests
            }

        # 清理临时证书
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": f"resize_{workload_type}",
            "workload_type": workload_type,
            "name": name,
            "namespace": namespace,
            "old_replicas": old_replicas,
            "new_replicas": new_obj.spec.replicas,
            "old_resources": old_resources,
            "new_resources": new_resources,
            "message": f"{workload_type.capitalize()} '{name}' resized successfully"
        }

    except Exception as e:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def delete_cce_workload(region: str, cluster_id: str, workload_type: str, name: str, namespace: str, confirm: bool = False, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Delete a CCE workload (Deployment or StatefulSet)

    ⚠️ 二次确认机制：
    - 第一步：不带 confirm 参数调用，返回确认提示
    - 第二步：带 confirm=true 再次调用，执行操作
    
    WARNING: 此操作将删除工作负载及其所有 Pod，不可恢复！

    Example:
        # 第一步：预览操作
        delete_cce_workload region=xxx cluster_id=xxx workload_type=deployment name=my-app namespace=default
        
        # 第二步：确认执行
        delete_cce_workload region=xxx cluster_id=xxx workload_type=deployment name=my-app namespace=default confirm=true

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        workload_type: Type of workload - 'deployment' or 'statefulset'
        name: Name of the workload to delete
        namespace: Kubernetes namespace
        confirm: True to confirm and execute (default: False)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with deletion result
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

    if not name or not namespace:
        return {
            "success": False,
            "error": "name and namespace are required"
        }

    if workload_type not in ['deployment', 'statefulset']:
        return {
            "success": False,
            "error": "workload_type must be 'deployment' or 'statefulset'"
        }

    # ========== 二次确认机制 ==========
    if not confirm:
        # 第一步：返回确认提示
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "delete_workload",
            "warning": f"⚠️ 危险操作：即将删除 {workload_type} '{name}' (命名空间: {namespace}) 及其所有 Pod",
            "cluster_id": cluster_id,
            "namespace": namespace,
            "name": name,
            "workload_type": workload_type,
            "hint": "确认操作请添加 confirm=true 参数",
            "note": "⚠️ 此操作不可恢复！",
            "example": f"delete_cce_workload region={region} cluster_id={cluster_id} workload_type={workload_type} name={name} namespace={namespace} confirm=true"
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
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_del_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_del_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration
        k8s_client.Configuration.set_default(configuration)

        # Delete the workload
        if workload_type == 'deployment':
            apps_v1 = k8s_client.AppsV1Api()
            apps_v1.delete_namespaced_deployment(name, namespace)

            return {
                "success": True,
                "region": region,
                "cluster_id": cluster_id,
                "action": "delete_deployment",
                "workload_type": "deployment",
                "name": name,
                "namespace": namespace,
                "message": f"Deployment '{name}' in namespace '{namespace}' deleted successfully"
            }

        elif workload_type == 'statefulset':
            apps_v1 = k8s_client.AppsV1Api()
            apps_v1.delete_namespaced_stateful_set(name, namespace)

            return {
                "success": True,
                "region": region,
                "cluster_id": cluster_id,
                "action": "delete_statefulset",
                "workload_type": "statefulset",
                "name": name,
                "namespace": namespace,
                "message": f"StatefulSet '{name}' in namespace '{namespace}' deleted successfully"
            }

        # 清理临时证书文件
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def get_kubernetes_nodes(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get nodes in a CCE cluster"""
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
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
            "success": False,
            "error": "Could not find cluster endpoint"
        }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_node_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_node_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration and get nodes
        k8s_client.Configuration.set_default(configuration)
        v1 = k8s_client.CoreV1Api()

        # Get all nodes
        nodes = v1.list_node()

        node_list = []
        for node in nodes.items:
            # Get conditions
            ready = "Unknown"
            conditions = []
            for c in node.status.conditions:
                condition_info = {
                    "type": getattr(c, "type", None),
                    "status": getattr(c, "status", None),
                    "reason": getattr(c, "reason", None),
                    "message": getattr(c, "message", None),
                    "last_heartbeat_time": str(getattr(c, "last_heartbeat_time", None)) if getattr(c, "last_heartbeat_time", None) else None,
                    "last_transition_time": str(getattr(c, "last_transition_time", None)) if getattr(c, "last_transition_time", None) else None,
                }
                conditions.append(condition_info)
                if c.type == 'Ready':
                    ready = c.status

            # Get capacity
            cpu = node.status.capacity.get('cpu', 'unknown') if node.status.capacity else 'unknown'
            memory = node.status.capacity.get('memory', 'unknown') if node.status.capacity else 'unknown'
            pods = node.status.capacity.get('pods', 'unknown') if node.status.capacity else 'unknown'

            # Get allocatable
            allocatable_cpu = node.status.allocatable.get('cpu', 'unknown') if node.status.allocatable else 'unknown'
            allocatable_memory = node.status.allocatable.get('memory', 'unknown') if node.status.allocatable else 'unknown'

            # Get node info
            node_info = {
                "name": node.metadata.name,
                "ready": ready,
                "cpu": cpu,
                "memory": memory,
                "max_pods": pods,
                "allocatable_cpu": allocatable_cpu,
                "allocatable_memory": allocatable_memory,
                "created": str(node.metadata.creation_timestamp) if node.metadata.creation_timestamp else None,
                "labels": node.metadata.labels,
                "conditions": conditions,
            }
            condition_map = {cond.get("type"): cond.get("status") for cond in conditions}
            node_info["memory_pressure"] = condition_map.get("MemoryPressure")
            node_info["disk_pressure"] = condition_map.get("DiskPressure")
            node_info["pid_pressure"] = condition_map.get("PIDPressure")
            node_info["network_unavailable"] = condition_map.get("NetworkUnavailable")

            # Get taints
            if node.spec:
                if node.spec.taints:
                    taints = []
                    for taint in node.spec.taints:
                        taints.append({
                            "key": taint.key,
                            "value": taint.value,
                            "effect": taint.effect,
                        })
                    node_info["taints"] = taints
                else:
                    node_info["taints"] = []

            # Get internal IP
            if node.status.addresses:
                for addr in node.status.addresses:
                    if addr.type == 'InternalIP':
                        node_info["internal_ip"] = addr.address
                    elif addr.type == 'Hostname':
                        node_info["hostname"] = addr.address

            node_list.append(node_info)

        # 清理临时证书文件
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)
        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "get_cce_nodes",
            "count": len(node_list),
            "nodes": node_list
        }

        

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def get_kubernetes_events(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None, limit: int = 500) -> Dict[str, Any]:
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
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_event_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_event_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration and get events
        k8s_client.Configuration.set_default(configuration)
        v1 = k8s_client.CoreV1Api()

        # Collect events with pagination
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

        # 清理临时证书文件
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

def get_kubernetes_pvcs(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None) -> Dict[str, Any]:
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
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_pvc_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_pvc_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration and get PVCs
        k8s_client.Configuration.set_default(configuration)
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
            # PV details
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

        # 清理临时证书文件
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

def get_kubernetes_pvs(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
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
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_pv_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_pv_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration and get PVs
        k8s_client.Configuration.set_default(configuration)
        v1 = k8s_client.CoreV1Api()

        pvs = v1.list_persistent_volume()

        pv_list = []
        for pv in pvs.items:
            # Get capacity from status
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
            # PV claim ref
            if pv.spec.claim_ref:
                pv_info["claim_ref"] = {
                    "namespace": pv.spec.claim_ref.namespace,
                    "name": pv.spec.claim_ref.name,
                }
            # PV source details - use hasattr to check attributes
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

        # 清理临时证书文件
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

def get_kubernetes_services(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None) -> Dict[str, Any]:
    """Get services in a CCE cluster
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        namespace: Kubernetes namespace (optional, defaults to all namespaces)
    
    Returns:
        Dict with success status and list of services
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

    cert_file = None
    key_file = None

    try:
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_client_service.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_client_service.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # Create API client
        k8s_client.Configuration.set_default(configuration)
        core_v1 = k8s_client.CoreV1Api()

        # Get services
        service_list = []
        if namespace:
            services = core_v1.list_namespaced_service(namespace)
        else:
            services = core_v1.list_service_for_all_namespaces()

        for svc in services.items:
            # Build service info
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

            # Extract LoadBalancer info
            if svc.spec.type == "LoadBalancer":
                if svc.status.load_balancer and svc.status.load_balancer.ingress:
                    for ingress in svc.status.load_balancer.ingress:
                        svc_info["load_balancer_ingress"].append({
                            "ip": ingress.ip,
                            "hostname": ingress.hostname
                        })
                    if svc_info["load_balancer_ingress"]:
                        svc_info["load_balancer_ip"] = svc_info["load_balancer_ingress"][0].get("ip")

            # Extract ports
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

        # Cleanup
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

def get_kubernetes_ingresses(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None) -> Dict[str, Any]:
    """Get ingresses in a CCE cluster
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        namespace: Kubernetes namespace (optional, defaults to all namespaces)
    
    Returns:
        Dict with success status and list of ingresses
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

    cert_file = None
    key_file = None

    try:
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_client_ingress.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_client_ingress.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # Create API client
        k8s_client.Configuration.set_default(configuration)
        networking_v1 = k8s_client.NetworkingV1Api()

        # Get ingresses
        ingress_list = []
        if namespace:
            ingresses = networking_v1.list_namespaced_ingress(namespace)
        else:
            ingresses = networking_v1.list_ingress_for_all_namespaces()

        for ingress in ingresses.items:
            # Build ingress info
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

            # Extract default backend
            if ingress.spec.default_backend:
                ingress_info["default_backend"] = {
                    "service_name": ingress.spec.default_backend.service.name if ingress.spec.default_backend.service else None,
                    "service_port": ingress.spec.default_backend.service.port.number if ingress.spec.default_backend.service and ingress.spec.default_backend.service.port else None
                }

            # Extract rules
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

            # Extract TLS
            if ingress.spec.tls:
                for tls in ingress.spec.tls:
                    tls_info = {
                        "hosts": tls.hosts,
                        "secret_name": tls.secret_name
                    }
                    ingress_info["tls"].append(tls_info)

            # Extract LoadBalancer ingress status
            if ingress.status.load_balancer and ingress.status.load_balancer.ingress:
                for lb_ingress in ingress.status.load_balancer.ingress:
                    ingress_info["load_balancer_ingress"].append({
                        "ip": lb_ingress.ip,
                        "hostname": lb_ingress.hostname
                    })

            ingress_list.append(ingress_info)

        # Cleanup
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

def list_cce_configmaps(region: str, cluster_id: str, namespace: Optional[str] = None, limit: int = 100, offset: int = 0, include_data: bool = False, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """List ConfigMaps in a CCE cluster
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        namespace: Kubernetes namespace (optional, default: all namespaces)
        limit: Number of results to return (default: 100)
        offset: Pagination offset (default: 0)
        include_data: Whether to include ConfigMap data content (default: False, only return keys)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with configmaps list
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

    try:
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_configmaps_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_configmaps_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration
        k8s_client.Configuration.set_default(configuration)

        # List configmaps
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

        # 清理临时证书文件
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
    """List Secrets in a CCE Kubernetes cluster
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        namespace: Kubernetes namespace (optional, default: all namespaces)
        limit: Number of results to return (default: 100)
        include_data: Whether to include Secret data content (default: False, only return keys)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with secrets list
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

    try:
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_secrets_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_secrets_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration
        k8s_client.Configuration.set_default(configuration)

        # List secrets
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

        # 清理临时证书文件
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
    """List DaemonSets in a CCE Kubernetes cluster
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        namespace: Kubernetes namespace (optional, default: all namespaces)
        limit: Number of results to return (default: 100)
        include_data: Whether to include full spec content (default: False)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with daemonsets list
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

    try:
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_daemonsets_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_daemonsets_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration
        k8s_client.Configuration.set_default(configuration)

        # List daemonsets
        apps_v1 = k8s_client.AppsV1Api()
        if namespace:
            daemonsets = apps_v1.list_namespaced_daemon_set(namespace, limit=limit)
        else:
            daemonsets = apps_v1.list_daemon_set_for_all_namespaces(limit=limit)

        daemonset_list = []
        for ds in daemonsets.items:
            # Extract images
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

        # 清理临时证书文件
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
    """List StatefulSets in a CCE Kubernetes cluster
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        namespace: Kubernetes namespace (optional, default: all namespaces)
        limit: Number of results to return (default: 100)
        include_data: Whether to include full spec content (default: False)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with statefulsets list
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

    try:
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Write certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            cert_file = '/tmp/cce_statefulsets_client.crt'
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            key_file = '/tmp/cce_statefulsets_client.key'
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        # 注册临时证书文件以便后续清理
        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        # Set default configuration
        k8s_client.Configuration.set_default(configuration)

        # List statefulsets
        apps_v1 = k8s_client.AppsV1Api()
        if namespace:
            statefulsets = apps_v1.list_namespaced_stateful_set(namespace, limit=limit)
        else:
            statefulsets = apps_v1.list_stateful_set_for_all_namespaces(limit=limit)

        statefulset_list = []
        for sts in statefulsets.items:
            # Extract images
            images = []
            if hasattr(sts.spec, 'template') and hasattr(sts.spec.template, 'spec') and hasattr(sts.spec.template.spec, 'containers'):
                for container in sts.spec.template.spec.containers:
                    images.append(container.image)
            
            # Extract volume claim templates
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

        # 清理临时证书文件
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


def hibernate_cce_cluster(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    confirm: bool = False,
) -> Dict[str, Any]:
    """Hibernate a CCE cluster (pause billing + workloads)

    Puts the cluster into hibernated state. Billing for control plane is paused.
    Workloads are stopped. Use awake_cce_cluster to resume.

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        confirm: Must be True to confirm the operation

    Returns:
        Dictionary with result
    """
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "hibernate_cce_cluster",
            "cluster_id": cluster_id,
            "error": f"Hibernate will pause cluster {cluster_id} and stop all workloads. Billing for control plane is paused.",
            "hint": f"Add confirm=true to confirm. Example: huawei_hibernate_cce_cluster region=cn-north-4 cluster_id=xxx confirm=true"
        }

    try:
        from huaweicloudsdkcce.v3 import HibernateClusterRequest

        client = create_cce_client(region, access_key, secret_key, proj_id)
        request = HibernateClusterRequest()
        request.cluster_id = cluster_id
        response = client.hibernate_cluster(request)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "hibernate_cce_cluster",
            "message": "Cluster hibernation request submitted successfully",
            "status_code": response.status_code if hasattr(response, "status_code") else None,
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, "request_id", None),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


def awake_cce_cluster(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    confirm: bool = False,
) -> Dict[str, Any]:
    """Awake a hibernated CCE cluster (resume billing + workloads)

    Wakes up a previously hibernated cluster. Billing for control plane resumes
    and workloads will be restarted.

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        confirm: Must be True to confirm the operation

    Returns:
        Dictionary with result
    """
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "operation": "awake_cce_cluster",
            "cluster_id": cluster_id,
            "error": f"Awake will resume cluster {cluster_id}. Control plane billing resumes and workloads restart.",
            "hint": f"Add confirm=true to confirm. Example: huawei_awake_cce_cluster region=cn-north-4 cluster_id=xxx confirm=true"
        }

    try:
        from huaweicloudsdkcce.v3 import AwakeClusterRequest

        client = create_cce_client(region, access_key, secret_key, proj_id)
        request = AwakeClusterRequest()
        request.cluster_id = cluster_id
        response = client.awake_cluster(request)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "awake_cce_cluster",
            "message": "Cluster awake request submitted successfully",
            "status_code": response.status_code if hasattr(response, "status_code") else None,
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, "request_id", None),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


def list_cce_cronjobs(
    region: str,
    cluster_id: str,
    namespace: str = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """List CronJobs in a CCE cluster

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        namespace: Kubernetes namespace (optional, default: all namespaces)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with list of CronJobs
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
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        cert_file = '/tmp/cce_cronjob_client.crt'
        key_file = '/tmp/cce_cronjob_client.key'

        if user_data and user_data.get('client_certificate_data'):
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file

        if user_data and user_data.get('client_key_data'):
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file

        _register_cert_file(cert_file)
        _register_cert_file(key_file)

        k8s_client.Configuration.set_default(configuration)
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

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, "request_id", None),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


def get_pod_logs(
    region: str,
    cluster_id: str,
    pod_name: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    namespace: str = "default",
    container: Optional[str] = None,
    previous: bool = False,
    tail_lines: int = 100
) -> Dict[str, Any]:
    """Get logs from a pod in a CCE cluster (simulates kubectl logs)
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        pod_name: Name of the pod
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        namespace: Pod namespace (default: "default")
        container: Container name (optional, returns first container if not specified)
        previous: Get logs from previous terminated container (default: False)
        tail_lines: Number of lines to return from the end (default: 100)
    
    Returns:
        Dictionary with success status and logs content
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

    if not pod_name:
        return {
            "success": False,
            "error": "pod_name is required"
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
    temp_files = []

    try:
        # Get cluster credentials
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)

        cert_request = CreateKubernetesClusterCertRequest()
        cert_request.cluster_id = cluster_id
        body = ClusterCertDuration()
        body.duration = 1
        cert_request.body = body

        cert_response = cce_client.create_kubernetes_cluster_cert(cert_request)
        kubeconfig_data = cert_response.to_dict()

        # Find external cluster endpoint
        external_cluster = None
        for c in kubeconfig_data.get('clusters', []):
            if 'external' in c.get('name', '') and 'TLS' not in c.get('name', ''):
                external_cluster = c
                break

        if not external_cluster:
            external_cluster = kubeconfig_data.get('clusters', [{}])[0]

        if not external_cluster:
            return {
                "success": False,
                "error": "Could not find cluster endpoint"
            }

        # Configure Kubernetes client
        configuration = k8s_client.Configuration()
        configuration.host = external_cluster.get('cluster', {}).get('server')
        configuration.verify_ssl = False

        # Set certificates
        user_data = None
        for u in kubeconfig_data.get('users', []):
            if u.get('name') == 'user':
                user_data = u.get('user', {})
                break

        if user_data and user_data.get('client_certificate_data'):
            import tempfile
            cert_file = tempfile.mktemp(suffix=".crt")
            with open(cert_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_certificate_data']))
            configuration.cert_file = cert_file
            temp_files.append(cert_file)
            _register_cert_file(cert_file)

        if user_data and user_data.get('client_key_data'):
            key_file = tempfile.mktemp(suffix=".key")
            with open(key_file, 'wb') as f:
                f.write(base64.b64decode(user_data['client_key_data']))
            configuration.key_file = key_file
            temp_files.append(key_file)
            _register_cert_file(key_file)

        # Set default configuration and get logs
        k8s_client.Configuration.set_default(configuration)
        v1 = k8s_client.CoreV1Api()

        try:
            import json
            log_content = v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                container=container,
                follow=False,
                tail_lines=tail_lines,
                previous=previous
            )

            return {
                "success": True,
                "region": region,
                "cluster_id": cluster_id,
                "action": "get_pod_logs",
                "pod_name": pod_name,
                "namespace": namespace,
                "container": container,
                "tail_lines": tail_lines,
                "previous": previous,
                "logs": log_content
            }

        except k8s_client.rest.ApiException as api_err:
            error_body = json.loads(api_err.body) if api_err.body else {}
            return {
                "success": False,
                "error": error_body.get("message", str(api_err.reason)),
                "error_type": "ApiException",
                "status": api_err.status
            }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, "request_id", None),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }

    finally:
        # Cleanup temporary certificate files
        for f in temp_files:
            _safe_delete_file(f)


# ---- CCE Node Operations ----

def _node_operation(region: str, cluster_id: str, node_name: str, operation: str,
                   confirm: bool = False, ak: Optional[str] = None, sk: Optional[str] = None,
                   project_id: str = None) -> Dict[str, Any]:
    """Internal helper for CCE node operations (cordon/uncordon/drain/status)

    Args:
        region: Huawei Cloud region
        cluster_id: CCE cluster ID
        node_name: Node name or IP address
        operation: One of 'cordon', 'uncordon', 'drain', 'status'
        confirm: Required for write operations (cordon/uncordon/drain)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with operation result
    """
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided."}

    if not K8S_AVAILABLE:
        return {"success": False, "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"}

    # Temp file paths (must be defined before try block for finally cleanup)
    ca_cert_file = client_cert_file = client_key_file = None

    try:
        # Get cluster kubeconfig
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)
        from huaweicloudsdkcce.v3 import CreateKubernetesClusterCertRequest, ClusterCertDuration
        cert_req = CreateKubernetesClusterCertRequest(cluster_id=cluster_id)
        cert_req.body = ClusterCertDuration(duration=1)
        kubeconfig_data = cce_client.create_kubernetes_cluster_cert(cert_req).to_dict()

        kubeconfig_str = kubeconfig_data.get("kubeconfig") or kubeconfig_data.get("content", "")
        import tempfile, os, kubernetes
        with tempfile.NamedTemporaryFile(mode='w', suffix='.kubeconfig', delete=False) as f:
            f.write(kubeconfig_str)
            cert_file = f.name

        try:
            import kubernetes as k8s
            from kubernetes.client import Configuration, CoreV1Api
            import yaml, base64

            # kubeconfig_data structure: SDK returns flat dict (not nested under 'kubeconfig' key)
            raw_kc = kubeconfig_data.get("kubeconfig") or kubeconfig_data.get("content", "") or kubeconfig_data
            kc = yaml.safe_load(raw_kc) if isinstance(raw_kc, str) and raw_kc else raw_kc
            # Get current context and resolve to cluster/user
            current_ctx = kc.get('current_context', '')
            ctx_entry = next((c for c in kc.get('contexts', []) if c['name'] == current_ctx), None)
            if not ctx_entry:
                return {"success": False, "error": f"Context '{current_ctx}' not found in kubeconfig"}
            cluster_name = ctx_entry['context']['cluster']
            user_name = ctx_entry['context']['user']

            # Get cluster config
            cluster_entry = next((c for c in kc.get('clusters', []) if c['name'] == cluster_name), None)
            if not cluster_entry:
                return {"success": False, "error": f"Cluster '{cluster_name}' not found in kubeconfig"}
            cluster_cfg = cluster_entry['cluster']

            # Get user config
            user_entry = next((u for u in kc.get('users', []) if u['name'] == user_name), None)
            if not user_entry:
                return {"success": False, "error": f"User '{user_name}' not found in kubeconfig"}
            user_cfg = user_entry['user']

            # Extract server (prefer current context; fallback to clusters[0] for compatibility)
            server = cluster_cfg.get('server', '')

            # Write certs to temp files
            ca_cert_file = None
            client_cert_file = None
            client_key_file = None

            ca_data = cluster_cfg.get('certificate_authority_data')
            if ca_data:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.crt', delete=False) as f:
                    f.write(base64.b64decode(ca_data).decode())
                    ca_cert_file = f.name

            cert_data = user_cfg.get('client_certificate_data')
            key_data = user_cfg.get('client_key_data')
            if cert_data and key_data:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.crt', delete=False) as f:
                    f.write(base64.b64decode(cert_data).decode())
                    client_cert_file = f.name
                with tempfile.NamedTemporaryFile(mode='w', suffix='.key', delete=False) as f:
                    f.write(base64.b64decode(key_data).decode())
                    client_key_file = f.name

            # Determine if skip TLS verify (only for 'external' context which has insecure_skip_tls_verify=true)
            skip_tls = cluster_cfg.get('insecure_skip_tls_verify', False)

            # Create configuration with explicit certs
            config = Configuration()
            config.host = server
            config.verify_ssl = not skip_tls
            if ca_cert_file:
                config.ssl_ca_cert = ca_cert_file
            if client_cert_file:
                config.cert_file = client_cert_file
            if client_key_file:
                config.key_file = client_key_file

            api_client = k8s.client.ApiClient(config)
            core_v1 = CoreV1Api(api_client)

            if operation == 'status':
                node = core_v1.read_node(node_name)
                conditions = {c.type: c.status for c in node.status.conditions}
                node_labels = dict(node.metadata.labels) if node.metadata.labels else {}
                return {
                    "success": True, "operation": "status", "node": node_name,
                    "schedulable": node.spec.unschedulable is None,
                    "ready": conditions.get("Ready") == "True", "conditions": conditions,
                    "os_version": node_labels.get("node.kubernetes.io/os_version", ""),
                    "kernel_version": node_labels.get("node.kubernetes.io/kernel_version", ""),
                }
            elif operation == 'cordon':
                if not confirm:
                    return {
                        "success": False, "requires_confirmation": True,
                        "operation": "cordon", "node": node_name,
                        "error": f"Cordon will mark node {node_name} as unschedulable.",
                        "hint": f"Add confirm=true to confirm. Example: cce_node_cordon region=cn-north-4 cluster_id=xxx node_name=192.168.x.x confirm=true"
                    }
                core_v1.patch_node(node_name, {'spec': {'unschedulable': True}})
                return {"success": True, "operation": "cordon", "node": node_name, "message": "Node marked as unschedulable"}
            elif operation == 'uncordon':
                if not confirm:
                    return {
                        "success": False, "requires_confirmation": True,
                        "operation": "uncordon", "node": node_name,
                        "error": f"Uncordon will mark node {node_name} as schedulable. New pods may be immediately assigned.",
                        "hint": f"Add confirm=true to confirm. Example: cce_node_uncordon region=cn-north-4 cluster_id=xxx node_name=192.168.x.x confirm=true"
                    }
                core_v1.patch_node(node_name, {'spec': {'unschedulable': None}})
                return {"success": True, "operation": "uncordon", "node": node_name, "message": "Node marked as schedulable"}
            elif operation == 'drain':
                if not confirm:
                    pods_preview = core_v1.list_pod_for_all_namespaces(field_selector=f'spec.nodeName={node_name}').items
                    affected = [f"{p.metadata.namespace}/{p.metadata.name}"
                                for p in pods_preview
                                if p.metadata.namespace not in ('kube-system', 'hss', 'monitoring')]
                    return {
                        "success": False, "requires_confirmation": True,
                        "operation": "drain", "node": node_name,
                        "affected_pods": affected,
                        "error": f"Drain will delete {len(affected)} non-system pods on node {node_name}.",
                        "hint": f"Add confirm=true to confirm. Example: cce_node_drain region=cn-north-4 cluster_id=xxx node_name=192.168.x.x confirm=true"
                    }
                skip_ns = set(['kube-system', 'hss', 'monitoring'])
                grace = 30
                pods = core_v1.list_pod_for_all_namespaces(field_selector=f'spec.nodeName={node_name}').items
                deleted, skipped = [], []
                for p in pods:
                    ns, pname = p.metadata.namespace, p.metadata.name
                    if ns in skip_ns:
                        skipped.append(f"{ns}/{pname}"); continue
                    try:
                        body = k8s.client.V1DeleteOptions(grace_period_seconds=grace)
                        core_v1.delete_namespaced_pod(pname, ns, body=body)
                        deleted.append(f"{ns}/{pname}")
                    except Exception as e:
                        skipped.append(f"{ns}/{pname} ({e})"[:100])
                return {"success": True, "operation": "drain", "node": node_name, "deleted": deleted, "skipped": skipped}
            else:
                return {"success": False, "error": f"Unknown operation: {operation}"}
        finally:
            # Clean up all temp files
            for f in [ca_cert_file, client_cert_file, client_key_file]:
                if f and os.path.exists(f):
                    try:
                        os.unlink(f)
                    except Exception:
                        pass
    except ClientRequestException as e:
        return {"success": False, "error": f"{e.error_code} - {e.error_msg}", "request_id": getattr(e, "request_id", None)}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": type(e).__name__}


def _extract_host(kubeconfig_str: str) -> str:
    """Extract hostname from kubeconfig YAML"""
    try:
        import yaml, re
        config = yaml.safe_load(kubeconfig_str)
        clusters = config.get('clusters', [])
        if clusters:
            server = clusters[0].get('cluster', {}).get('server', '')
            match = re.match(r'https?://([^:/]+)', server)
            if match:
                return f"https://{match.group(1)}:6443"
    except Exception:
        pass
    return "https://127.0.0.1:6443"


def cce_node_cordon(region: str, cluster_id: str, node_name: str, confirm: bool = False,
                    ak: Optional[str] = None, sk: Optional[str] = None,
                    project_id: str = None) -> Dict[str, Any]:
    """Mark CCE node as unschedulable (cordon)

    Args:
        region: Huawei Cloud region
        cluster_id: CCE cluster ID
        node_name: Node name or IP address
        confirm: Must be True to confirm the operation
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with operation result
    """
    return _node_operation(region, cluster_id, node_name, 'cordon', confirm=confirm, ak=ak, sk=sk, project_id=project_id)


def cce_node_uncordon(region: str, cluster_id: str, node_name: str, confirm: bool = False,
                      ak: Optional[str] = None, sk: Optional[str] = None,
                      project_id: str = None) -> Dict[str, Any]:
    """Mark CCE node as schedulable (uncordon)

    Args:
        region: Huawei Cloud region
        cluster_id: CCE cluster ID
        node_name: Node name or IP address
        confirm: Must be True to confirm the operation
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with operation result
    """
    return _node_operation(region, cluster_id, node_name, 'uncordon', confirm=confirm, ak=ak, sk=sk, project_id=project_id)


def cce_node_drain(region: str, cluster_id: str, node_name: str, confirm: bool = False,
                   ak: Optional[str] = None, sk: Optional[str] = None,
                   project_id: str = None) -> Dict[str, Any]:
    """Drain CCE node (evict all non-system pods)

    Args:
        region: Huawei Cloud region
        cluster_id: CCE cluster ID
        node_name: Node name or IP address
        confirm: Must be True to confirm the operation
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with operation result
    """
    return _node_operation(region, cluster_id, node_name, 'drain', confirm=confirm, ak=ak, sk=sk, project_id=project_id)


def cce_node_status(region: str, cluster_id: str, node_name: str,
                    ak: Optional[str] = None, sk: Optional[str] = None,
                    project_id: str = None) -> Dict[str, Any]:
    """Query CCE node schedulability status

    Args:
        region: Huawei Cloud region
        cluster_id: CCE cluster ID
        node_name: Node name or IP address
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with node status (schedulable, ready, conditions)
    """
    return _node_operation(region, cluster_id, node_name, 'status', confirm=True, ak=ak, sk=sk, project_id=project_id)


def bind_cce_cluster_eip(
    region: str,
    cluster_id: str,
    eip_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Bind an EIP to a CCE cluster master node for public API access

    Associates an existing Elastic IP with the cluster's control plane,
    enabling public access to the Kubernetes API server.

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        eip_id: EIP resource ID to bind (use huawei_list_eip to find available EIPs)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with result including the public endpoint URL
    """
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    if not eip_id:
        return {"success": False, "error": "eip_id is required"}

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    try:
        from huaweicloudsdkcce.v3 import (
            UpdateClusterEipRequest,
            MasterEIPRequest,
            MasterEIPRequestSpec,
            MasterEIPRequestSpecSpec,
        )

        client = create_cce_client(region, access_key, secret_key, proj_id)

        spec_spec = MasterEIPRequestSpecSpec(id=eip_id)
        spec = MasterEIPRequestSpec(action="bind", spec=spec_spec)
        body = MasterEIPRequest(spec=spec)
        request = UpdateClusterEipRequest(cluster_id=cluster_id, body=body)

        client.update_cluster_eip(request)

        # Query cluster to get the updated endpoint
        from huaweicloudsdkcce.v3 import ShowClusterRequest
        resp = client.show_cluster(ShowClusterRequest(cluster_id=cluster_id))
        public_url = None
        if hasattr(resp, 'status') and hasattr(resp.status, 'endpoints'):
            for ep in resp.status.endpoints:
                if ep.type == "External":
                    public_url = ep.url
                    break

        result = {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "bind_cce_cluster_eip",
            "eip_id": eip_id,
            "message": "EIP bound to cluster master successfully",
        }
        if public_url:
            result["public_endpoint"] = public_url

        return result

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, "request_id", None),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }


def unbind_cce_cluster_eip(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Unbind the EIP from a CCE cluster master node

    Removes the Elastic IP association from the cluster's control plane,
    disabling public access to the Kubernetes API server.

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with result
    """
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    try:
        from huaweicloudsdkcce.v3 import (
            UpdateClusterEipRequest,
            MasterEIPRequest,
            MasterEIPRequestSpec,
        )

        client = create_cce_client(region, access_key, secret_key, proj_id)

        spec = MasterEIPRequestSpec(action="unbind")
        body = MasterEIPRequest(spec=spec)
        request = UpdateClusterEipRequest(cluster_id=cluster_id, body=body)

        client.update_cluster_eip(request)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "unbind_cce_cluster_eip",
            "message": "EIP unbound from cluster master successfully",
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, "request_id", None),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
        }
