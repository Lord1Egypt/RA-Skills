## Description:

Whop (whop.com). Use this skill for ANY Whop request — searching and reading data. Whenever a task involves Whop, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an OOMOL-connected Whop account can retrieve Whop account, company, membership, product, and authorized-user data through the oo CLI. The skill guides the agent to check each action's schema and return the resulting data for the user's request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run a remote CLI installer, and its exact local changes were not available for inspection.

Mitigation: Review and install the CLI yourself before enabling the skill, and connect Whop with only the permissions needed for the requested reads.

Risk: Bundled skills may be synchronized into other agents during setup.

Mitigation: Review the oo CLI command reference and set OO_SKILLS_SYNC_DISABLED if you want to disable that synchronization.

## Reference(s):

- [Whop API documentation](https://docs.whop.com/developer/api/getting-started)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Whop data returned as JSON, with text or Markdown summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented data; results depend on the connected account and selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
