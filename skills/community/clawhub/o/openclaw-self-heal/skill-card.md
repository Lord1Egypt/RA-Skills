## Description:

Autonomously diagnoses and resolves OpenClaw system issues affecting the UI, messaging channels, gateway, memory/plugins, pairing, sessions, and heartbeat behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbauman-26](https://clawhub.ai/user/jbauman-26)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to triage local OpenClaw failures, apply safe recovery actions such as restarts and cache/config reloads, verify service health, and escalate only when data loss, credentials, or repeated failures require human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may restart OpenClaw services or stop processes while diagnosing gateway and UI failures.

Mitigation: Install only where the agent is authorized to perform OpenClaw recovery actions, and require human confirmation before broad process termination or other disruptive actions.

Risk: The skill may inspect local OpenClaw configuration, session, and log files during troubleshooting.

Mitigation: Run it only in environments where the agent is permitted to view those files, and avoid exposing credentials, tokens, or private session contents in reports.

Risk: Pairing approvals and credential-related fixes can affect access control.

Mitigation: Require explicit human validation for pairing approvals, credential resets, token rotation, or significant configuration changes.

## Reference(s):

- [OpenClaw Diagnostics](references/diagnostics.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status summaries, recovery steps, verification results, escalation notes, and action logs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
