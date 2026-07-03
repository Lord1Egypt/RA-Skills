#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为云 LTS (Log Tank Service) 日志服务工具

使用华为云官方SDK查询LTS日志服务。

功能:
1. 查询日志组列表
2. 查询日志流列表
3. 查询日志内容 (支持时间范围)
4. 查询CCE集群日志
"""

from __future__ import annotations

import os
import sys
import json
import base64
import tempfile
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.region.region import Region
from huaweicloudsdkcore.exceptions.exceptions import ClientRequestException
from huaweicloudsdklts.v2 import LtsClient, ListLogGroupsRequest, ListLogStreamsRequest

from .common import get_credentials, get_project_id_for_region


# LTS 服务端点 (按区域)
LTS_ENDPOINTS = {
    "cn-north-4": "lts.cn-north-4.myhuaweicloud.com",
    "cn-north-1": "lts.cn-north-1.myhuaweicloud.com",
    "cn-north-9": "lts.cn-north-9.myhuaweicloud.com",
    "cn-east-3": "lts.cn-east-3.myhuaweicloud.com",
    "cn-east-2": "lts.cn-east-2.myhuaweicloud.com",
    "cn-south-1": "lts.cn-south-1.myhuaweicloud.com",
    "cn-south-2": "lts.cn-south-2.myhuaweicloud.com",
    "cn-south-4": "lts.cn-south-4.myhuaweicloud.com",
    "cn-west-3": "lts.cn-west-3.myhuaweicloud.com",
    "cn-southwest-2": "lts.cn-southwest-2.myhuaweicloud.com",
    "ap-southeast-1": "lts.ap-southeast-1.myhuaweicloud.com",
    "ap-southeast-2": "lts.ap-southeast-2.myhuaweicloud.com",
    "ap-southeast-3": "lts.ap-southeast-3.myhuaweicloud.com",
    "eu-west-0": "lts.eu-west-0.myhuaweicloud.com",
}


def get_lts_client(region: str, ak: str, sk: str, project_id: str = None) -> LtsClient:
    """创建LTS客户端"""
    if not project_id:
        project_id = get_project_id_for_region(region, ak, sk)
    credentials = BasicCredentials(ak, sk, project_id)
    endpoint = LTS_ENDPOINTS.get(region, f"lts.{region}.myhuaweicloud.com")
    client = LtsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(Region(id=region, endpoint=endpoint)) \
        .build()
    return client


def list_log_groups(region: str, ak: str = None, sk: str = None,
                   project_id: str = None) -> Dict[str, Any]:
    """查询日志组列表"""
    try:
        ak, sk, project_id = get_credentials(ak, sk, project_id)
        if not ak or not sk:
            return {"success": False, "error": "Credentials not provided"}

        client = get_lts_client(region, ak, sk, project_id)
        request = ListLogGroupsRequest()
        response = client.list_log_groups(request)

        log_groups = []
        if response.log_groups:
            for group in response.log_groups:
                log_groups.append({
                    "log_group_id": group.log_group_id,
                    "log_group_name": group.log_group_name,
                    "creation_time": group.creation_time,
                    "ttl_in_days": group.ttl_in_days if hasattr(group, 'ttl_in_days') else 7,
                    "tags": group.tags if hasattr(group, 'tags') else []
                })

        return {"success": True, "total": len(log_groups), "log_groups": log_groups}

    except ClientRequestException as e:
        return {"success": False, "error": e.error_msg, "error_code": e.error_code, "status_code": e.status_code}
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_log_streams(region: str, log_group_id: str = None, ak: str = None,
                    sk: str = None, project_id: str = None) -> Dict[str, Any]:
    """查询日志流列表"""
    try:
        ak, sk, project_id = get_credentials(ak, sk, project_id)
        if not ak or not sk:
            return {"success": False, "error": "Credentials not provided"}

        client = get_lts_client(region, ak, sk, project_id)
        request = ListLogStreamsRequest()
        if log_group_id:
            request.log_group_id = log_group_id

        response = client.list_log_streams(request)

        log_streams = []
        if response.log_streams:
            for stream in response.log_streams:
                log_streams.append({
                    "log_stream_id": stream.log_stream_id,
                    "log_stream_name": stream.log_stream_name,
                    "log_group_id": stream.log_group_id if hasattr(stream, 'log_group_id') else log_group_id,
                    "creation_time": stream.creation_time if hasattr(stream, 'creation_time') else None,
                    "filter_count": stream.filter_count if hasattr(stream, 'filter_count') else 0
                })

        return {"success": True, "total": len(log_streams), "log_streams": log_streams}

    except ClientRequestException as e:
        return {"success": False, "error": e.error_msg, "error_code": e.error_code, "status_code": e.status_code}
    except Exception as e:
        return {"success": False, "error": str(e)}


def query_logs(region: str, log_group_id: str, log_stream_id: str,
              start_time: str = None, end_time: str = None,
              keywords: str = None, limit: int = 1000,
              scroll_id: str = None, is_desc: bool = True,
              is_iterative: bool = False,
              labels: Optional[Dict[str, str]] = None,
              ak: str = None, sk: str = None,
              project_id: str = None) -> Dict[str, Any]:
    """查询日志内容"""
    try:
        ak, sk, project_id = get_credentials(ak, sk, project_id)
        if not ak or not sk:
            return {"success": False, "error": "Credentials not provided"}

        client = get_lts_client(region, ak, sk, project_id)

        if start_time:
            if isinstance(start_time, str) and '-' in start_time:
                start_ts = int(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
            else:
                start_ts = int(start_time)
        else:
            start_ts = int((datetime.now() - timedelta(hours=1)).timestamp() * 1000)

        if end_time:
            if isinstance(end_time, str) and '-' in end_time:
                end_ts = int(datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S').timestamp() * 1000)
            else:
                end_ts = int(end_time)
        else:
            end_ts = int(datetime.now().timestamp() * 1000)

        from huaweicloudsdklts.v2 import ListLogsRequest, QueryLtsLogParams

        query_params = QueryLtsLogParams(
            start_time=start_ts,
            end_time=end_ts,
            limit=limit,
            is_desc=is_desc
        )

        if keywords:
            query_params.keywords = keywords
        if labels:
            query_params.labels = labels
        if scroll_id:
            query_params.scroll_id = scroll_id
        if is_iterative:
            query_params.is_iterative = is_iterative

        request = ListLogsRequest(
            log_group_id=log_group_id,
            log_stream_id=log_stream_id,
            body=query_params
        )

        response = client.list_logs(request)

        logs = []
        if response.logs:
            for log in response.logs:
                logs.append({
                    "content": log.content if hasattr(log, 'content') else str(log),
                    "timestamp": log.timestamp if hasattr(log, 'timestamp') else None,
                    "log_group_id": log_group_id,
                    "log_stream_id": log_stream_id
                })

        next_scroll_id = None
        if hasattr(response, 'scroll_id') and response.scroll_id:
            next_scroll_id = response.scroll_id

        return {
            "success": True,
            "log_group_id": log_group_id,
            "log_stream_id": log_stream_id,
            "start_time": start_ts,
            "end_time": end_ts,
            "total": len(logs),
            "scroll_id": next_scroll_id,
            "has_more": next_scroll_id is not None,
            "logs": logs
        }

    except ClientRequestException as e:
        return {"success": False, "error": e.error_msg, "error_code": e.error_code, "status_code": e.status_code}
    except Exception as e:
        return {"success": False, "error": str(e)}


def query_logs_by_keywords(region: str, log_group_id: str, log_stream_id: str,
                          keywords: str = None, start_time: str = None,
                          end_time: str = None, limit: int = 100,
                          ak: str = None, sk: str = None,
                          project_id: str = None) -> Dict[str, Any]:
    """通过关键词查询日志"""
    return query_logs(region, log_group_id, log_stream_id, start_time, end_time, keywords, limit,
                     ak=ak, sk=sk, project_id=project_id)


def get_cce_logconfigs(region: str, cluster_id: str, ak: str = None,
                       sk: str = None, project_id: str = None,
                       namespace: str = None) -> Dict[str, Any]:
    """从CCE集群获取 LogConfig 自定义资源（CR）"""
    try:
        from huaweicloudsdkcce.v3 import CceClient
        from huaweicloudsdkcce.v3.region.cce_region import CceRegion
        from huaweicloudsdkcce.v3.model.create_kubernetes_cluster_cert_request import CreateKubernetesClusterCertRequest
        from huaweicloudsdkcce.v3.model.cluster_cert_duration import ClusterCertDuration
    except ImportError as e:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {e}"}

    try:
        import kubernetes
        from kubernetes import client
    except ImportError as e:
        return {"success": False, "error": f"Kubernetes SDK not installed: {e}"}

    ak, sk, project_id = get_credentials(ak, sk, project_id)
    if not ak or not sk:
        return {"success": False, "error": "Credentials not provided"}

    def _create_cce_client(region_name, access_key, secret_key, proj_id):
        credentials = BasicCredentials(access_key, secret_key)
        return CceClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(getattr(CceRegion, region_name.upper().replace("-", "_"))) \
            .build()

    temp_files = []

    try:
        cce_client = _create_cce_client(region, ak, sk, project_id)
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
            return {"success": False, "error": "Could not find cluster endpoint"}

        configuration = kubernetes.client.Configuration()
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
            cert_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.crt', delete=False)
            cert_file.write(base64.b64decode(user_data['client_certificate_data']))
            cert_file.close()
            configuration.cert_file = cert_file.name
            temp_files.append(cert_file.name)

        if user_data and user_data.get('client_key_data'):
            key_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.key', delete=False)
            key_file.write(base64.b64decode(user_data['client_key_data']))
            key_file.close()
            configuration.key_file = key_file.name
            temp_files.append(key_file.name)

        kubernetes.client.Configuration.set_default(configuration)
        custom_api = kubernetes.client.CustomObjectsApi()

        logconfig_list = []
        tried_combinations = []
        cr_combinations = [
            ("lts.opentelekomcloud.com", "v1", "logconfigs"),
            ("lts.huaweicloud.com", "v1", "logconfigs"),
            ("lts.io", "v1", "logconfigs"),
            ("logging.huaweicloud.com", "v1", "logconfigs"),
            ("lts.opentelekomcloud.com", "v1alpha1", "logconfigs"),
            ("lts.opentelekomcloud.com", "v1beta1", "logconfigs"),
        ]

        for group, version, plural in cr_combinations:
            tried_combinations.append(f"{group}/{version}/{plural}")
            try:
                if namespace:
                    result = custom_api.list_namespaced_custom_object(group, version, namespace, plural)
                else:
                    result = custom_api.list_cluster_custom_object(group, version, plural)

                if result and 'items' in result:
                    for item in result['items']:
                        logconfig_list.append({
                            "name": item.get('metadata', {}).get('name'),
                            "namespace": item.get('metadata', {}).get('namespace'),
                            "creation_time": str(item.get('metadata', {}).get('creationTimestamp')),
                            "spec": item.get('spec', {}),
                            "status": item.get('status', {}),
                            "api_version": f"{group}/{version}"
                        })
                    if logconfig_list:
                        break
            except Exception:
                continue

        for f in temp_files:
            try:
                os.unlink(f)
            except Exception:
                pass

        return {
            "success": True,
            "cluster_id": cluster_id,
            "namespace": namespace or "all",
            "count": len(logconfig_list),
            "tried_api_combinations": tried_combinations,
            "logconfigs": logconfig_list,
            "note": "如果没有找到LogConfig，说明集群可能没有安装相关CRD"
        }

    except Exception as e:
        for f in temp_files:
            try:
                os.unlink(f)
            except Exception:
                pass
        return {"success": False, "error": str(e), "error_type": type(e).__name__}


def query_aom_logs(region: str, cluster_id: str, namespace: str = None,
                  pod_name: str = None, container_name: str = None,
                  start_time: str = None, end_time: str = None,
                  keywords: str = None, limit: int = 100,
                  ak: str = None, sk: str = None,
                  project_id: str = None) -> Dict[str, Any]:
    """查询AOM应用日志"""
    return {
        "success": True,
        "message": "AOM logs query - requires specific log group/stream IDs",
        "cluster_id": cluster_id,
        "namespace": namespace,
        "pod_name": pod_name,
        "note": "Use query_logs with specific log_group_id and log_stream_id"
    }


def get_recent_logs(region: str, log_group_id: str, log_stream_id: str,
                   hours: int = 1, limit: int = 1000,
                   keywords: str = None,
                   labels: Optional[Dict[str, str]] = None,
                   ak: str = None, sk: str = None,
                   project_id: str = None) -> Dict[str, Any]:
    """获取最近的日志"""
    ak, sk, project_id = get_credentials(ak, sk, project_id)
    if not ak or not sk:
        return {"success": False, "error": "Credentials not provided"}

    end_time_dt = datetime.now()
    start_time_dt = end_time_dt - timedelta(hours=hours)

    return query_logs(
        region, log_group_id, log_stream_id,
        start_time_dt.strftime('%Y-%m-%d %H:%M:%S'),
        end_time_dt.strftime('%Y-%m-%d %H:%M:%S'),
        keywords=keywords,
        limit=limit,
        scroll_id=None,
        is_desc=True,
        is_iterative=False,
        labels=labels,
        ak=ak, sk=sk, project_id=project_id
    )
