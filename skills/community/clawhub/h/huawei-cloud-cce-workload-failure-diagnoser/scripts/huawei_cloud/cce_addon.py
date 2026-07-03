"""CCE Addon management functions."""

from typing import Any, Dict, Optional
from copy import deepcopy

from huaweicloudsdkcore.exceptions.exceptions import ClientRequestException
from huaweicloudsdkcce.v3 import (
    ShowAddonInstanceRequest,
    ListAddonInstancesRequest,
    CreateAddonInstanceRequest,
    AddonInstance,
    InstanceSpec,
    AddonMetadata,
    UpdateAddonInstanceRequest,
    DeleteAddonInstanceRequest,
    ShowClusterRequest,
)

from .common import get_credentials, create_cce_client, SDK_AVAILABLE, IMPORT_ERROR


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


def install_cce_addon(
    region: str,
    cluster_id: str,
    addon_template_name: str,
    addon_version: str,
    values: Dict[str, Any],
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None
) -> Dict[str, Any]:
    """Install an addon to a CCE cluster

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        addon_template_name: Addon template name (e.g., "coredns", "metrics-server")
        addon_version: Addon version to install
        values: Addon-specific configuration values
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with installation result
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

    if not addon_template_name:
        return {
            "success": False,
            "error": "addon_template_name is required"
        }

    if not addon_version:
        return {
            "success": False,
            "error": "addon_version is required"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        metadata = AddonMetadata(
            annotations={"addon.install/type": "install"}
        )

        spec = InstanceSpec(
            cluster_id=cluster_id,
            version=addon_version,
            addon_template_name=addon_template_name,
            values=values
        )

        body = AddonInstance(
            kind="Addon",
            api_version="v3",
            metadata=metadata,
            spec=spec
        )

        request = CreateAddonInstanceRequest()
        request.body = body

        response = client.create_addon_instance(request)

        addon_info = {}
        if hasattr(response, 'metadata') and response.metadata:
            addon_info["uid"] = getattr(response.metadata, 'uid', None)
            addon_info["name"] = getattr(response.metadata, 'name', None)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "install_cce_addon",
            "addon_template_name": addon_template_name,
            "addon_version": addon_version,
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


def uninstall_cce_addon(
    region: str,
    cluster_id: str,
    addon_id: str,
    confirm: bool,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None
) -> Dict[str, Any]:
    """Uninstall an addon from a CCE cluster

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        addon_id: Addon ID (name or UID)
        confirm: Must be True to proceed with uninstallation
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with uninstallation result
    """
    if not confirm:
        return {
            "success": False,
            "error": "Uninstallation requires explicit confirmation. Set confirm=True to proceed."
        }

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

    if not addon_id:
        return {
            "success": False,
            "error": "addon_id is required"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        request = DeleteAddonInstanceRequest()
        request.cluster_id = cluster_id
        request.id = addon_id

        client.delete_addon_instance(request)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "uninstall_cce_addon",
            "addon_id": addon_id,
            "message": f"Addon {addon_id} uninstallation initiated"
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


def update_cce_addon(
    region: str,
    cluster_id: str,
    addon_id: str,
    addon_version: str,
    values: Dict[str, Any],
    addon_template_name: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None
) -> Dict[str, Any]:
    """Update an addon in a CCE cluster

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        cluster_id: CCE cluster ID
        addon_id: Addon ID (name or UID)
        addon_version: New addon version
        values: Addon-specific configuration values
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)

    Returns:
        Dictionary with update result
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

    if not addon_id:
        return {
            "success": False,
            "error": "addon_id is required"
        }

    if not addon_version:
        return {
            "success": False,
            "error": "addon_version is required"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        metadata = AddonMetadata(
            annotations={"addon.upgrade/type": "upgrade"}
        )

        spec_kwargs: Dict[str, Any] = {
            "cluster_id": cluster_id,
            "version": addon_version,
            "values": values,
        }
        if addon_template_name:
            spec_kwargs["addon_template_name"] = addon_template_name
        spec = InstanceSpec(**spec_kwargs)

        body = AddonInstance(
            kind="Addon",
            api_version="v3",
            metadata=metadata,
            spec=spec
        )

        request = UpdateAddonInstanceRequest()
        request.id = addon_id
        request.body = body

        response = client.update_addon_instance(request)

        addon_info = {}
        if hasattr(response, 'metadata') and response.metadata:
            addon_info["uid"] = getattr(response.metadata, 'uid', None)
            addon_info["name"] = getattr(response.metadata, 'name', None)

        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "update_cce_addon",
            "addon_id": addon_id,
            "addon_version": addon_version,
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


def _resolve_addon_instance_id(client: Any, cluster_id: str, addon_id: str) -> Optional[str]:
    """Resolve addon instance uid from uid/name/template name."""
    request = ListAddonInstancesRequest()
    request.cluster_id = cluster_id
    response = client.list_addon_instances(request)

    if not hasattr(response, "items") or not response.items:
        return None

    for addon in response.items:
        metadata = getattr(addon, "metadata", None)
        spec = getattr(addon, "spec", None)
        uid = getattr(metadata, "uid", None) if metadata else None
        name = getattr(metadata, "name", None) if metadata else None
        template = getattr(spec, "addon_template_name", None) if spec else None
        if addon_id in {uid, name, template}:
            return uid
    return None


def configure_cce_bursting_addon(
    region: str,
    cluster_id: str,
    subnet_id: str,
    subnets: Optional[list[str]] = None,
    addon_id: str = "virtual-kubelet",
    addon_version: Optional[str] = None,
    enable_schedule_profile_local_surge: Optional[bool] = None,
    is_install_proxy: Optional[bool] = None,
    enable_log_collection: Optional[bool] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Configure CCI bursting addon network params for CCE->CCI2.0 scheduling."""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}
    if not subnet_id:
        return {"success": False, "error": "subnet_id is required"}
    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_cce_client(region, access_key, secret_key, proj_id)

        resolved_id = _resolve_addon_instance_id(client, cluster_id, addon_id)
        if not resolved_id:
            return {
                "success": False,
                "error": f"Addon instance not found by id/name/template: {addon_id}"
            }

        show_request = ShowAddonInstanceRequest()
        show_request.cluster_id = cluster_id
        show_request.id = resolved_id
        addon_detail = client.show_addon_instance(show_request).to_dict()

        spec = addon_detail.get("spec", {})
        current_values = spec.get("values") or {}
        if not isinstance(current_values, dict):
            return {
                "success": False,
                "error": "Current addon values are not a JSON object. Cannot patch safely."
            }

        values = deepcopy(current_values)
        values.setdefault("custom", {})
        values.setdefault("basic", {})

        # Fill mandatory basic fields required by virtual-kubelet provider init.
        cluster_name = None
        vpc_id = None
        try:
            cluster_request = ShowClusterRequest()
            cluster_request.cluster_id = cluster_id
            cluster_detail = client.show_cluster(cluster_request).to_dict()
            cluster_root = cluster_detail.get("cluster", cluster_detail)
            cluster_name = cluster_root.get("metadata", {}).get("name")
            host_network = (
                cluster_root.get("spec", {}).get("host_network")
                or cluster_root.get("spec", {}).get("hostNetwork")
                or {}
            )
            vpc_id = host_network.get("vpc")
        except Exception:
            # Best effort enrichment; keep existing values if cluster lookup fails.
            pass

        normalized_subnets = [s for s in (subnets or []) if s]
        if not normalized_subnets:
            normalized_subnets = [subnet_id]
        network_subnet_id = normalized_subnets[0]
        subnet_entries = [{"subnetID": subnet} for subnet in normalized_subnets]

        values["basic"]["cluster_id"] = cluster_id
        values["basic"]["clusterID"] = cluster_id
        if cluster_name:
            values["basic"]["cluster_name"] = cluster_name
            values["basic"]["clusterName"] = cluster_name
        if vpc_id:
            values["basic"]["vpc_id"] = vpc_id
            values["basic"]["vpcID"] = vpc_id
        values["basic"]["network_id"] = network_subnet_id
        values["basic"]["networkID"] = network_subnet_id
        values["basic"]["project_id"] = proj_id
        values["basic"]["projectID"] = proj_id
        values["custom"]["subnet_id"] = subnet_id
        values["custom"]["subnets"] = subnet_entries
        values["basic"]["subnet_id"] = network_subnet_id

        if enable_schedule_profile_local_surge is not None:
            values["custom"]["enableScheduleProfileLocalSurge"] = enable_schedule_profile_local_surge
        if is_install_proxy is not None:
            values["custom"]["isInstallProxy"] = is_install_proxy
        if enable_log_collection is not None:
            values["custom"]["enableLogCollection"] = enable_log_collection

        target_version = addon_version or spec.get("version")
        if not target_version:
            return {
                "success": False,
                "error": "addon_version is required but not found from current addon spec"
            }

        metadata = AddonMetadata(annotations={"addon.upgrade/type": "upgrade"})
        instance_spec = InstanceSpec(
            cluster_id=cluster_id,
            version=target_version,
            addon_template_name=spec.get("addon_template_name"),
            values=values
        )
        body = AddonInstance(
            kind="Addon",
            api_version="v3",
            metadata=metadata,
            spec=instance_spec
        )

        update_request = UpdateAddonInstanceRequest()
        update_request.id = resolved_id
        update_request.body = body
        response = client.update_addon_instance(update_request)

        response_dict = response.to_dict()
        return {
            "success": True,
            "region": region,
            "cluster_id": cluster_id,
            "action": "configure_cce_bursting_addon",
            "addon_id": addon_id,
            "resolved_addon_id": resolved_id,
            "addon_version": target_version,
            "applied": {
                "subnet_id": subnet_id,
                "subnets": subnet_entries,
                "network_id": network_subnet_id,
                "enableScheduleProfileLocalSurge": values["custom"].get("enableScheduleProfileLocalSurge"),
                "isInstallProxy": values["custom"].get("isInstallProxy"),
                "enableLogCollection": values["custom"].get("enableLogCollection"),
            },
            "addon": {
                "uid": response_dict.get("metadata", {}).get("uid"),
                "name": response_dict.get("metadata", {}).get("name"),
            }
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
