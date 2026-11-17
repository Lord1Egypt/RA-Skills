## Description:

Headout (headout.com). Use this skill for ANY Headout request — searching and reading data. Whenever a task involves Headout, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to search and read Headout information through their connected account, including cities, products, categories, inventory, and bookings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can make broader, persistent changes to agent skills during startup synchronization.

Mitigation: Review CLI installation and agent-skill changes, use a reviewed fixed CLI release, and set OO_SKILLS_SYNC_DISABLED=1 before invoking oo when startup synchronization is not wanted.

Risk: Remote installers, binaries, and hosted connector behavior were not verified.

Mitigation: Review the remote components and approve installation separately before enabling the skill.

Risk: The connected Headout account determines which account data the skill can access.

Mitigation: Connect only the Headout account needed for the task.

## Reference(s):

- [Headout](https://www.headout.com)
- [Headout API documentation](https://developers.headout.com/docs/api/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector results with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response fields depend on the selected Headout action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
