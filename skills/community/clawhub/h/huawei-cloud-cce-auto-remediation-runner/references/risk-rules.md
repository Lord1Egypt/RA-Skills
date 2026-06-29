# Risk Rules

## R1 — Read-Only Verification

- Pod, Node, Events, diagnosis, and status queries may be executed automatically without `confirm=true`.

## R2 — Runtime Impact

- `huawei_scale_cce_workload`
- `huawei_resize_cce_workload`
- `huawei_resize_cce_nodepool`
- `huawei_cce_node_cordon`
- `huawei_cce_node_uncordon`
- `huawei_start_ecs_instance`
- `huawei_stop_ecs_instance`
- `huawei_bind_cce_cluster_eip`
- `huawei_unbind_cce_cluster_eip`
- `huawei_configure_cce_hpa`
- `huawei_rollback_cce_workload`
- `huawei_auto_remediation_run` (when the strategy involves Deployment rollback, scale, resize, or other runtime state changes)

**Rule:** Must preview first. Auto-adding `confirm=true` is prohibited.

## R3 — High Risk / Destructive

- `huawei_delete_cce_cluster`
- `huawei_delete_cce_node`
- `huawei_delete_cce_workload`
- `huawei_cce_node_drain`
- `huawei_reboot_ecs`
- `huawei_hibernate_cce_cluster`
- `huawei_awake_cce_cluster`
- `huawei_hss_change_vul_status`

**Rule:** Must receive explicit user confirmation of the action and target object before passing `confirm=true`. Post-execution verification is mandatory. Auto, batch, or fuzzy-target execution is prohibited.