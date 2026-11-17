## Description:

Audits OpenClaw configuration against 12 production primitives and 8 common setup footguns, returning a severity-ranked assessment with specific fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnpetros](https://clawhub.ai/user/shawnpetros)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill after setup, major configuration changes, migration, or periodic checks to audit OpenClaw installations for operational gaps, credential handling issues, stale session state, and channel leak risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to inspect sensitive local OpenClaw secrets, auth, session, and workspace files more broadly than necessary.

Mitigation: Require redaction and field-only extraction; do not allow secret values or full session contents into the report.

Risk: The audit may suggest deleting or archiving session and thread-binding state as part of remediation.

Mitigation: Manually review any suggested deletions or archival actions before applying them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown structured by severity with score and prioritized fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-ranked findings with critical, warning, and info sections plus an overall 0/20 score.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
