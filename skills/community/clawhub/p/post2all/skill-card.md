## Description:

Create, validate, draft, schedule, publish, update, cancel, and manage platform-specific social posts across connected post2all accounts. Use when the user wants OpenClaw to publish to multiple social networks, adapt copy per platform, handle images or video, or maintain a review-first social workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[post2all](https://clawhub.ai/user/post2all)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users can prepare and manage social posts across their connected accounts through post2all. They can adapt content by platform, attach media, and keep work in drafts for review before scheduling or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attached local media is uploaded to post2all even when the related post remains a draft.

Mitigation: Use only files and content authorized for sharing with post2all, and keep the draft-first workflow for review before publication.

Risk: Scheduling and publishing can expose content publicly, while cancellation and deletion affect existing posts.

Mitigation: Verify accounts and current platform settings, obtain approval before scheduling or publishing, and inspect the exact post and target before destructive actions.

Risk: The external CLI and remote post2all service were not audited in the bundled-file review.

Mitigation: Keep credentials out of chat, prompts, committed files, and logs; use the documented local prompt or OAuth flow.

## Reference(s):

- [Setup and authentication](references/setup.md)
- [Publishing boundaries and safety](references/safety.md)
- [Example workflows](references/workflows.md)
- [post2all for OpenClaw](https://www.post2all.com/openclaw)
- [post2all MCP documentation](https://www.post2all.com/docs/mcp)
- [Account connections API](https://www.post2all.com/docs/api-reference/account-connections)
- [Webhooks documentation](https://www.post2all.com/docs/webhooks)
- [API reference](https://www.post2all.com/docs/api-reference)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions]

**Output Format:** [Social post drafts and platform-specific variants, with CLI/API commands and JSON request or response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include uploaded media and destination-specific settings; drafts are the default delivery mode.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
