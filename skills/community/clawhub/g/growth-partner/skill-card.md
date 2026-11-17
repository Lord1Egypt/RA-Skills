## Description:

Growth Partner monitors Feishu messages, group mentions, whitelisted chats, documents, and calendar events to surface work insights, summaries, risk signals, and action recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cscguochang](https://clawhub.ai/user/cscguochang)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace users and operators use this skill to run a recurring Feishu work assistant that summarizes active topics, reconstructs timelines, flags risks, and suggests follow-up actions from approved communications and work records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to repeatedly access private messages, group chats, documents, calendars, and historical records.

Mitigation: Install only with explicit Feishu tenant-owner and monitored-user approval; require per-source consent and disable private-message and historical transcript searches by default.

Risk: The artifact includes hard-coded user and chat identifiers and retains derived insights in memory files.

Mitigation: Replace IDs with deployment-specific configuration and define review and deletion procedures for retained memory files before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cscguochang/skills/growth-partner)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries with timelines, source notes, risk observations, and action recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update retained insight and activity logs when configured.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact changelog, released 2026-04-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
