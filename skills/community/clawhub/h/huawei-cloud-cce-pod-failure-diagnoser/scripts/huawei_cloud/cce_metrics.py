from .common import *
from . import aom, cce

def get_cce_pod_metrics_topN(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None, label_selector: str = None, top_n: int = 10, hours: int = 1, cpu_query: str = None, memory_query: str = None, node_ip: Optional[str] = None) -> Dict[str, Any]:
    """获取 CCE 集群 Pod 监控数据

    自动获取 AOM 实例并执行 Pod CPU/内存监控查询，返回 Top N 数据。

    Args:
        region: 华为云区域 (如 cn-north-4)
        cluster_id: CCE 集群 ID
        ak: Access Key ID (可选)
        sk: Secret Access Key (可选)
        project_id: Project ID (可选)
        namespace: 命名空间过滤 (可选，默认所有命名空间)
        label_selector: Pod 标签选择器 (可选，格式: "app=nginx,version=v1")
        top_n: 返回 Top N 数据 (默认 10)
        hours: 查询时间范围（小时）(默认 1)
        cpu_query: 自定义 CPU PromQL (可选)
        memory_query: 自定义内存 PromQL (可选)
        node_ip: 节点 IP 过滤 (可选，只返回指定节点上的 Pod)

    Returns:
        Dict with success status and pod metrics data
    """
    # Explicitly assign to ensure node_ip is in scope
    node_ip = node_ip
    import time as time_module

    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}

    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    # ========== 1. 获取集群名称 ==========
    cluster_name = cluster_id
    try:
        clusters_result = cce.list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters_result.get("success"):
            for c in clusters_result.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass

    # ========== 2. 如果有 label_selector，先获取符合条件的 Pod 列表 ==========
    pod_filter_list = None  # 用于过滤的 Pod 名称列表
    matched_pods_info = []  # 匹配的 Pod 详细信息

    if label_selector:
        # 解析 label_selector (格式: "app=nginx,version=v1")
        label_filters = {}
        for part in label_selector.split(","):
            part = part.strip()
            if "=" in part:
                key, value = part.split("=", 1)
                label_filters[key.strip()] = value.strip()

        if label_filters:
            # 获取 Pod 列表
            pods_result = cce.get_kubernetes_pods(region, cluster_id, access_key, secret_key, proj_id, namespace)
            if pods_result.get("success"):
                matched_pods = []
                for pod in pods_result.get("pods", []):
                    pod_labels = pod.get("labels", {})
                    pod_name = pod.get("name", "")
                    pod_ns = pod.get("namespace", "")

                    # 检查是否匹配所有 label 条件
                    match = True
                    for key, value in label_filters.items():
                        if pod_labels.get(key) != value:
                            match = False
                            break

                    if match:
                        matched_pods.append(pod_name)
                        matched_pods_info.append({
                            "name": pod_name,
                            "namespace": pod_ns,
                            "labels": pod_labels,
                            "status": pod.get("status"),
                            "node": pod.get("node")
                        })

                if matched_pods:
                    pod_filter_list = matched_pods
                else:
                    # 没有匹配的 Pod，直接返回空结果
                    return {
                        "success": True,
                        "region": region,
                        "cluster_id": cluster_id,
                        "cluster_name": cluster_name,
                        "aom_instance_id": None,
                        "inspection_time": time_module.strftime('%Y-%m-%d %H:%M:%S', time_module.localtime()),
                        "query_params": {
                            "top_n": top_n,
                            "hours": hours,
                            "namespace": namespace,
                            "label_selector": label_selector
                        },
                        "label_filter": {
                            "selector": label_selector,
                            "parsed": label_filters,
                            "matched_count": 0,
                            "matched_pods": []
                        },
                        "promql": {"cpu": None, "memory": None},
                        "metrics": {
                            "cpu_top_n": [],
                            "memory_top_n": [],
                            "all_pods": []
                        },
                        "summary": {
                            "total_pods": 0,
                            "critical_cpu": 0,
                            "critical_memory": 0,
                            "warning_cpu": 0,
                            "warning_memory": 0
                        },
                        "message": f"没有找到匹配 label_selector '{label_selector}' 的 Pod"
                    }

    # ========== 3. 获取 AOM 实例 ==========
    from .cce_diagnosis import get_aom_instance
    aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
    if not aom_result.get("success"):
        return {
            "success": False,
            "error": aom_result.get("error", "未找到可用的 AOM 实例"),
            "error_type": aom_result.get("error_type"),
            "cluster_id": cluster_id,
            "cluster_name": cluster_name
        }
    aom_instance_id = aom_result.get("aom_instance_id")

    # ========== 4. 构建 PromQL 查询 ==========
    # 构建 Pod 过滤条件
    pod_filter_clause = ""
    if pod_filter_list:
        # 使用正则匹配多个 Pod 名称
        pod_regex = "|".join(pod_filter_list[:100])  # 限制最多 100 个 Pod
        pod_filter_clause = f',pod=~"{pod_regex}"'

    # 构建节点过滤条件
    node_filter_clause = ""
    if node_ip:
        node_filter_clause = f',node="{node_ip}"'

    # 默认 CPU 使用率 PromQL (相对 Limit %)
    if cpu_query is None:
        if namespace:
            cpu_query = f'topk({top_n}, sum by (pod, namespace) (rate(container_cpu_usage_seconds_total{{image!="",namespace="{namespace}"{pod_filter_clause}{node_filter_clause}}}[5m])) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{{resource="cpu",namespace="{namespace}"{pod_filter_clause}{node_filter_clause}}}) * 100)'
        else:
            cpu_query = f'topk({top_n}, sum by (pod, namespace) (rate(container_cpu_usage_seconds_total{{image!=""{pod_filter_clause}{node_filter_clause}}}[5m])) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{{resource="cpu"{pod_filter_clause}{node_filter_clause}}}) * 100)'

    # 默认内存使用率 PromQL (相对 Limit %)
    if memory_query is None:
        if namespace:
            memory_query = f'topk({top_n}, sum by (pod, namespace) (container_memory_working_set_bytes{{image!="",namespace="{namespace}"{pod_filter_clause}{node_filter_clause}}}) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{{resource="memory",namespace="{namespace}"{pod_filter_clause}{node_filter_clause}}}) * 100)'
        else:
            memory_query = f'topk({top_n}, sum by (pod, namespace) (container_memory_working_set_bytes{{image!=""{pod_filter_clause}{node_filter_clause}}}) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{{resource="memory"{pod_filter_clause}{node_filter_clause}}}) * 100)'

    # ========== 5. 执行查询 ==========
    cpu_result = aom.get_aom_prom_metrics_http(region, aom_instance_id, cpu_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
    memory_result = aom.get_aom_prom_metrics_http(region, aom_instance_id, memory_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)

    # ========== 6. 解析结果 ==========
    cpu_metrics = []
    if cpu_result.get("success") and cpu_result.get("result", {}).get("data", {}).get("result"):
        for item in cpu_result["result"]["data"]["result"]:
            metric = item.get("metric", {})
            values = item.get("values", [])
            if values:
                try:
                    latest_value = float(values[-1][1])
                    cpu_metrics.append({
                        "pod": metric.get("pod", "unknown"),
                        "namespace": metric.get("namespace", "unknown"),
                        "cpu_usage_percent": round(latest_value, 2),
                        "status": "critical" if latest_value > 80 else "warning" if latest_value > 50 else "normal",
                        "time_series": values  # 保存完整的时序数据
                    })
                except (ValueError, IndexError):
                    pass

    memory_metrics = []
    if memory_result.get("success") and memory_result.get("result", {}).get("data", {}).get("result"):
        for item in memory_result["result"]["data"]["result"]:
            metric = item.get("metric", {})
            values = item.get("values", [])
            if values:
                try:
                    latest_value = float(values[-1][1])
                    memory_metrics.append({
                        "pod": metric.get("pod", "unknown"),
                        "namespace": metric.get("namespace", "unknown"),
                        "memory_usage_percent": round(latest_value, 2),
                        "status": "critical" if latest_value > 80 else "warning" if latest_value > 50 else "normal",
                        "time_series": values  # 保存完整的时序数据
                    })
                except (ValueError, IndexError):
                    pass

    # 按 CPU 使用率排序
    cpu_metrics.sort(key=lambda x: x["cpu_usage_percent"], reverse=True)
    memory_metrics.sort(key=lambda x: x["memory_usage_percent"], reverse=True)

    # 合并 CPU 和内存数据
    pod_metrics_map = {}
    for m in cpu_metrics[:top_n]:
        key = f"{m['namespace']}/{m['pod']}"
        pod_metrics_map[key] = m
    for m in memory_metrics[:top_n]:
        key = f"{m['namespace']}/{m['pod']}"
        if key in pod_metrics_map:
            pod_metrics_map[key]["memory_usage_percent"] = m["memory_usage_percent"]
        else:
            pod_metrics_map[key] = m

    # ========== 7. 返回结果 ==========
    result = {
        "success": True,
        "region": region,
        "cluster_id": cluster_id,
        "cluster_name": cluster_name,
        "aom_instance_id": aom_instance_id,
        "inspection_time": time_module.strftime('%Y-%m-%d %H:%M:%S', time_module.localtime()),
        "query_params": {
            "top_n": top_n,
            "hours": hours,
            "namespace": namespace
        },
        "promql": {
            "cpu": cpu_query,
            "memory": memory_query
        },
        "metrics": {
            "cpu_top_n": cpu_metrics[:top_n],
            "memory_top_n": memory_metrics[:top_n],
            "all_pods": list(pod_metrics_map.values())
        },
        "summary": {
            "total_pods": len(pod_metrics_map),
            "critical_cpu": len([m for m in cpu_metrics if m["status"] == "critical"]),
            "critical_memory": len([m for m in memory_metrics if m["status"] == "critical"]),
            "warning_cpu": len([m for m in cpu_metrics if m["status"] == "warning"]),
            "warning_memory": len([m for m in memory_metrics if m["status"] == "warning"])
        }
    }

    # 如果有 label 过滤，添加过滤信息
    if label_selector:
        result["query_params"]["label_selector"] = label_selector
        result["label_filter"] = {
            "selector": label_selector,
            "matched_count": len(matched_pods_info),
            "matched_pods": matched_pods_info[:50]  # 最多返回 50 个 Pod 信息
        }

    return result

def get_cce_pod_metrics(region: str, cluster_id: str, pod_name: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, namespace: str = None, hours: int = 1, cpu_query: str = None, memory_query: str = None) -> Dict[str, Any]:
    """获取指定CCE Pod的CPU、内存使用率监控时序数据

    Args:
        region: 华为云区域 (如 cn-north-4)
        cluster_id: CCE 集群 ID
        pod_name: Pod名称
        ak: Access Key ID (可选)
        sk: Secret Access Key (可选)
        project_id: Project ID (可选)
        namespace: 命名空间（可选，默认所有命名空间）
        hours: 查询时间范围（小时）(默认 1)
        cpu_query: 自定义 CPU PromQL (可选)
        memory_query: 自定义内存 PromQL (可选)

    Returns:
        Dict with success status and specified pod metrics time series data
    """
    import time as time_module

    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}

    if not cluster_id or not pod_name:
        return {"success": False, "error": "cluster_id and pod_name are required"}

    # ========== 1. 获取集群名称 ==========
    cluster_name = cluster_id
    try:
        clusters_result = cce.list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters_result.get("success"):
            for c in clusters_result.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass

    # ========== 2. 获取Pod详细信息 ==========
    pod_info = {}
    pods_result = cce.get_kubernetes_pods(region, cluster_id, access_key, secret_key, proj_id, namespace)
    if pods_result.get("success"):
        for pod in pods_result.get("pods", []):
            if pod.get("name") == pod_name:
                pod_info = pod
                break

    # ========== 3. 获取 AOM 实例 ==========
    from .cce_diagnosis import get_aom_instance
    aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
    if not aom_result.get("success"):
        return {
            "success": False,
            "error": aom_result.get("error", "未找到可用的 AOM 实例"),
            "error_type": aom_result.get("error_type"),
            "cluster_id": cluster_id,
            "cluster_name": cluster_name,
            "pod_name": pod_name,
            "namespace": namespace
        }
    aom_instance_id = aom_result.get("aom_instance_id")

    # ========== 4. 构建 PromQL 查询（筛选指定Pod） ==========
    pod_filter = f',pod="{pod_name}"'
    namespace_filter = f',namespace="{namespace}"' if namespace else ""

    # 默认 CPU 使用率 PromQL (相对 Limit %)
    if cpu_query is None:
        cpu_query = f'sum by (pod, namespace) (rate(container_cpu_usage_seconds_total{{image!=""{namespace_filter}{pod_filter}}}[5m])) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{{resource="cpu"{namespace_filter}{pod_filter}}}) * 100'

    # 默认内存使用率 PromQL (相对 Limit %)
    if memory_query is None:
        memory_query = f'sum by (pod, namespace) (container_memory_working_set_bytes{{image!=""{namespace_filter}{pod_filter}}}) / on (pod, namespace) group_left sum by (pod, namespace) (kube_pod_container_resource_limits{{resource="memory"{namespace_filter}{pod_filter}}}) * 100'

    # ========== 5. 执行查询 ==========
    cpu_result = aom.get_aom_prom_metrics_http(region, aom_instance_id, cpu_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
    memory_result = aom.get_aom_prom_metrics_http(region, aom_instance_id, memory_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)

    # ========== 6. 解析结果 ==========
    def parse_metric_result(result, metric_name):
        """解析监控结果，返回时序数据"""
        if result.get("success") and result.get("result", {}).get("data", {}).get("result"):
            for item in result["result"]["data"]["result"]:
                values = item.get("values", [])
                if values:
                    time_series = []
                    for ts, val in values:
                        try:
                            time_series.append({
                                "timestamp": int(ts),
                                "time": time_module.strftime('%Y-%m-%d %H:%M:%S', time_module.localtime(int(ts))),
                                "value": round(float(val), 2)
                            })
                        except (ValueError, IndexError):
                            pass
                    if time_series:
                        latest_value = time_series[-1]["value"]
                        return {
                            metric_name: latest_value,
                            "status": "critical" if latest_value > 80 else "warning" if latest_value > 50 else "normal",
                            "time_series": time_series
                        }
        return None

    cpu_data = parse_metric_result(cpu_result, "cpu_usage_percent")
    memory_data = parse_metric_result(memory_result, "memory_usage_percent")

    # ========== 7. 返回结果 ==========
    return {
        "success": True,
        "region": region,
        "cluster_id": cluster_id,
        "cluster_name": cluster_name,
        "pod_name": pod_name,
        "namespace": pod_info.get("namespace", namespace),
        "pod_info": pod_info,
        "aom_instance_id": aom_instance_id,
        "query_time": time_module.strftime('%Y-%m-%d %H:%M:%S', time_module.localtime()),
        "query_params": {
            "hours": hours
        },
        "promql": {
            "cpu": cpu_query,
            "memory": memory_query
        },
        "metrics": {
            "cpu": cpu_data,
            "memory": memory_data
        }
    }

def get_cce_node_metrics_topN(region: str, cluster_id: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, top_n: int = 10, hours: int = 1, cpu_query: str = None, memory_query: str = None, disk_query: str = None) -> Dict[str, Any]:
    """获取 CCE 集群节点监控数据

    自动获取 AOM 实例并执行节点 CPU/内存/磁盘监控查询，返回 Top N 数据。

    Args:
        region: 华为云区域 (如 cn-north-4)
        cluster_id: CCE 集群 ID
        ak: Access Key ID (可选)
        sk: Secret Access Key (可选)
        project_id: Project ID (可选)
        top_n: 返回 Top N 数据 (默认 10)
        hours: 查询时间范围（小时）(默认 1)
        cpu_query: 自定义 CPU PromQL (可选)
        memory_query: 自定义内存 PromQL (可选)
        disk_query: 自定义磁盘 PromQL (可选)

    Returns:
        Dict with success status and node metrics data
    """
    import time as time_module

    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}

    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    # ========== 1. 获取集群名称 ==========
    cluster_name = cluster_id
    try:
        clusters_result = cce.list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters_result.get("success"):
            for c in clusters_result.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass

    # ========== 2. 获取节点信息映射 ==========
    node_info_map = {}  # IP -> 节点信息

    # 从 Kubernetes API 获取节点信息（节点名称即 IP）
    k8s_nodes_result = cce.get_kubernetes_nodes(region, cluster_id, access_key, secret_key, proj_id)
    if k8s_nodes_result.get("success"):
        for node in k8s_nodes_result.get("nodes", []):
            node_name = node.get("name", "")  # Kubernetes 节点名即 IP
            if node_name:
                node_info_map[node_name] = {
                    "name": node_name,
                    "ip": node_name,
                    "status": node.get("status", "Unknown"),
                    "kubelet_version": node.get("kubelet_version", ""),
                    "os": node.get("os", ""),
                    "container_runtime": node.get("container_runtime", "")
                }

    # 从 CCE API 获取节点规格等信息（按名称匹配）
    cce_nodes_result = cce.list_cce_cluster_nodes(region, cluster_id, access_key, secret_key, proj_id)
    if cce_nodes_result.get("success"):
        for cce_node in cce_nodes_result.get("nodes", []):
            cce_node_name = cce_node.get("name", "")
            # 尝试通过名称匹配
            for ip, node_info in node_info_map.items():
                if ip in cce_node_name or cce_node_name.endswith(ip.replace(".", "")):
                    node_info["cce_name"] = cce_node_name
                    node_info["id"] = cce_node.get("id", "")
                    node_info["flavor"] = cce_node.get("flavor", "")
                    node_info["cce_status"] = cce_node.get("status", "")
                    break

    # ========== 3. 获取 AOM 实例 ==========
    from .cce_diagnosis import get_aom_instance
    aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
    if not aom_result.get("success"):
        return {
            "success": False,
            "error": aom_result.get("error", "未找到可用的 AOM 实例"),
            "error_type": aom_result.get("error_type"),
            "cluster_id": cluster_id,
            "cluster_name": cluster_name
        }
    aom_instance_id = aom_result.get("aom_instance_id")

    # ========== 4. 构建 PromQL 查询 ==========
    # 默认 CPU 使用率 PromQL
    if cpu_query is None:
        cpu_query = f"topk({top_n}, 100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode='idle',cluster_name='{cluster_name}'}}[5m])) * 100))"

    # 默认内存使用率 PromQL
    if memory_query is None:
        memory_query = f"topk({top_n}, avg by (instance) ((1 - node_memory_MemAvailable_bytes{{cluster_name='{cluster_name}'}} / node_memory_MemTotal_bytes{{cluster_name='{cluster_name}'}})) * 100)"

    # 默认磁盘使用率 PromQL
    if disk_query is None:
        disk_query = f"topk({top_n}, avg by (instance) ((1 - node_filesystem_avail_bytes{{mountpoint='/',fstype!~'tmpfs|fuse.lxcfs',cluster_name='{cluster_name}'}} / node_filesystem_size_bytes{{mountpoint='/',fstype!~'tmpfs|fuse.lxcfs',cluster_name='{cluster_name}'}})) * 100)"

    # ========== 5. 执行查询 ==========
    cpu_result = aom.get_aom_prom_metrics_http(region, aom_instance_id, cpu_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
    memory_result = aom.get_aom_prom_metrics_http(region, aom_instance_id, memory_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
    disk_result = aom.get_aom_prom_metrics_http(region, aom_instance_id, disk_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)

    # ========== 6. 解析结果 ==========
    def parse_node_result(result, metric_name):
        """解析节点监控结果"""
        metrics = []
        if result.get("success") and result.get("result", {}).get("data", {}).get("result"):
            for item in result["result"]["data"]["result"]:
                metric = item.get("metric", {})
                values = item.get("values", [])
                if values:
                    try:
                        latest_value = float(values[-1][1])
                        instance = metric.get("instance", "unknown")
                        # 提取 IP 地址
                        instance_ip = instance.split(":")[0] if ":" in instance else instance

                        # 获取节点信息
                        node_info = node_info_map.get(instance_ip, {})
                        # 优先使用节点名称，否则使用 IP
                        node_name = node_info.get("name", instance_ip)

                        metrics.append({
                            "instance": instance,
                            "node_ip": instance_ip,
                            "node_name": node_name,
                            "node_id": node_info.get("id", ""),
                            "flavor": node_info.get("flavor", ""),
                            metric_name: round(latest_value, 2),
                            "status": "critical" if latest_value > 80 else "warning" if latest_value > 50 else "normal",
                            "time_series": values  # 保存完整的时序数据
                        })
                    except (ValueError, IndexError):
                        pass
        return metrics

    cpu_metrics = parse_node_result(cpu_result, "cpu_usage_percent")
    memory_metrics = parse_node_result(memory_result, "memory_usage_percent")
    disk_metrics = parse_node_result(disk_result, "disk_usage_percent")

    # 按使用率排序
    cpu_metrics.sort(key=lambda x: x["cpu_usage_percent"], reverse=True)
    memory_metrics.sort(key=lambda x: x["memory_usage_percent"], reverse=True)
    disk_metrics.sort(key=lambda x: x["disk_usage_percent"], reverse=True)

    # 合并所有节点的监控数据
    all_nodes_map = {}
    for m in cpu_metrics:
        key = m["node_ip"]
        all_nodes_map[key] = m
    for m in memory_metrics:
        key = m["node_ip"]
        if key in all_nodes_map:
            all_nodes_map[key]["memory_usage_percent"] = m["memory_usage_percent"]
            all_nodes_map[key]["status"] = "critical" if m["memory_usage_percent"] > 80 else "warning" if m["memory_usage_percent"] > 50 else all_nodes_map[key]["status"]
        else:
            all_nodes_map[key] = m
    for m in disk_metrics:
        key = m["node_ip"]
        if key in all_nodes_map:
            all_nodes_map[key]["disk_usage_percent"] = m["disk_usage_percent"]
            if m["disk_usage_percent"] > 80:
                all_nodes_map[key]["status"] = "critical"
            elif m["disk_usage_percent"] > 50 and all_nodes_map[key]["status"] == "normal":
                all_nodes_map[key]["status"] = "warning"
        else:
            all_nodes_map[key] = m

    # ========== 7. 返回结果 ==========
    return {
        "success": True,
        "region": region,
        "cluster_id": cluster_id,
        "cluster_name": cluster_name,
        "aom_instance_id": aom_instance_id,
        "inspection_time": time_module.strftime('%Y-%m-%d %H:%M:%S', time_module.localtime()),
        "query_params": {
            "top_n": top_n,
            "hours": hours
        },
        "promql": {
            "cpu": cpu_query,
            "memory": memory_query,
            "disk": disk_query
        },
        "metrics": {
            "cpu_top_n": cpu_metrics[:top_n],
            "memory_top_n": memory_metrics[:top_n],
            "disk_top_n": disk_metrics[:top_n],
            "all_nodes": list(all_nodes_map.values())
        },
        "summary": {
            "total_nodes": len(all_nodes_map),
            "critical_cpu": len([m for m in cpu_metrics if m["status"] == "critical"]),
            "critical_memory": len([m for m in memory_metrics if m["status"] == "critical"]),
            "critical_disk": len([m for m in disk_metrics if m["status"] == "critical"]),
            "warning_cpu": len([m for m in cpu_metrics if m["status"] == "warning"]),
            "warning_memory": len([m for m in memory_metrics if m["status"] == "warning"]),
            "warning_disk": len([m for m in disk_metrics if m["status"] == "warning"])
        }
    }

def get_cce_node_metrics(region: str, cluster_id: str, node_ip: str, ak: Optional[str] = None, sk: Optional[str] = None, project_id: Optional[str] = None, hours: int = 1, cpu_query: str = None, memory_query: str = None, disk_query: str = None) -> Dict[str, Any]:
    """获取指定CCE节点的CPU、内存、磁盘使用率监控时序数据

    Args:
        region: 华为云区域 (如 cn-north-4)
        cluster_id: CCE 集群 ID
        node_ip: 节点IP地址
        ak: Access Key ID (可选)
        sk: Secret Access Key (可选)
        project_id: Project ID (可选)
        hours: 查询时间范围（小时）(默认 1)
        cpu_query: 自定义 CPU PromQL (可选)
        memory_query: 自定义内存 PromQL (可选)
        disk_query: 自定义磁盘 PromQL (可选)

    Returns:
        Dict with success status and specified node metrics time series data
    """
    import time as time_module

    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided"}

    if not cluster_id or not node_ip:
        return {"success": False, "error": "cluster_id and node_ip are required"}

    # ========== 1. 获取集群名称 ==========
    cluster_name = cluster_id
    try:
        clusters_result = cce.list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters_result.get("success"):
            for c in clusters_result.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass

    # ========== 2. 获取节点信息 ==========
    node_info = {}
    # 从 Kubernetes API 获取节点信息
    k8s_nodes_result = cce.get_kubernetes_nodes(region, cluster_id, access_key, secret_key, proj_id)
    if k8s_nodes_result.get("success"):
        for node in k8s_nodes_result.get("nodes", []):
            if node.get("ip") == node_ip:
                node_info = node
                break

    # 从 CCE API 获取节点规格等信息
    if not node_info:
        cce_nodes_result = cce.list_cce_cluster_nodes(region, cluster_id, access_key, secret_key, proj_id)
        if cce_nodes_result.get("success"):
            for cce_node in cce_nodes_result.get("nodes", []):
                cce_node_name = cce_node.get("name", "")
                if node_ip in cce_node_name or cce_node_name.endswith(node_ip.replace(".", "")):
                    node_info["cce_name"] = cce_node_name
                    node_info["id"] = cce_node.get("id", "")
                    node_info["flavor"] = cce_node.get("flavor", "")
                    node_info["cce_status"] = cce_node.get("status", "")
                    break

    # ========== 3. 获取 AOM 实例 ==========
    from .cce_diagnosis import get_aom_instance
    aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
    if not aom_result.get("success"):
        return {
            "success": False,
            "error": aom_result.get("error", "未找到可用的 AOM 实例"),
            "error_type": aom_result.get("error_type"),
            "cluster_id": cluster_id,
            "cluster_name": cluster_name,
            "node_ip": node_ip
        }
    aom_instance_id = aom_result.get("aom_instance_id")

    # ========== 4. 构建 PromQL 查询（筛选指定节点IP） ==========
    # 默认 CPU 使用率 PromQL
    if cpu_query is None:
        cpu_query = f"100 - (avg by (instance) (irate(node_cpu_seconds_total{{mode='idle',cluster_name='{cluster_name}',instance=~'{node_ip}.*'}}[5m])) * 100"

    # 默认内存使用率 PromQL
    if memory_query is None:
        memory_query = f"avg by (instance) ((1 - node_memory_MemAvailable_bytes{{cluster_name='{cluster_name}',instance=~'{node_ip}.*'}} / node_memory_MemTotal_bytes{{cluster_name='{cluster_name}',instance=~'{node_ip}.*'}})) * 100"

    # 默认磁盘使用率 PromQL
    if disk_query is None:
        disk_query = f"avg by (instance) ((1 - node_filesystem_avail_bytes{{mountpoint='/',fstype!~'tmpfs|fuse.lxcfs',cluster_name='{cluster_name}',instance=~'{node_ip}.*'}} / node_filesystem_size_bytes{{mountpoint='/',fstype!~'tmpfs|fuse.lxcfs',cluster_name='{cluster_name}',instance=~'{node_ip}.*'}})) * 100"

    # ========== 5. 执行查询 ==========
    cpu_result = aom.get_aom_prom_metrics_http(region, aom_instance_id, cpu_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
    memory_result = aom.get_aom_prom_metrics_http(region, aom_instance_id, memory_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)
    disk_result = aom.get_aom_prom_metrics_http(region, aom_instance_id, disk_query, hours=hours, ak=access_key, sk=secret_key, project_id=proj_id)

    # ========== 6. 解析结果 ==========
    def parse_metric_result(result, metric_name):
        """解析监控结果，返回时序数据"""
        if result.get("success") and result.get("result", {}).get("data", {}).get("result"):
            for item in result["result"]["data"]["result"]:
                values = item.get("values", [])
                if values:
                    time_series = []
                    for ts, val in values:
                        try:
                            time_series.append({
                                "timestamp": int(ts),
                                "time": time_module.strftime('%Y-%m-%d %H:%M:%S', time_module.localtime(int(ts))),
                                "value": round(float(val), 2)
                            })
                        except (ValueError, IndexError):
                            pass
                    if time_series:
                        latest_value = time_series[-1]["value"]
                        return {
                            metric_name: latest_value,
                            "status": "critical" if latest_value > 80 else "warning" if latest_value > 50 else "normal",
                            "time_series": time_series
                        }
        return None

    cpu_data = parse_metric_result(cpu_result, "cpu_usage_percent")
    memory_data = parse_metric_result(memory_result, "memory_usage_percent")
    disk_data = parse_metric_result(disk_result, "disk_usage_percent")

    # ========== 7. 返回结果 ==========
    return {
        "success": True,
        "region": region,
        "cluster_id": cluster_id,
        "cluster_name": cluster_name,
        "node_ip": node_ip,
        "node_info": node_info,
        "aom_instance_id": aom_instance_id,
        "query_time": time_module.strftime('%Y-%m-%d %H:%M:%S', time_module.localtime()),
        "query_params": {
            "hours": hours
        },
        "promql": {
            "cpu": cpu_query,
            "memory": memory_query,
            "disk": disk_query
        },
        "metrics": {
            "cpu": cpu_data,
            "memory": memory_data,
            "disk": disk_data
        }
    }
