## Description:

Mystock is a stock analysis assistant for quotes, limit-up tracking, shareholder activity, portfolio notes, and AI-assisted investment research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangz](https://clawhub.ai/user/wangz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Mystock to run a local stock analysis assistant that retrieves market data, tracks watchlists and memos, reviews limit-up and shareholder activity, and asks optional AI providers for investment research support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local service can expose and mutate portfolio and memo data without authentication.

Mitigation: Run it only on a trusted local machine or network, avoid exposing port 8000, and remove bundled portfolio or memo data before use or redistribution.

Risk: Financial context and API keys may be sent to configured external AI providers.

Mitigation: Do not configure AI keys until provider destinations and transmitted data are clear; rotate any real key used with the zhipu option.

Risk: Stock data and AI-generated analysis can be delayed, incomplete, or misleading for investment decisions.

Mitigation: Treat outputs as research support, verify critical information through official sources, and avoid relying on the skill as financial advice.

## Reference(s):

- [ClawHub Mystock Skill Page](https://clawhub.ai/wangz/skills/mystock)
- [README](artifact/README.md)
- [Usage Examples](artifact/references/usage_examples.md)
- [AI Service Configuration Guide](artifact/backend/AI_CONFIG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or text responses with API examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local API calls, portfolio and memo updates, and stock-analysis guidance; financial outputs should be verified before use.]

## Skill Version(s):

1.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
