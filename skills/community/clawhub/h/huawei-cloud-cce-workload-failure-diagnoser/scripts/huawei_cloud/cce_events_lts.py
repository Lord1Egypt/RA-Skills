"""
Query Kubernetes events from LTS log streams.

This module implements huawei_query_k8s_events_from_lts tool which:
1. Gets LogConfigs from a CCE cluster
2. Finds Event->LTS LogConfig with events enabled
3. Queries LTS for K8s events in the specified time range
4. Parses and returns structured event data
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional, List

try:
    from . import lts as lts_mod
    from . import cce_app_logs
    from .common import get_credentials
    _lts_available = True
except ImportError:
    _lts_available = False
    lts_mod = None
    cce_app_logs = None


def _convert_timestamp_to_ms(time_str: str) -> int:
    """Convert 'YYYY-MM-DD HH:MM:SS' to milliseconds timestamp."""
    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp() * 1000)


def _parse_event_content(log_content: str) -> Optional[Dict[str, Any]]:
    """
    Parse K8s event from LTS log content.

    Supports two formats:
    - Format A: lowercase keys (standard K8s event format)
    - Format B: uppercase keys (Huawei CCE event format)

    Returns normalized dict with lowercase keys, or None if parsing fails.
    """
    try:
        data = json.loads(log_content)
    except (json.JSONDecodeError, TypeError):
        return None

    if not isinstance(data, dict):
        return None

    normalized = {}

    # Handle both lowercase and uppercase key formats
    key_mapping = {
        'reason': 'reason',
        'message': 'message',
        'type': 'type',
        'count': 'count',
        'firsttimestamp': 'first_timestamp',
        'lasttimestamp': 'last_timestamp',
        'involvedobject': 'involved_object',
    }

    # Uppercase format mapping
    uppercase_mapping = {
        'Reason': 'reason',
        'Message': 'message',
        'Type': 'type',
        'Count': 'count',
        'FirstTimestamp': 'first_timestamp',
        'LastTimestamp': 'last_timestamp',
        'InvolvedObject': 'involved_object',
    }

    # Determine which format we're dealing with
    if 'reason' in data:
        # Format A (lowercase)
        for k, v in data.items():
            if k in key_mapping:
                normalized[key_mapping[k]] = v
            else:
                normalized[k] = v
    elif 'Reason' in data:
        # Format B (uppercase) - convert to lowercase
        for k, v in data.items():
            mapped_key = uppercase_mapping.get(k, k.lower())
            normalized[mapped_key] = v
    else:
        # Unknown format, just lowercase everything
        for k, v in data.items():
            normalized[k.lower()] = v

    return normalized


def _normalize_involved_object(obj: Any) -> Optional[Dict[str, Any]]:
    """Normalize involvedObject field to consistent format."""
    if not obj:
        return None

    if isinstance(obj, dict):
        result = {}
        # Handle both formats
        for k, v in obj.items():
            key_lower = k.lower()
            if key_lower in ('kind', 'name', 'namespace'):
                result[key_lower] = v
        return result if result else None

    return None


def _get_cce_logconfigs(region, cluster_id, ak=None, sk=None, project_id=None):
    """Wrapper to get CCE logconfigs via cce_app_logs module."""
    if not _lts_available or cce_app_logs is None:
        return {"success": False, "error": "cce_app_logs module not available"}
    
    params = {
        "region": region,
        "cluster_id": cluster_id,
    }
    if ak:
        params["ak"] = ak
    if sk:
        params["sk"] = sk
    if project_id:
        params["project_id"] = project_id
    
    return cce_app_logs.get_cce_logconfigs_action(params)


def _query_k8s_events_from_lts(
    region: str,
    cluster_id: str,
    start_time: str,
    end_time: str,
    keywords: Optional[str] = None,
    limit: int = 500,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Query K8s events from LTS based on LogConfig settings.

    Args:
        region: Huawei Cloud region
        cluster_id: CCE cluster ID
        start_time: Start time 'YYYY-MM-DD HH:MM:SS'
        end_time: End time 'YYYY-MM-DD HH:MM:SS'
        keywords: Optional keywords to filter events
        limit: Maximum number of events to return (default 500)
        ak: Access key (optional, uses env if not provided)
        sk: Secret key (optional, uses env if not provided)
        project_id: Project ID (optional)

    Returns:
        Dict with success status, events, and metadata
    """
    if not _lts_available:
        return {
            "success": False,
            "error": "LTS module not available. Install huaweicloudsdklts."
        }

    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)

    if not access_key or not secret_key:
        return {
            "success": False,
            "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."
        }

    # Step 1: Get LogConfigs using cce_app_logs module (which has correct CRD discovery)
    logconfigs_result = _get_cce_logconfigs(region, cluster_id, access_key, secret_key, proj_id)

    if not logconfigs_result.get("success"):
        return {
            "success": False,
            "error": f"Failed to get LogConfigs: {logconfigs_result.get('error', 'Unknown error')}"
        }

    logconfigs = logconfigs_result.get("logconfigs", [])

    # Step 2: Find Event->LTS LogConfig with events enabled
    event_config = None
    for config in logconfigs:
        spec = config.get("spec", {})
        input_detail = spec.get("inputDetail", {})
        output_detail = spec.get("outputDetail", {})

        # Check if it's event type and LTS output
        if input_detail.get("type") != "event":
            continue
        if output_detail.get("type") != "LTS":
            continue

        # Check if events are enabled
        event_cfg = input_detail.get("event", {})
        normal_enabled = event_cfg.get("normalEvents", {}).get("enable", False)
        warning_enabled = event_cfg.get("warningEvents", {}).get("enable", False)

        if normal_enabled or warning_enabled:
            event_config = config
            break

    if not event_config:
        return {
            "success": False,
            "error": "未在集群中找到开启K8s事件LTS采集的LogConfig。请检查default-event配置或确认事件采集已开启。",
            "cluster_id": cluster_id,
            "region": region,
            "checked_logconfigs": len(logconfigs),
            "available_configs": [{"name": lc.get("name"), "input_type": lc.get("input_type"), "output_type": lc.get("output_type")} for lc in logconfigs]
        }

    # Step 3: Extract LTS config
    lts_config = event_config.get("spec", {}).get("outputDetail", {}).get("LTS", {})
    log_group_id = lts_config.get("ltsGroupID")
    log_stream_id = lts_config.get("ltsStreamID")

    if not log_group_id or not log_stream_id:
        return {
            "success": False,
            "error": "LogConfig中未找到LTS Group/Stream ID配置",
            "config_name": event_config.get("name", "unknown")
        }

    # Step 4: Convert time to milliseconds
    try:
        start_ms = _convert_timestamp_to_ms(start_time)
        end_ms = _convert_timestamp_to_ms(end_time)
    except ValueError as e:
        return {
            "success": False,
            "error": f"时间格式错误，应为 'YYYY-MM-DD HH:MM:SS': {str(e)}"
        }

    # Step 5: Query LTS with pagination
    all_events = []
    scroll_id = None
    total_fetched = 0
    page_count = 0
    page_limit = 1000  # LTS API page size

    while total_fetched < limit:
        page_count += 1
        page_remaining = limit - total_fetched
        current_page_limit = min(page_limit, page_remaining)

        lts_result = lts_mod.query_logs(
            region=region,
            log_group_id=log_group_id,
            log_stream_id=log_stream_id,
            start_time=str(start_ms),
            end_time=str(end_ms),
            keywords=keywords,
            limit=current_page_limit,
            scroll_id=scroll_id,
            ak=access_key,
            sk=secret_key,
            project_id=proj_id
        )

        if not lts_result.get("success"):
            return {
                "success": False,
                "error": f"LTS查询失败: {lts_result.get('error', 'Unknown error')}",
                "log_group_id": log_group_id,
                "log_stream_id": log_stream_id,
                "events_fetched": total_fetched,
                "pages_fetched": page_count - 1
            }

        # Step 6: Parse events from logs
        raw_logs = lts_result.get("logs", [])
        for log in raw_logs:
            content = log.get("content", "")
            if not content:
                continue

            parsed = _parse_event_content(content)
            if not parsed:
                continue

            # Normalize involved object
            involved_obj = parsed.get("involved_object")
            if involved_obj:
                parsed["involved_object"] = _normalize_involved_object(involved_obj)

            all_events.append(parsed)
            total_fetched += 1

            if total_fetched >= limit:
                break

        # Check for next page
        scroll_id = lts_result.get("scroll_id")
        if not scroll_id:
            break

    # Step 7: Build response
    return {
        "success": True,
        "region": region,
        "cluster_id": cluster_id,
        "log_group_id": log_group_id,
        "log_stream_id": log_stream_id,
        "keywords": keywords,
        "event_count": len(all_events),
        "events": all_events,
        "time_range": {
            "start": start_time,
            "end": end_time
        },
        "log_config": {
            "name": event_config.get("name", "unknown"),
            "namespace": event_config.get("namespace", "unknown"),
            "input_type": "event",
            "warning_events_enabled": event_config.get("spec", {}).get("inputDetail", {}).get("event", {}).get("warningEvents", {}).get("enable", False),
            "normal_events_enabled": event_config.get("spec", {}).get("inputDetail", {}).get("event", {}).get("normalEvents", {}).get("enable", False)
        },
        "pagination": {
            "pages_fetched": page_count,
            "limit": limit,
            "has_more": scroll_id is not None and total_fetched >= limit
        }
    }


def query_k8s_events_from_lts_action(params: Dict[str, str]) -> Dict[str, Any]:
    """
    Action handler for huawei_query_k8s_events_from_lts tool.

    Expected parameters:
    - region: Huawei Cloud region (required)
    - cluster_id: CCE cluster ID (required)
    - start_time: Start time 'YYYY-MM-DD HH:MM:SS' (required)
    - end_time: End time 'YYYY-MM-DD HH:MM:SS' (required)
    - keywords: Optional keywords to filter events
    - limit: Maximum number of events to return (default 500)
    """
    region = params.get("region")
    cluster_id = params.get("cluster_id")
    start_time = params.get("start_time")
    end_time = params.get("end_time")
    keywords = params.get("keywords")

    # Validate required parameters
    if not region:
        return {"success": False, "error": "region is required"}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}
    if not start_time:
        return {"success": False, "error": "start_time is required"}
    if not end_time:
        return {"success": False, "error": "end_time is required"}

    # Parse limit parameter
    try:
        limit = int(params.get("limit", 500))
    except (ValueError, TypeError):
        limit = 500

    return _query_k8s_events_from_lts(
        region=region,
        cluster_id=cluster_id,
        start_time=start_time,
        end_time=end_time,
        keywords=keywords,
        limit=limit,
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id")
    )