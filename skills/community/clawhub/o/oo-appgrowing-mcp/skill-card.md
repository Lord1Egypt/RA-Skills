## Description:

This skill guides agents in using AppGrowing Global MCP through an OOMOL-connected account for advertising creative, app, publisher, and developer research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use the skill to search global advertising creatives, retrieve creative analysis, compare selling-point trends, and inspect available AppGrowing research tools. It also provides setup guidance and approval rules for account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs users to a remote installer without a separate approval checkpoint.

Mitigation: Install a verified CLI release yourself and review its automatic skill installation and synchronization behavior.

Risk: Some connector actions can change or remove account data, and business queries may consume credits.

Mitigation: Follow the documented confirmation rules for write or destructive actions, and check credit costs before business queries.

## Reference(s):

- [AppGrowing Global MCP](https://appgrowing.net/)
- [AppGrowing MCP installation documentation](https://docs.appgrowing.net/mcp/installation/)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API responses, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on live connector schemas and account access.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
