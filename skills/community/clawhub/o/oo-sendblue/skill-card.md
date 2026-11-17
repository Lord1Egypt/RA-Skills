## Description:

Sendblue (sendblue.com). Use this skill for ANY Sendblue request — reading, creating, updating, and deleting data. Whenever a task involves Sendblue, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to read and manage Sendblue contacts through an OOMOL-connected account. Read actions retrieve contact records; write and delete actions change contact data and require user confirmation under the skill's guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded CLI software without separate approval.

Mitigation: Review and approve CLI installation separately, use a verified release where available, and check its automatic skill-installation behavior before running it.

Risk: The connected account gives OOMOL access to Sendblue connection and contact data.

Mitigation: Review whether this data handling is appropriate before connecting Sendblue, and retain the skill's confirmation steps for changes and deletions.

## Reference(s):

- [Sendblue API documentation](https://docs.sendblue.com/)
- [Sendblue homepage](https://www.sendblue.com/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector requests and results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contact data returned by read actions; write and delete effects require confirmation as described by the skill.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
