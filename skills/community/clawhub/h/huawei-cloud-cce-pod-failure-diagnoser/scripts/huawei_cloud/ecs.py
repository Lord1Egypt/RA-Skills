from .common import *
from huaweicloudsdkcore.exceptions.exceptions import ClientRequestException

def list_ecs_instances(region: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """List ECS instances in the specified region with pagination"""
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
        client = create_ecs_client(region, access_key, secret_key, proj_id)

        request = ListServersDetailsRequest()
        request.limit = str(limit)
        request.offset = str(offset)

        response = client.list_servers_details(request)

        instances = []
        if hasattr(response, 'servers') and response.servers:
            for server in response.servers:
                instance = {
                    "id": server.id,
                    "name": server.name,
                    "status": server.status,
                    "created": server.created,
                    "updated": server.updated,
                }
                if hasattr(server, 'flavor') and server.flavor:
                    instance["flavor"] = {
                        "id": server.flavor.id,
                        "name": server.flavor.name,
                    }
                if hasattr(server, 'addresses') and server.addresses:
                    addresses = []
                    for addr_list in server.addresses.values():
                        for addr in addr_list:
                            addr_info = {
                                "addr": getattr(addr, 'addr', None),
                                "version": getattr(addr, 'version', None),
                            }
                            # Try to get OS extended info
                            if hasattr(addr, 'os_ext_ip_sport_id'):
                                addr_info["type"] = getattr(addr, 'os_ext_ips_type', 'fixed')
                            addresses.append(addr_info)
                    instance["addresses"] = addresses
                if hasattr(server, 'metadata') and server.metadata:
                    instance["metadata"] = server.metadata
                instances.append(instance)

        return {
            "success": True,
            "region": region,
            "action": "list_ecs",
            "count": len(instances),
            "instances": instances
        }

    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, 'request_id', None),
            "hint": "Try setting HUAWEI_PROJECT_ID environment variable or pass project_id parameter"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def get_ecs_metrics(region: str, instance_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get monitoring metrics for a specific ECS instance"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not instance_id:
        return {
            "success": False,
            "error": "instance_id is required"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_ces_client(region, access_key, secret_key, proj_id)

        end_time = int(datetime.now(timezone.utc).timestamp() * 1000)
        start_time = int((datetime.now(timezone.utc) - timedelta(hours=1)).timestamp() * 1000)

        metrics_to_query = [
            "cpu_util",
            "mem_util",
            "disk_util",
            "network_incoming_bytes_rate",
            "network_outgoing_bytes_rate",
            "disk_read_bytes_rate",
            "disk_write_bytes_rate",
        ]

        all_metrics = {}

        for metric_name in metrics_to_query:
            try:
                request = ShowMetricDataRequest()
                request.namespace = "SYS.ECS"
                request.metric_name = metric_name
                request.dim_0 = f"instance_id,{instance_id}"
                request._from = start_time
                request.to = end_time
                request.period = 300
                request.filter = "average"

                response = client.show_metric_data(request)

                if hasattr(response, 'datapoints') and response.datapoints:
                    datapoints = []
                    for dp in response.datapoints:
                        datapoints.append({
                            "timestamp": dp.timestamp,
                            "average": getattr(dp, 'average', None),
                            "min": getattr(dp, 'min', None),
                            "max": getattr(dp, 'max', None),
                            "unit": getattr(dp, 'unit', '')
                        })
                    latest = datapoints[-1] if datapoints else None
                    all_metrics[metric_name] = {
                        "datapoints": datapoints,
                        "latest_value": latest.get('average') if latest else None,
                        "unit": latest.get('unit', '') if latest else ''
                    }
                else:
                    all_metrics[metric_name] = {"datapoints": [], "note": "No data available"}

            except Exception as e:
                all_metrics[metric_name] = {"error": str(e)}

        return {
            "success": True,
            "region": region,
            "instance_id": instance_id,
            "time_range": {
                "start": datetime.fromtimestamp(start_time/1000, tz=timezone.utc).isoformat(),
                "end": datetime.fromtimestamp(end_time/1000, tz=timezone.utc).isoformat(),
                "period": "5min"
            },
            "metrics": all_metrics
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

def get_ecs_metrics_with_chart(region: str, instance_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get monitoring metrics for a specific ECS instance with chart"""
    result = get_ecs_metrics(region, instance_id, ak, sk, project_id)

    # Generate chart if metrics available
    if result.get('success') and result.get('metrics'):
        chart_path = generate_monitoring_chart(result, f"ecs-{instance_id}", "ecs")
        if chart_path:
            result['chart_file'] = chart_path

    return result

def list_ecs_flavors(region: str, az: str = None, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """List available ECS flavors (instance types) in the region with pagination"""
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
        client = create_ecs_client(region, access_key, secret_key, proj_id)

        request = ListFlavorsRequest()
        if az:
            request.availability_zone = az

        response = client.list_flavors(request)

        flavors = []
        if hasattr(response, 'flavors'):
            for flavor in response.flavors:
                flavor_info = {
                    "id": flavor.id,
                    "name": flavor.name,
                    "vcpus": flavor.vcpus,
                    "ram": flavor.ram,
                    "disk": getattr(flavor, 'disk', None),
                }
                flavors.append(flavor_info)

        return {
            "success": True,
            "region": region,
            "action": "list_flavors",
            "availability_zone": az,
            "count": len(flavors),
            "flavors": flavors
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



def stop_ecs_instance(
    region: str,
    instance_id: str,
    stop_type: str = "SOFT",
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    confirm: bool = False,
) -> Dict[str, Any]:
    """Stop (shutdown) an ECS instance

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        instance_id: ECS instance ID to stop
        stop_type: Shutdown type - SOFT (normal) or HARD (force), default: SOFT
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        confirm: Must be set to True to confirm the stop operation

    Returns:
        Dictionary with operation result
    """
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not instance_id:
        return {"success": False, "error": "instance_id is required"}

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    if not confirm:
        return {
            "success": False,
            "error": "Operation not confirmed. Set confirm=true to stop the ECS instance.",
            "warning": "Stopping an ECS instance will shut down the VM. Are you sure?",
            "hint": "Add confirm=true parameter to confirm. Example: stop_ecs_instance region=cn-north-4 instance_id=xxx confirm=true"
        }

    try:
        from huaweicloudsdkecs.v2 import (
            BatchStopServersRequest,
            BatchStopServersRequestBody,
            BatchStopServersOption,
            ServerId,
        )

        client = create_ecs_client(region, access_key, secret_key, proj_id)

        sid = ServerId(id=instance_id)
        os_stop_option = BatchStopServersOption(servers=[sid], type=stop_type)

        body = BatchStopServersRequestBody(os_stop=os_stop_option)
        body.os_stop = BatchStopServersOption(type=stop_type)

        request = BatchStopServersRequest()
        request.body = body

        response = client.batch_stop_servers(request)

        return {
            "success": True,
            "region": region,
            "instance_id": instance_id,
            "action": "stop_ecs_instance",
            "message": "ECS instance stop request submitted successfully",
            "stop_type": stop_type,
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


def start_ecs_instance(
    region: str,
    instance_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Start (power on) an ECS instance

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        instance_id: ECS instance ID to start
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

    if not instance_id:
        return {"success": False, "error": "instance_id is required"}

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    try:
        from huaweicloudsdkecs.v2 import (
            BatchStartServersRequest,
            BatchStartServersRequestBody,
            BatchStartServersOption,
            ServerId,
        )

        client = create_ecs_client(region, access_key, secret_key, proj_id)

        sid = ServerId(id=instance_id)
        os_start_option = BatchStartServersOption(servers=[sid])

        body = BatchStartServersRequestBody(os_start=os_start_option)

        request = BatchStartServersRequest()
        request.body = body

        response = client.batch_start_servers(request)

        return {
            "success": True,
            "region": region,
            "instance_id": instance_id,
            "action": "start_ecs_instance",
            "message": "ECS instance start request submitted successfully",
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


def reboot_ecs_instance(
    region: str,
    instance_id: str,
    reboot_type: str = "SOFT",
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: str = None,
    confirm: bool = False,
) -> Dict[str, Any]:
    """Reboot an ECS instance (SOFT or HARD)

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        instance_id: ECS instance ID to reboot
        reboot_type: Reboot type - SOFT (normal) or HARD (force), default: SOFT
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        confirm: Must be set to True to confirm the reboot

    Returns:
        Dictionary with operation result
    """
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not instance_id:
        return {"success": False, "error": "instance_id is required"}

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "instance_id": instance_id,
            "reboot_type": reboot_type.upper(),
            "error": f"ECS reboot will forcibly restart instance {instance_id}. Unsaved data may be lost.",
            "hint": f"Add confirm=true to confirm. Example: reboot_ecs_instance region=cn-north-4 instance_id=xxx confirm=true reboot_type=SOFT"
        }

    try:
        from huaweicloudsdkecs.v2 import BatchRebootServersRequest, BatchRebootServersRequestBody, BatchRebootSeversOption, ServerId

        client = create_ecs_client(region, access_key, secret_key, proj_id)

        server = ServerId(id=instance_id)
        reboot_opt = BatchRebootSeversOption(servers=[server], type=reboot_type.upper())
        body = BatchRebootServersRequestBody(reboot=reboot_opt)
        request = BatchRebootServersRequest(body=body)
        response = client.batch_reboot_servers(request)

        return {
            "success": True,
            "region": region,
            "instance_id": instance_id,
            "reboot_type": reboot_type.upper(),
            "action": "reboot_ecs_instance",
            "message": "ECS instance reboot request submitted successfully",
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
