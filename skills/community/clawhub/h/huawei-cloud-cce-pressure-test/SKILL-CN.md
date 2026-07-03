---
name: 全链路压测
description: Use this skill for Huawei Cloud CCE end-to-end workload pressure tests and performance evaluation. It builds a complete traffic path from k6 client through ELB to nginx-ingress to workload pods, supports short-connection, keepalive, and ramp traffic models, collects ELB metrics and AOM observability data, evaluates elasticity phases, and generates bilingual Markdown and HTML reports with performance curves.
---

# 全链路压测

Use this skill to run controlled workload pressure tests on Huawei Cloud CCE.
Keep mutations preview-first. Service and Ingress changes, traffic generation,
and workload scaling require explicit user approval before calling an action
with `confirm=true`.

## Workflow

1. Confirm `region`, `cluster_id`, workload namespace and name, target port, test window, traffic model, traffic size, and output directory.
2. Inspect existing Services, Ingresses, HPA, ingress controller, and ELB context.
3. When an isolated Java sample is needed,
run `huawei_deploy_cce_pressure_test_java_sample` without confirmation.
Review the Namespace, ConfigMap, and Deployment, then apply with
`confirm=true` only after approval.
4. If no reusable ingress-controller ELB exists, inspect VPC subnets,
preview `huawei_create_elb`, review chargeable fields, and create it
with `confirm=true` only after approval. Do not silently create an EIP.
5. Run `huawei_prepare_cce_pressure_test_route` without confirmation. Review the Service and Ingress manifest, then apply it with `confirm=true` only after approval.
6. Run `huawei_generate_cce_pressure_test_client` to review the k6 ConfigMap and Job. Use a regional SWR mirror for the k6 image if public image pulls are unavailable.
7. Run `huawei_run_cce_pressure_test` without confirmation first. After approval, run it with `confirm=true`.
8. Run `huawei_collect_cce_pressure_test_observability`. Pass `elb_id` for ELB traffic, connection, latency, and success-rate curves. Pod CPU and memory are collected from node metrics.
9. Generate the report with `huawei_generate_cce_pressure_test_report`.
10. For elasticity evaluation, run a baseline phase, preview `huawei_scale_cce_workload`, apply scaling only after approval with `confirm=true`, then run a second phase and compare reports.

## Observability

Use ELB metrics for traffic, connections, latency, and HTTP success-rate evidence. Use LTS to correlate application errors with curve changes when available. Use node metrics for Pod CPU and memory utilization.

## References

- Read `references/workflow.md` for staged execution and action parameters.
- Read `references/risk-rules.md` before sending traffic or applying Kubernetes changes.
- Read `references/output-schema.md` when consuming JSON evidence or combining phase reports.