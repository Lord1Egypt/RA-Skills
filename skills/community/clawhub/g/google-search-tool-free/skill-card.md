## Description:

谷歌搜索工具基于 Google Custom Search Engine 帮助代理执行联网搜索，并返回标题、链接和摘要等结构化结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, students, researchers, and teams use this skill to search public web information, technical documentation, current news, and SEO or keyword research topics through Google CSE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may disclose confidential project names, secrets, or sensitive topics to external services.

Mitigation: Use the skill only for non-sensitive public web searches and keep confidential data out of query strings.

Risk: API credentials can be exposed if stored in committed files or pasted into shared shell history.

Mitigation: Store Google API Key and CSE ID in environment variables or a secret manager, and do not commit .env files.

Risk: The artifact requests broad exec/write authority but does not include a bounded implementation script.

Mitigation: Review the skill before installation and grant only the minimum tool permissions needed for the intended workflow.

Risk: Search results can be stale, incomplete, or misleading.

Mitigation: Validate important results against authoritative sources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/google-search-tool-free)
- [Google APIs endpoint referenced by the skill](https://www.googleapis.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured search-result expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Google API Key and Google CSE ID; documented single-query results are capped at 10 items.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
