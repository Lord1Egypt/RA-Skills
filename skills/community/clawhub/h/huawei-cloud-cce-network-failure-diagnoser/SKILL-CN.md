---
name: network-failure-diagnoser
description: Use this skill for CCE Kubernetes network failures such as Service unreachable, DNS/CoreDNS errors, Ingress 502/504, NetworkPolicy blocks, ELB backend health issues, EIP/NAT/VPC/security-group problems, and end-to-end Markdown diagnosis reports.
---

# network-failure-diagnoser

你负责诊断 CCE 网络链路，从节点底座、DNS、Service/EndpointSlice、NetworkPolicy、Ingress 到云 ELB/EIP/NAT/VPC 安全策略逐层排查。默认产出一份完整 Markdown 报告，必须包含排查过程、证据、结论、置信度和验证标准。

## 处理步骤

1. 收集 `region`、`cluster_id`、`namespace`，尽量补齐 `target_kind`、`target_name`、`service_name`、`ingress_name`、`source_pod`、`destination_pod`、`domain`、`failure_symptom` 或 `elb_id`。
2. 首选调用 `huawei_network_failure_diagnose`，一次性采集 K8s 与云侧只读快照，并返回 `report_markdown`。
3. 如果用户只要原始对象，再按需调用 `huawei_get_cce_services`、`huawei_get_cce_ingresses`、`huawei_get_cce_pods`、`huawei_get_kubernetes_nodes`、`huawei_get_cce_events`、`huawei_get_pod_logs`。
4. 若是外部访问链路，补充 `huawei_get_elb_backend_status`、`huawei_get_elb_metrics`、`huawei_list_security_groups`、`huawei_list_vpc_acls`、`huawei_list_eip`、`huawei_list_nat`。
5. 输出时必须引用具体对象、事件、日志片段或云 API 字段；没有证据时写“证据不足”，不要把猜测写成结论。

## References

- 复用能力、缺口和分层诊断流水线读 `references/workflow.md`。
- 绑定/解绑、扩缩容验证等动作边界读 `references/risk-rules.md`。
- 输出结构按 `references/output-schema.md`。

## 推荐 action

首选诊断：`huawei_network_failure_diagnose`。该 action 会返回结构化字段和完整 `report_markdown`。

Kubernetes 证据：`huawei_get_cce_services`、`huawei_get_cce_ingresses`、`huawei_get_cce_pods`、`huawei_get_kubernetes_nodes`、`huawei_get_cce_events`、`huawei_get_pod_logs`。

云网络证据：`huawei_get_elb_backend_status`、`huawei_get_elb_metrics`、`huawei_list_elb`、`huawei_list_elb_listeners`、`huawei_list_eip`、`huawei_get_eip_metrics`、`huawei_list_nat`、`huawei_get_nat_gateway_metrics`、`huawei_list_security_groups`、`huawei_list_vpc_acls`。

兼容旧流程：`huawei_network_diagnose`、`huawei_network_diagnose_by_alarm`、`huawei_network_verify_pod_scheduling`。

## 风险约束

本 skill 只做只读查询和报告生成，不绑定或解绑 EIP，不修改安全组/ACL/ELB 监听器，不扩缩容，不重启组件。需要变更时输出预案并转交 `auto-remediation-runner`。
