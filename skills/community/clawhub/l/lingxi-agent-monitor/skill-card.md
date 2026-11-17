## Description:

Monitor OpenClaw Agent health, uptime, task status, and system metrics, with alerts for failures, performance degradation, and unusual behavior plus memory management, session cleanup, and proactive self-healing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nima54851](https://clawhub.ai/user/nima54851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw agent uptime, active sessions, memory usage, task queues, MCP connectivity, API latency, and error rates. It produces health reports, alert guidance, and recovery actions for maintaining agent availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic cleanup, restarts, provider fallback, and recovery actions can change an agent environment without enough user control or scoping.

Mitigation: Disable self-healing by default, run read-only health checks first, and require confirmation before cleanup, restarts, or provider switching.

Risk: Memory pruning and session cleanup can remove useful working context or records if thresholds are too broad.

Mitigation: Use explicit retention settings, archive summaries before deletion, and review planned cleanup actions before applying them.

Risk: External alert messages can expose secrets, private user content, or sensitive infrastructure details.

Mitigation: Scrub alert payloads, restrict alert channels, and avoid sending raw logs or credentials to notification services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nima54851/skills/lingxi-agent-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown health reports with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include alert thresholds, scheduled health checks, dashboard endpoint guidance, and self-healing recommendations]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
