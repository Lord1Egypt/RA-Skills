## Description: <br>
多源 AI 科技新闻简报聚合器，覆盖 AI 大模型、科技、财经，按热度分级输出，并保留新闻来源以便追溯。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sweesama](https://clawhub.ai/user/sweesama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and news-focused agent workflows use this skill to assemble daily Chinese-language AI, technology, finance, and policy briefings from multiple searchable sources. It is intended for time-sensitive news collection, source checking, heat-level ranking, and concise briefing output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports that the skill asks users to copy live Twitter/X browser cookies and store credentials in plaintext. <br>
Mitigation: Prefer the Grok/API route or a dedicated low-risk X account, restrict credential-file permissions, avoid shell history exposure, and enable scheduled runs only when recurring automation is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sweesama/mzu-news-briefing) <br>
- [AIHOT public selected items](https://aihot.virxact.com/api/public/items?mode=selected&take=50) <br>
- [AIHOT public daily briefing](https://aihot.virxact.com/api/public/daily) <br>
- [xAI API](https://x.ai/api) <br>
- [OpenAI release updates](https://releasebot.io/updates/openai) <br>
- [LLM release tracker](https://llm-stats.com/llm-updates) <br>
- [AI funding tracker](https://aifundingtracker.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown briefing with links, source labels, ranked sections, and inline shell commands for setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-first briefing output; expected sections include high, medium, and low heat items with source traceability.] <br>

## Skill Version(s): <br>
2.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
