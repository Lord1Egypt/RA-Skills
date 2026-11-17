## Description:

Social media scheduler and social media automation for AI agents. Schedule posts, post to Instagram, post to LinkedIn, post to X (Twitter), TikTok, Facebook, Pinterest, Threads, Bluesky, Reddit, YouTube, Telegram, Snapchat and Google Business with Orshot, with the image, carousel or video rendered from a template in the same call. Use to schedule a social post, run a weekly content calendar, cross-post to every platform, queue drafts for review, read post analytics and follower growth, find the best time to post, or build an agent that posts and learns. Everything runs over the hosted Orshot MCP server (OAuth, no key); REST with an API key for headless jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orshot](https://clawhub.ai/user/orshot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media teams can use the skill to connect social accounts, prepare and review posts, render media from templates, schedule or publish approved content across platforms, and review analytics. It also guides setup of the Orshot MCP server or REST access for automated jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing to connected social accounts can send unintended content or target the wrong account.

Mitigation: Review OAuth permissions and the exact accounts, caption, and schedule; obtain explicit approval before publishing.

Risk: REST publishing may publish immediately if the request omits its status, and content is sent to Orshot.

Mitigation: For REST drafts, explicitly set status to draft; review content and schedules before approval.

Risk: Media links used for publishing must be publicly accessible, and connecting accounts may incur paid-plan charges.

Mitigation: Use intended public media links and check plan costs before connecting accounts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/orshot/skills/orshot-social-media-scheduler)
- [Orshot agent documentation](https://orshot.com/agents/openclaw)
- [Orshot social publishing API](https://orshot.com/docs/api-reference/social-publish.md)
- [Orshot social posts API](https://orshot.com/docs/api-reference/social-posts-list.md)
- [Orshot publishing introduction](https://orshot.com/docs/publish/introduction.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Social media post drafts, Rendered image, carousel, or video media, Analytics summaries, Shell commands, Configuration instructions, API request examples, Operational guidance]

**Output Format:** [Markdown guidance, social post content, media outputs, shell commands, and JSON or REST request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can prepare, schedule, or publish content to connected accounts; publishing should follow explicit user approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release and metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
