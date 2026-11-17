## Description:

国泰海通证券-灵犀自选股管理 helps an agent query quotes for the user's "My Watchlist" group and add or remove stocks by code or name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtht-tech](https://clawhub.ai/user/gtht-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to authenticate with Lingxi services, review quotes for the "My Watchlist" group, and add or remove stocks after required confirmation for deletion. The current version is limited to the "My Watchlist" group and does not provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a reusable API key in a shared local JSON file.

Mitigation: Install and run it only on trusted machines, restrict access to the shared credential file, and rotate or revoke the API key if the environment is shared or suspected to be compromised.

Risk: The skill can make authenticated changes to the user's "My Watchlist" stock list.

Mitigation: Review stock names and codes before add or remove operations, and require explicit confirmation before any deletion.

Risk: Authorization binding collects device information and contacts GTJA/GTHHT gateway services.

Mitigation: Use the skill only when the user accepts the publisher's authorization flow and device-binding behavior, and avoid use in untrusted local environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gtht-tech/skills/lingxi-watchlist-skill)
- [Publisher Profile](https://clawhub.ai/user/gtht-tech)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown tables, command snippets, and plain text status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorization; deletion operations require explicit user confirmation before execution.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
