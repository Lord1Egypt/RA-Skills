## Description:

Authorization gatekeeper for OpenClaw agents with scoped grants, time-bound permissions, skill scanning, prompt injection detection, and audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanfiguera](https://clawhub.ai/user/juanfiguera)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to gate agent actions through scoped approvals, scan skills before installation, detect prompt injection, and review audit trails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on prompt-level enforcement and may not provide a hard security boundary on its own.

Mitigation: Review before installation for high-assurance use and pair it with OpenClaw or platform-level enforcement where available.

Risk: Audit logging can retain sensitive user, file, or action context.

Mitigation: Configure audit storage with redaction, restricted file permissions, retention limits, and protected export handling.

Risk: The README uses an unpinned npx @latest installation command.

Mitigation: Pin installer versions and verify release hashes before installing in managed environments.

## Reference(s):

- [Jean-Claw Van Damme ClawHub Release](https://clawhub.ai/juanfiguera/skills/jean-claw-van-damme)
- [APOA Framework](https://agenticpoa.com)
- [APOA SDK](https://github.com/agenticpoa/apoa)
- [ClawHavoc Incident Background](https://snyk.io/blog/clawhub-malicious-google-skill-openclaw-malware/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce security scan reports, authorization decisions, audit summaries, and policy guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
