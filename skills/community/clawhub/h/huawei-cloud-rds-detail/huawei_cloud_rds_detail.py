#!/usr/bin/env python3
"""
huawei-cloud-rds-detail: 查询华为云 RDS 实例列表、详情和监控指标。

Usage:
    python3 scripts/huawei_cloud_rds_detail.py list [--region REGION] [--timeout SECONDS]
    python3 scripts/huawei_cloud_rds_detail.py show <instance-id> [--region REGION] [--timeout SECONDS]
    python3 scripts/huawei_cloud_rds_detail.py metrics <instance-id> [--region REGION] [--timeout SECONDS]
    python3 scripts/huawei_cloud_rds_detail.py capability-list
    python3 scripts/huawei_cloud_rds_detail.py --help
"""

import os
import sys
import json
import argparse
from typing import Optional, Dict, Any, List, Tuple


def _load_credentials() -> Tuple[str, str]:
    """动态扫描环境变量获取 AK/SK，不依赖固定变量名。"""
    ak, sk = '', ''
    for k, v in os.environ.items():
        u = k.upper()
        if not (u.startswith('HUAWEI') or u.startswith('HW') or u.startswith('HWC')):
            continue
        if 'ACCESS_KEY' in u or u.endswith('_AK') or u == 'AK':
            ak = v or ak
        if 'SECRET_KEY' in u or u.endswith('_SK') or u == 'SK':
            sk = v or sk
    return ak, sk


def _get_base_url() -> str:
    """获取系统基础 URL（预留项目知识扫描）。"""
    return ''


class RdsQuery:
    """华为云 RDS 详情查询客户端。"""

    def __init__(self, region: str = 'cn-north-4', timeout: int = 30):
        self.region = region
        self.timeout = timeout
        self._project_id = None

        ak, sk = _load_credentials()
        if not ak or not sk:
            print(json.dumps({
                'error': '凭据缺失',
                'message': '未找到 HUAWEI_AK/HUAWEI_SK 或 HUAWEICLOUD_SDK_AK/HUAWEICLOUD_SDK_SK 环境变量。'
            }, ensure_ascii=False))
            sys.exit(3)

        self.ak = ak
        self.sk = sk

    def _get_project_id(self) -> str:
        """获取项目 ID（首次调用后缓存）。"""
        if self._project_id:
            return self._project_id
        try:
            from huaweicloudsdkcore.auth.credentials import BasicCredentials
            from huaweicloudsdkiam.v3 import IamClient, KeystoneListProjectsRequest
            from huaweicloudsdkcore.http.http_config import HttpConfig

            credentials = BasicCredentials(ak=self.ak, sk=self.sk)
            config = HttpConfig.get_default_config()
            config.timeout = self.timeout
            config.ignore_ssl_verification = True

            client = IamClient.new_builder() \
                .with_http_config(config) \
                .with_credentials(credentials) \
                .with_endpoint(f'https://iam.{self.region}.myhuaweicloud.com') \
                .build()

            request = KeystoneListProjectsRequest(name=self.region)
            response = client.keystone_list_projects(request)
            if hasattr(response, 'projects') and response.projects:
                self._project_id = response.projects[0].id
                return self._project_id
            else:
                print(json.dumps({
                    'error': '获取项目ID失败',
                    'message': f'无法获取区域 {self.region} 的项目 ID'
                }, ensure_ascii=False))
                sys.exit(1)
        except Exception as e:
            print(json.dumps({
                'error': '获取项目ID失败',
                'message': str(e)
            }, ensure_ascii=False))
            sys.exit(1)

    def _get_rds_client(self):
        """创建 RDS 客户端。"""
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkrds.v3 import RdsClient
        from huaweicloudsdkcore.http.http_config import HttpConfig

        project_id = self._get_project_id()
        credentials = BasicCredentials(ak=self.ak, sk=self.sk, project_id=project_id)
        config = HttpConfig.get_default_config()
        config.timeout = self.timeout
        config.ignore_ssl_verification = True

        return RdsClient.new_builder() \
            .with_http_config(config) \
            .with_credentials(credentials) \
            .with_endpoint(f'https://rds.{self.region}.myhuaweicloud.com') \
            .build()

    def _get_ces_client(self):
        """创建 CES 客户端。"""
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkces.v1 import CesClient
        from huaweicloudsdkcore.http.http_config import HttpConfig

        project_id = self._get_project_id()
        credentials = BasicCredentials(ak=self.ak, sk=self.sk, project_id=project_id)
        config = HttpConfig.get_default_config()
        config.timeout = self.timeout
        config.ignore_ssl_verification = True

        return CesClient.new_builder() \
            .with_http_config(config) \
            .with_credentials(credentials) \
            .with_endpoint(f'https://ces.{self.region}.myhuaweicloud.com') \
            .build()

    def list_instances(self, limit: int = 100) -> Dict[str, Any]:
        """列出所有 RDS 实例。"""
        from huaweicloudsdkrds.v3 import ListInstancesRequest
        client = self._get_rds_client()
        request = ListInstancesRequest(limit=limit)
        response = client.list_instances(request)
        return self._format_list_response(response)

    def _format_list_response(self, response) -> Dict[str, Any]:
        """格式化列表响应。"""
        instances = []
        if hasattr(response, 'instances') and response.instances:
            for inst in response.instances:
                item = {
                    'id': inst.id,
                    'name': inst.name,
                    'status': inst.status,
                    'type': inst.type,
                    'engine': f"{inst.datastore.type} {inst.datastore.version}" if hasattr(inst, 'datastore') and inst.datastore else '',
                    'flavor': inst.flavor_ref,
                    'volume_type': inst.volume.type if hasattr(inst, 'volume') and inst.volume else '',
                    'volume_size': inst.volume.size if hasattr(inst, 'volume') and inst.volume else '',
                    'region': inst.region if hasattr(inst, 'region') else '',
                    'created': inst.created,
                    'private_ips': inst.private_ips if hasattr(inst, 'private_ips') else [],
                    'public_ips': inst.public_ips if hasattr(inst, 'public_ips') else [],
                    'vpc_id': inst.vpc_id if hasattr(inst, 'vpc_id') else '',
                    'subnet_id': inst.subnet_id if hasattr(inst, 'subnet_id') else '',
                    'security_group_id': inst.security_group_id if hasattr(inst, 'security_group_id') else '',
                }
                instances.append(item)
        return {
            'total_count': getattr(response, 'total_count', len(instances)),
            'instances': instances
        }

    def show_instance(self, instance_id: str) -> Dict[str, Any]:
        """按实例 ID 查询单实例详情。"""
        from huaweicloudsdkrds.v3 import ListInstancesRequest
        client = self._get_rds_client()
        request = ListInstancesRequest(id=instance_id, limit=1)
        response = client.list_instances(request)
        return self._format_detail_response(response)

    def _format_detail_response(self, response) -> Dict[str, Any]:
        """格式化实例详情响应。"""
        if not hasattr(response, 'instances') or not response.instances:
            return {'error': '实例未找到', 'instances': []}
        inst = response.instances[0]
        detail = {
            'id': inst.id,
            'name': inst.name,
            'status': inst.status,
            'type': inst.type,
            'region': inst.region if hasattr(inst, 'region') else '',
            'engine': {
                'type': inst.datastore.type if hasattr(inst, 'datastore') and inst.datastore else '',
                'version': inst.datastore.version if hasattr(inst, 'datastore') and inst.datastore else '',
            },
            'flavor_ref': inst.flavor_ref,
            'volume': {
                'type': inst.volume.type if hasattr(inst, 'volume') and inst.volume else '',
                'size': inst.volume.size if hasattr(inst, 'volume') and inst.volume else '',
            } if hasattr(inst, 'volume') else {},
            'created': inst.created,
            'updated': inst.updated if hasattr(inst, 'updated') else '',
            'private_ips': inst.private_ips if hasattr(inst, 'private_ips') else [],
            'public_ips': inst.public_ips if hasattr(inst, 'public_ips') else [],
            'vpc_id': inst.vpc_id if hasattr(inst, 'vpc_id') else '',
            'subnet_id': inst.subnet_id if hasattr(inst, 'subnet_id') else '',
            'security_group_id': inst.security_group_id if hasattr(inst, 'security_group_id') else '',
            'time_zone': inst.time_zone if hasattr(inst, 'time_zone') else '',
            'maintenance_window': inst.maintenance_window if hasattr(inst, 'maintenance_window') else '',
            'switch_strategy': inst.switch_strategy if hasattr(inst, 'switch_strategy') else '',
            'ha': {
                'mode': inst.ha.mode if hasattr(inst, 'ha') and inst.ha else '',
                'replication_mode': inst.ha.replication_mode if hasattr(inst, 'ha') and inst.ha else '',
            } if hasattr(inst, 'ha') else {},
            'nodes': [{
                'id': n.id,
                'name': n.name,
                'role': n.role,
                'status': n.status,
            } for n in (inst.nodes or [])] if hasattr(inst, 'nodes') else [],
            'related_graph': inst.related_graph if hasattr(inst, 'related_graph') else '',
            'backup_strategy': {
                'keep_days': inst.backup_strategy.keep_days if hasattr(inst, 'backup_strategy') and inst.backup_strategy else '',
                'start_time': inst.backup_strategy.start_time if hasattr(inst, 'backup_strategy') and inst.backup_strategy else '',
                'period': inst.backup_strategy.period if hasattr(inst, 'backup_strategy') and inst.backup_strategy else '',
            } if hasattr(inst, 'backup_strategy') else {},
        }
        return {'instance': detail}

    def get_metrics(self, instance_id: str) -> Dict[str, Any]:
        """查询实例的 CPU/内存/磁盘监控指标。"""
        from huaweicloudsdkces.v1 import CesClient, BatchListMetricDataRequest
        from huaweicloudsdkces.v1.model import BatchListMetricDataRequestBody, MetricInfo, MetricsDimension

        # RDS 监控指标命名空间和维度
        namespace = 'SYS.RDS'
        dimensions = [MetricsDimension(name='rds_cluster_id', value=instance_id)]

        # 需要查询的三个指标
        metric_names = [
            'rds001_cpu_util',      # CPU 使用率
            'rds002_mem_util',      # 内存使用率
            'rds003_disk_util',     # 磁盘使用率
        ]

        metrics = [
            MetricInfo(namespace=namespace, metric_name=name, dimensions=dimensions)
            for name in metric_names
        ]

        client = self._get_ces_client()
        body = BatchListMetricDataRequestBody(metrics=metrics)

        # 构建请求
        request = BatchListMetricDataRequest(body=body)
        response = client.batch_list_metric_data(request)

        return self._format_metrics_response(response)

    def _format_metrics_response(self, response) -> Dict[str, Any]:
        """格式化监控指标响应。"""
        result = {}
        if hasattr(response, 'metrics') and response.metrics:
            for metric in response.metrics:
                metric_name = metric.metric_name if hasattr(metric, 'metric_name') else 'unknown'
                data_points = []
                if hasattr(metric, 'data_points') and metric.data_points:
                    for dp in metric.data_points:
                        data_points.append({
                            'timestamp': dp.timestamp if hasattr(dp, 'timestamp') else '',
                            'average': dp.average if hasattr(dp, 'average') else '',
                            'unit': dp.unit if hasattr(dp, 'unit') else '',
                        })
                result[metric_name] = {
                    'unit': metric.unit if hasattr(metric, 'unit') else '',
                    'data_points': data_points,
                }
        return {'metrics': result} if result else {'metrics': {}, 'message': '未查询到监控数据'}

    def capability_list(self) -> Dict[str, Any]:
        """返回能力列表。"""
        return {
            'skill': 'huawei-cloud-rds-detail',
            'version': '1.0.0',
            'description': '查询华为云 RDS 实例列表、详情和监控指标',
            'region': self.region,
            'capabilities': [
                {
                    'name': 'list',
                    'description': '列出当前账号下所有 RDS 实例',
                    'usage': 'python3 scripts/huawei_cloud_rds_detail.py list'
                },
                {
                    'name': 'show',
                    'description': '按实例 ID 查询单实例详情',
                    'usage': 'python3 scripts/huawei_cloud_rds_detail.py show <instance-id>',
                    'args': [{'name': 'instance-id', 'description': 'RDS 实例 ID'}]
                },
                {
                    'name': 'metrics',
                    'description': '查询实例的 CPU/内存/磁盘监控指标',
                    'usage': 'python3 scripts/huawei_cloud_rds_detail.py metrics <instance-id>',
                    'args': [{'name': 'instance-id', 'description': 'RDS 实例 ID'}]
                }
            ]
        }


def main():
    parser = argparse.ArgumentParser(
        description='华为云 RDS 详情查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--region', default='cn-north-4', help='华为云区域（默认: cn-north-4）')
    parser.add_argument('--timeout', type=int, default=30, help='API 超时秒数（默认: 30）')

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # list 子命令
    subparsers.add_parser('list', help='列出所有 RDS 实例')

    # show 子命令
    show_parser = subparsers.add_parser('show', help='查询单实例详情')
    show_parser.add_argument('instance_id', help='RDS 实例 ID')

    # metrics 子命令
    metrics_parser = subparsers.add_parser('metrics', help='查询监控指标')
    metrics_parser.add_argument('instance_id', help='RDS 实例 ID')

    # capability-list 子命令
    subparsers.add_parser('capability-list', help='列出能力列表')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    query = RdsQuery(region=args.region, timeout=args.timeout)

    try:
        if args.command == 'list':
            result = query.list_instances()
        elif args.command == 'show':
            result = query.show_instance(args.instance_id)
        elif args.command == 'metrics':
            result = query.get_metrics(args.instance_id)
        elif args.command == 'capability-list':
            result = query.capability_list()
        else:
            parser.print_help()
            sys.exit(1)

        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        error_info = {
            'error': '操作失败',
            'message': str(e),
        }
        print(json.dumps(error_info, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()