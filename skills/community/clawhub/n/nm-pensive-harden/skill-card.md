## Description:

Applies NIST/CWE security hardening to Python and Rust code

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to audit Python and Rust repositories for security weaknesses and produce citation-backed findings with concrete remediation proposals for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial, and some referenced paths could not be resolved, so the available review does not cover everything the skill refers to.

Mitigation: Resolve and review the referenced paths before relying on the findings as a complete assessment.

Risk: Security details could be exposed through pull requests or issues, and dependency metadata could be sent to external services.

Mitigation: Review and redact sensitive details before posting findings; check external-service destinations before submitting dependency metadata.

Risk: The skill is marked suspicious with medium confidence because scanners report possible disclosure risks and concerns about whether its guidance matches its hardening purpose.

Mitigation: Review the skill's guidance and proposed changes before execution or adoption.

## Reference(s):

- [Skill release on ClawHub](https://clawhub.ai/athola/skills/nm-pensive-harden)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Configuration instructions, Shell commands]

**Output Format:** [Markdown security report with findings and proposed code or configuration changes, including shell commands where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repository-specific results; proposed changes are presented for user approval before application.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
