## Description:

Helps agents read and manage Google Business Profile listings, reviews, photos, posts, verification status, and performance insights through Maton-managed access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maton](https://clawhub.ai/user/maton)

### License/Terms of Use:

MIT-0

## Use Case:

Business owners and teams use this skill to audit listings, review customer feedback, update public business information, and inspect engagement metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect edits or deletions can change public business listings, posts, photos, and review replies.

Mitigation: Start with read/list calls; confirm the exact location and proposed change with the user before every write or deletion.

Risk: Hosted functions and triggers can continue acting on a connected account after the initial task.

Mitigation: Require separate approval for automation and review or delete unused functions, triggers, and destinations.

Risk: Raw API keys and business or customer data may be exposed when using direct API access or sharing responses.

Mitigation: Prefer the authenticated CLI; use raw API keys only when necessary and share only the response fields needed for the task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/maton/skills/google-business-profile)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Google Business Profile API overview](https://developers.google.com/my-business/ref_overview)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
