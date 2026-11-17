## Description:

Use Slite through a connected account to search, read, create, update, and delete notes and groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with Slite use this skill to find and manage notes and groups through their connected Slite account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded code, and the remote installer and runtime were not verified in this review; setup may also make broader agent changes.

Mitigation: Review and approve CLI installation separately, use a verified release, and disable automatic skill synchronization if Slite access is all you need.

Risk: Creating, updating, or deleting notes can change Slite data.

Mitigation: Follow the documented approval requirements for writes and deletions, confirming the exact action and target before execution.

## Reference(s):

- [Slite homepage](https://slite.com)
- [Slite API documentation](https://developers.slite.com/docs/getting-started)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-slite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Structured data]

**Output Format:** [Retrieved Slite content and action results; note bodies may be returned in Markdown, HTML, or SliteML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Note content format depends on the requested Slite response format.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
