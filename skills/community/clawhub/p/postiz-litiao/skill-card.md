## Description:

Postiz is a tool to schedule social media and chat posts to 28+ channels including X, LinkedIn, Reddit, Instagram, Facebook Page, Threads, YouTube, Google My Business, TikTok, Pinterest, Discord, Slack, Mastodon, Bluesky, Telegram, WordPress, and ListMonk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, social media operators, and AI agents use this skill to configure and run the Postiz CLI for scheduling posts, uploading media, discovering integration settings, resolving missing platform IDs, and reviewing analytics across connected social channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a Postiz CLI installation that the security evidence describes as unaudited, including global install examples.

Mitigation: Use a pinned and trusted Postiz CLI version, prefer non-global installation where practical, and review the resolved package before running commands.

Risk: Postiz commands require an API key and the evidence flags weak API-key handling guidance.

Mitigation: Store POSTIZ_API_KEY in a secret manager or short-lived environment, avoid shell startup files and terminal output, and use a narrowly scoped key.

Risk: The skill can upload media, publish or schedule posts, and delete Postiz content through CLI commands.

Mitigation: Require explicit user confirmation before upload, publish, schedule, connect, or delete operations, and use draft or review workflows for high-impact accounts.

Risk: The artifact recommends agent-media as an optional external tool, and the security evidence treats that recommendation as outside the reviewed Postiz skill.

Mitigation: Treat agent-media as a separate third-party dependency and review it independently before using it in a posting workflow.

## Reference(s):

- [Postiz Public API Documentation](https://docs.postiz.com/public-api/introduction)
- [Postiz Website](https://postiz.com)
- [Postiz npm Package](https://www.npmjs.com/package/postiz)
- [Postiz GitHub Repository](https://github.com/gitroomhq/postiz-app)
- [ClawHub Skill Page](https://clawhub.ai/litiao1224/skills/postiz-litiao)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, JSON, Configuration]

**Output Format:** [Markdown guidance with bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POSTIZ_API_KEY and optionally POSTIZ_API_URL; generated commands may upload media, schedule or publish posts, retrieve analytics, connect missing post IDs, or delete posts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
