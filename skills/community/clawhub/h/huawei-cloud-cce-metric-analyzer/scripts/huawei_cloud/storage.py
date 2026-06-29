from .common import *

def get_evs_metrics(region: str, volume_id: str, instance_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get monitoring metrics for a specific EVS volume"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not volume_id:
        return {
            "success": False,
            "error": "volume_id is required"
        }
    
    if not instance_id:
        return {
            "success": False,
            "error": "instance_id (ECS instance ID that the volume is attached to) is required"
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

        # 构建disk_name维度: {instance-id}-volume-{volume-id}
        disk_name = f"{instance_id}-volume-{volume_id}"

        # EVS monitoring metrics (使用 disk_device_ 前缀)
        metrics_to_query = [
            "disk_device_read_bytes_rate",
            "disk_device_write_bytes_rate",
            "disk_device_read_requests_rate",
            "disk_device_write_requests_rate",
        ]

        all_metrics = {}

        for metric_name in metrics_to_query:
            try:
                request = ShowMetricDataRequest()
                request.namespace = "SYS.EVS"
                request.metric_name = metric_name
                request.dim_0 = f"disk_name,{disk_name}"
                request._from = start_time
                request.to = end_time
                request.period = 60
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
            "volume_id": volume_id,
            "time_range": {
                "start": datetime.fromtimestamp(start_time/1000, timezone.utc).isoformat(),
                "end": datetime.fromtimestamp(end_time/1000, timezone.utc).isoformat(),
                "period": "5min"
            },
            "metrics": all_metrics
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def list_evs_volumes(region: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100, offset: int = 0, volume_type: str = None, availability_zone: str = None) -> Dict[str, Any]:
    """List EVS volumes (cloud disks) in the specified region with pagination"""
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
        client = create_evs_client(region, access_key, secret_key, proj_id)

        request = ListVolumesRequest()
        request.limit = str(limit)
        request.offset = str(offset)
        if volume_type:
            request.volume_type = volume_type
        if availability_zone:
            request.availability_zone = availability_zone

        response = client.list_volumes(request)

        volumes = []
        if hasattr(response, 'volumes') and response.volumes:
            for volume in response.volumes:
                volume_info = {
                    "id": volume.id,
                    "name": volume.name,
                    "status": volume.status,
                    "volume_type": volume.volume_type,
                    "size": volume.size,
                    "created_at": str(volume.created_at) if volume.created_at else None,
                }
                if hasattr(volume, 'attachments') and volume.attachments:
                    attachments = []
                    for att in volume.attachments:
                        attachments.append({
                            "device": att.device,
                            "server_id": att.server_id,
                            "attachment_id": att.attachment_id,
                        })
                    volume_info["attachments"] = attachments
                if hasattr(volume, 'availability_zone'):
                    volume_info["availability_zone"] = volume.availability_zone
                if hasattr(volume, 'bootable'):
                    volume_info["bootable"] = volume.bootable
                if hasattr(volume, 'encrypted'):
                    volume_info["encrypted"] = volume.encrypted
                if hasattr(volume, 'tags'):
                    volume_info["tags"] = volume.tags
                if hasattr(volume, 'metadata'):
                    volume_info["metadata"] = volume.metadata
                if hasattr(volume, 'description'):
                    volume_info["description"] = volume.description
                if hasattr(volume, 'shareable'):
                    volume_info["shareable"] = volume.shareable
                if hasattr(volume, 'multiattach'):
                    volume_info["multiattach"] = volume.multiattach
                volumes.append(volume_info)

        # Get pagination info
        response_info = {
            "success": True,
            "region": region,
            "action": "list_evs_volumes",
            "count": len(volumes),
            "limit": limit,
            "offset": offset,
            "volumes": volumes
        }

        # Add markers if available
        if hasattr(response, 'volumes_links') and response.volumes_links:
            response_info["links"] = [{"rel": link.rel, "href": link.href} for link in response.volumes_links]

        return response_info

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

def list_sfs_turbo(region: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """List SFS Turbo file systems in the specified region
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        limit: Number of results to return (default: 100)
        offset: Pagination offset (default: 0)

    Returns:
        Dictionary with SFS Turbo file systems list
    """
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
        # 基于官方SDK实现：https://github.com/huaweicloud/huaweicloud-sdk-python-v3/tree/master/huaweicloud-sdk-sfsturbo
        from huaweicloudsdksfsturbo.v1 import SFSTurboClient
        from huaweicloudsdksfsturbo.v1.model.list_shares_request import ListSharesRequest
        from huaweicloudsdksfsturbo.v1.region.sfsturbo_region import SFSTurboRegion

        # 初始化SFS Turbo客户端（注意SDK中类名是全大写的SFSTurboClient和SFSTurboRegion）
        client = SFSTurboClient.new_builder() \
            .with_credentials(BasicCredentials(access_key, secret_key, proj_id)) \
            .with_region(SFSTurboRegion.value_of(region)) \
            .build()

        # 构造请求
        request = ListSharesRequest()
        request.limit = limit
        request.offset = offset

        # 发送请求
        response = client.list_shares(request)

        # 处理响应
        turbos = []
        if hasattr(response, 'shares') and response.shares:
            for turbo in response.shares:
                turbo_info = {
                    "id": getattr(turbo, 'id', None),
                    "name": getattr(turbo, 'name', None),
                    "status": getattr(turbo, 'status', None),
                    "size": getattr(turbo, 'size', None),  # 总容量(GB)
                    "used_size": getattr(turbo, 'used_size', None),  # 已用容量(GB)
                    "share_proto": getattr(turbo, 'share_proto', None),  # 协议：NFS/CIFS
                    "share_type": getattr(turbo, 'share_type', None),  # 类型：STANDARD(标准型)/PERFORMANCE(性能型)
                    "availability_zone": getattr(turbo, 'availability_zone', None),
                    "vpc_id": getattr(turbo, 'vpc_id', None),
                    "subnet_id": getattr(turbo, 'subnet_id', None),
                    "security_group_id": getattr(turbo, 'security_group_id', None),
                    "export_location": getattr(turbo, 'export_location', None),  # 挂载地址
                    "created_at": str(getattr(turbo, 'created_at', None)) if getattr(turbo, 'created_at', None) else None,
                    "description": getattr(turbo, 'description', None)
                }
                turbos.append(turbo_info)

        return {
            "success": True,
            "region": region,
            "action": "list_sfs_turbo",
            "count": len(turbos),
            "sfsturbos": turbos
        }

    except ImportError as e:
        return {
            "success": False,
            "error": f"SFS Turbo SDK import error: {str(e)}",
            "hint": "请从GitHub源码安装：\n"
                    "git clone https://github.com/huaweicloud/huaweicloud-sdk-python-v3.git\n"
                    "cd huaweicloud-sdk-python-v3/huaweicloud-sdk-sfsturbo\n"
                    "pip3 install ."
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

def list_sfs(region: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """List SFS (Scalable File Service) file systems in the specified region
    基于官方API实现：OpenStack Manila API (v2)
    使用HTTP直接调用，AK/SK签名参考huawei_get_aom_metrics
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        limit: Number of results to return (default: 100)
        offset: Pagination offset (default: 0)

    Returns:
        Dictionary with SFS file systems list
    """
    import hashlib
    import hmac
    import time as time_module
    import urllib.parse
    from urllib.parse import quote, unquote
    import requests
    
    # 获取凭证（包括project_id）
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

    if not access_key or not secret_key or not proj_id:
        return {
            "success": False,
            "error": "Credentials and project_id are required"
        }

    try:
        now = int(time_module.time())
        
        # ========== 构建URL和查询参数 ==========
        base_url = f"https://sfs.{region}.myhuaweicloud.com"
        resource_path = f"/v2/{proj_id}/shares"
        
        # 查询参数
        query_params = [
            ('limit', str(limit)),
            ('offset', str(offset))
        ]
        
        # ========== 按SDK方式构建签名 ==========
        timestamp = time_module.strftime('%Y%m%dT%H%M%SZ', time_module.gmtime(now))
        
        # 1. HTTP方法
        http_method = 'GET'
        
        # 2. Canonical URI
        def url_encode(s):
            return quote(s, safe='~')
        
        pattens = unquote(resource_path).split('/')
        uri_parts = []
        for v in pattens:
            uri_parts.append(url_encode(v))
        canonical_uri = "/".join(uri_parts)
        if canonical_uri[-1] != '/':
            canonical_uri = canonical_uri + "/"
        
        # 3. Canonical Query String (排序)
        sorted_params = sorted(query_params, key=lambda x: x[0])
        canonical_querystring = '&'.join(['{}={}'.format(url_encode(k), url_encode(str(v))) for k, v in sorted_params])
        
        # 4. Headers
        host_header = f"sfs.{region}.myhuaweicloud.com"
        
        # 签名的headers（按字母顺序）
        signed_headers_list = ['host', 'x-project-id', 'x-sdk-date']
        signed_headers = ';'.join(signed_headers_list)
        
        # Canonical headers (每个header一行，最后有\n)
        canonical_headers = 'host:{}\nx-project-id:{}\nx-sdk-date:{}\n'.format(
            host_header, proj_id, timestamp)
        
        # 5. 空body的hash
        hashed_body = hashlib.sha256(b'').hexdigest()
        
        # 6. 构建Canonical Request
        canonical_request = '{}\n{}\n{}\n{}\n{}\n{}'.format(
            http_method, canonical_uri, canonical_querystring,
            canonical_headers, signed_headers, hashed_body)
        
        # 7. StringToSign (SDK格式：只有3行)
        algorithm = 'SDK-HMAC-SHA256'
        hashed_canonical_request = hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        string_to_sign = '{}\n{}\n{}'.format(algorithm, timestamp, hashed_canonical_request)
        
        # 8. 签名 - 使用hex编码
        signature = hmac.new(
            secret_key.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest().hex()
        
        # 9. Authorization
        authorization = '{} Access={}, SignedHeaders={}, Signature={}'.format(
            algorithm, access_key, signed_headers, signature)
        
        # 10. 构建请求URL
        url_query_string = '&'.join(['{}={}'.format(k, urllib.parse.quote(str(v))) for k, v in query_params])
        url = "{}{}?{}".format(base_url, resource_path, url_query_string)
        
        # 11. 请求headers
        headers = {
            'Host': host_header,
            'X-Project-Id': proj_id,
            'X-Sdk-Date': timestamp,
            'Authorization': authorization,
        }
        
        # 发送请求
        resp = requests.get(url, headers=headers, verify=False, timeout=30)
        
        if resp.status_code == 200:
            data = resp.json()
            sfs_list = []
            if "shares" in data:
                for sfs in data["shares"]:
                    sfs_info = {
                        "id": sfs.get("id"),
                        "name": sfs.get("name"),
                        "status": sfs.get("status"),
                        "size": sfs.get("size"),  # 总容量(GB)
                        "used_size": sfs.get("used_size"),  # 已用容量(GB)
                        "share_proto": sfs.get("share_proto"),  # 协议类型：NFS/CIFS
                        "availability_zone": sfs.get("availability_zone"),
                        "vpc_id": sfs.get("vpc_id"),
                        "export_location": sfs.get("export_location"),  # 挂载地址
                        "created_at": sfs.get("created_at"),
                        "description": sfs.get("description"),
                        "is_public": sfs.get("is_public"),
                        "share_type": sfs.get("share_type")  # 文件系统类型
                    }
                    sfs_list.append(sfs_info)
            
            return {
                "success": True,
                "region": region,
                "action": "list_sfs",
                "count": len(sfs_list),
                "sfs": sfs_list
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {resp.status_code}: {resp.text[:500]}",
                "url": url,
                "request_headers": {k: v for k, v in headers.items() if k != 'Authorization'}
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

