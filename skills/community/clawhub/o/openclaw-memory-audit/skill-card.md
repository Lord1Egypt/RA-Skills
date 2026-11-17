## Description:

Scans an OpenClaw workspace and memory-related files for leaked API keys, tokens, and sensitive credentials, and checks whether a recurring audit schedule is active.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shingo0620](https://clawhub.ai/user/shingo0620)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to run local, best-effort secret scans of workspace files and verify that a recurring memory security audit routine is in place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads files in the selected local workspace while looking for secret-like patterns.

Mitigation: Run it only against the intended workspace path and review findings locally before taking remediation steps.

Risk: A clean scan is best-effort and may not prove that every memory log or audit schedule is covered.

Mitigation: Verify separately that the relevant memory logs and recurring weekly audit schedule are included.

## Reference(s):

- [OpenClaw Memory Audit on ClawHub](https://clawhub.ai/shingo0620/skills/openclaw-memory-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and local scan findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Best-effort local scan results; no provider credentials required.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
