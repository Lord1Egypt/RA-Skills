## Description:

OpenClaw安全审计与防护 helps agents log sensitive operations, generate audit reports, analyze risky operation chains, enforce two-stage confirmations, scan external content, and check skill integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangdongmingisok](https://clawhub.ai/user/yangdongmingisok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add audit logging, daily or weekly audit reporting, high-risk operation confirmation, content and URL checks, rate monitoring, operation-chain analysis, and skill integrity checks to OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded Feishu credentials can be exposed or reused if the skill is installed as-is.

Mitigation: Remove the embedded secret, rotate the Feishu credential, and load deployment-owned credentials from secure configuration before use.

Risk: Sensitive audit details may be sent to a fixed external recipient without deployment-specific control.

Mitigation: Replace recipient IDs with deployment-owned configuration, disable external alerts by default, and redact sensitive audit details before sending notifications.

Risk: Confirmation replies may be ambiguous if they are not bound to the exact high-risk request.

Mitigation: Bind each confirmation to an exact per-request nonce and reject stale, ambiguous, or mismatched replies.

Risk: URL scanning can reach unsafe or unintended destinations.

Mitigation: Restrict URL scanning to safe allowed destinations controlled by the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangdongmingisok/skills/openclaw-audit-log)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON/JSONL audit records, shell command snippets, Python usage snippets, and plain-text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local audit state and send Feishu notifications when deployment-controlled credentials and recipients are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
