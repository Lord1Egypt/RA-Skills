## Description:

Memory Scan audits AI agent memory files and workspace configuration for malicious instructions, prompt injection, credential leaks, data exfiltration, guardrail bypass attempts, behavior manipulation, and privilege-escalation content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and security reviewers use this skill to scan AI agent memory files and workspace configuration for malicious content, leaked credentials, injection attempts, and related memory safety issues before trusting or automating those files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads memory and workspace configuration files that may contain sensitive content.

Mitigation: Install only when this file access is acceptable, keep local mode as the default, and avoid running with sudo unless a narrowly scoped administrative review justifies it.

Risk: Remote LLM analysis and callback configuration can transmit or route scan context outside the local workspace.

Mitigation: Review remote LLM and callback settings before use, enable remote analysis only when needed, and confirm that redaction and destination settings match the deployment policy.

Risk: Scheduled monitoring, alerts, and quarantine writes can create operational changes without continuous human attention.

Mitigation: Enable scheduled monitoring only after confirming where alerts go, review findings before quarantine, and keep backups available for restore.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memory-scan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local scans, optional remote LLM analysis, scheduled monitoring, and quarantine or restore actions that require user review.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
