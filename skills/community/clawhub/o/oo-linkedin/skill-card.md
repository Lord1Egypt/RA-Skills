## Description:

Use LinkedIn to retrieve the connected member profile and create, reshare, or delete posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to retrieve their connected LinkedIn member profile and manage posts by creating, resharing, or deleting them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup runs remote installer scripts, and their behavior was not verified.

Mitigation: Review and approve CLI installation separately, use a verified fixed release, and disable unwanted skill synchronization.

Risk: LinkedIn actions can create or delete posts, while OOMOL mediates account access.

Mitigation: Grant only the permissions needed and retain confirmation of the exact effect before posting or deleting.

## Reference(s):

- [LinkedIn API documentation](https://learn.microsoft.com/en-us/linkedin/shared/api-guide/concepts)
- [LinkedIn](https://www.linkedin.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON action results with profile or post data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and connected LinkedIn account.]

## Skill Version(s):

1.0.6 (source: artifact frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
