## Description:

Social Fetch (socialfetch.dev). Use this skill for ANY Social Fetch request — searching and reading data. Whenever a task involves Social Fetch, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use Social Fetch through an OOMOL-connected account to retrieve the connected account and credit balance, or look up public social profiles and channels. The skill guides the agent to inspect each action's schema before sending a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified remote installer code and may change installed agent skills.

Mitigation: Review and approve CLI installation separately; prefer a pinned, integrity-verified installer and decide whether bundled skill syncing is allowed.

## Reference(s):

- [Social Fetch API documentation](https://www.socialfetch.dev/docs)
- [Social Fetch homepage](https://www.socialfetch.dev)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON connector responses, natural-language summaries, and Markdown guidance with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account, balance, and public-profile lookups; results depend on Social Fetch availability, connected-account access, and credits.]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
