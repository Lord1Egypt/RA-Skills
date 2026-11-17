## Description:

Schedule and manage social media posts across multiple social platforms, query analytics, manage the queue, and publish immediately via natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[col000r](https://clawhub.ai/user/col000r)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate a PostThatLater account for scheduling, editing, deleting, publishing, and reviewing social media posts and analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent authority to schedule, edit, delete, and publish posts through a PostThatLater account.

Mitigation: Install only for intended account management use, keep PTL_API_KEY scoped to the intended account, and review actions before scheduling, editing, deleting, or publishing.

Risk: Immediate publishing is irreversible once the publish-now endpoint is used.

Mitigation: Require explicit user confirmation before publishing immediately.

Risk: Image URLs supplied to the API are sent to PostThatLater for storage and processing.

Mitigation: Provide only image URLs that the user is comfortable sending to PostThatLater.

Risk: Incorrect account IDs, platform limits, or timezone conversion can send the wrong content or schedule it at the wrong time.

Mitigation: Fetch accounts and live platform capabilities before posting, ask for timezone once per session, and convert scheduled times to UTC.

## Reference(s):

- [PostThatLater homepage](https://postthatlater.com)
- [PostThatLater ClawHub skill listing](https://clawhub.ai/col000r/skills/postthatlater)
- [Publisher profile](https://clawhub.ai/user/col000r)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text]

**Output Format:** [Markdown guidance with curl examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PTL_API_KEY and a PostThatLater subscription; agents should fetch account IDs and platform limits before posting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
