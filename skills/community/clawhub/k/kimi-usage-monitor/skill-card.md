## Description:

Monitor Kimi K2.5 API usage and quota from the Kimi console so agents can check remaining usage, reset timers, rate-limit status, and usage patterns for resource planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xd4o](https://clawhub.ai/user/xd4o)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to inspect Kimi K2.5 usage and quota state before starting intensive tasks, spawning subagents, or planning work around reset windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read authenticated browser tab snapshots while checking the Kimi console.

Mitigation: Use it only with a Chrome context you are comfortable exposing to OpenClaw, and keep unrelated sensitive tabs out of that browser context.

Risk: The subagent guard allows spawning when its usage check fails.

Mitigation: Treat the guard as advisory unless the fail-open behavior is changed, and manually review quota before high-cost tasks when checks fail.

Risk: Scheduled monitoring may create usage logs before storage and retention expectations are clear.

Mitigation: Avoid cron or background monitoring until logging location, retention, and access expectations are defined.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xd4o/skills/kimi-usage-monitor)
- [Kimi console](https://www.kimi.com/code/console)
- [Kimi console membership view](https://www.kimi.com/code/console?from=membership)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Console text and JSON with usage percentages, reset timing, rate-limit status, and capacity guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated Kimi console session in Chrome with OpenClaw browser control enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
