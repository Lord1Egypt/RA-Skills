## Description:

CoderPad (coderpad.io). Use this skill for ANY CoderPad request — reading, creating, and updating data. Whenever a task involves CoderPad, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Interviewers and developers use it to retrieve CoderPad organization, interview pad, question, statistics, and event data, and to create interview pads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code and automatic skill synchronization may introduce unreviewed changes.

Mitigation: Review the CLI source and approve installation separately at a verified fixed version; inspect and control automatic synchronization before enabling it.

Risk: Connecting CoderPad gives OOMOL credential-backed access to interview and organization data.

Mitigation: Connect an account with appropriate access and retain the required confirmations before making data changes.

## Reference(s):

- [CoderPad](https://coderpad.io)
- [CoderPad API documentation](https://coderpad.io/resources/docs/interview/more-interview-resources/api-documentation/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Shell commands, Guidance]

**Output Format:** [JSON responses and text guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected CoderPad action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
