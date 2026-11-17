## Description:

Social media scheduling & publishing CLI — plan, schedule and publish posts across 16 networks: Instagram, TikTok, YouTube, X (Twitter), Facebook, LinkedIn, Threads, Bluesky, Mastodon, Discord, Telegram, WordPress, Dev.to, Tumblr, Pinterest and Google Business, powered by PosteAhora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sashadiz](https://clawhub.ai/user/sashadiz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and AI agents use this skill to manage social content across connected accounts: draft, schedule, publish, and review posts, upload media, organize ideas, and retrieve analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing sends content to external social platforms and may be difficult to undo.

Mitigation: Before publishing, get approval for the exact caption, destination accounts, and timing; use draft mode when approval is pending.

Risk: Authentication troubleshooting guidance requests broader account access than may be necessary.

Mitigation: Use a key limited to the intended workspace and required permissions, and investigate authentication errors rather than automatically granting full access.

Risk: Uploaded media receives a public URL, and authentication is saved locally unless removed.

Mitigation: Confirm media is appropriate for public access, protect the local credential store, and remove saved authentication when it is no longer needed.

## Reference(s):

- [PosteAhora website](https://posteahora.com)
- [PosteAhora documentation](https://posteahora.com/docs)
- [PosteAhora API reference](https://posteahora.com/docs/api)
- [PosteAhora CLI on npm](https://www.npmjs.com/package/@posteahora/cli)
- [PosteAhora MCP server](https://github.com/posteahora/mcp)
- [ClawHub skill release](https://clawhub.ai/sashadiz/skills/posteahora)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Guidance]

**Output Format:** [Shell commands for content management and publishing; social captions and structured JSON records or analytics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishing may be immediate, scheduled, or saved as a draft; results depend on connected accounts and platform capabilities.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
