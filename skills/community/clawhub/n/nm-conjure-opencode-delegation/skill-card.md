## Description:

Delegates to OpenCode (opencode run)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when delegation-core selects OpenCode, especially when they need a provider configured in OpenCode or a local or self-hosted model. It sends the task through `opencode run` and saves the response as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports incomplete evidence for the associated workflow because two local path references could not be resolved.

Mitigation: Resolve and review those references before relying on the associated workflow.

## Reference(s):

- [Conjure plugin homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)

## Skill Output:

**Output Type(s):** [Markdown, Text, Code]

**Output Format:** [OpenCode response saved as a timestamped Markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contents depend on the delegated prompt and OpenCode's configured provider and model.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
