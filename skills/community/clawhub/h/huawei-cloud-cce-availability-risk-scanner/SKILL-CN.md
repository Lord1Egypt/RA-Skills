---
name: availability-risk-scanner
description: Use this skill for Huawei Cloud CCE availability risk scanning, including master HA and utilization, node and workload AZ balance, single replicas, missing PodDisruptionBudgets, health probes, unreasonable affinity or nodepool pinning, core addon anti-affinity, gateway workload distribution, and request/limit overcommit.
---

# availability-risk-scanner

你负责扫描 CCE 集群的可用性风险。默认只做只读检查、报告输出和整改计划，不直接修改工作负载、PDB、亲和性、探针、节点池或集群配置。

## 处理步骤

1. 收集 region、cluster_id、排除命名空间和网关关键字；默认排除 `kube-system` 的普通业务风险，但仍关注核心插件如 CoreDNS、nginx-ingress。
2. 优先调用 `huawei_scan_cce_availability_risk` 完成组合扫描，并在需要留痕时传入 `output_dir`。
3. 检查控制面可见性、master 高可用、master CPU/内存指标、节点 AZ 分布和节点池分布。
4. 检查 Deployment、StatefulSet、DaemonSet 的副本数、PDB、Pod 分布、健康检查、亲和性、反亲和、拓扑分散和资源 request/limit。
5. 重点识别网关类工作负载，例如 nginx、gateway、ingress、proxy、kong、apisix、traefik。
6. 输出报告、风险等级、整改建议和授权后执行计划；真实整改必须先获得客户明确授权。

## References

- 扫描流程、判断规则和人工复核点读 `references/workflow.md`。
- 整改授权、安全边界和禁用动作读 `references/risk-rules.md`。
- 输出结构读 `references/output-schema.md`。

## 推荐 action

组合扫描：`huawei_scan_cce_availability_risk`。

补充查询：`huawei_get_kubernetes_nodes`、`huawei_get_cce_pods`、`huawei_get_cce_deployments`、`huawei_get_cce_services`、`huawei_get_cce_ingresses`、`huawei_list_cce_nodepools`、`huawei_list_cce_daemonsets`、`huawei_list_cce_statefulsets`、`huawei_get_cce_node_metrics_topN`。

## 风险边界

本 skill 不自动扩副本、不创建 PDB、不修改探针、不调整亲和性、不迁移节点、不扩缩节点池。可以生成整改计划、YAML 建议和验证清单；执行整改时必须由用户明确授权，并交给有写权限的 action 或人工变更流程。
