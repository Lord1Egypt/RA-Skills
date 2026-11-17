# Automation review — OpenClaw 2026.9.4

Use `optimizer.py audit --live --agent YOUR_AGENT --json` to inspect enabled jobs.

For each agent job, confirm effective model, timeout, delivery, failure policy,
and required context. Consider `lightContext` only when the omitted instructions
are not necessary. The linter marks candidates for review, not safe automatic fixes.

Deterministic calculations, API polling, and fixed threshold alerts may use command
jobs with no LLM inference. Commands can still have external API or infrastructure
costs. Keep their secrets in native protected configuration, not in published examples.

The CLI uses the installed native `cron list --all --json` command. If its response
is paginated, the report explicitly notes partial coverage. It never runs or edits jobs.
