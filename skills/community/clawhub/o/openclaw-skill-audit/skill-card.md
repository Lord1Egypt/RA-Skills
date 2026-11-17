## Description:

Security scanner for OpenClaw skills that analyzes skill folders and .skill files for prompt injection, data exfiltration, malicious scripts, suspicious network connections, dangerous code patterns, and unauthorized access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[produktentdecker](https://clawhub.ai/user/produktentdecker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan OpenClaw skill folders or packaged .skill files before installation, during audits, or when assessing whether a skill appears safe to use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning untrusted .skill archives may expose the local machine to archive-handling risk.

Mitigation: Run scans in a sandbox or low-privilege account, especially for skills from unknown sources.

Risk: The documented critical-risk workflow can delete a skill folder when the user confirms removal.

Mitigation: Confirm that the resolved target path is inside an approved skills directory before allowing any recursive deletion command.

Risk: Static analysis can miss logic-level attacks, stronger obfuscation, or runtime-only behavior.

Mitigation: Use scanner results as a review aid and perform manual review for high-stakes deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/produktentdecker/skills/openclaw-skill-audit)
- [Source code](https://github.com/ProduktEntdecker/skill-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and optional JSON scan reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static-analysis findings are advisory and should be reviewed before acting on deletion or installation guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
