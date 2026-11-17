## Description:

OpenClaw Diagnostics analyzes OpenClaw agent inference latency, token usage, tool-call statistics, run timelines, Gateway restart history, and errors with summary, full-report, agent-filtered, and advanced follow modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw administrators and developers use this skill to inspect runtime health, performance bottlenecks, token usage, tool-call behavior, errors, and Gateway restart history across one or more agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad cross-agent session, log, token, timing, tool-call, and error details.

Mitigation: Install it only for agents authorized to administer OpenClaw diagnostics, prefer `-a <agent>` for scoped checks, and avoid sharing raw or full reports in shared chats.

Risk: Advanced follow mode changes OpenClaw diagnostics and debug logging configuration and restarts the Gateway.

Mitigation: Use `-f --advanced` only as a planned maintenance operation, confirm the configuration change, and restore the original configuration after diagnosis.

## Reference(s):

- [OpenClaw Diagnostics ClawHub page](https://clawhub.ai/wujiaming88/skills/openclaw-diag)
- [Advanced mode reference](references/advanced-mode.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown and terminal-style diagnostic text, including shell command invocations and summarized or raw report output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw log, session, token, timing, tool-call, error, and agent activity details.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
