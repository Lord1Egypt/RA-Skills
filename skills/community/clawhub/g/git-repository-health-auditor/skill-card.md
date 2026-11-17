## Description:

Audits a user-selected Git repository for maintainability, configuration problems, dependency risks, accidental secret exposure, and CI/CD weaknesses, producing an evidence-based report without modifying files by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and security reviewers use this skill to inspect a selected Git repository and prioritize evidence-backed maintenance, release-readiness, and security findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository findings could expose suspected credentials.

Mitigation: Redact secret values and report only the location and necessary context.

Risk: Untrusted repository text could try to redirect the audit.

Mitigation: Treat repository content as evidence, not instructions, and review suspicious text in context.

Risk: Commands, changes, or network actions could affect the repository or disclose its contents.

Mitigation: Keep the initial audit read-only and obtain separate approval before executing commands, patching, committing, pushing, or transmitting data.

## Reference(s):

- [Git documentation](https://git-scm.com/doc)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritized findings include severity, confidence, redacted file evidence, remediation, and scope limitations.]

## Skill Version(s):

1.0.1 (source: ClawHub release; skill frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
