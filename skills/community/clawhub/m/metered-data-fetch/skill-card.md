## Description:

Metered Data Fetch helps agents discover, quote, and call paid SettleMesh data APIs for live web search, scraping, SEO/SERP, finance and market data, and LLM requests without separate provider API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[structureintelligence](https://clawhub.ai/user/structureintelligence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when an agent needs live paid data retrieval through SettleMesh, including web search, page scraping, SEO/SERP data, market data, and LLM calls with upfront quotes and metered billing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate SettleMesh account login and cache an authenticated session.

Mitigation: Approve login deliberately, use the skill only with a trusted SettleMesh account, and know how to clear the cached session before relying on it.

Risk: The skill can make metered paid network calls through a globally installed CLI.

Mitigation: Use a pinned or isolated settlemesh CLI install, inspect cost quotes before calls, and review ledger entries after use.

Risk: Requested data tasks are sent through SettleMesh.

Mitigation: Avoid submitting sensitive data unless that routing is acceptable for the intended use case.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/structureintelligence/skills/metered-data-fetch)
- [Publisher Profile](https://clawhub.ai/user/structureintelligence)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides authenticated, metered network calls through the settlemesh CLI and expects cost quotes before paid calls.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
