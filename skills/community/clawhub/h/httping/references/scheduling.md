# Scheduling notes for httping

- One-off probe: run the loop inline in the calling tool; no persistence needed.
- Repeated probes across deployments: use the OpenClaw `cron` tool to schedule a one-shot or recurring agent turn that runs httping and reports degraded endpoints.
- Avoid `exec sleep` polling loops; they burn the foreground session. Prefer `cron` for periodic work.
- Pair with `taskflow` when a probe must wait on an external confirmation (e.g., a deploy pipeline) before resuming: httping emits probe facts, taskflow owns the waiting/resume lifecycle.
