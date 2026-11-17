## Description:

Use this skill for Favro requests involving reading, creating, or updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working in Favro can read cards, organizations, collections, and boards, and create or update cards in their connected workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes an unverified remote CLI installer.

Mitigation: Review and verify the CLI installation separately before allowing setup.

Risk: The CLI can make broader changes to installed agent skills through automatic synchronization.

Mitigation: Disable automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1 before setup.

Risk: The connector acts with the Favro access granted to OOMOL.

Mitigation: Connect only the Favro access you intend OOMOL to hold.

## Reference(s):

- [Favro API documentation](https://favro.com/developer/)
- [Favro homepage](https://www.favro.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-favro)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON Favro action results with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve data; card creation and updates change Favro state and require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
