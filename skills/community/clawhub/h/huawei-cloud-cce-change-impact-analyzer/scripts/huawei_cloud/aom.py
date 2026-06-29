from .common import *


def _filter_events_by_cluster(events: list, cluster_id: Optional[str] = None, cluster_name: Optional[str] = None) -> list:
    """Filter parsed AOM events by CCE cluster identity."""
    if not cluster_id and not cluster_name:
        return events

    filtered = []
    for event in events:
        resource_id = event.get("resource_id", "")
        if cluster_id and (event.get("cluster_id") == cluster_id or cluster_id in resource_id):
            filtered.append(event)
            continue
        if cluster_name and (
            event.get("cluster_name") == cluster_name
            or cluster_name in event.get("cluster_alias_name", "")
        ):
            filtered.append(event)
    return filtered


def _build_aom_dimensions(dimensions: Optional[list]) -> Optional[list]:
    if not dimensions:
        return None
    from huaweicloudsdkaom.v2 import Dimension

    built = []
    for item in dimensions:
        if isinstance(item, Dimension):
            built.append(item)
        elif isinstance(item, dict):
            built.append(Dimension(name=item.get("name"), value=item.get("value")))
        else:
            raise ValueError("dimensions must be a JSON array of objects with name and value")
    return built


def _get_v4_alarm_rule_by_id(region: str, access_key: str, secret_key: str, proj_id: str, rule_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a metric/event alarm rule by id from v4 list API (all enterprise projects)."""
    from huaweicloudsdkaom.v2 import ListMetricOrEventAlarmRuleRequest

    client = create_aom_client(region, access_key, secret_key, proj_id)
    offset = 0
    limit = 200
    while True:
        page = client.list_metric_or_event_alarm_rule(
            ListMetricOrEventAlarmRuleRequest(
                limit=str(limit),
                offset=str(offset),
                enterprise_project_id="all_granted_eps",
            )
        ).to_dict()
        batch = page.get("alarm_rules") or []
        for item in batch:
            if str(item.get("alarm_rule_id")) == str(rule_id):
                return item
        if len(batch) < limit:
            break
        offset += limit
    return None


def _update_v4_alarm_rule_enable(
    region: str,
    access_key: str,
    secret_key: str,
    proj_id: str,
    rule: Dict[str, Any],
    enabled: bool,
) -> Dict[str, Any]:
    """Update alarm_rule_enable via v4 update-alarm-action and verify by readback."""
    from huaweicloudsdkcore.auth.credentials import BasicCredentials
    from huaweicloudsdkcore.signer.signer import Signer
    from huaweicloudsdkcore.sdk_request import SdkRequest
    import json
    import requests

    ep_id = rule.get("enterprise_project_id") or "0"
    payload = {
        "alarm_rule_name": rule.get("alarm_rule_name"),
        "alarm_rule_type": rule.get("alarm_rule_type"),
        "alarm_rule_enable": bool(enabled),
        "alarm_rule_description": rule.get("alarm_rule_description"),
        "prom_instance_id": rule.get("prom_instance_id"),
        "event_alarm_spec": rule.get("event_alarm_spec"),
        "metric_alarm_spec": rule.get("metric_alarm_spec"),
        "alarm_notifications": rule.get("alarm_notifications"),
    }

    host = f"aom.{region}.myhuaweicloud.com"
    path = f"/v4/{proj_id}/alarm-rules"
    req = SdkRequest(
        method="POST",
        schema="https",
        host=host,
        resource_path=path,
        query_params=[("action_id", "update-alarm-action")],
        header_params={
            "Content-Type": "application/json",
            "Enterprise-Project-Id": ep_id,
        },
        body=json.dumps(payload, ensure_ascii=False),
    )
    signer = Signer(BasicCredentials(access_key, secret_key, proj_id))
    signed = signer.sign(req)
    url = f"{signed.schema}://{signed.host}{signed.uri}"
    resp = requests.post(url, headers=signed.header_params, data=signed.body, timeout=30)

    result: Dict[str, Any] = {
        "http_status": resp.status_code,
        "response_text": resp.text if resp.text else None,
    }
    if resp.status_code != 200:
        result["success"] = False
        return result

    verify_rule = _get_v4_alarm_rule_by_id(region, access_key, secret_key, proj_id, str(rule.get("alarm_rule_id")))
    result.update({
        "success": True,
        "verified_alarm_rule_enable": None if not verify_rule else verify_rule.get("alarm_rule_enable"),
        "verified_alarm_rule_status": None if not verify_rule else verify_rule.get("alarm_rule_status"),
        "verified_alarm_update_time": None if not verify_rule else verify_rule.get("alarm_update_time"),
    })
    return result


def _resolve_cluster_and_prom_for_alarm(
    region: str,
    access_key: str,
    secret_key: str,
    proj_id: str,
    cluster_id: Optional[str] = None,
    cluster_name: Optional[str] = None,
    enterprise_project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Resolve cluster id/name and corresponding CCE Prometheus instance for alarm creation."""
    if not cluster_id and not cluster_name:
        return {"success": False, "error": "cluster_id or cluster_name is required"}

    try:
        cce_client = create_cce_client(region, access_key, secret_key, proj_id)
        clusters = cce_client.list_clusters(ListClustersRequest()).to_dict().get("items") or []
    except Exception as e:
        return {"success": False, "error": f"Failed to list CCE clusters: {e}"}

    target = None
    for item in clusters:
        if cluster_id and str(item.get("metadata", {}).get("uuid")) == str(cluster_id):
            target = item
            break
        if cluster_name and str(item.get("metadata", {}).get("name")) == str(cluster_name):
            target = item
            break
    if not target:
        return {
            "success": False,
            "error": f"Cluster not found: cluster_id={cluster_id}, cluster_name={cluster_name}",
        }

    resolved_cluster_id = target.get("metadata", {}).get("uuid")
    resolved_cluster_name = target.get("metadata", {}).get("name")

    from huaweicloudsdkaom.v2 import ListPromInstanceRequest
    aom_client = create_aom_client(region, access_key, secret_key, proj_id)
    ep_scope = enterprise_project_id or "all_granted_eps"
    prom_resp = aom_client.list_prom_instance(
        ListPromInstanceRequest(cce_cluster_enable="true", enterprise_project_id=ep_scope)
    ).to_dict()
    prom_items = prom_resp.get("prometheus") or []

    matched_prom = None
    for item in prom_items:
        cce_spec = str(item.get("cce_spec_config"))
        if str(resolved_cluster_id) in cce_spec:
            matched_prom = item
            break
    if not matched_prom:
        return {
            "success": False,
            "error": f"No Prometheus instance found for cluster_id={resolved_cluster_id}",
        }

    return {
        "success": True,
        "cluster_id": resolved_cluster_id,
        "cluster_name": resolved_cluster_name,
        "prom_instance_id": matched_prom.get("prom_id"),
        "enterprise_project_id": matched_prom.get("enterprise_project_id") or "0",
    }


def _normalize_alarm_rule_name(rule_name: str) -> str:
    return "_".join(str(rule_name).split())


def _resolve_prom_instance_id_for_cluster(
    region: str,
    access_key: str,
    secret_key: str,
    proj_id: str,
    cluster_id: str,
    enterprise_project_id: Optional[str] = None,
) -> Optional[str]:
    from huaweicloudsdkaom.v2 import ListPromInstanceRequest

    prom_resp = create_aom_client(region, access_key, secret_key, proj_id).list_prom_instance(
        ListPromInstanceRequest(
            cce_cluster_enable="true",
            enterprise_project_id=enterprise_project_id or "all_granted_eps",
        )
    )
    for item in (prom_resp.to_dict().get("prometheus") or []):
        if str(cluster_id) in str(item.get("cce_spec_config")):
            return item.get("prom_id")
    return None


def _build_direct_alarm_notification(bind_notification_rule_id: str, notify_frequency: int = 0):
    from huaweicloudsdkaom.v2 import AlarmNotification

    return AlarmNotification(
        notification_type="direct",
        route_group_enable=False,
        route_group_rule="",
        notification_enable=True,
        bind_notification_rule_id=bind_notification_rule_id,
        notify_resolved=False,
        notify_triggered=False,
        notify_frequency=notify_frequency,
    )




def list_aom_instances(region: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, prom_type: Optional[str] = None, enterprise_project_id: Optional[str] = None) -> Dict[str, Any]:
    """List AOM Prometheus instances and their details

    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional, will auto-fetch if not provided)
        prom_type: Filter by Prometheus type (optional) - CCE, APPLICATION, default

    Returns:
        Dictionary with AOM Prometheus instances details including endpoints
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
            "error": "Project ID not found. Please provide project_id parameter or ensure the account has access to the region."
        }

    if not AOM_AVAILABLE:
        return {
            "success": False,
            "error": f"AOM SDK not installed: {AOM_IMPORT_ERROR}"
        }

    try:
        from huaweicloudsdkaom.v2 import AomClient, ListPromInstanceRequest

        client = create_aom_client(region, access_key, secret_key, proj_id)

        ep_scope = enterprise_project_id or "all_granted_eps"
        request = ListPromInstanceRequest(enterprise_project_id=ep_scope)

        response = client.list_prom_instance(request)
        result = response.to_dict()

        instances = result.get('prometheus', [])

        # 按类型过滤
        if prom_type:
            instances = [i for i in instances if i.get('prom_type', '').upper() == prom_type.upper()]

        # 提取关键信息
        formatted_instances = []
        for inst in instances:
            inst_info = {
                "name": inst.get('prom_name'),
                "id": inst.get('prom_id'),
                "type": inst.get('prom_type'),
                "version": inst.get('prom_version'),
                "project_id": inst.get('project_id'),
                "created_at": inst.get('prom_create_timestamp'),
            }

            # 如果有配置信息，提取endpoint
            spec_config = inst.get('prom_spec_config')
            if spec_config:
                inst_info["endpoints"] = {
                    "remote_write_url": spec_config.get('remote_write_url'),
                    "remote_read_url": spec_config.get('remote_read_url'),
                    "prom_http_api_endpoint": spec_config.get('prom_http_api_endpoint'),
                }

            formatted_instances.append(inst_info)

        return {
            "success": True,
            "region": region,
            "action": "list_aom_instances",
            "enterprise_project_id": ep_scope,
            "count": len(formatted_instances),
            "instances": formatted_instances
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

def get_aom_prom_metrics_http(region: str, aom_instance_id: str, query: str, start: int = None, end: int = None, step: int = 60, hours: int = 1, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """Get Prometheus metrics from AOM using direct HTTP request with manual signature
    
    Reference: huaweicloudsdkcore/signer/signer.py
    """
    import hashlib
    import hmac
    import time as time_module
    import urllib.parse
    from urllib.parse import quote, unquote
    import requests
    
    # Auto-fetch project_id if not provided
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    
    if not proj_id:
        return {"success": False, "error": "Project ID not found. Please provide project_id parameter."}
    
    now = int(time_module.time())
    end_time = end if end else now
    start_time = start if start else (end_time - hours * 3600)
    
    # ========== 构建URL和查询参数 ==========
    base_url = "https://aom.{}.myhuaweicloud.com".format(region)
    
    # 查询参数
    query_params = [
        ('end', str(end_time)),
        ('query', query),
        ('start', str(start_time)),
        ('step', str(step))
    ]
    
    # ========== 按SDK方式构建签名 ==========
    
    # 时间戳
    timestamp = time_module.strftime('%Y%m%dT%H%M%SZ', time_module.gmtime(now))
    
    # 1. HTTP方法
    http_method = 'GET'
    
    # 2. Canonical URI - 统一使用 /aom/api/v1/query_range 路径
    # 所有实例都使用: /v1/{project_id}/{instance_id}/aom/api/v1/query_range
    if aom_instance_id and aom_instance_id not in ['default', '0', 'Prometheus_AOM_Default']:
        resource_path = "/v1/{}/{}/aom/api/v1/query_range".format(proj_id, aom_instance_id)
    else:
        resource_path = "/v1/{}/aom/api/v1/query_range".format(proj_id)
    # SDK的_process_canonical_uri会在URI后面加斜杠
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
    host_header = 'aom.{}.myhuaweicloud.com'.format(region)
    
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
    
    # 8. 签名 - 使用hex编码，不是base64！
    signature = hmac.new(
        secret_key.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest().hex()  # 关键：使用hex()，不是base64
    
    # 9. Authorization
    authorization = '{} Access={}, SignedHeaders={}, Signature={}'.format(
        algorithm, access_key, signed_headers, signature)
    
    # 10. 构建请求URL - 使用resource_path
    url_query_string = '&'.join(['{}={}'.format(k, urllib.parse.quote(str(v))) for k, v in query_params])
    url = "{}{}?{}".format(base_url, resource_path, url_query_string)
    
    # 11. 请求headers
    headers = {
        'Host': host_header,
        'X-Project-Id': proj_id,
        'X-Sdk-Date': timestamp,
        'Authorization': authorization,
    }
    
    try:
        resp = requests.get(url, headers=headers, verify=True, timeout=30)
        
        if resp.status_code == 200:
            result = resp.json()
            return {"success": True, "region": region, "aom_instance_id": aom_instance_id, "endpoint": "https://aom." + region + ".myhuaweicloud.com/v1/" + proj_id + "/" + aom_instance_id, "query": query, "time_range": {"start": start_time, "end": end_time, "step": step}, "url": url, "result": result}
        else:
            return {
                "success": False,
                "error": "HTTP " + str(resp.status_code) + ": " + resp.text[:500],
                "url": url,
                "request_headers": {k: v for k, v in headers.items() if k != 'Authorization'},
                "request_context": {
                    "canonical_uri": canonical_uri,
                    "signed_headers": signed_headers,
                },
            }
    except Exception as e:
        return {"success": False, "error": str(e), "url": url}

def list_aom_alarm_rules(region: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100, offset: int = 0, enterprise_project_id: Optional[str] = None) -> Dict[str, Any]:
    """List AOM alarm rules via v4 alarm-rules API
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        limit: Maximum number of rules to return (default: 100)
        offset: Offset for pagination (default: 0)
    
    Returns:
        Dict with success status and list of alarm rules
    """
    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}
    
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    if not proj_id:
        return {"success": False, "error": f"Project ID not found for region={region}"}
    
    try:
        from huaweicloudsdkaom.v2 import ListMetricOrEventAlarmRuleRequest, ListServiceDiscoveryRulesRequest
        
        client = create_aom_client(region, access_key, secret_key, proj_id)
        
        ep_scope = enterprise_project_id or "all_granted_eps"
        metric_rules = []
        event_rules = []
        all_rules = []
        page_size = max(1, limit)
        current_offset = max(0, offset)
        total_count = None

        while True:
            alarm_request = ListMetricOrEventAlarmRuleRequest(
                limit=str(page_size),
                offset=str(current_offset),
                enterprise_project_id=ep_scope,
            )
            page = client.list_metric_or_event_alarm_rule(alarm_request).to_dict()
            if total_count is None:
                total_count = page.get("count")
            batch = page.get("alarm_rules") or []
            if not batch:
                break
            for rule in batch:
                metric_spec = rule.get("metric_alarm_spec") or {}
                event_spec = rule.get("event_alarm_spec") or {}
                trigger = (metric_spec.get("trigger_conditions") or [None])[0] or {}
                event_trigger = (event_spec.get("trigger_conditions") or [None])[0] or {}
                rule_info = {
                    "rule_name": rule.get("alarm_rule_name"),
                    "rule_id": rule.get("alarm_rule_id"),
                    "rule_type": rule.get("alarm_rule_type"),
                    "rule_description": rule.get("alarm_rule_description"),
                    "rule_status": rule.get("alarm_rule_status"),
                    "alarm_level": next(iter(trigger.get("thresholds", {}).keys()), None) or next(iter(event_trigger.get("thresholds", {}).keys()), None),
                    "metric_name": trigger.get("metric_name"),
                    "metric_namespace": trigger.get("metric_namespace"),
                    "promql": trigger.get("promql"),
                    "event_names": [item.get("event_name") for item in (event_spec.get("monitor_objects") or []) if item.get("event_name")],
                    "monitor_objects": metric_spec.get("monitor_objects") or event_spec.get("monitor_objects"),
                    "prom_instance_id": rule.get("prom_instance_id"),
                    "created_at": str(rule.get("alarm_create_time")) if rule.get("alarm_create_time") else None,
                    "updated_at": str(rule.get("alarm_update_time")) if rule.get("alarm_update_time") else None,
                }
                all_rules.append(rule_info)
                if rule.get("alarm_rule_type") == "event":
                    event_rules.append(rule_info)
                else:
                    metric_rules.append(rule_info)

            if len(batch) < page_size:
                break
            current_offset += page_size
            if total_count is not None and current_offset >= int(total_count):
                break

        # 服务发现规则
        sd_request = ListServiceDiscoveryRulesRequest()
        sd_response = client.list_service_discovery_rules(sd_request)
        
        discoveries = []
        if hasattr(sd_response, 'service_discovery_rules') and sd_response.service_discovery_rules:
            for sd in sd_response.service_discovery_rules:
                sd_info = {
                    "id": getattr(sd, 'service_discovery_id', None),
                    "name": getattr(sd, 'service_discovery_name', None),
                    "status": getattr(sd, 'status', None),
                    "type": getattr(sd, 'service_discovery_type', None),
                }
                discoveries.append(sd_info)
        
        return {
            "success": True,
            "region": region,
            "action": "list_aom_alarm_rules",
            "enterprise_project_id": ep_scope,
            "alarm_rules_count": int(total_count) if total_count is not None else len(all_rules),
            "returned_alarm_rules_count": len(all_rules),
            "alarm_rules": all_rules,
            "threshold_alarm_rules_count": len(metric_rules),
            "threshold_alarm_rules": metric_rules,
            "event_alarm_rules_count": len(event_rules),
            "event_alarm_rules": event_rules,
            "service_discovery_count": len(discoveries),
            "service_discovery_rules": discoveries
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def create_aom_alarm_rule(
    region: str,
    rule_name: str,
    metric_name: str,
    namespace: str,
    comparison_operator: str,
    threshold: str,
    period: int,
    evaluation_periods: int,
    statistic: str,
    alarm_level: int,
    create_fields: Optional[Dict[str, Any]] = None,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create an AOM threshold alarm rule. Requires confirm=true to execute."""
    required_values = {
        "rule_name": rule_name,
        "metric_name": metric_name,
        "namespace": namespace,
        "comparison_operator": comparison_operator,
        "threshold": threshold,
        "period": period,
        "evaluation_periods": evaluation_periods,
        "statistic": statistic,
        "alarm_level": alarm_level,
    }
    missing = [key for key, value in required_values.items() if value in (None, "")]
    if missing:
        return {"success": False, "error": f"{', '.join(missing)} are required"}

    create_fields = create_fields or {}
    requested_rule_name = rule_name
    rule_name = _normalize_alarm_rule_name(rule_name)
    rule_payload = {
        **create_fields,
        "requested_rule_name": requested_rule_name,
        "alarm_rule_name": rule_name,
        "metric_name": metric_name,
        "namespace": namespace,
        "comparison_operator": comparison_operator,
        "threshold": threshold,
        "period": period,
        "evaluation_periods": evaluation_periods,
        "statistic": statistic,
        "alarm_level": alarm_level,
    }

    preview = {
        "success": True,
        "action": "create_aom_alarm_rule",
        "region": region,
        "rule_name": rule_name,
        "rule_payload": rule_payload,
        "risk": "MEDIUM",
        "confirm_required": True,
        "will_execute": bool(confirm),
    }
    if not confirm:
        preview.update({
            "executed": False,
            "message": "Preview only. Add confirm=true to create the AOM alarm rule.",
            "confirm_example": f"python3 huawei-cloud.py huawei_create_aom_alarm_rule region={region} rule_name={rule_name} metric_name={metric_name} namespace={namespace} comparison_operator={comparison_operator} threshold={threshold} period={period} evaluation_periods={evaluation_periods} statistic={statistic} alarm_level={alarm_level} confirm=true",
        })
        return preview

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    if not proj_id:
        return {"success": False, "error": f"Project ID not found for region={region}"}

    try:
        if create_fields.get("promql"):
            from huaweicloudsdkaom.v2 import (
                AddOrUpdateMetricOrEventAlarmRuleRequest,
                AddOrUpdateAlarmRuleV4RequestBody,
                AlarmTags,
                MetricAlarmSpec,
                RecoveryCondition,
                TriggerCondition,
            )

            promql = str(create_fields["promql"])
            cluster_id = create_fields.get("cluster_id")
            prom_instance_id = create_fields.get("prom_instance_id")
            enterprise_project_id = create_fields.get("enterprise_project_id") or "0"
            bind_notification_rule_id = create_fields.get("bind_notification_rule_id") or create_fields.get("notification_rule_name")
            alarm_rule_description = create_fields.get("alarm_rule_description") or create_fields.get("alarm_description") or "Created by Codex tool."

            if not cluster_id:
                return {"success": False, "error": "fields.cluster_id is required for PromQL AOM alarm rules"}
            if not bind_notification_rule_id:
                return {"success": False, "error": "fields.bind_notification_rule_id is required for PromQL AOM alarm rules"}

            if not prom_instance_id:
                prom_instance_id = _resolve_prom_instance_id_for_cluster(
                    region,
                    access_key,
                    secret_key,
                    proj_id,
                    cluster_id,
                )
                if not prom_instance_id:
                    return {
                        "success": False,
                        "action": "create_aom_alarm_rule",
                        "region": region,
                        "rule_name": rule_name,
                        "error": f"No Prometheus instance found for cluster_id={cluster_id}",
                    }

            severity = create_fields.get("alarm_level_name") or create_fields.get("severity") or "Major"
            notification = _build_direct_alarm_notification(
                bind_notification_rule_id,
                int(create_fields.get("notify_frequency", 0)),
            )
            trigger = TriggerCondition(
                metric_query_mode=create_fields.get("metric_query_mode", "NATIVE_PROM"),
                metric_namespace=create_fields.get("metric_namespace"),
                metric_name=metric_name,
                metric_unit=create_fields.get("metric_unit") or create_fields.get("unit"),
                metric_labels=create_fields.get("metric_labels", ["cluster", "cluster_name", "node"]),
                promql=promql,
                trigger_times=int(create_fields.get("trigger_times", evaluation_periods or 1)),
                trigger_interval=create_fields.get("trigger_interval", "1m"),
                trigger_type=create_fields.get("trigger_type", "FIXED_RATE"),
                promql_for=create_fields.get("promql_for", "1m"),
                operator=create_fields.get("operator"),
                thresholds={severity: str(create_fields.get("threshold_value", 0))},
            )
            metric_spec = MetricAlarmSpec(
                monitor_type=create_fields.get("monitor_type", "promql"),
                alarm_tags=[
                    AlarmTags(
                        auto_tags=create_fields.get("auto_tags", []),
                        custom_tags=create_fields.get("custom_tags", ["resource_type=node"]),
                        custom_annotations=create_fields.get("custom_annotations", []),
                    )
                ],
                monitor_objects=[{"cluster": cluster_id}],
                recovery_conditions=RecoveryCondition(
                    recovery_timeframe=int(create_fields.get("recovery_timeframe", 1))
                ),
                trigger_conditions=[trigger],
                alarm_rule_template_bind_enable=False,
                alarm_rule_template_id=create_fields.get("alarm_rule_template_id", "at0000000000000000cce001"),
            )
            body = AddOrUpdateAlarmRuleV4RequestBody(
                alarm_notifications=notification,
                alarm_rule_description=alarm_rule_description,
                alarm_rule_enable=True,
                alarm_rule_name=rule_name,
                alarm_rule_type="metric",
                metric_alarm_spec=metric_spec,
                prom_instance_id=prom_instance_id,
                alias=create_fields.get("alias") or rule_name,
            )
            request = AddOrUpdateMetricOrEventAlarmRuleRequest(
                action_id="add-alarm-action",
                enterprise_project_id=enterprise_project_id,
                body=body,
            )
            response = create_aom_client(region, access_key, secret_key, proj_id).add_or_update_metric_or_event_alarm_rule(request)
            return {
                **preview,
                "rule_name": rule_name,
                "rule_payload": {
                    **rule_payload,
                    "alarm_rule_name": rule_name,
                    "cluster_id": cluster_id,
                    "prom_instance_id": prom_instance_id,
                    "enterprise_project_id": enterprise_project_id,
                    "bind_notification_rule_id": bind_notification_rule_id,
                },
                "executed": True,
                "message": "AOM PromQL metric alarm rule created.",
                "request_body": body.to_dict(),
                "response": response.to_dict() if hasattr(response, "to_dict") else str(response),
            }

        from huaweicloudsdkaom.v2 import AddAlarmRuleRequest, AlarmRuleParam

        legacy_rule_payload = {
            key: value for key, value in rule_payload.items()
            if key != "requested_rule_name"
        }
        supported_fields = set(AlarmRuleParam.openapi_types.keys())
        unsupported = sorted(set(legacy_rule_payload) - supported_fields)
        if unsupported:
            return {
                "success": False,
                "error": f"Unsupported create fields: {', '.join(unsupported)}",
                "supported_fields": sorted(supported_fields),
            }

        if "dimensions" in legacy_rule_payload:
            legacy_rule_payload["dimensions"] = _build_aom_dimensions(legacy_rule_payload["dimensions"])

        body = AlarmRuleParam()
        for key, value in legacy_rule_payload.items():
            setattr(body, key, value)

        request = AddAlarmRuleRequest(body=body)
        response = create_aom_client(region, access_key, secret_key, proj_id).add_alarm_rule(request)
        return {
            **preview,
            "executed": True,
            "message": "AOM alarm rule created.",
            "response": response.to_dict() if hasattr(response, "to_dict") else str(response),
        }
    except Exception as e:
        return {
            "success": False,
            "action": "create_aom_alarm_rule",
            "region": region,
            "rule_name": rule_name,
            "error": str(e),
            "error_type": type(e).__name__,
        }


def update_aom_alarm_rule(
    region: str,
    rule_name: str,
    update_fields: Optional[Dict[str, Any]] = None,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Update an AOM threshold alarm rule. Requires confirm=true to execute."""
    if not rule_name:
        return {"success": False, "error": "rule_name is required"}

    update_fields = update_fields or {}
    if not update_fields:
        return {"success": False, "error": "No update fields provided"}

    preview = {
        "success": True,
        "action": "update_aom_alarm_rule",
        "region": region,
        "rule_name": rule_name,
        "update_fields": update_fields,
        "risk": "HIGH",
        "confirm_required": True,
        "will_execute": bool(confirm),
    }
    if not confirm:
        preview.update({
            "executed": False,
            "message": "Preview only. Add confirm=true to update the AOM alarm rule.",
            "confirm_example": f"python3 huawei-cloud.py huawei_update_aom_alarm_rule region={region} rule_name={rule_name} confirm=true ...",
        })
        return preview

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    if not proj_id:
        return {"success": False, "error": f"Project ID not found for region={region}"}

    try:
        from huaweicloudsdkaom.v2 import UpdateAlarmRuleParam, UpdateAlarmRuleRequest

        supported_fields = set(UpdateAlarmRuleParam.openapi_types.keys())
        unsupported = sorted(set(update_fields) - supported_fields)
        if unsupported:
            return {
                "success": False,
                "error": f"Unsupported update fields: {', '.join(unsupported)}",
                "supported_fields": sorted(supported_fields),
            }

        if "dimensions" in update_fields:
            update_fields["dimensions"] = _build_aom_dimensions(update_fields["dimensions"])

        body = UpdateAlarmRuleParam(alarm_rule_name=rule_name)
        for key, value in update_fields.items():
            setattr(body, key, value)

        request = UpdateAlarmRuleRequest(body=body)
        response = create_aom_client(region, access_key, secret_key, proj_id).update_alarm_rule(request)
        return {
            **preview,
            "executed": True,
            "message": "AOM alarm rule updated.",
            "response": response.to_dict() if hasattr(response, "to_dict") else str(response),
        }
    except Exception as e:
        return {
            "success": False,
            "action": "update_aom_alarm_rule",
            "region": region,
            "rule_name": rule_name,
            "error": str(e),
            "error_type": type(e).__name__,
        }


def delete_aom_alarm_rule(
    region: str,
    rule_name: str,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete an AOM metric/event alarm rule by rule name. Requires confirm=true."""
    if not rule_name:
        return {"success": False, "error": "rule_name is required"}

    preview = {
        "success": True,
        "action": "delete_aom_alarm_rule",
        "region": region,
        "rule_name": rule_name,
        "risk": "HIGH",
        "confirm_required": True,
        "will_execute": bool(confirm),
    }
    if not confirm:
        preview.update({
            "executed": False,
            "message": "Preview only. Add confirm=true to delete the AOM alarm rule.",
            "confirm_example": f"python3 huawei-cloud.py huawei_delete_aom_alarm_rule region={region} rule_name={rule_name} confirm=true",
        })
        return preview

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}

    try:
        from huaweicloudsdkaom.v2 import (
            DeleteMetricOrEventAlarmRuleRequest,
            DeleteAlarmRuleV4RequestBody,
            ListMetricOrEventAlarmRuleRequest,
        )

        client = create_aom_client(region, access_key, secret_key, proj_id)
        delete_key = str(rule_name)

        # Verify existence by rule name before delete.
        matched_before = None
        offset = 0
        limit = 200
        while True:
            page = client.list_metric_or_event_alarm_rule(
                ListMetricOrEventAlarmRuleRequest(
                    limit=str(limit),
                    offset=str(offset),
                    enterprise_project_id="all_granted_eps",
                )
            ).to_dict()
            batch = page.get("alarm_rules") or []
            for item in batch:
                if str(item.get("alarm_rule_name")) == delete_key:
                    matched_before = item
                    break
            if matched_before or len(batch) < limit:
                break
            offset += limit

        if not matched_before:
            return {
                **preview,
                "executed": True,
                "verified_deleted": True,
                "message": "Rule not found before deletion; treated as already deleted.",
            }

        req = DeleteMetricOrEventAlarmRuleRequest(
            body=DeleteAlarmRuleV4RequestBody(alarm_rules=[delete_key])
        )
        resp = client.delete_metric_or_event_alarm_rule(req)

        # Verify deletion by name.
        exists_after = False
        offset = 0
        while True:
            page = client.list_metric_or_event_alarm_rule(
                ListMetricOrEventAlarmRuleRequest(
                    limit=str(limit),
                    offset=str(offset),
                    enterprise_project_id="all_granted_eps",
                )
            ).to_dict()
            batch = page.get("alarm_rules") or []
            if any(str(item.get("alarm_rule_name")) == delete_key for item in batch):
                exists_after = True
                break
            if len(batch) < limit:
                break
            offset += limit

        if exists_after:
            return {
                "success": False,
                "action": "delete_aom_alarm_rule",
                "region": region,
                "rule_name": delete_key,
                "executed": True,
                "verified_deleted": False,
                "error": "SDK delete returned success but rule still exists after verification.",
                "response": resp.to_dict() if hasattr(resp, "to_dict") else str(resp),
            }

        return {
            **preview,
            "executed": True,
            "verified_deleted": True,
            "message": "AOM alarm rule deleted and verified.",
            "response": resp.to_dict() if hasattr(resp, "to_dict") else str(resp),
        }
    except Exception as e:
        return {
            "success": False,
            "action": "delete_aom_alarm_rule",
            "region": region,
            "rule_name": rule_name,
            "error": str(e),
            "error_type": type(e).__name__,
        }


def disable_aom_alarm_rule(
    region: str,
    rule_id: str,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Disable an AOM alarm rule by rule_id. Requires confirm=true to execute."""
    if not rule_id:
        return {"success": False, "error": "rule_id is required"}

    preview = {
        "success": True,
        "action": "disable_aom_alarm_rule",
        "region": region,
        "rule_id": str(rule_id),
        "risk": "HIGH",
        "confirm_required": True,
        "will_execute": bool(confirm),
    }
    if not confirm:
        preview.update({
            "executed": False,
            "message": "Preview only. Add confirm=true to disable the AOM alarm rule.",
            "confirm_example": f"python3 huawei-cloud.py huawei_disable_aom_alarm_rule region={region} rule_id={rule_id} confirm=true",
        })
        return preview

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}

    try:
        target = _get_v4_alarm_rule_by_id(region, access_key, secret_key, proj_id, str(rule_id))
        if not target:
            return {
                "success": False,
                "action": "disable_aom_alarm_rule",
                "region": region,
                "rule_id": str(rule_id),
                "error": f"Rule not found by rule_id={rule_id}",
            }

        update_result = _update_v4_alarm_rule_enable(
            region=region,
            access_key=access_key,
            secret_key=secret_key,
            proj_id=proj_id,
            rule=target,
            enabled=False,
        )
        if not update_result.get("success"):
            return {
                "success": False,
                "action": "disable_aom_alarm_rule",
                "region": region,
                "rule_id": str(rule_id),
                "error": f"HTTP {update_result.get('http_status')}: {update_result.get('response_text')}",
            }
        return {
            **preview,
            "executed": True,
            "message": "AOM alarm rule disabled.",
            "verified_alarm_rule_enable": update_result.get("verified_alarm_rule_enable"),
            "verified_alarm_rule_status": update_result.get("verified_alarm_rule_status"),
            "verified_alarm_update_time": update_result.get("verified_alarm_update_time"),
        }
    except Exception as e:
        return {
            "success": False,
            "action": "disable_aom_alarm_rule",
            "region": region,
            "rule_id": str(rule_id),
            "error": str(e),
            "error_type": type(e).__name__,
        }


def enable_aom_alarm_rule(
    region: str,
    rule_id: str,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Enable an AOM alarm rule by rule_id. Requires confirm=true to execute."""
    if not rule_id:
        return {"success": False, "error": "rule_id is required"}

    preview = {
        "success": True,
        "action": "enable_aom_alarm_rule",
        "region": region,
        "rule_id": str(rule_id),
        "risk": "HIGH",
        "confirm_required": True,
        "will_execute": bool(confirm),
    }
    if not confirm:
        preview.update({
            "executed": False,
            "message": "Preview only. Add confirm=true to enable the AOM alarm rule.",
            "confirm_example": f"python3 huawei-cloud.py huawei_enable_aom_alarm_rule region={region} rule_id={rule_id} confirm=true",
        })
        return preview

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}

    try:
        target = _get_v4_alarm_rule_by_id(region, access_key, secret_key, proj_id, str(rule_id))
        if not target:
            return {
                "success": False,
                "action": "enable_aom_alarm_rule",
                "region": region,
                "rule_id": str(rule_id),
                "error": f"Rule not found by rule_id={rule_id}",
            }

        update_result = _update_v4_alarm_rule_enable(
            region=region,
            access_key=access_key,
            secret_key=secret_key,
            proj_id=proj_id,
            rule=target,
            enabled=True,
        )
        if not update_result.get("success"):
            return {
                "success": False,
                "action": "enable_aom_alarm_rule",
                "region": region,
                "rule_id": str(rule_id),
                "error": f"HTTP {update_result.get('http_status')}: {update_result.get('response_text')}",
            }

        return {
            **preview,
            "executed": True,
            "message": "AOM alarm rule enabled.",
            "verified_alarm_rule_enable": update_result.get("verified_alarm_rule_enable"),
            "verified_alarm_rule_status": update_result.get("verified_alarm_rule_status"),
            "verified_alarm_update_time": update_result.get("verified_alarm_update_time"),
        }
    except Exception as e:
        return {
            "success": False,
            "action": "enable_aom_alarm_rule",
            "region": region,
            "rule_id": str(rule_id),
            "error": str(e),
            "error_type": type(e).__name__,
        }


def create_aom_event_alarm_rule(
    region: str,
    cluster_id: str,
    rule_name: str,
    event_name: str,
    bind_notification_rule_id: Optional[str] = None,
    event_label: Optional[str] = None,
    alarm_level: str = "Major",
    description: Optional[str] = None,
    alias: Optional[str] = None,
    trigger_type: str = "immediately",
    frequency: str = "-1",
    prom_instance_id: Optional[str] = None,
    enterprise_project_id: Optional[str] = None,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Create an AOM event alarm rule. Requires confirm=true to execute."""
    cce_event_name_map = {
        "PodOOMKilling": "Pod内存不足OOM##PodOOMKilling",
        "TaskHung": "节点任务夯住##TaskHung",
        "UpdateLoadBalancerFailed": "更新负载均衡失败##UpdateLoadBalancerFailed",
        "OOMKilling": "节点内存不足强杀进程##OOMKilling",
        "InvalidStoragePool": "节点存储池配置有误##InvalidStoragePool",
        "FailedToScaleUpGroup": "节点池扩容节点失败##FailedToScaleUpGroup",
        "ScaleDownFailed": "节点池缩容节点失败##ScaleDownFailed",
        "NodePoolSoldOut": "节点池资源售罄##NodePoolSoldOut",
        "NodeNotReady": "节点状态异常##NodeNotReady",
        "NodeHasDiskPressure": "节点磁盘空间不足##NodeHasDiskPressure",
        "ScaleUpTimedOut": "扩容节点超时##ScaleUpTimedOut",
        "Cluster status is Unavailable": "集群状态不可用##Cluster status is Unavailable",
        "Pod内存不足OOM": "Pod内存不足OOM##PodOOMKilling",
        "节点任务夯住": "节点任务夯住##TaskHung",
        "更新负载均衡失败": "更新负载均衡失败##UpdateLoadBalancerFailed",
        "节点内存不足强杀进程": "节点内存不足强杀进程##OOMKilling",
        "节点存储池配置有误": "节点存储池配置有误##InvalidStoragePool",
        "节点池扩容节点失败": "节点池扩容节点失败##FailedToScaleUpGroup",
        "节点池缩容节点失败": "节点池缩容节点失败##ScaleDownFailed",
        "节点池资源售罄": "节点池资源售罄##NodePoolSoldOut",
        "节点状态异常": "节点状态异常##NodeNotReady",
        "节点磁盘空间不足": "节点磁盘空间不足##NodeHasDiskPressure",
        "扩容节点超时": "扩容节点超时##ScaleUpTimedOut",
        "集群状态不可用": "集群状态不可用##Cluster status is Unavailable",
        "FailedStart": "启动失败##FailedStart",
        "FailedPullImage": "拉取镜像失败##FailedPullImage",
        "BackOffStart": "启动重试失败##BackOffStart",
        "FailedScheduling": "调度失败##FailedScheduling",
        "BackOffPullImage": "拉取镜像重试失败##BackOffPullImage",
        "FailedCreate": "创建失败##FailedCreate",
        "Unhealthy": "状态异常##Unhealthy",
        "FailedDelete": "删除失败##FailedDelete",
        "ErrImageNeverPull": "未拉取镜像异常##ErrImageNeverPull",
        "FailedScaleOut": "扩容失败##FailedScaleOut",
        "FailedStandBy": "待机失败##FailedStandBy",
        "FailedReconfig": "更新配置失败##FailedReconfig",
        "FailedActive": "激活失败##FailedActive",
        "FailedRollback": "回滚失败##FailedRollback",
        "FailedUpdate": "更新失败##FailedUpdate",
        "FailedScaleIn": "缩容失败##FailedScaleIn",
        "FailedRestart": "重启失败##FailedRestart",
        "CreatingLoadBalancerFailed": "创建负载均衡失败##CreatingLoadBalancerFailed",
        "DeletingLoadBalancerFailed": "删除负载均衡失败##DeletingLoadBalancerFailed",
        "Rebooted": "节点重启##Rebooted",
        "NodeNotSchedulable": "节点不可调度##NodeNotSchedulable",
        "NodeOutOfDisk": "节点磁盘空间已满##NodeOutOfDisk",
        "NodeHasInsufficientMemory": "节点内存空间不足##NodeHasInsufficientMemory",
        "ConntrackFull": "节点的连接跟踪表已满##ConntrackFull",
        "KUBELETIsDown": "节点kubelet故障##KUBELETIsDown",
        "KUBEPROXYIsDown": "节点kube-proxy故障##KUBEPROXYIsDown",
        "CNIIsDown": "节点cni插件故障##CNIIsDown",
        "NTPIsDown": "节点ntp服务故障##NTPIsDown",
        "ScaleDown": "缩容节点##ScaleDown",
        "NotTriggerScaleUp": "未触发节点扩容##NotTriggerScaleUp",
        "DeleteUnregistered": "删除未注册节点成功##DeleteUnregistered",
        "ScaleDownEmpty": "缩容空闲节点成功##ScaleDownEmpty",
        "ScaledUpGroup": "节点池扩容节点成功##ScaledUpGroup",
        "ScaleUpFailed": "扩容节点失败##ScaleUpFailed",
        "FixNodeGroupSizeDone": "修复节点池节点个数成功##FixNodeGroupSizeDone",
        "NodeGroupInBackOff": "节点池退避重试中##NodeGroupInBackOff",
        "FixNodeGroupSizeError": "修复节点池节点个数失败##FixNodeGroupSizeError",
        "TriggeredScaleUp": "触发节点扩容##TriggeredScaleUp",
        "StartScaledUpGroup": "节点池扩容节点启动##StartScaledUpGroup",
        "DeleteUnregisteredFailed": "删除未注册节点失败##DeleteUnregisteredFailed",
    }
    allowed_event_names = sorted(set(cce_event_name_map.values()))

    if not cluster_id or not rule_name or not event_name:
        return {"success": False, "error": "cluster_id, rule_name, event_name are required"}

    event_display = cce_event_name_map.get(event_name, event_name)
    if "##" not in event_display and event_label:
        event_display = cce_event_name_map.get(f"{event_label}##{event_name}", f"{event_label}##{event_name}")
    if event_display not in allowed_event_names:
        return {
            "success": False,
            "action": "create_aom_event_alarm_rule",
            "region": region,
            "rule_name": rule_name,
            "error": f"Unsupported event_name: {event_name}",
            "allowed_event_names": allowed_event_names,
        }

    requested_rule_name = rule_name
    rule_name = _normalize_alarm_rule_name(rule_name)
    notification_rule = bind_notification_rule_id or f"auto-cluster-{cluster_id}"
    effective_enterprise_project_id = enterprise_project_id or "0"
    payload = {
        "cluster_id": cluster_id,
        "requested_rule_name": requested_rule_name,
        "rule_name": rule_name,
        "event_name": event_display,
        "bind_notification_rule_id": notification_rule,
        "alarm_level": alarm_level,
        "trigger_type": trigger_type,
        "frequency": frequency,
        "prom_instance_id": prom_instance_id,
        "enterprise_project_id": effective_enterprise_project_id,
        "alias": alias or rule_name,
    }
    preview = {
        "success": True,
        "action": "create_aom_event_alarm_rule",
        "region": region,
        "risk": "MEDIUM",
        "confirm_required": True,
        "will_execute": bool(confirm),
        "rule_payload": payload,
    }
    if not confirm:
        preview.update({
            "executed": False,
            "message": "Preview only. Add confirm=true to create the AOM event alarm rule.",
        })
        return preview

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    if not proj_id:
        return {"success": False, "error": f"Project ID not found for region={region}"}

    try:
        from huaweicloudsdkaom.v2 import (
            AddOrUpdateMetricOrEventAlarmRuleRequest,
            AddOrUpdateAlarmRuleV4RequestBody,
            EventAlarmSpec,
            EventTriggerCondition,
        )

        if not prom_instance_id:
            prom_instance_id = _resolve_prom_instance_id_for_cluster(
                region,
                access_key,
                secret_key,
                proj_id,
                cluster_id,
                enterprise_project_id,
            )
            if not prom_instance_id:
                return {
                    "success": False,
                    "action": "create_aom_event_alarm_rule",
                    "region": region,
                    "rule_name": rule_name,
                    "error": f"No Prometheus instance found for cluster_id={cluster_id}",
                }
            payload["prom_instance_id"] = prom_instance_id

        notification = _build_direct_alarm_notification(
            notification_rule,
            -1 if trigger_type == "immediately" else 0,
        )
        trigger = EventTriggerCondition(
            event_name=event_display,
            trigger_type=trigger_type,
            aggregation_window=0,
            operator=">",
            thresholds={alarm_level: 0},
            frequency=frequency,
        )
        body = AddOrUpdateAlarmRuleV4RequestBody(
            alarm_notifications=notification,
            alarm_rule_description=description or "Created by Codex tool.",
            alarm_rule_enable=True,
            alarm_rule_name=rule_name,
            alarm_rule_type="event",
            event_alarm_spec=EventAlarmSpec(
                alarm_source="CCE",
                event_source="CCE",
                monitor_objects=[{"event_name": event_display, "clusterId": cluster_id}],
                trigger_conditions=[trigger],
                alarm_rule_template_bind_enable=False,
                alarm_rule_template_id="at0000000000000000cce001",
            ),
            prom_instance_id=prom_instance_id,
            alias=alias or rule_name,
        )
        request = AddOrUpdateMetricOrEventAlarmRuleRequest(
            action_id="add-alarm-action",
            enterprise_project_id=effective_enterprise_project_id,
            body=body,
        )
        response = create_aom_client(region, access_key, secret_key, proj_id).add_or_update_metric_or_event_alarm_rule(request)
        return {
            **preview,
            "rule_payload": payload,
            "executed": True,
            "message": "AOM event alarm rule created.",
            "request_body": body.to_dict(),
            "enterprise_project_id": effective_enterprise_project_id,
            "response": response.to_dict() if hasattr(response, "to_dict") else str(response),
        }
    except Exception as e:
        return {
            "success": False,
            "action": "create_aom_event_alarm_rule",
            "region": region,
            "rule_name": rule_name,
            "error": str(e),
            "error_type": type(e).__name__,
        }


def list_aom_action_rules(
    region: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    enterprise_project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """List AOM action rules (notification rules)
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        enterprise_project_id: Enterprise project scope (default all_granted_eps)
    
    Returns:
        Dict with success status and list of action rules
    """
    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}
    
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    
    try:
        from huaweicloudsdkaom.v2 import ListActionRuleRequest
        
        client = create_aom_client(region, access_key, secret_key, proj_id)
        
        ep_scope = enterprise_project_id or "all_granted_eps"
        request = ListActionRuleRequest()
        
        response = client.list_action_rule(request)
        
        rules = []
        if hasattr(response, 'action_rules') and response.action_rules:
            for rule in response.action_rules:
                rule_info = {
                    "rule_name": getattr(rule, 'rule_name', None),
                    "description": getattr(rule, 'desc', None),
                    "type": getattr(rule, 'type', None),
                    "notification_template": getattr(rule, 'notification_template', None),
                    "time_zone": getattr(rule, 'time_zone', None),
                    "create_time": getattr(rule, 'create_time', None),
                    "update_time": getattr(rule, 'update_time', None),
                    "user_name": getattr(rule, 'user_name', None),
                }
                
                # 获取SMN主题
                smn_topics = getattr(rule, 'smn_topics', [])
                if smn_topics:
                    rule_info["smn_topics"] = [
                        {
                            "name": getattr(t, 'name', None),
                            "topic_urn": getattr(t, 'topic_urn', None),
                            "status": getattr(t, 'status', None),
                            "push_policy": getattr(t, 'push_policy', None),
                        } for t in smn_topics
                    ]
                
                rules.append(rule_info)
        
        return {
            "success": True,
            "region": region,
            "action": "list_aom_action_rules",
            "enterprise_project_id": ep_scope,
            "enterprise_project_filter_supported": False,
            "enterprise_project_filter_note": "Current AOM SDK list_action_rule interface does not accept enterprise_project_id filtering.",
            "count": len(rules),
            "action_rules": rules
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def delete_aom_action_rule(
    region: str,
    rule_name: str,
    confirm: bool = False,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete an AOM action rule (notification rule). Requires confirm=true to execute."""
    if not rule_name:
        return {"success": False, "error": "rule_name is required"}

    preview = {
        "success": True,
        "action": "delete_aom_action_rule",
        "region": region,
        "rule_name": rule_name,
        "risk": "HIGH",
        "confirm_required": True,
        "will_execute": bool(confirm),
    }
    if not confirm:
        preview.update({
            "executed": False,
            "message": "Preview only. Add confirm=true to delete the AOM action rule.",
            "confirm_example": f"python3 huawei-cloud.py huawei_delete_aom_action_rule region={region} rule_name={rule_name} confirm=true",
        })
        return preview

    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}

    try:
        from huaweicloudsdkaom.v2 import DeleteActionRuleRequest

        request = DeleteActionRuleRequest(body=[rule_name])
        response = create_aom_client(region, access_key, secret_key, proj_id).delete_action_rule(request)
        return {
            **preview,
            "executed": True,
            "message": "AOM action rule deleted.",
            "response": response.to_dict() if hasattr(response, "to_dict") else str(response),
        }
    except Exception as e:
        return {
            "success": False,
            "action": "delete_aom_action_rule",
            "region": region,
            "rule_name": rule_name,
            "error": str(e),
            "error_type": type(e).__name__,
        }

def list_aom_mute_rules(region: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None) -> Dict[str, Any]:
    """List AOM mute rules (silence rules)
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
    
    Returns:
        Dict with success status and list of mute rules
    """
    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}
    
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    
    try:
        from huaweicloudsdkaom.v2 import ListMuteRuleRequest
        
        client = create_aom_client(region, access_key, secret_key, proj_id)
        
        request = ListMuteRuleRequest()
        
        response = client.list_mute_rule(request)
        
        rules = []
        if hasattr(response, 'mute_rules') and response.mute_rules:
            for rule in response.mute_rules:
                rule_info = {
                    "rule_id": getattr(rule, 'rule_id', None),
                    "rule_name": getattr(rule, 'rule_name', None),
                    "description": getattr(rule, 'description', None),
                    "status": getattr(rule, 'status', None),
                    "create_time": getattr(rule, 'create_time', None),
                    "update_time": getattr(rule, 'update_time', None),
                }
                rules.append(rule_info)
        
        return {
            "success": True,
            "region": region,
            "action": "list_aom_mute_rules",
            "count": len(rules),
            "mute_rules": rules
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }

def list_aom_current_alarms(region: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, event_type: str = "active_alert", event_severity: str = None, time_range: str = None, limit: int = 100, cluster_id: Optional[str] = None) -> Dict[str, Any]:
    """List AOM events and alerts using ListEvents API
    
    Args:
        region: Huawei Cloud region (e.g., cn-north-4)
        ak: Access Key ID (optional)
        sk: Secret Access Key (optional)
        project_id: Project ID (optional)
        event_type: Query type - 'active_alert' (active alerts), 'history_alert' (historical alerts), or empty for all (default: 'active_alert')
        event_severity: Filter by severity - 'Critical', 'Major', 'Minor', 'Info' (optional)
        time_range: Time range in format 'startTime.endTime.duration', e.g., '-1.-1.60' for last 60 minutes (default: last 24 hours)
        limit: Maximum number of events to return (default: 100)
        cluster_id: Filter events to a specific CCE cluster ID (optional)
    
    Returns:
        Dict with success status and list of events/alerts
    
    API Reference: https://support.huaweicloud.com/api-aom/ListEvents.html
    """
    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}
    
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}
    
    try:
        from huaweicloudsdkaom.v2 import (
            ListEventsRequest, 
            EventQueryParam2,
            RelationModel,
            EventQueryParam2Sort
        )
        
        client = create_aom_client(region, access_key, secret_key, proj_id)
        
        # 构建请求
        request = ListEventsRequest()
        
        # 设置查询类型
        if event_type:
            request.type = event_type
        
        request.limit = limit
        
        # 构建请求体
        body = EventQueryParam2()
        
        # 时间范围：默认最近24小时
        if time_range:
            body.time_range = time_range
        else:
            body.time_range = "-1.-1.1440"  # 最近24小时 (1440分钟)
        
        # 构建查询条件
        metadata_relations = []
        
        # 事件类型条件
        metadata_relations.append(
            RelationModel(
                key="event_type",
                value=["alarm"],
                relation="AND"
            )
        )
        
        # 严重级别条件
        if event_severity:
            severities = [event_severity] if isinstance(event_severity, str) else event_severity
            metadata_relations.append(
                RelationModel(
                    key="event_severity",
                    value=severities,
                    relation="AND"
                )
            )
        else:
            # 默认查询所有级别
            metadata_relations.append(
                RelationModel(
                    key="event_severity",
                    value=["Critical", "Major", "Minor", "Info"],
                    relation="AND"
                )
            )
        
        body.metadata_relation = metadata_relations
        
        # 排序：按开始时间倒序
        sort = EventQueryParam2Sort(
            order_by=["starts_at"],
            order="desc"
        )
        body.sort = sort
        
        # 搜索条件（可选）
        body.search = ""
        
        request.body = body
        
        # 发送请求
        response = client.list_events(request)
        
        # 解析响应
        events = []
        if hasattr(response, 'events') and response.events:
            for event in response.events:
                event_info = {
                    'id': getattr(event, 'id', None),
                    'event_sn': getattr(event, 'event_sn', None),
                    'starts_at': getattr(event, 'starts_at', None),
                    'ends_at': getattr(event, 'ends_at', None),
                    'arrives_at': getattr(event, 'arrives_at', None),
                    'timeout': getattr(event, 'timeout', None),
                    'enterprise_project_id': getattr(event, 'enterprise_project_id', None),
                }
                
                # 解析metadata
                metadata = getattr(event, 'metadata', {})
                if metadata:
                    event_info['event_name'] = metadata.get('event_name')
                    event_info['event_severity'] = metadata.get('event_severity')
                    event_info['event_type'] = metadata.get('event_type')
                    event_info['resource_provider'] = metadata.get('resource_provider')
                    event_info['resource_type'] = metadata.get('resource_type')
                    event_info['resource_id'] = metadata.get('resource_id')
                
                # 从resource_id解析集群信息
                resource_id = metadata.get('resource_id', '') if metadata else ''
                if resource_id:
                    # 解析格式: clusterName=xxx;clusterID=xxx;...
                    parts = resource_id.split(';')
                    for part in parts:
                        if '=' in part:
                            key, value = part.split('=', 1)
                            if key == 'clusterName':
                                event_info['cluster_name'] = value
                            elif key == 'clusterID':
                                event_info['cluster_id'] = value
                            elif key == 'namespace':
                                event_info['namespace'] = value
                            elif key == 'name':
                                event_info['pod_name'] = value
                            elif key == 'kind':
                                event_info['resource_kind'] = value
                            elif key == 'clusterAliasName':
                                event_info['cluster_alias_name'] = value
                
                # 解析annotations
                annotations = getattr(event, 'annotations', {})
                if annotations:
                    event_info['message'] = annotations.get('message')
                    event_info['alarm_probableCause_zh_cn'] = annotations.get('alarm_probableCause_zh_cn')
                    event_info['alarm_fix_suggestion_zh_cn'] = annotations.get('alarm_fix_suggestion_zh_cn')
                
                # 判断告警状态
                ends_at = getattr(event, 'ends_at', None)
                if ends_at and ends_at > 0:
                    event_info['status'] = 'resolved'
                else:
                    event_info['status'] = 'firing'
                
                events.append(event_info)
        
        events = _filter_events_by_cluster(events, cluster_id=cluster_id)

        # 分页信息
        page_info = {}
        if hasattr(response, 'page_info') and response.page_info:
            page_info = {
                'current_count': getattr(response.page_info, 'current_count', 0),
                'next_marker': getattr(response.page_info, 'next_marker', None),
                'previous_marker': getattr(response.page_info, 'previous_marker', None),
            }
        
        # 统计
        firing_count = sum(1 for e in events if e.get('status') == 'firing')
        resolved_count = sum(1 for e in events if e.get('status') == 'resolved')
        
        # 按严重级别统计
        severity_stats = {}
        for e in events:
            sev = e.get('event_severity', 'Unknown')
            severity_stats[sev] = severity_stats.get(sev, 0) + 1
        
        return {
            "success": True,
            "region": region,
            "action": "list_aom_current_alarms",
            "api": "ListEvents",
            "query_type": event_type,
            "cluster_id": cluster_id,
            "time_range": body.time_range,
            "total_count": len(events),
            "firing_count": firing_count,
            "resolved_count": resolved_count,
            "severity_stats": severity_stats,
            "events": events,
            "page_info": page_info
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def list_aom_alarms(
    region: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    hours: int = 1,
    event_severity: Optional[str] = None,
    cluster_id: Optional[str] = None,
    cluster_name: Optional[str] = None,
    limit: int = 500,
) -> Dict[str, Any]:
    """查询所有告警（活跃 + 历史），合并去重后返回。

    核心原则：查告警必须同时看「正在触发的」和「已恢复的」，因为：
    - 资源类告警（CPU/内存/磁盘）往往持续时间短，查的时候可能已恢复
    - 压测、突发流量等场景下告警恢复快，只看 active 会漏掉关键事件
    - 已恢复的告警仍然有价值：说明曾经出现过异常，需要关注

    Args:
        region: 华为云区域
        ak/sk/project_id: 认证信息
        hours: 查询时间范围(小时)
        event_severity: 严重级别过滤 (Critical/Major/Minor/Info)
        cluster_id: 集群 ID 过滤(可选)
        cluster_name: 集群名称过滤(可选)
        limit: 每种类型的最大返回条数

    Returns:
        Dict with combined events, stats, and per-type summary
    """
    from datetime import datetime, timezone, timedelta
    import re

    time_range_minutes = hours * 60
    time_range_str = f"-1.-1.{time_range_minutes}"
    tz8 = timezone(timedelta(hours=8))

    # 1) 查询活跃告警
    active_result = list_aom_current_alarms(
        region=region, ak=ak, sk=sk, project_id=project_id,
        event_type='active_alert',
        event_severity=event_severity,
        time_range=time_range_str,
        limit=limit,
        cluster_id=cluster_id,
    )
    active_events = active_result.get('events', []) if active_result.get('success') else []

    # 2) 查询历史告警
    history_result = list_aom_current_alarms(
        region=region, ak=ak, sk=sk, project_id=project_id,
        event_type='history_alert',
        event_severity=event_severity,
        time_range=time_range_str,
        limit=limit,
        cluster_id=cluster_id,
    )
    history_events = history_result.get('events', []) if history_result.get('success') else []

    # 3) 合并去重（按 event_sn 去重）
    seen_sns = set()
    all_events = []
    for e in active_events + history_events:
        sn = e.get('event_sn')
        if sn and sn in seen_sns:
            continue
        if sn:
            seen_sns.add(sn)
        all_events.append(e)

    # 4) 按集群 ID 或集群名称过滤
    all_events = _filter_events_by_cluster(all_events, cluster_id=cluster_id, cluster_name=cluster_name)

    # 5) 统计分析
    firing_count = sum(1 for e in all_events if e.get('status') == 'firing')
    resolved_count = sum(1 for e in all_events if e.get('status') == 'resolved')

    # 按告警类型分组统计
    type_stats = {}
    for e in all_events:
        name = e.get('event_name', 'Unknown')
        if name not in type_stats:
            type_stats[name] = {'count': 0, 'firing': 0, 'resolved': 0}
        type_stats[name]['count'] += 1
        if e.get('status') == 'firing':
            type_stats[name]['firing'] += 1
        else:
            type_stats[name]['resolved'] += 1

    # 按严重级别统计
    severity_stats = {}
    for e in all_events:
        sev = e.get('event_severity', 'Unknown')
        severity_stats[sev] = severity_stats.get(sev, 0) + 1

    # 6) 生成可读摘要
    lines = []
    lines.append(f'📊 告警查询报告 (近 {hours} 小时, 活跃+历史)')
    lines.append(f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    lines.append(f'活跃告警: {firing_count} 条 | 已恢复: {resolved_count} 条 | 合并去重后: {len(all_events)} 条')
    lines.append('')

    if type_stats:
        lines.append('按类型统计:')
        sorted_types = sorted(type_stats.items(), key=lambda x: x[1]['count'], reverse=True)
        for name, stats in sorted_types:
            status_str = f"🔴{stats['firing']}条触发中" if stats['firing'] > 0 else f"✅{stats['resolved']}条已恢复"
            lines.append(f'  {name}: {stats["count"]}条 ({status_str})')
        lines.append('')

    # 突出显示资源类告警 (CPU/内存/磁盘 等)
    resource_alarms = [e for e in all_events if any(
        kw in (e.get('event_name', '') + ' ' + e.get('message', ''))
        for kw in ['CPU', 'cpu', 'Memory', 'memory', '内存', '磁盘', 'Disk', 'OOM', 'oom', 'Pressure', 'pressure']
    )]
    if resource_alarms:
        lines.append(f'⚠️ 资源相关告警 ({len(resource_alarms)} 条) — 重点关注!')
        lines.append('─' * 40)
        for e in sorted(resource_alarms, key=lambda x: x.get('starts_at', 0), reverse=True)[:10]:
            ts = datetime.fromtimestamp(e['starts_at']/1000, tz=tz8).strftime('%H:%M:%S') if e.get('starts_at') else '?'
            status = '🔴触发中' if e.get('status') == 'firing' else '✅已恢复'
            lines.append(f'  [{ts}] {e.get("event_name", "")} {status}')
            msg = e.get('message', '')[:120]
            if msg:
                lines.append(f'    {msg}')
        lines.append('')

    report = '\n'.join(lines)

    return {
        'success': True,
        'region': region,
        'action': 'list_aom_alarms',
        'hours': hours,
        'cluster_id': cluster_id,
        'cluster_name': cluster_name,
        'total_count': len(all_events),
        'firing_count': firing_count,
        'resolved_count': resolved_count,
        'active_count': len(active_events),
        'history_count': len(history_events),
        'type_stats': type_stats,
        'severity_stats': severity_stats,
        'events': all_events,
        'report': report,
        'message': f'查询完成: {len(all_events)}条告警(活跃{firing_count}+已恢复{resolved_count}), {len(type_stats)}种类型',
    }


def analyze_aom_alarms(
    region: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    cluster_id: Optional[str] = None,
    cluster_name: Optional[str] = None,
    hours: int = 1,
    chronic_threshold: int = 5,
    sudden_window_minutes: int = 10,
) -> Dict[str, Any]:
    """智能告警过滤分析 — 区分突发告警与常态告警，标注优先级。

    策略:
      - 常态告警 (chronic): 同一告警类型+同一资源在时间段内反复出现 >= chronic_threshold 次，
        或命中已知常态模式(Pending/FailedScheduling/NotTriggerScaleUp 等) → 🟢 低优先级
      - 突发告警 (sudden): 首次出现或近期突然新增，且不在常态模式中 → 🔴 高优先级
      - 关注告警 (attention): 反复出现但可能重要的告警(如CPU/内存/磁盘相关) → 🟡 中优先级

    Args:
        region: 华为云区域
        ak/sk/project_id: 认证信息
        cluster_id: 集群 ID 过滤(可选)
        cluster_name: 集群名称过滤(可选)
        hours: 查询时间范围(小时)
        chronic_threshold: 同一告警在时间窗口内重复出现次数>=此值才视为常态
        sudden_window_minutes: 突发告警判定窗口(分钟)，仅在此窗口内首次出现的告警视为突发

    Returns:
        Dict with grouped alarms, priority tags, summary stats
    """
    from datetime import datetime, timezone, timedelta
    import re

    # 1) Fetch ALL alarms (active + history) — 活跃和已恢复的告警都要看
    result = list_aom_alarms(
        region=region, ak=ak, sk=sk, project_id=project_id,
        hours=hours, cluster_id=cluster_id, cluster_name=cluster_name,
    )
    if not result.get('success'):
        return {'success': False, 'error': f'获取告警失败: {result.get("error", "")}'}

    all_alarms = result.get('events', [])
    if not all_alarms:
        return {
            'success': True, 'region': region,
            'cluster_id': cluster_id, 'cluster_name': cluster_name,
            'total_alarms': 0,
            'sudden_alarms': [], 'attention_alarms': [], 'chronic_alarms': [],
            'summary': {'total': 0, 'sudden': 0, 'attention': 0, 'chronic': 0},
            'message': f'近{hours}小时无告警（活跃+历史均无）',
        }

    # Cluster filter already applied in list_aom_alarms if cluster_id or cluster_name is set

    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    sudden_window_ms = sudden_window_minutes * 60 * 1000

    # 2) Known chronic patterns — alarm names that are typically low-priority noise
    CHRONIC_PATTERNS = [
        'NotTriggerScaleUp', '未触发节点扩容',
        'FailedScheduling', '调度失败',
        'Unhealthy', '不健康',
        'NodeNotReady', '节点未就绪',
    ]

    # 3) Resource-related keywords — these should get attention even if recurring
    RESOURCE_KEYWORDS = [
        'CPU', 'cpu', 'Memory', 'memory', '内存', '磁盘', 'Disk', 'disk',
        'OOM', 'oom', 'Evicted', 'evicted', '驱赶',
        'CrashLoopBackOff', 'crashloopbackoff',
        'Pressure', 'pressure', '压力',
        'NetworkUnavailable', 'network-unavailable',
    ]

    # 4) Group alarms by (event_name, resource_key) for dedup & frequency analysis
    #    resource_key = namespace + pod_name or resource_id (shortened)
    groups: Dict[str, Dict] = {}

    for alarm in all_alarms:
        event_name = alarm.get('event_name', 'Unknown')
        namespace = alarm.get('namespace', '')
        pod_name = alarm.get('pod_name', '')
        resource_id = alarm.get('resource_id', '')

        # Build a dedup key: event_name + resource identity
        if pod_name:
            # Strip deployment hash suffix for grouping (nginx-56fbbc86f-2btqn → nginx-*)
            base_pod = re.sub(r'-[a-z0-9]{5,10}$', '', pod_name)
            resource_key = f'{namespace}/{base_pod}'
        else:
            # Fallback: use first 80 chars of resource_id
            resource_key = resource_id[:80]

        group_key = f'{event_name}||{resource_key}'

        if group_key not in groups:
            groups[group_key] = {
                'event_name': event_name,
                'resource_key': resource_key,
                'namespace': namespace,
                'pod_name': pod_name,
                'pods': set(),
                'sample_alarm': alarm,
                'count': 0,
                'first_seen_ms': now_ms,
                'last_seen_ms': 0,
                'severity': alarm.get('event_severity', 'Major'),
                'messages': set(),
            }

        g = groups[group_key]
        g['count'] += 1
        if pod_name:
            g['pods'].add(pod_name)
        starts = alarm.get('starts_at', 0)
        if starts and starts < g['first_seen_ms']:
            g['first_seen_ms'] = starts
        if starts and starts > g['last_seen_ms']:
            g['last_seen_ms'] = starts
        msg = alarm.get('message', '')[:200]
        if msg:
            g['messages'].add(msg)

    # 5) Classify each group
    sudden_alarms = []
    attention_alarms = []
    chronic_alarms = []

    for gk, g in groups.items():
        event_name = g['event_name']
        count = g['count']
        first_seen = g['first_seen_ms']
        severity = g['severity']

        # Time since first alarm in this group
        time_span_ms = now_ms - first_seen if first_seen else 0
        is_recently_started = (now_ms - first_seen) < sudden_window_ms if first_seen else False

        # Check if alarm matches known chronic pattern
        is_chronic_pattern = any(p in event_name for p in CHRONIC_PATTERNS)

        # Check if alarm has resource keywords
        has_resource_keyword = any(kw in event_name or any(kw in m for m in g['messages'])
                                    for kw in RESOURCE_KEYWORDS)

        # Determine priority
        if is_chronic_pattern and count >= chronic_threshold and not has_resource_keyword:
            # Classic chronic: known noise pattern, repeated many times
            priority = 'chronic'
            priority_label = '🟢 常态'
            reason = f'已知常态模式({event_name})在{hours}h内重复{count}次'
        elif is_chronic_pattern and count >= chronic_threshold and has_resource_keyword:
            # Chronic pattern BUT has resource keywords — needs attention
            priority = 'attention'
            priority_label = '🟡 关注'
            reason = f'虽为常见模式但涉及资源指标({event_name})，重复{count}次'
        elif is_recently_started and count <= 3:
            # Just appeared, few occurrences — sudden
            priority = 'sudden'
            priority_label = '🔴 突发'
            reason = f'近{sudden_window_minutes}分钟内首次出现，当前{count}次'
        elif has_resource_keyword and count <= chronic_threshold:
            # Resource-related but not yet chronic → attention/sudden
            priority = 'sudden'
            priority_label = '🔴 突发'
            reason = f'涉及资源指标(CPU/内存/磁盘)且出现次数较少({count}次)'
        elif has_resource_keyword:
            priority = 'attention'
            priority_label = '🟡 关注'
            reason = f'涉及资源指标，重复{count}次需持续关注'
        elif is_recently_started:
            priority = 'sudden'
            priority_label = '🔴 突发'
            reason = f'近{sudden_window_minutes}分钟内新增，当前{count}次'
        elif is_chronic_pattern:
            priority = 'chronic'
            priority_label = '🟢 常态'
            reason = f'已知常态模式({event_name})'
        elif count >= chronic_threshold:
            priority = 'chronic'
            priority_label = '🟢 常态'
            reason = f'重复{count}次，属于持续性问题'
        else:
            priority = 'attention'
            priority_label = '🟡 关注'
            reason = f'出现{count}次，需要关注'

        # Build alarm entry
        entry = {
            'priority': priority,
            'priority_label': priority_label,
            'event_name': event_name,
            'namespace': g['namespace'],
            'pods': sorted(g['pods']),
            'pod_count': len(g['pods']),
            'alarm_count': count,
            'severity': severity,
            'first_seen': datetime.fromtimestamp(g['first_seen_ms'] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC') if g['first_seen_ms'] else '-',
            'last_seen': datetime.fromtimestamp(g['last_seen_ms'] / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC') if g['last_seen_ms'] else '-',
            'sample_message': list(g['messages'])[0] if g['messages'] else '-',
            'reason': reason,
        }

        if priority == 'sudden':
            sudden_alarms.append(entry)
        elif priority == 'attention':
            attention_alarms.append(entry)
        else:
            chronic_alarms.append(entry)

    # 5.5) Cross-group correlation: if a Pod/resource has chronic alarms,
    #       its other alarm types should also be marked chronic (same root cause)
    chronic_resources = set()
    for a in chronic_alarms:
        # Build resource identity from namespace + pods
        for pod in a.get('pods', []):
            # Strip deployment hash to get base deployment name
            base_pod = re.sub(r'-[a-z0-9]{5,10}$', '', pod)
            chronic_resources.add(f'{a["namespace"]}/{base_pod}')
        if not a.get('pods') and a.get('resource_key'):
            chronic_resources.add(a['resource_key'])

    # Check sudden/attention alarms — if same resource as chronic, downgrade
    demoted_from_sudden = []
    demoted_from_attention = []
    remaining_sudden = []
    remaining_attention = []

    for a in sudden_alarms:
        is_related = False
        for pod in a.get('pods', []):
            base_pod = re.sub(r'-[a-z0-9]{5,10}$', '', pod)
            if f'{a["namespace"]}/{base_pod}' in chronic_resources:
                is_related = True
                break
        if not is_related and a.get('resource_key') in chronic_resources:
            is_related = True

        if is_related and not any(kw in a['event_name'] or any(kw in (a.get('sample_message','')) for kw in RESOURCE_KEYWORDS) for kw in RESOURCE_KEYWORDS):
            a['priority'] = 'chronic'
            a['priority_label'] = '🟢 常态'
            a['reason'] = f'与常态告警同源(Pod: {", ".join(a["pods"][:2])})，根因相同，降级'
            demoted_from_sudden.append(a)
        else:
            remaining_sudden.append(a)

    for a in attention_alarms:
        is_related = False
        for pod in a.get('pods', []):
            base_pod = re.sub(r'-[a-z0-9]{5,10}$', '', pod)
            if f'{a["namespace"]}/{base_pod}' in chronic_resources:
                is_related = True
                break
        if is_related and not any(kw in a['event_name'] or any(kw in (a.get('sample_message','')) for kw in RESOURCE_KEYWORDS) for kw in RESOURCE_KEYWORDS):
            a['priority'] = 'chronic'
            a['priority_label'] = '🟢 常态'
            a['reason'] = f'与常态告警同源(Pod: {", ".join(a["pods"][:2])})，根因相同，降级'
            demoted_from_attention.append(a)
        else:
            remaining_attention.append(a)

    sudden_alarms = remaining_sudden
    attention_alarms = remaining_attention
    chronic_alarms = chronic_alarms + demoted_from_sudden + demoted_from_attention

    # Sort each list by alarm_count desc
    sudden_alarms.sort(key=lambda x: x['alarm_count'], reverse=True)
    attention_alarms.sort(key=lambda x: x['alarm_count'], reverse=True)
    chronic_alarms.sort(key=lambda x: x['alarm_count'], reverse=True)

    # 6) Build summary
    total = len(all_alarms)
    unique_groups = len(groups)
    summary = {
        'total_raw_alarms': total,
        'unique_alarm_groups': unique_groups,
        'sudden_count': len(sudden_alarms),
        'attention_count': len(attention_alarms),
        'chronic_count': len(chronic_alarms),
        'sudden_alarm_raw_count': sum(a['alarm_count'] for a in sudden_alarms),
        'attention_alarm_raw_count': sum(a['alarm_count'] for a in attention_alarms),
        'chronic_alarm_raw_count': sum(a['alarm_count'] for a in chronic_alarms),
        'noise_reduction_pct': round(
            sum(a['alarm_count'] for a in chronic_alarms) / total * 100, 1
        ) if total > 0 else 0,
    }

    # 7) Build text report for quick reading
    lines = []
    lines.append(f'📊 告警过滤分析报告 (近 {hours} 小时)')
    lines.append(f'━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
    lines.append(f'原始告警: {total} 条 → 去重后: {unique_groups} 组')
    lines.append(f'噪音削减: {summary["noise_reduction_pct"]}% 的告警为常态重复')
    lines.append('')

    if sudden_alarms:
        lines.append(f'🔴 突发告警 ({len(sudden_alarms)} 组) — 重点关注!')
        lines.append('─' * 40)
        for a in sudden_alarms:
            pods_str = ', '.join(a['pods'][:3]) + ('...' if len(a['pods']) > 3 else '')
            lines.append(f'  [{a["severity"]}] {a["event_name"]}')
            lines.append(f'    命名空间: {a["namespace"]} | Pod: {pods_str}')
            lines.append(f'    次数: {a["alarm_count"]} | {a["reason"]}')
            if a['sample_message'] != '-':
                lines.append(f'    消息: {a["sample_message"][:120]}')
            lines.append('')
    else:
        lines.append('🔴 突发告警: 无 ✅')
        lines.append('')

    if attention_alarms:
        lines.append(f'🟡 关注告警 ({len(attention_alarms)} 组)')
        lines.append('─' * 40)
        for a in attention_alarms:
            pods_str = ', '.join(a['pods'][:3]) + ('...' if len(a['pods']) > 3 else '')
            lines.append(f'  [{a["severity"]}] {a["event_name"]}')
            lines.append(f'    命名空间: {a["namespace"]} | Pod: {pods_str}')
            lines.append(f'    次数: {a["alarm_count"]} | {a["reason"]}')
            lines.append('')
    else:
        lines.append('🟡 关注告警: 无')
        lines.append('')

    if chronic_alarms:
        lines.append(f'🟢 常态告警 ({len(chronic_alarms)} 组) — 低优先级')
        lines.append('─' * 40)
        for a in chronic_alarms:
            pods_str = ', '.join(a['pods'][:3]) + ('...' if len(a['pods']) > 3 else '')
            lines.append(f'  [{a["severity"]}] {a["event_name"]}')
            lines.append(f'    命名空间: {a["namespace"]} | Pod: {pods_str}')
            lines.append(f'    次数: {a["alarm_count"]} | {a["reason"]}')
            lines.append('')
    else:
        lines.append('🟢 常态告警: 无')
        lines.append('')

    report = '\n'.join(lines)

    return {
        'success': True,
        'region': region,
        'cluster_id': cluster_id,
        'cluster_name': cluster_name,
        'hours': hours,
        'chronic_threshold': chronic_threshold,
        'sudden_window_minutes': sudden_window_minutes,
        'summary': summary,
        'sudden_alarms': sudden_alarms,
        'attention_alarms': attention_alarms,
        'chronic_alarms': chronic_alarms,
        'report': report,
        'message': f'告警过滤完成: {total}条原始告警 → {summary["sudden_count"]}突发 + {summary["attention_count"]}关注 + {summary["chronic_count"]}常态 (噪音削减{summary["noise_reduction_pct"]}%)',
    }
