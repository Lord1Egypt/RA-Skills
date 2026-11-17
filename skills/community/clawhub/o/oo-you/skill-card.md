## Description:

You.com (you.com). Use this skill for ANY You.com request — reading, creating, and updating data. Whenever a task involves You.com, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the skill to search You.com, fetch webpage content, check account balance, and request cited research or finance research through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI may synchronize additional agent skills beyond this setup.

Mitigation: Review the CLI setup and use a verified release; set OO_SKILLS_SYNC_DISABLED=1 for every oo invocation to prevent startup skill synchronization.

Risk: Connected You.com requests may consume credits.

Mitigation: Check the connected account balance and consider credit use before running research or finance research actions.

## Reference(s):

- [You.com API documentation](https://you.com/docs)
- [oo CLI command reference and environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Connector results as JSON, including text answers, citations, fetched webpage content, or account balance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research responses may include citations; fetched content may be HTML, Markdown, or metadata.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
