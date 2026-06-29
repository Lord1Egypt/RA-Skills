from .common import *


def _list_value(value: Optional[str | List[str]]) -> Optional[List[str]]:
    if value is None:
        return None
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def create_elb_loadbalancer(
    region: str,
    name: str,
    vip_subnet_cidr_id: str,
    vpc_id: Optional[str] = None,
    availability_zone_list: Optional[str | List[str]] = None,
    l4_flavor_id: Optional[str] = None,
    l7_flavor_id: Optional[str] = None,
    elb_virsubnet_ids: Optional[str | List[str]] = None,
    description: Optional[str] = None,
    provider: Optional[str] = None,
    guaranteed: Optional[bool] = None,
    deletion_protection_enable: bool = True,
    ip_target_enable: Optional[bool] = None,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Preview or create an ELB load balancer with the ELB v3 API."""
    if not name:
        return {"success": False, "error": "name is required"}
    if not vip_subnet_cidr_id:
        return {"success": False, "error": "vip_subnet_cidr_id is required"}

    plan = {
        "operation": "create_elb_loadbalancer",
        "region": region,
        "loadbalancer": {
            "name": name,
            "description": description,
            "vip_subnet_cidr_id": vip_subnet_cidr_id,
            "vpc_id": vpc_id,
            "availability_zone_list": _list_value(availability_zone_list),
            "l4_flavor_id": l4_flavor_id,
            "l7_flavor_id": l7_flavor_id,
            "elb_virsubnet_ids": _list_value(elb_virsubnet_ids),
            "provider": provider,
            "guaranteed": guaranteed,
            "deletion_protection_enable": bool(deletion_protection_enable),
            "ip_target_enable": ip_target_enable,
        },
        "notes": [
            "This creates a billable ELB resource.",
            "vip_subnet_cidr_id must be the ELB VIP subnet network ID expected by the ELB v3 API.",
            "No public EIP is created automatically.",
        ],
    }
    plan["loadbalancer"] = {key: value for key, value in plan["loadbalancer"].items() if value is not None}
    if not confirm:
        return {
            "success": False,
            "requires_confirmation": True,
            "message": "Preview only. Re-run with confirm=true after explicit approval.",
            "plan": plan,
        }

    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    if not proj_id:
        return {"success": False, "error": f"Project ID not found for region={region}"}
    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    try:
        from huaweicloudsdkelb.v3 import CreateLoadBalancerOption, CreateLoadBalancerRequest, CreateLoadBalancerRequestBody

        option = CreateLoadBalancerOption(name=name, vip_subnet_cidr_id=vip_subnet_cidr_id)
        for key, value in plan["loadbalancer"].items():
            if key not in {"name", "vip_subnet_cidr_id"}:
                setattr(option, key, value)

        request = CreateLoadBalancerRequest(body=CreateLoadBalancerRequestBody(loadbalancer=option))
        response = create_elb_client(region, access_key, secret_key, proj_id).create_load_balancer(request)
        data = response.to_dict() if hasattr(response, "to_dict") else {}
        return {
            "success": True,
            "action": "create_elb_loadbalancer",
            "region": region,
            "loadbalancer": data.get("loadbalancer", data),
            "request_id": getattr(response, "request_id", None),
        }
    except ClientRequestException as e:
        return {
            "success": False,
            "error": f"{e.error_code} - {e.error_msg}",
            "request_id": getattr(e, "request_id", None),
        }
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": type(e).__name__}


def list_elb_loadbalancers(region: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100, marker: str = None) -> Dict[str, Any]:
    """List ELB load balancers in the specified region"""
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
        client = create_elb_client(region, access_key, secret_key, proj_id)

        request = ListLoadBalancersRequest()
        request.page_size = str(limit)
        if marker:
            request.marker = marker

        response = client.list_load_balancers(request)

        loadbalancers = []
        if hasattr(response, 'loadbalancers') and response.loadbalancers:
            for lb in response.loadbalancers:
                # 获取关键字段用于判断ELB类型
                guaranteed = getattr(lb, 'guaranteed', None)
                provider = getattr(lb, 'provider', None)
                lb_type = getattr(lb, 'type', None)
                l4_flavor_id = getattr(lb, 'l4_flavor_id', None)
                l7_flavor_id = getattr(lb, 'l7_flavor_id', None)
                
                # 判断ELB类型
                # 独享型: guaranteed=True 或 provider包含vlb 或 type="Dedicated" 或 有flavor_id
                is_dedicated = (
                    guaranteed is True or
                    (provider and 'vlb' in str(provider).lower()) or
                    (lb_type and lb_type.lower() == 'dedicated') or
                    l4_flavor_id is not None or
                    l7_flavor_id is not None
                )
                
                elb_type = "独享型" if is_dedicated else "共享型"
                
                lb_info = {
                    "id": lb.id,
                    "name": lb.name,
                    "type": lb_type,
                    "elb_type": elb_type,  # 独享型/共享型
                    "guaranteed": guaranteed,
                    "provider": provider,
                    "l4_flavor_id": l4_flavor_id,
                    "l7_flavor_id": l7_flavor_id,
                    "provisioning_status": getattr(lb, 'provisioning_status', None),
                    "vpc_id": getattr(lb, 'vpc_id', None),
                    "vip_address": getattr(lb, 'vip_address', None),
                    "vip_port_id": getattr(lb, 'vip_port_id', None),
                    "created_at": str(getattr(lb, 'created_at', None)) if getattr(lb, 'created_at', None) else None,
                    "updated_at": str(getattr(lb, 'updated_at', None)) if getattr(lb, 'updated_at', None) else None,
                }
                # Optional fields
                if hasattr(lb, 'description'):
                    lb_info["description"] = lb.description
                if hasattr(lb, 'project_id'):
                    lb_info["project_id"] = lb.project_id
                if hasattr(lb, 'domain'):
                    lb_info["domain"] = lb.domain
                if hasattr(lb, 'eip_address'):
                    lb_info["eip_address"] = lb.eip_address
                if hasattr(lb, 'eip_info'):
                    lb_info["eip_info"] = {
                        "eip": lb.eip_info.eip if lb.eip_info else None,
                        "eip_id": lb.eip_info.eip_id if lb.eip_info else None
                    } if hasattr(lb, 'eip_info') else None
                if hasattr(lb, 'az'):
                    lb_info["az"] = lb.az
                if hasattr(lb, 'tags'):
                    lb_info["tags"] = lb.tags
                loadbalancers.append(lb_info)

        # Get pagination info
        result = {
            "success": True,
            "region": region,
            "action": "list_elb_loadbalancers",
            "count": len(loadbalancers),
            "loadbalancers": loadbalancers
        }

        if hasattr(response, 'page_info') and response.page_info:
            result["page_info"] = {
                "next_marker": response.page_info.next_marker,
                "current_count": response.page_info.current_count
            }

        return result

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

def list_elb_listeners(region: str, loadbalancer_id: str = None, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
    """List ELB listeners"""
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
        client = create_elb_client(region, access_key, secret_key, proj_id)

        request = ListListenersRequest()
        request.page_size = str(limit)
        if loadbalancer_id:
            request.loadbalancer_id = loadbalancer_id

        response = client.list_listeners(request)

        listeners = []
        if hasattr(response, 'listeners') and response.listeners:
            for listener in response.listeners:
                listener_info = {
                    "id": getattr(listener, 'id', None),
                    "name": getattr(listener, 'name', None),
                    "protocol": getattr(listener, 'protocol', None),
                    "port": getattr(listener, 'port', None),
                    "backend_port": getattr(listener, 'backend_port', None),
                    "status": getattr(listener, 'status', None),
                    "created_at": str(getattr(listener, 'created_at', None)) if getattr(listener, 'created_at', None) else None,
                }
                if hasattr(listener, 'description'):
                    listener_info["description"] = getattr(listener, 'description', None)
                if hasattr(listener, 'default_tls_container_ref'):
                    listener_info["default_tls"] = getattr(listener, 'default_tls_container_ref', None)
                listeners.append(listener_info)

        return {
            "success": True,
            "region": region,
            "loadbalancer_id": loadbalancer_id,
            "action": "list_elb_listeners",
            "count": len(listeners),
            "listeners": listeners
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

def get_elb_backend_status(region: str, elb_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 200) -> Dict[str, Any]:
    """Get ELB pools, members, health monitors, and load balancer status.

    This is read-only and intended for CCE network diagnosis. It complements
    get_elb_metrics by returning backend member health instead of time-series
    counters only.
    """
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not elb_id:
        return {
            "success": False,
            "error": "elb_id is required"
        }

    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_elb_client(region, access_key, secret_key, proj_id)

        lb_status = {}
        try:
            status_request = ShowLoadBalancerStatusRequest()
            status_request.loadbalancer_id = elb_id
            status_response = client.show_load_balancer_status(status_request)
            if hasattr(status_response, "to_dict"):
                lb_status = status_response.to_dict()
        except Exception as exc:
            lb_status = {"error": str(exc), "error_type": type(exc).__name__}

        pools_request = ListPoolsRequest()
        pools_request.loadbalancer_id = [elb_id]
        pools_request.limit = limit
        pools_response = client.list_pools(pools_request)
        pools = []
        pool_ids = []
        for pool in getattr(pools_response, "pools", None) or []:
            pool_info = pool.to_dict() if hasattr(pool, "to_dict") else {}
            pools.append(pool_info)
            if pool_info.get("id"):
                pool_ids.append(pool_info["id"])

        members = []
        for pool_id in pool_ids:
            try:
                members_request = ListMembersRequest()
                members_request.pool_id = pool_id
                members_request.limit = limit
                members_response = client.list_members(members_request)
                for member in getattr(members_response, "members", None) or []:
                    member_info = member.to_dict() if hasattr(member, "to_dict") else {}
                    member_info["pool_id"] = pool_id
                    members.append(member_info)
            except Exception as exc:
                members.append({"pool_id": pool_id, "error": str(exc), "error_type": type(exc).__name__})

        health_monitors = []
        try:
            monitors_request = ListHealthMonitorsRequest()
            monitors_request.limit = limit
            monitors_response = client.list_health_monitors(monitors_request)
            for monitor in getattr(monitors_response, "healthmonitors", None) or []:
                monitor_info = monitor.to_dict() if hasattr(monitor, "to_dict") else {}
                if not pool_ids or monitor_info.get("id") in {pool.get("healthmonitor_id") for pool in pools}:
                    health_monitors.append(monitor_info)
        except Exception as exc:
            health_monitors.append({"error": str(exc), "error_type": type(exc).__name__})

        unhealthy_members = [
            member for member in members
            if str(member.get("operating_status") or "").upper() not in {"", "ONLINE", "NORMAL", "NO_MONITOR"}
        ]

        return {
            "success": True,
            "region": region,
            "elb_id": elb_id,
            "action": "get_elb_backend_status",
            "loadbalancer_status": lb_status,
            "pools": pools,
            "members": members,
            "health_monitors": health_monitors,
            "unhealthy_member_count": len(unhealthy_members),
            "unhealthy_members": unhealthy_members,
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

def get_elb_metrics(region: str, elb_id: str, hours: int = 1, period: int = 300, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """获取指定ELB负载均衡的监控指标（自动识别ELB类型，查询对应的四层/七层指标）"""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    if not elb_id:
        return {
            "success": False,
            "error": "elb_id是必填参数"
        }
    
    # 校验采样周期
    valid_periods = [300, 1200, 3600]
    if period not in valid_periods:
        period = 300
    
    # 计算时间范围
    end_time = int(datetime.now(timezone.utc).timestamp() * 1000)
    start_time = int((datetime.now(timezone.utc) - timedelta(hours=hours)).timestamp() * 1000)
    
    # ========== 第一步：查询ELB基本信息，判断支持的协议类型 ==========
    try:
        from huaweicloudsdkelb.v3 import ElbClient
        from huaweicloudsdkelb.v3.region.elb_region import ElbRegion
        from huaweicloudsdkelb.v3.model.show_loadbalancer_request import ShowLoadBalancerRequest
        
        elb_client = ElbClient.new_builder() \
            .with_ak(access_key) \
            .with_sk(secret_key) \
            .with_region(ElbRegion.value_of(region)) \
            .with_project_id(proj_id) \
            .build()
        
        req = ShowLoadBalancerRequest()
        req.loadbalancer_id = elb_id
        resp = elb_client.show_load_balancer(req)
        elb_info = resp.loadbalancer.to_dict()
        
        elb_name = elb_info.get('name', '')
        elb_type = elb_info.get('l4_flavor_id') and elb_info.get('l7_flavor_id') and "四七层共享型" or \
                   elb_info.get('l4_flavor_id') and "四层独享型" or \
                   elb_info.get('l7_flavor_id') and "七层独享型" or "未知类型"
        support_l4 = bool(elb_info.get('l4_flavor_id'))
        support_l7 = bool(elb_info.get('l7_flavor_id'))
        
    except Exception as e:
        # 查询ELB信息失败，默认同时查询四七层指标
        support_l4 = True
        support_l7 = True
        elb_name = ""
        elb_type = "未知类型（默认同时查询四七层）"
    
    # ========== 第二步：根据ELB类型确定要查询的指标 ==========
    # 四层指标定义（华为云官方标准指标）
    l4_metrics = {
        "m1_cps": "并发连接数（个）",
        "m2_act_conn": "活跃连接数（个）",
        "m3_inact_conn": "非活跃连接数（个）",
        "m4_ncps": "新建连接数（次/秒）",
        "m5_in_pps": "流入数据包速率（个/秒）",
        "m6_out_pps": "流出数据包速率（个/秒）",
        "m7_in_Bps": "网络流入速率（Byte/秒）",
        "m8_out_Bps": "网络流出速率（Byte/秒）",
        "m22_in_bandwidth": "入网带宽（bit/秒）",
        "m23_out_bandwidth": "出网带宽（bit/秒）",
        "l4_con_usage": "四层并发连接使用率（%）",
        "l4_in_bps_usage": "四层入带宽使用率（%）",
        "l4_out_bps_usage": "四层出带宽使用率（%）",
        "l4_ncps_usage": "四层新建连接数使用率（%）",
        "m9_abnormal_servers": "异常后端服务器数（个）",
        "ma_normal_servers": "正常后端服务器数（个）",
        "dropped_connections": "丢弃连接速率（次/秒）",
        "dropped_packets": "丢弃数据包速率（个/秒）",
        "dropped_traffic": "丢弃带宽（bit/秒）"
    }
    
    # 七层指标定义（华为云官方标准指标）
    l7_metrics = {
        "mb_l7_qps": "7层查询速率（QPS，次/秒）",
        "mc_l7_http_2xx": "7层2XX响应状态码速率（个/秒）",
        "md_l7_http_3xx": "7层3XX响应状态码速率（个/秒）",
        "me_l7_http_4xx": "7层4XX响应状态码速率（个/秒）",
        "mf_l7_http_5xx": "7层5XX响应状态码速率（个/秒）",
        "m11_l7_http_404": "7层404响应状态码速率（个/秒）",
        "m12_l7_http_499": "7层499响应状态码速率（个/秒）",
        "m13_l7_http_502": "7层502响应状态码速率（个/秒）",
        "m14_l7_rt": "7层平均响应时间（ms）",
        "m1c_l7_rt_max": "7层最大响应时间（ms）",
        "m1d_l7_rt_min": "7层最小响应时间（ms）",
        "m17_l7_upstream_rt": "7层后端平均响应时间（ms）",
        "l7_con_usage": "7层并发连接使用率（%）",
        "l7_in_bps_usage": "7层入带宽使用率（%）",
        "l7_out_bps_usage": "7层出带宽使用率（%）",
        "l7_ncps_usage": "7层新建连接数使用率（%）",
        "l7_qps_usage": "7层QPS使用率（%）",
        "l7_2xx_ratio": "7层2XX响应占比（%）",
        "l7_4xx_ratio": "7层4XX响应占比（%）",
        "l7_5xx_ratio": "7层5XX响应占比（%）"
    }
    
    # 动态组合要查询的指标
    metric_desc = {}
    if support_l4:
        metric_desc.update(l4_metrics)
    if support_l7:
        metric_desc.update(l7_metrics)
    
    if not metric_desc:
        return {
            "success": False,
            "error": "未识别到ELB支持的指标类型"
        }
    
    if not SDK_AVAILABLE:
        return {
            "success": False,
            "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"
        }

    try:
        client = create_ces_client(region, access_key, secret_key, proj_id)
        metrics_result = {}
        
        for metric_name in metric_desc.keys():
            try:
                request = ShowMetricDataRequest()
                request.namespace = "SYS.ELB"
                request.metric_name = metric_name
                request.dim_0 = f"lbaas_instance_id,{elb_id}"
                request._from = start_time
                request.to = end_time
                request.period = period
                request.filter = "average"
                
                response = client.show_metric_data(request)
                
                if hasattr(response, 'datapoints') and response.datapoints:
                    # 格式化数据
                    processed_data = []
                    for point in response.datapoints:
                        processed_data.append({
                            "timestamp": point.timestamp,
                            "time": datetime.fromtimestamp(point.timestamp/1000, timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                            "average": round(float(getattr(point, 'average', 0)), 2) if getattr(point, 'average', None) is not None else None,
                            "max": round(float(getattr(point, 'max', 0)), 2) if getattr(point, 'max', None) is not None else None,
                            "min": round(float(getattr(point, 'min', 0)), 2) if getattr(point, 'min', None) is not None else None
                        })
                    
                    # 计算最新值
                    latest_value = processed_data[-1]["average"] if processed_data else None
                    
                    metrics_result[metric_name] = {
                        "name_cn": metric_desc[metric_name],
                        "latest_value": latest_value,
                        "unit": metric_desc[metric_name].split("（")[1].rstrip("）") if "（" in metric_desc[metric_name] else "",
                        "time_series": processed_data
                    }
                else:
                    metrics_result[metric_name] = {
                        "name_cn": metric_desc[metric_name],
                        "latest_value": None,
                        "unit": metric_desc[metric_name].split("（")[1].rstrip("）") if "（" in metric_desc[metric_name] else "",
                        "note": "No data available"
                    }
            except Exception as e:
                metrics_result[metric_name] = {
                    "name_cn": metric_desc[metric_name],
                    "error": str(e)
                }
        
        return {
            "success": True,
            "region": region,
            "elb_id": elb_id,
            "elb_name": elb_name,
            "elb_type": elb_type,
            "support_protocol": {
                "layer4": support_l4,
                "layer7": support_l7
            },
            "query_params": {
                "hours": hours,
                "period": period
            },
            "metrics": metrics_result
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"查询ELB监控失败: {str(e)}"
        }
