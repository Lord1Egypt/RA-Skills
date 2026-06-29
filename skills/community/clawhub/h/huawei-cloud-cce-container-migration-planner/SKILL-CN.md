---
name: container-migration-planner
description: Use this skill for Huawei Cloud CCE migration planning, resource inventory, delivery方案, dependency mapping, and migration risk assessment without executing changes.
---

# container-migration-planner

你负责迁移方案和交付规划。目标是盘点现状、识别依赖、输出迁移批次、风险和验证计划，不执行真实迁移动作。

## 处理步骤

1. 收集源集群、目标约束、业务窗口、迁移粒度和合规要求。
2. 盘点 CCE 集群、节点池、插件、工作负载、Service、Ingress、PVC/PV、ConfigMap、Secret。
3. 盘点 VPC、子网、安全组、ELB、EIP、EVS、SFS/SFS Turbo。
4. 建立依赖矩阵和迁移批次。
5. 输出风险清单、回退策略、验证清单和需要人工确认的动作。

## References

- 资源盘点和迁移批次读 `references/workflow.md`。
- 方案阶段的安全边界读 `references/risk-rules.md`。
- 方案输出按 `references/output-schema.md`。

## 推荐 action

CCE：`huawei_list_cce_clusters`、`huawei_list_cce_nodes`、`huawei_list_cce_nodepools`、`huawei_get_cce_deployments`、`huawei_get_cce_services`、`huawei_get_cce_ingresses`。

存储和配置：`huawei_get_cce_pvcs`、`huawei_get_cce_pvs`、`huawei_list_cce_configmaps`、`huawei_list_cce_secrets`。

云资源：`huawei_list_vpc`、`huawei_list_vpc_subnets`、`huawei_list_security_groups`、`huawei_list_elb`、`huawei_list_eip`、`huawei_list_evs`、`huawei_list_sfs`。

## 风险约束

本 skill 只做盘点和方案。不创建目标资源，不修改网络，不迁移数据，不删除源资源。

