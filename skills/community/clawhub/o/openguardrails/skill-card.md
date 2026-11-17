## Description:

MoltGuard helps protect OpenClaw agents and users from prompt injection, data exfiltration, and malicious commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaslwang](https://clawhub.ai/user/thomaslwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, test, configure, update, and remove MoltGuard protection for agent security checks. It focuses on prompt and instruction risk, behavioral risk, data risk, and enterprise Core enrollment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing this third-party plugin can route sensitive agent security data to an external Core service with limited disclosure.

Mitigation: Before installing in environments with confidential prompts, customer data, credentials, or regulated information, confirm the exact plugin version, publisher provenance, Core endpoint, transmitted data, retention and deletion terms, credential handling, and disable or revoke procedures.

Risk: Enterprise enrollment changes which Core endpoint the skill uses.

Mitigation: Use enterprise enrollment only with a Core endpoint that the organization administratively trusts.

## Reference(s):

- [OpenGuardrails MoltGuard homepage](https://github.com/openguardrails/openguardrails/tree/main/moltguard)
- [OpenGuardrails skill page on ClawHub](https://clawhub.ai/thomaslwang/skills/openguardrails)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, test, status, account, configuration, dashboard, enterprise enrollment, update, and uninstall guidance.]

## Skill Version(s):

6.8.20 (source: frontmatter and server release metadata, released 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
