## Description:

多源 AI 科技新闻简报聚合器。覆盖 AI 大模型、科技、财经，按热度分级输出，来源全程可溯。AIHOT 168 信源并行覆盖。8 维度强制搜索，15-20 条精选内容。支持 Twitter/X 和 Grok API。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sweesama](https://clawhub.ai/user/sweesama)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Chinese-first daily AI, technology, finance, and world-news briefings. The skill guides an agent through multi-source collection, source verification, heat ranking, and concise Markdown briefing output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cookie-based Twitter/X backend asks users to store live session cookies in a plaintext local file.

Mitigation: Use a dedicated or low-risk account, restrict credential file permissions to the owner, avoid committing or syncing the file, and rotate cookies if exposed.

Risk: The Grok API backend asks users to store an API key in a plaintext local file.

Mitigation: Prefer a scoped API key when available, keep the key file out of source control and shared sync folders, and rotate the key if exposed.

Risk: Install commands do not pin dependency versions, which can make later executions depend on changed upstream packages.

Mitigation: Review dependencies before installation and pin package versions in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sweesama/skills/mzu-news-briefing)
- [xAI API](https://x.ai/api)
- [AIHOT](https://aihot.virxact.com)
- [Releasebot OpenAI updates](https://releasebot.io/updates/openai)
- [LLM Stats updates](https://llm-stats.com/llm-updates)
- [AI Funding Tracker](https://aifundingtracker.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing with source links, heat tiers, concise summaries, and setup guidance that may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first output with English technical terms where useful; news entries retain source attribution and coverage counts.]

## Skill Version(s):

2.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
