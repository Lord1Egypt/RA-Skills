## Description:

Guides agents to read Feishu IM chat history, thread replies, searchable messages, and downloadable message resources using the user's Feishu permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenfa188](https://clawhub.ai/user/chenfa188)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with Feishu access use this skill to help an agent retrieve permitted chat history, expand thread replies, search messages by filters such as keyword, sender, chat, or time range, and fetch message attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive Feishu chat history, thread replies, search results, and attachments available to the user.

Mitigation: Limit requests by chat, sender, keyword, and time range, and fetch only attachments explicitly needed for the task.

Risk: Broad or underspecified searches can return more accessible conversation content than intended.

Mitigation: Ask the agent to narrow searches before execution and review returned messages before using or sharing their contents.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Markdown guidance with JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls operate under the user's existing Feishu authorization and accessible conversations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
