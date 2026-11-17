## Description:

Audits a personal Notion space for mixed content, navigation problems, placeholders, and sensitivity boundaries, then proposes an information architecture and migration plan; read-only by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use this skill to review a personal Notion hub and receive an organization plan, including destinations for ambiguous or sensitive content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial, with one unresolved reference, and the skill may be used while reviewing sensitive personal information.

Mitigation: Review the unresolved reference and the skill instructions before use when memory or access-token handling matters; keep the audit read-only and exclude access tokens from reports.

## Reference(s):

- [Notion Personal Space Audit on ClawHub](https://clawhub.ai/haiyangchenbj/skills/notion-personal-space-audit)
- [Audit Dimensions Checklist](references/audit-checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with findings, a proposed information architecture, migration map, phased plan, and access-gap notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; makes no Notion changes without explicit authorization.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
