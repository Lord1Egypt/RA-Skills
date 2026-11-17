## Description:

Schedule a social media post for a future time through PostLake, and list, reschedule, or cancel scheduled posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[postlake](https://clawhub.ai/user/postlake)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent schedule, list, reschedule, edit, or cancel PostLake social media posts for a planned publishing calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can prepare API requests that schedule, edit, or cancel social media posts.

Mitigation: Review the generated text, target profile or account, scheduled time, and cancellation target before sending POST, PATCH, or DELETE requests.

Risk: A local-time conversion error could schedule a post for the wrong time.

Mitigation: Confirm the user's local time and timezone in human-readable form, then send an ISO 8601 scheduledAt value in UTC or with an explicit offset.

## Reference(s):

- [PostLake schedule on ClawHub](https://clawhub.ai/postlake/skills/postlake-schedule)
- [PostLake API base URL](https://api.postlake.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses POSTLAKE_API_KEY for authenticated PostLake API requests.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
