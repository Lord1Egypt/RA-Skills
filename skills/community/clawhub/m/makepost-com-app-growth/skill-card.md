## Description:

Manage social media across 9 platforms by drafting captions, hashtags, post ideas, and AI images, then scheduling, publishing, automating recurring posts, and triggering webhooks through MakePost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makepost](https://clawhub.ai/user/makepost)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to manage MakePost-connected social accounts from an agent, including drafting content, uploading media, publishing or scheduling posts, setting recurring posting plans, and managing webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, schedule, reschedule, cancel, or delete live social media content through connected MakePost accounts.

Mitigation: Use a limited API key where available, test with non-production accounts first, and require explicit confirmation before publish, delete, cancel, or bulk actions.

Risk: Recurring posting plans and webhooks can create persistent automation that continues after the initial agent conversation.

Mitigation: Review plan schedules, target accounts, webhook URLs, subscribed events, and pause or remove automation that is no longer intended.

Risk: The MCP configuration runs an unpinned npx package while passing the MakePost API key to the remote MCP endpoint.

Mitigation: Prefer a pinned or locally verified mcp-remote runtime and keep MAKEPOST_API_KEY scoped, rotated, and stored only in the agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/makepost/skills/makepost-com-app-growth)
- [MakePost OpenClaw integration guide](https://makepost.com/openclaw)
- [MakePost MCP documentation](https://makepost.com/mcp)
- [MakePost API documentation](https://api.makepost.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown, plain text, JSON-like tool results, and shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MakePost API key and npx-based MCP remote connection.]

## Skill Version(s):

1.0.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
