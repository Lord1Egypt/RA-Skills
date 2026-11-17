## Description:

Capture Weibo, Xiaohongshu, WeChat, and Xiaoyuzhou links, extract text, images, metadata, and optional transcript context, then save a Markdown note with an AI deep summary to the user's Obsidian vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tt-bltn](https://clawhub.ai/user/tt-bltn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save supported social-media posts and podcast episodes into Obsidian as structured Markdown notes with local media references, summaries, and optional transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials, cookies, or local data could be exposed because the skill handles cookies, browser automation, media uploads, and remote downloads with weak scoping.

Mitigation: Review before installing, run in a limited environment, and use scoped or disposable credentials.

Risk: Platform cookies or ASR API keys may be unsafe to configure until hostname validation, download restrictions, endpoint validation, and .env permissions are fixed.

Mitigation: Avoid configuring platform cookies or API keys until those controls are fixed; check links before capture if the skill is used.

## Reference(s):

- [LinkMind homepage](https://github.com/tt-bltn/LinkMind)
- [ClawHub skill page](https://clawhub.ai/tt-bltn/skills/linkmind-capture)
- [Deep Summary Guidelines](references/deep-summary-guide.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [Markdown note files with YAML frontmatter, inline media references, AI summaries, optional transcript excerpts, and JSON handler-script results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes notes under the configured Obsidian vault and may reference downloaded attachments.]

## Skill Version(s):

0.3.0 (source: server release evidence and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
