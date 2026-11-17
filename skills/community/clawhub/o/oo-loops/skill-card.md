## Description:

Use this skill to read, create, update, and delete Loops data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage Loops contacts, contact properties, mailing lists, and events through an agent. The skill requires confirmation for writes and explicit approval for deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes downloaded code that has not been verified, and the remote installers and hosted connector implementation were not verified.

Mitigation: Review CLI installation separately and prefer a pinned, verified release. Check bundled-skill synchronization settings and the OOMOL account and Loops permissions being authorized; retain exact-payload confirmation for writes and explicit approval for deletions.

## Reference(s):

- [Loops](https://loops.so)
- [Loops API Reference](https://loops.so/docs/api-reference/intro)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Loops skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-loops)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON connector responses presented as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
