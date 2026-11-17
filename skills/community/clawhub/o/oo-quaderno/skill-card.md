## Description:

Quaderno (quaderno.io). Use this skill for ANY Quaderno request — reading, creating, updating, and deleting data. Whenever a task involves Quaderno, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Quaderno through an OOMOL-connected account can use this skill to calculate tax rates and read, create, update, or delete Quaderno contacts and products. It guides the agent to inspect each action's schema and seek approval before writes or deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI may silently install persistent skills across other agents.

Mitigation: Review the CLI setup, use a verified release, and set OO_SKILLS_SYNC_DISABLED=1 before invoking oo to prevent startup skill synchronization.

Risk: Quaderno writes can change account data, and deletions are permanent.

Mitigation: Keep the required user approvals; confirm the exact write payload or deletion target before running the action.

Risk: The exact installer payload and hosted connector implementation are unverified.

Mitigation: Review the CLI setup before installation and use a verified release.

## Reference(s):

- [Quaderno skill on ClawHub](https://clawhub.ai/oomol/skills/oo-quaderno)
- [Quaderno](https://quaderno.io/)
- [Quaderno API documentation](https://developers.quaderno.io/api/)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes action safety labels and setup guidance.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
