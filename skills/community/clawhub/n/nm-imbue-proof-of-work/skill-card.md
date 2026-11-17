## Description:

Enforces validation and evidence before claiming work complete; use it before declaring implementation done, creating a PR, or submitting deliverables for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to require reproducible validation evidence, edge-case checks, and explicit acceptance criteria before recommending a solution or reporting work complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the skill suspicious because it reports actions outside its stated validation purpose, including global package installation and commands that can change Git history; the verdict does not establish malicious intent.

Mitigation: Consider avoiding installation unless the publisher clarifies or removes the reported actions, pins dependencies, and adds safeguards for global installs and sensitive evidence.

Risk: The security scan is incomplete: 11 of 12 components were fully inspected, one was partly inspected, and a referenced quality-gates document was missing.

Mitigation: Review the partially inspected component and missing referenced material before relying on the scan as complete.

## Reference(s):

- [Related project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-imbue-proof-of-work)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Analysis]

**Output Format:** [Markdown with reproducible validation steps, command output snippets, and evidence citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include acceptance criteria, validation checklists, and evidence logs.]

## Skill Version(s):

1.10.3 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
