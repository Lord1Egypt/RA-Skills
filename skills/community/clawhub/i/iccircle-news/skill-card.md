## Description:

Fetch and aggregate semiconductor and chip industry news from IC技术圈 (iccircle.com) RSS feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billchen1020](https://clawhub.ai/user/billchen1020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to fetch recent semiconductor, chip industry, EDA, and related technology news from predefined RSS sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts iccircle.com, vlsiblogs.com, ithome.com, and 36kr.com to fetch RSS feeds.

Mitigation: Install and run it only in environments where outbound requests to those news sources are acceptable.

Risk: The output is primarily Chinese formatted news and may include broader technology items from filtered RSS sources.

Mitigation: Review the returned items before relying on them, and narrow the configured feed list if strictly semiconductor-only or IC技术圈-only content is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/billchen1020/skills/iccircle-news)
- [IC技术圈 RSS Feed](https://iccircle.com/feed)
- [VLSI Blogs Aggregate RSS](https://vlsiblogs.com/aggrss)
- [IT之家 RSS Feed](https://www.ithome.com/rss/)
- [36氪 RSS Feed](https://www.36kr.com/feed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Formatted text suitable for Markdown presentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints source headers, timestamps, and links from predefined RSS feeds.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
