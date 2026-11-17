## Description:

Use an OOMOL-connected Greenhouse account to retrieve jobs, candidates, and applications or add candidate notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams can use the skill to inspect Greenhouse jobs, candidates, and applications, and to add candidate activity notes through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unverified software or make broader agent changes without clear approval.

Mitigation: Install a verified CLI release separately and require approval before automatic setup; consider disabling startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Recruiting data is processed through the OOMOL-connected service.

Mitigation: Confirm that OOMOL may process the relevant recruiting data and retain approval requirements for changes to Greenhouse records.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Greenhouse Harvest API documentation](https://developers.greenhouse.io/harvest.html)

## Skill Output:

**Output Type(s):** [API responses, Guidance]

**Output Format:** [JSON connector requests and responses with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that add candidate notes change Greenhouse data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
