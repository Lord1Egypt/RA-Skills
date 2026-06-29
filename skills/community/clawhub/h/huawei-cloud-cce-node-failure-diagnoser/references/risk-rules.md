# Risk Rules

- Allowed: automatic execution of node read-only queries, Lease queries, Event queries, Pod queries, metric queries, inspection items, and HSS queries.
- `huawei_node_failure_diagnose` is a read-only diagnosis tool; it generates structured evidence and Markdown reports only — it does not execute recovery actions.
- This skill must NOT directly invoke cordon, uncordon, drain, reboot, or vulnerability status modification actions.
- Before recommending reboot or drain, you must explain: business impact, Pods on the node, rollback method, and verification steps.
- HSS remediation actions must note that `confirm=true` may only be passed after explicit user confirmation.