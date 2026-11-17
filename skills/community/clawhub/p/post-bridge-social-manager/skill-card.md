## Description:

Create, schedule, and manage social media posts across Instagram, TikTok, YouTube, X, LinkedIn, Facebook, Pinterest, Threads, and Bluesky via the Post Bridge API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackfriks](https://clawhub.ai/user/jackfriks)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan, draft, publish, schedule, update, delete, and analyze social media posts across connected Post Bridge accounts. It supports CLI/API workflows for media upload, platform-specific configuration, draft review, queue scheduling, analytics, and post-result checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule content to real social media accounts.

Mitigation: Keep confirmation and draft workflows enabled for publishing actions, and prefer draft mode when user intent is unclear.

Risk: The skill uses live Post Bridge API keys and may send media, captions, account IDs, and scheduling metadata to Post Bridge.

Mitigation: Use narrowly scoped or rotated API keys, avoid placing live keys directly in shell commands, and store credentials only in expected configuration locations.

Risk: The primary CLI path uses an unpinned npm package that handles posting credentials and account actions.

Mitigation: Prefer the bundled artifact script or a pinned, audited CLI version before using the skill with production social accounts.

Risk: Optional workflows can run local commands, move files, or create scheduled jobs.

Mitigation: Confirm the exact command, source and destination paths, or crontab entry with the user before performing those actions.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/jackfriks/skills/post-bridge-social-manager)
- [Post Bridge](https://post-bridge.com)
- [Post Bridge API reference](https://api.post-bridge.com/reference)
- [Post Bridge MCP](https://post-bridge.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON payloads, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Post Bridge CLI commands, API request bodies, MCP configuration snippets, captions, schedules, status checks, and analytics summaries.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
