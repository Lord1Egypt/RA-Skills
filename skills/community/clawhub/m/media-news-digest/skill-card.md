## Description:

Generates media and entertainment industry news digests from RSS, Twitter/X, Reddit, and web search, then formats results for Discord or email with optional PDF attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinstein](https://clawhub.ai/user/dinstein)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to collect, deduplicate, score, summarize, archive, and deliver scheduled media and entertainment news digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network fetching and email delivery are under-scoped enough to expose users to unsafe URL and recipient handling.

Mitigation: Review and fix default sources and delivery settings before installation; use trusted workspace configs and validate email recipients before enabling scheduled delivery.

Risk: Full-text enrichment performs additional outbound network access.

Mitigation: Avoid --enrich unless outbound network access is sandboxed from private or internal addresses.

Risk: Configured Discord or email delivery can externally share generated content.

Mitigation: Treat Discord and email outputs as external sharing and configure only intended channels or recipients.

Risk: Default Twitter handles may need correction according to the security guidance.

Mitigation: Correct or disable bad Twitter handles before enabling Twitter collection.

## Reference(s):

- [Digest Prompt Template](references/digest-prompt.md)
- [Discord Output Template](references/templates/discord.md)
- [Email Output Template](references/templates/email.md)
- [ClawHub Skill Page](https://clawhub.ai/dinstein/skills/media-news-digest)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files]

**Output Format:** [Markdown digest with JSON pipeline artifacts and optional HTML, PDF, Discord, or email delivery artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include archived digest files and external Discord or email delivery when configured.]

## Skill Version(s):

2.1.1 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
