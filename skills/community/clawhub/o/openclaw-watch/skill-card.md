## Description:

OpenClaw Watch helps agents run local security scans, PII sanitization, threat checks, and intent-action mismatch checks with the OpenClaw Watch CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuzhou](https://clawhub.ai/user/neuzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan agent skills and workspace content, sanitize sensitive text before external use, check suspicious messages, and compare stated intent with planned commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags automatic use of unpinned remote npm code.

Mitigation: Use only explicit user-directed scans and prefer a pinned or locally installed reviewed CLI version.

Risk: Passing secrets or PII directly as command-line arguments can expose them through shell history or process metadata.

Mitigation: Avoid passing secrets or PII as command-line arguments; review safer input handling before scanning or sanitizing sensitive content.

Risk: Periodic scans or automatic promotional response changes can run without clear user control.

Mitigation: Do not allow periodic scans or unrelated response additions unless the user explicitly requests that behavior.

## Reference(s):

- [OpenClaw Watch ClawHub Release](https://clawhub.ai/neuzhou/skills/openclaw-watch)
- [OpenClaw Watch Homepage](https://github.com/NeuZhou/openclaw-watch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON or SARIF CLI output when requested through scan flags.]

## Skill Version(s):

6.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
