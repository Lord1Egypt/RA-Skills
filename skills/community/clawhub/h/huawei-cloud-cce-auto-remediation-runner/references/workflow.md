# Workflow

1. Convert the user's intent or root cause conclusion into an action, object, parameters, and verification criteria.
2. If the root cause is that a Deployment's new version is unavailable due to startup command, image, probe, or CrashLoop, prefer `rollback_previous_revision` strategy.
3. Check the action's risk level. Deployment rollback, scale, resize, cordon, uncordon are R2; delete, drain, reboot, HSS status change are R3.
4. The first invocation must NOT include `confirm=true`. Call the action to obtain a preview or risk prompt.
5. Output the preview result, impact scope, rollback method, and post-execution verification plan to the user.
6. Wait for explicit user confirmation. The confirmation must include at least: action, object, region, and cluster_id.
7. Only after user confirmation is it permitted to call the action with `confirm=true`.
8. After execution, call read-only tools to verify Pod, Node, Workload, Events, or vulnerability status.
9. For auto-remediation orchestration, output a complete Markdown execution report containing diagnosis basis, action results, and verification results.