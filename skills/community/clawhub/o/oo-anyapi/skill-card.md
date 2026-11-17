## Description:

AnyAPI (getanyapi.com). Use this skill for ANY AnyAPI request — reading, creating, and updating data. Whenever a task involves AnyAPI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read, create, and update data through AnyAPI from an OOMOL-connected account. It guides the agent to inspect each action's current schema before sending a request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs downloaded code that has not been verified and may add skills to other agents.

Mitigation: Review and approve the CLI installation separately, use a reviewed version-specific installation with integrity verification, and inspect skills it adds before allowing automatic setup.

Risk: Requests may send account or business information through OOMOL and AnyAPI, and some requests are paid or change data.

Mitigation: Send only necessary information, account for paid requests, and retain confirmation requirements for write actions.

## Reference(s):

- [AnyAPI](https://getanyapi.com)
- [AnyAPI documentation](https://getanyapi.com/docs)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured JSON results summarized in text, with shell commands for CLI actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on each action's live schema; some requests are paid, and write actions require confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
