# Native scheduling integration

Discover the scheduler tool available in the current runtime. Inspect its active schema before a write. The current OpenClaw CLI also exposes `openclaw automations` (`cron` is an alias); use `automations add --help` for the installed version.

The local helper validates inputs and records read-back receipts. Its prepare action returns status prepared and never registers a timer by itself. Perform registration using the real native scheduler. Native chat-context tools are preferable to CLI when they preserve the exact current chat route.

Read back the stored job. Normalize the real result into jobId, enabled, nextRunAtMs, timezone, schedule {kind,value} and delivery {agentId,channel,accountId,to}. Confirm actual account and recipient IDs, not lowercased session-key guesses. Then record the receipt. The CLI argument array from prepare is an alternative for an authorized host executor; do not pass it through shell interpolation.

If the tool is absent, name the missing capability and provide the prepared schedule for the user to enable in their host. Report status prepared; after successful scheduler read-back report status scheduled; after run history confirms a delivered result report status delivered. These stages are distinct. An enabled job alone is not a delivery receipt.

Manage only jobs whose current owner/route matches this workspace's saved receipt. Read back after edits and pause/resume/removal. Resolve uncertainty by inspecting existing jobs before retrying creation. Do not edit the scheduler's JSON/database directly or enable broader permissions.

Reference: https://docs.openclaw.ai/cli/cron
Reference: https://docs.openclaw.ai/automation/cron-jobs/managing-jobs
