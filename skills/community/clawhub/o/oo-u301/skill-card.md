## Description:

Use U301 through an OOMOL-connected account to list short-link domains, create short links, and delete links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other U301 users use this skill to inspect available short-link domains, create short links, and delete links through an OOMOL-connected account. It guides the agent to check each action's input schema and obtain approval before creating or deleting links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup downloads and runs an oo CLI installer whose exact contents were not verified.

Mitigation: Review setup before installing and use a verified CLI release.

Risk: The oo CLI may persistently install or change other agent skills.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if those automatic changes are not wanted.

Risk: Creating or deleting U301 links changes account data.

Mitigation: Keep explicit approval for the exact create or delete action and its target.

## Reference(s):

- [U301 API documentation](https://u301.com/docs/u301-js)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [U301 skill listing](https://clawhub.ai/oomol/skills/oo-u301)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
