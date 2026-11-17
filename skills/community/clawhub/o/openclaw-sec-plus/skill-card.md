## Description:

AI Agent Security Suite - Real-time protection against prompt injection, command injection, SSRF, path traversal, secrets exposure, and content policy violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lockdown56](https://clawhub.ai/user/lockdown56)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use Openclaw Sec to scan prompts, tool calls, shell commands, URLs, file paths, and content for injection, SSRF, traversal, secret exposure, and related risks before an agent proceeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation persistently enables OpenClaw prompt and tool hooks.

Mitigation: Review the hook configuration before installing, use a controlled OpenClaw profile, and disable plugin entries when the controls are not needed.

Risk: Hooks can inspect prompts and tool arguments, block calls, and modify prompt construction.

Mitigation: Test the skill in a non-production profile and review sensitivity, warning, and blocking policies before relying on it in routine agent workflows.

Risk: Scanned prompt and tool content may be retained in a local database without clear redaction.

Mitigation: Use the skill only where local retention is acceptable, avoid scanning unnecessary sensitive content, and plan database cleanup when uninstalling or rotating profiles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lockdown56/skills/openclaw-sec-plus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation results, warnings, block decisions, setup commands, and configuration guidance.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
