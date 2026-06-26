## Description: <br>
Create, schedule, and manage social media posts, comments, and DMs across Facebook, Instagram, TikTok, LinkedIn, YouTube, X/Twitter, Threads, Pinterest, Bluesky, Telegram, and Google Business via the Postproxy API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danbaranov](https://clawhub.ai/user/danbaranov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage social publishing workflows through Postproxy, including drafts, scheduled posts, queue operations, comments, direct messages, webhooks, and profile analytics. It is intended for agents acting on the user's connected social media accounts after confirming outward-facing or irreversible actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing, deleting, queue changes, comments, and direct messages can affect real social accounts or private conversations. <br>
Mitigation: Confirm the exact action, content, target profile, placement, and scope before execution; prefer drafts or paused queues when intent is uncertain. <br>
Risk: POSTPROXY_API_KEY and webhook secrets are sensitive credentials. <br>
Mitigation: Keep credentials out of chat logs, source control, and public endpoints; only register HTTPS webhook destinations the user controls and trusts. <br>
Risk: Platform defaults or missing placement details can publish to an unintended account or location. <br>
Mitigation: Resolve and confirm placement-specific targets for Facebook, LinkedIn, Pinterest, Telegram, and Google Business before posting. <br>


## Reference(s): <br>
- [ClawHub Postproxy Skill Page](https://clawhub.ai/danbaranov/postproxy) <br>
- [Postproxy Homepage](https://postproxy.dev) <br>
- [Postproxy API Keys](https://app.postproxy.dev/api_keys) <br>
- [Postproxy Skill README](README.md) <br>
- [Posts Rule Reference](rules/posts.md) <br>
- [Comments Rule Reference](rules/comments.md) <br>
- [Messages Rule Reference](rules/messages.md) <br>
- [Platforms Rule Reference](rules/platforms.md) <br>
- [Webhooks Rule Reference](rules/webhooks.md) <br>
- [Errors Rule Reference](rules/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl command examples, API request bodies, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POSTPROXY_API_KEY and curl; outward-facing or irreversible actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata; artifact frontmatter says 2.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
