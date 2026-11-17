## Description:

This skill should be used when creating commits or pull requests, enforcing a human-written PR structure, intent capture, and evidence in agentic workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joshp123](https://clawhub.ai/user/joshp123)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and coding agents use this skill to create reviewable commits and pull requests with human-written intent, factual change summaries, test evidence, prompt history, and environment metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PR bodies can expose full prompt transcripts and local tool or environment details.

Mitigation: Manually review the complete PR body before publication, omit unrelated or sensitive prompts, and consider disabling terminal or system metadata publication for private, customer, security, or public repositories.

## Reference(s):

- [Commit Workflow](references/workflow-commit.md)
- [PR Workflow](references/workflow-pr.md)
- [Human-Written PR Template](references/pr-human-template.md)
- [Commit Message Format](references/commit-format.md)
- [ClawHub Skill Page](https://clawhub.ai/joshp123/skills/pr-commit-workflow)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with PR and commit templates plus inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include human-supplied PR intent, prompt history, local environment metadata, and factual test evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
