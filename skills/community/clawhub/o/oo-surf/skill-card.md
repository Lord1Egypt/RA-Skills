## Description:

Surf (asksurf.ai). Use this skill for ANY Surf request — reading, creating, updating, and deleting data. Whenever a task involves Surf, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use a Surf-connected account to retrieve market, crypto, equity, news, wallet, and on-chain data, and to conduct research through Surf. The skill guides users through checking an action's schema and running connector actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may introduce broader changes to an agent's installed skills without explaining them.

Mitigation: Review or preinstall a vetted oo CLI version before use. To prevent additional agent-skill installation, set OO_SKILLS_SYNC_DISABLED=1 as described in the oo CLI command reference.

## Reference(s):

- [Surf Data API overview](https://docs.asksurf.ai/data-api/overview)
- [Surf](https://asksurf.ai)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Surf on ClawHub](https://clawhub.ai/oomol/skills/oo-surf)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON data and text summaries, with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Surf action; Surf requests may consume credits.]

## Skill Version(s):

1.0.2 (source: frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
