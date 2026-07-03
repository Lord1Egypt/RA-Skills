# Risk Rules

- Read-only diagnostic actions are allowed to execute automatically.
- This skill must NOT call scaling, workload deletion, node deletion, drain, or reboot operations.
- If `huawei_scale_cce_workload` or `huawei_resize_cce_workload` is recommended, it must be handed off to `huawei-cloud-cce-auto-remediation-runner`.
- Log output must contain only sanitized tail excerpts; never copy raw passwords, tokens, AK/SK, or Authorization headers from application logs into the output.
- For ImagePullBackOff, prioritize Events — do not repeatedly request container logs that do not exist.
- Scaling, isolation, delete-and-rebuild suggestions for OOMKilled, PendingScheduling, and Evicted are recovery proposals only; they are NOT executed within this skill.