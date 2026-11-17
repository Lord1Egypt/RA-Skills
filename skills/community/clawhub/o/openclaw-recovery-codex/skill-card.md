## Description:

OpenClaw Gateway recovery and infrastructure diagnostics for Codex agents when Gateway access, messaging channels, scheduled tasks, webhook pipelines, or status checks fail across Windows, macOS, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shunsukehayashi](https://clawhub.ai/user/shunsukehayashi)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to diagnose OpenClaw Gateway, messaging channel, scheduled task, webhook, configuration, security audit, and memory search issues. The agent discovers the local environment, checks service and port status, matches findings to known failure patterns, and reports recommended recovery actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill labels some configuration-changing repair commands as safe read-only actions, including openclaw doctor --fix and a BOM-removal Node snippet.

Mitigation: Require explicit human approval, a backup, and path verification before running commands that can modify OpenClaw configuration.

Risk: Diagnostics may expose local OpenClaw state paths, service status, port usage, security audit counts, and Tailscale status in agent output.

Mitigation: Review reports before sharing them outside the trusted operations context and redact local paths, ports, or network details when they are not needed.

## Reference(s):

- [Common OpenClaw Failures & Recovery Patterns](references/common-failures.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown report with inline shell commands and action-required recovery guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports detected OS, state directory, config path, Gateway reachability, channel status, agent count, security count, findings, evidence excerpts, and human-run recovery commands when needed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
