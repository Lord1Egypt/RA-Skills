## Description:

Helps an agent diagnose OpenClaw model, provider, authentication, rate-limit, timeout, endpoint, and streaming errors and propose or apply configuration-focused fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viratkumar123](https://clawhub.ai/user/viratkumar123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to troubleshoot failing OpenClaw model configurations, identify likely provider or gateway causes, and manage fixes such as provider switches, API key refreshes, retry settings, and endpoint changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect broad OpenClaw configuration and logs that can contain sensitive operational details.

Mitigation: Run it with explicit approval for log and configuration access, and redact secrets in reports, logs, and diffs.

Risk: The skill may change model defaults, switch providers, restart the gateway, or create persistent monitoring without clear approval.

Mitigation: Use read-only diagnosis first, then require confirmation and redacted diffs before configuration changes, restarts, provider switches, memory notes, or heartbeat behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viratkumar123/skills/model-troubleshooter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic summaries, proposed or applied configuration changes, verification steps, and monitoring guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
