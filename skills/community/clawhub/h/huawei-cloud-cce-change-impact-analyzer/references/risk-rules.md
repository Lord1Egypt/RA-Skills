# Risk Rules

## Read-Only Boundary

`huawei-cloud-cce-change-impact-analyzer` only performs read-only queries and report generation:

- May query audit logs, K8s events, AOM alarms, Pod/Service/Ingress/Node/ConfigMap/Secret/NodePool/Security Group/VPC ACL current state.
- May call Workload, Network, Node diagnosis actions for read-only drill-down.
- May write `report_markdown` to a user-specified `output_file`.

## Prohibited Actions

The following are prohibited within this skill:

- Roll back or re-release workloads.
- Modify Deployment/StatefulSet/DaemonSet, ConfigMap, Secret, Service, Ingress, Gateway.
- Modify NetworkPolicy, RBAC, Security Group, VPC ACL.
- Scale workloads or node pools.
- Cordon, uncordon, drain, delete, reboot nodes or ECS instances.
- Modify HSS vulnerability status.

## Remediation Action Handoff

When the report points to clear remediation actions:

1. Write the suggested action, risks, and verification criteria in the report.
2. Do not execute any change without `confirm=true`.
3. Hand off to `huawei-cloud-cce-auto-remediation-runner` to generate a preview.
4. Only after explicit user confirmation may the remediation skill execute actions.
5. After changes, run `huawei_change_impact_analyze` or the corresponding diagnoser again for verification.

## Conclusion Confidence

- `high`: Audit change, fault time proximity, event/alarm response, and topology impact — at least three of four evidence categories present.
- `medium`: Audit change plus at least one response signal, or global core change identified but response signals insufficient.
- `low`: Only object write operations or current snapshot present, lacking temporal/response/topology evidence.

Low-confidence conclusions must state data gaps in the report; do not present speculation as fact.