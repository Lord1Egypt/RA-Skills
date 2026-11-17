## Description:

Use this skill to search and read data from Jungle Scout (junglescout.com).

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can search Jungle Scout's Amazon product database and retrieve keyword, search-volume, sales-estimate, and share-of-voice data through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs remote installer code that was unavailable for inspection.

Mitigation: Install a verified oo CLI release yourself before enabling the skill, and review and approve any later installation changes.

Risk: Startup skill synchronization can make broader changes to agent skills without a clear explanation.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 as documented by upstream to prevent startup skill synchronization.

## Reference(s):

- [Jungle Scout](https://www.junglescout.com/)
- [Jungle Scout API documentation](https://developer.junglescout.com/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON data with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Jungle Scout account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
