## Description:

Search and read Keyword.com account, project, keyword, ranking, and region data through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Keyword.com users use this skill to inspect their profile, projects, tracked keywords and rankings, and project regions through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic software installation and automatic changes to other agent skills warrant review.

Mitigation: Review and install a verified oo CLI release; set OO_SKILLS_SYNC_DISABLED=1 before invoking it when only Keyword.com access is needed.

Risk: The connected account access is entrusted to OOMOL, and the live installer contents remain unverified.

Mitigation: Consider the account access granted to OOMOL and verify the CLI release before installation.

## Reference(s):

- [Keyword.com SERP API documentation](https://keyword.com/docs/serp-api)
- [Keyword.com](https://keyword.com)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Keyword.com ClawHub release](https://clawhub.ai/oomol/skills/oo-keyword)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses with concise guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account, project, keyword, ranking, and region data; requires the oo CLI and a connected Keyword.com account.]

## Skill Version(s):

1.0.6 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
