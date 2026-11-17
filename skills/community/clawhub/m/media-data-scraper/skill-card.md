## Description:

This skill helps agents scrape and analyze public work metrics from Douyin, Xiaohongshu, Bilibili, Kuaishou, and WeChat Channels, with optional Feishu Bitable sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu1982966308](https://clawhub.ai/user/wu1982966308)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect engagement metrics from supported Chinese social-media posts, format the results, save JSON or CSV files, and optionally sync successful records to Feishu Bitable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Social-media scraping may violate platform terms, local rules, or workspace policy.

Mitigation: Use only where scraping is allowed, limit collection to authorized public content, and review applicable platform and organizational rules before execution.

Risk: Feishu sync can store App ID, App Secret, base token, and table settings locally in plaintext.

Mitigation: Avoid enabling Feishu sync unless needed; use narrowly scoped Feishu credentials and run the skill in a controlled Python environment.

Risk: The security scan reports under-disclosed donation prompts, persistent local state, and browser or local server side effects.

Mitigation: Review the skill before installation, expect local state and browser prompts during repeated use, and run it in a sandboxed environment when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu1982966308/skills/media-data-scraper)
- [Publisher profile](https://clawhub.ai/user/wu1982966308)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime scraping functions return structured dictionaries and optional JSON or CSV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally push successful scrape records to Feishu Bitable when the user configures sync.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
