## Description:

Guides agents to write and review idiomatic Go source and API documentation comments that follow Go doc-comment conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rroy233](https://clawhub.ai/user/rroy233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add, correct, and audit comments in Go projects, especially documentation for exported declarations. It helps keep comments accurate, consistent with the surrounding language, and compatible with Go documentation tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested edits may misstate Go code behavior or change source comments unexpectedly.

Mitigation: Review proposed comment changes against the code before accepting them.

Risk: User-scoped installation makes the skill available across projects.

Mitigation: Install it project-scoped when it is only needed for one repository.

## Reference(s):

- [Go Doc Comments source repository](https://github.com/rroy233/go-doc-comments-skill)
- [Go Doc Comments ClawHub release](https://clawhub.ai/rroy233/skills/go-doc-comments-skill)
- [Go Doc Comments syntax reference](references/doc-comment-syntax.md)
- [Go Doc Comments documentation](https://go.dev/doc/comment)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Go source comments and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the existing comment language and Go documentation syntax.]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
