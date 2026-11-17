## Description:

Post job listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting and HR users can use this skill to post job listings and automate job posting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish job listings through an API key, but the artifact does not include the referenced job_poster.py implementation or enough destination scoping.

Mitigation: Verify the missing implementation and destination service before installation; require explicit confirmation of the posting target, final listing content, and user authority, and use a narrowly scoped API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-job-poster)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON results with shell command and environment variable configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JOB_API_KEY for the destination job posting service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
