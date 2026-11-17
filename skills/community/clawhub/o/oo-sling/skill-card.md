## Description:

Use Sling through an OOMOL-connected account to search and read shifts, tasks, users, groups, and calendar events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Sling users use the skill to retrieve shift and session details, look up tasks, users, groups, and coworkers, and read calendar events for their connected organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded CLI code without separate approval, and the remote installer payload remains unverified.

Mitigation: Review and approve CLI installation separately, preferably using a verified, fixed release.

Risk: The CLI can make broader changes to installed agent skills through automatic synchronization.

Mitigation: Before setup, consider disabling synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Requests are made through the connected Sling account and OOMOL processes them.

Mitigation: Connect only the intended Sling account and accept OOMOL's role in processing requests.

## Reference(s):

- [Sling](https://getsling.com)
- [Sling API documentation](https://api.getsling.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Sling data returned as JSON, with information and summaries presented as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the connected Sling account, organization, and requested action.]

## Skill Version(s):

1.0.4 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
