## Description:

Google Search Console API integration with managed OAuth. Query search performance analytics, inspect URL indexing status, review sitemaps, and manage verified site properties. Use this skill when users want to monitor SEO performance or troubleshoot indexing issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO operators use this skill to connect an agent to Google Search Console through ClawLink, query search performance, inspect indexing status, review sitemaps, and manage verified site properties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist an unpinned external ClawLink plugin that may expose a changing live tool catalog.

Mitigation: Review the ClawLink plugin before installation, confirm the visible Google Search Console tool catalog in a fresh chat, and proceed only if the publisher and plugin are trusted.

Risk: ClawLink stores and uses OAuth access for the connected Google Search Console account.

Mitigation: Connect only accounts and verified properties appropriate for the task, and confirm trust in ClawLink's credential handling before use.

Risk: Write operations can add or delete site properties or submit sitemaps.

Mitigation: Require clear previews and explicit user confirmation before any site addition, site deletion, or sitemap submission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/google-search-console-seo)
- [Publisher Profile](https://clawhub.ai/user/hith3sh)
- [Search Console API Overview](https://developers.google.com/webmaster-tools/search-console-api-original)
- [Search Analytics Reference](https://developers.google.com/webmaster-tools/search-console-api-original/v3/searchanalytics)
- [Sites Reference](https://developers.google.com/webmaster-tools/search-console-api-original/v3/sites)
- [Sitemaps Reference](https://developers.google.com/webmaster-tools/search-console-api-original/v3/sitemaps)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-search-console-seo)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated Google Search Console API actions through a live ClawLink tool catalog.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
