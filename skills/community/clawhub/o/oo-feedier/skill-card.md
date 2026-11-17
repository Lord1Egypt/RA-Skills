## Description:

Use Feedier to read, create, update, and delete reports through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Feedier users can retrieve and manage analytical reports through an already connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI may synchronize changes to installed agent skills during startup.

Mitigation: Review setup before installation, prefer a verified CLI release, and set OO_SKILLS_SYNC_DISABLED=1 for each invocation.

Risk: Feedier requests pass through OOMOL, and report updates, sharing, or deletion can affect account data.

Mitigation: Ensure the data flow is appropriate for the account and review each report change, share-link creation, or deletion before approval.

## Reference(s):

- [Feedier website](https://www.feedier.ai)
- [Feedier API documentation](https://developers.feedier.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Feedier skill release](https://clawhub.ai/oomol/skills/oo-feedier)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [Feedier report data and action results as JSON, with setup and action guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Feedier account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
