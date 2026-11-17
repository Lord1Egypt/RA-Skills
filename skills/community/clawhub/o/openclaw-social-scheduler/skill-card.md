## Description:

Schedule and post text, media, and threads to Discord, Reddit, Twitter/X, Mastodon, Bluesky, and Moltbook via CLI/API workflows with immediate or scheduled publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrshorrid](https://clawhub.ai/user/mrshorrid)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to automate social publishing workflows, including immediate posts, scheduled posts, queue management, media uploads, and threaded posts across supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled posts may store reusable social-media credentials in a local plaintext queue.

Mitigation: Use dedicated, revocable, least-privilege credentials; keep config files and storage/queue.json out of git, backups, and shared workspaces; and remove queued secrets after use.

Risk: Remote media URLs can introduce untrusted content into publishing workflows.

Mitigation: Prefer local vetted media or trusted domains, validate file type and size before upload, and avoid scheduling untrusted remote media URLs.

Risk: The dependency stack may need updates before use with sensitive social accounts.

Mitigation: Update or replace older dependencies and run security review before connecting high-value accounts.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mrshorrid/skills/openclaw-social-scheduler)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [MEDIA-GUIDE.md](MEDIA-GUIDE.md)
- [MOLTBOOK-USAGE.md](MOLTBOOK-USAGE.md)
- [Moltbook API documentation](https://github.com/moltbook/api)
- [Twitter API documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Discord Developer documentation](https://discord.com/developers/docs)
- [Mastodon API documentation](https://docs.joinmastodon.org/api/)
- [AT Protocol documentation](https://atproto.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces platform-specific posting, scheduling, media upload, queue management, and setup guidance for agent workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
