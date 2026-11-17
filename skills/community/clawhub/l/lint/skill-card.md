## Description:

Lint records developer code-quality activity in local log files and provides commands to review, search, export, and summarize that history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Lint to keep a timestamped local record of code review, linting, formatting, diff, fix, and report activity, then review, search, or export that history. It is best suited for local activity tracking rather than as a primary code analyzer or auto-fix engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is labeled as a linting tool but primarily records user-provided developer text in local logs.

Mitigation: Use it for local activity tracking only, and use a real linter or analyzer for code checks and auto-fixes.

Risk: Local logs and exports can contain secrets, proprietary code snippets, or sensitive review notes.

Mitigation: Do not record sensitive data, and review, protect, or delete files under ~/.local/share/lint before sharing or reuse.

Risk: Exported CSV, JSON, or TXT files may contain untrusted content from another person.

Mitigation: Treat exports as untrusted input and inspect them before importing, executing, or sharing downstream.

## Reference(s):

- [ClawHub Lint Skill](https://clawhub.ai/xueyetianya/skills/lint)
- [Publisher Profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Terminal text and local JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores logs and exports under ~/.local/share/lint]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata; artifact reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
