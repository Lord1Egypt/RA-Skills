# Risk Rules

## Default Read-Only

This skill's default behavior only allows reading and reporting; it does not allow directly changing cluster state.

Prohibited automatic execution:

- Creating, replacing, or deleting HPA.
- Modifying Deployment/StatefulSet replicas, requests, limits.
- Modifying node pool min/max; manually scaling node pools up or down.
- Installing, upgrading, or uninstalling CCE addons.
- Cordon, drain, delete, or reboot nodes.
- Expanding VPC subnets, applying for quotas, or modifying IAM agencies.

## Allowed Remediation Output

Allowed outputs:

- HPA YAML suggestions or `huawei_configure_cce_hpa` preview without `confirm=true`.
- Node pool autoscaling min/max suggestions.
- Request/limit adjustment suggestions.
- Affinity, taint, tolerations, nodeSelector remediation suggestions.
- Subnet, quota, IAM manual verification checklists.
- Pre-change and post-change verification steps and rollback paths.

## Actions Requiring Handoff

When the customer explicitly requests remediation execution, hand off to `huawei-cloud-cce-auto-remediation-runner` or a manual change process:

- HPA configuration: Preview manifest first, then require customer confirmation.
- Node pool scaling or min/max adjustment: Must confirm business impact, cost, AZ/spec, and rollback plan.
- Request/limit adjustment: Requires a release window or rolling update plan.
- Addon installation/upgrade: Must confirm addon version, cluster version compatibility, and rollback plan.