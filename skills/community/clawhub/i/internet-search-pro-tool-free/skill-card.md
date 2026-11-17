## Description:

联网搜索助手 helps an agent extract search keywords, retrieve current information, filter low-value results, and summarize concise Chinese-language findings with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for everyday Chinese-language web searches, recent news and product lookups, SEO-oriented keyword research, and short structured summaries. It is intended for single-query searches and does not claim multi-turn search, batch querying, export, or search history support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release suspicious because it requests shell execution and file-write capabilities that are broader than a basic search assistant needs.

Mitigation: Run it only in constrained environments, review commands before execution, and prefer a search-only configuration or command whitelist before broader deployment.

Risk: Search results may be incomplete, outdated, or affected by irrelevant pages and search-engine ranking behavior.

Mitigation: Check cited source links, ask for narrower search terms when results are weak, and avoid treating summaries as authoritative without source review.

Risk: Optional external search API configuration can expose credentials if keys are written into files or command history.

Mitigation: Use environment variables or platform secret storage, avoid hardcoding keys, and redact credentials from shared outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/internet-search-pro-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with source links and optional inline shell or environment-variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically returns 3-5 search results with a brief core finding, detailed items, and one practical suggestion.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
