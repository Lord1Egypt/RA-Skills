## Description:

Search and read SmartRecruiters data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams and agents use this skill to search jobs and candidates and retrieve individual job or candidate records through a connected SmartRecruiters account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unchecked remote installers and introduce broader agent changes without clear user control.

Mitigation: Use a reviewed, pinned oo CLI release; require approval for software installation or changes to other agent skills; consider disabling automatic skill synchronization.

Risk: OOMOL mediates access to recruitment data, while the hosted connector implementation was not verified.

Mitigation: Review the setup and data access implications before connecting the account.

## Reference(s):

- [SmartRecruiters API documentation](https://developers.smartrecruiters.com/)
- [SmartRecruiters](https://www.smartrecruiters.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON data, Text]

**Output Format:** [JSON connector responses with agent-readable summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only job and candidate search and retrieval; searches may be paginated.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
