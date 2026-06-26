## Description: <br>
Searches recent popular WeChat Official Account articles by keyword, ranks results by relevance, popularity, and recency, and presents trend-focused article recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, WeChat operators, brand teams, and self-media learners use this skill to discover recent high-performing WeChat articles, compare topic trends, and gather writing inspiration. It can also guide keyword-based recurring subscription workflows when the user explicitly wants scheduled tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a hardcoded Redfox API key in the release. <br>
Mitigation: Install only after the publisher removes and rotates the exposed key; configure your own REDFOX_API_KEY through environment variables and avoid placing it in prompts, code, logs, or output files. <br>
Risk: Search keywords and date ranges are sent to redfox.hk for article lookup. <br>
Mitigation: Use only queries that are acceptable to share with RedFoxHub, and avoid confidential topics or sensitive personal data. <br>
Risk: The skill includes optional calendar-style subscription behavior for recurring keyword reminders. <br>
Mitigation: Approve subscription creation only when recurring reminders are intended, and review the schedule and destination before enabling it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/gzh-explosive-content-detector) <br>
- [WeChat trend data format reference](references/gzh_trend_data_format.md) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, html, shell commands, configuration guidance] <br>
**Output Format:** [Markdown article tables and recommendations, with optional JSON or HTML output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses REDFOX_API_KEY for RedFoxHub requests; query results are limited to recent indexed WeChat articles and may include recurring subscription guidance.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
