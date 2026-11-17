## Description:

Autoblogging.ai (autoblogging.ai). Use this skill for ANY Autoblogging.ai request — reading, creating, and updating data. Whenever a task involves Autoblogging.ai, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Autoblogging.ai account can create article generation jobs and retrieve their status or results. The agent uses the oo CLI to inspect action schemas and submit requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the agent to run an installer downloaded from an external URL, and the downloaded installer was not verified.

Mitigation: Review and explicitly approve a verified CLI installation before running it.

Risk: The connected account is used to submit article requests, which may consume account credits or use connected-account access.

Mitigation: Review the account access and approve each article creation request.

## Reference(s):

- [Autoblogging.ai API documentation](https://autoblogging.ai/api-documentation/)
- [Autoblogging.ai](https://autoblogging.ai)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Text]

**Output Format:** [JSON action requests and responses, with article job status or results summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article creation returns a job ID and credit metadata; fetching returns the job status and available result.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
