## Description:

Continuously track the web for changes via the Parallel Monitor API. Creates a recurring research task that runs on a cadence and emits events on change, with optional webhook delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[normallygaussian](https://clawhub.ai/user/normallygaussian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create and manage recurring Parallel monitors for topics, pages, filings, pricing, launches, or other signals that should be watched over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring monitors can persist beyond the current session and may send events to configured webhooks.

Mitigation: Confirm the monitoring objective, cadence, and webhook URL before creating or updating a monitor.

Risk: Deleting a monitor stops the recurring observation task.

Mitigation: Confirm the exact monitor_id before deleting a monitor.

Risk: Untrusted monitor text passed through raw shell interpolation can change command behavior.

Mitigation: Pass objectives and schemas as quoted arguments or structured CLI options instead of interpolating raw text.

## Reference(s):

- [Parallel homepage](https://parallel.ai)
- [Parallel API docs](https://docs.parallel.ai)
- [Parallel Monitor API reference](https://docs.parallel.ai/api-reference/monitor)
- [Parallel CLI integration docs](https://docs.parallel.ai/integrations/cli)
- [ClawHub skill page](https://clawhub.ai/normallygaussian/skills/parallel-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include monitor IDs, cadence values, webhook URLs, structured output schemas, event summaries, and CLI error-handling guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
