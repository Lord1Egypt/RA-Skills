## Description:

Review GitHub repositories, group issues and pull requests by urgency, and propose or apply safe triage actions after confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and repository maintainers use this skill to review GitHub issues and pull requests, identify urgent or stale work, draft recommended labels or comments, and perform write actions only after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and globally enable an external ClawLink plugin that handles GitHub OAuth-backed actions without artifact evidence of exact OAuth scopes.

Mitigation: Install only if ClawLink is trusted, review OAuth scopes before connecting GitHub, limit repository access where GitHub permits it, and know how to revoke the grant and remove the plugin.

Risk: GitHub write actions can comment, relabel, assign, create, close, reopen, or edit issue metadata.

Mitigation: Use the skill's read-first workflow, preview intended changes where available, and require explicit user confirmation before any write operation.

Risk: Live ClawLink tool names and schemas may differ from examples in the artifact.

Mitigation: List, search, and describe live GitHub tools in the current turn, then treat the returned schema and guidance as the source of truth.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/github-triage-workflow)
- [GitHub REST API](https://docs.github.com/en/rest)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=github-triage-workflow)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured triage summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub issue and pull request recommendations, draft comments, label proposals, and confirmation-gated tool actions.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
