## Description:

Score Hong Kong IPOs, build decision cards, and batch-evaluate symbols or watchlists with explainable factors and execution guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackstoic](https://clawhub.ai/user/hackstoic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate Hong Kong IPO participation choices, position sizing, and batch watchlist decisions with explainable scoring and execution-oriented summaries. Outputs should be treated as financial research support, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces financial decision-support outputs that could be mistaken for investment advice.

Mitigation: Treat generated scores, decision cards, and execution plans as research inputs and have a qualified human review them before acting.

Risk: The runtime stores IPO preferences, watchlists, parameters, and decision history under ~/.hkipo-next.

Mitigation: Run in an isolated environment when appropriate and avoid placing sensitive personal or account data in local configuration files.

Risk: The runtime fetches public IPO data from external market sites, so outputs may reflect incomplete, delayed, or conflicting upstream data.

Mitigation: Cross-check important IPO facts against authoritative market disclosures and review partial outputs before use.

Risk: The package depends on Python dependencies and the uv runtime.

Mitigation: Install only with reviewed or locked dependencies and keep the execution environment scoped to this workflow.

## Reference(s):

- [HK IPO Decision Engine skill definition](SKILL.md)
- [hkipo-next README](runtime/hkipo-next/README.md)
- [AiPO API documentation](runtime/hkipo-next/references/aipo-api.md)
- [Analysis guide](runtime/hkipo-next/references/analysis-guide.md)
- [API guide](runtime/hkipo-next/references/api-guide.md)
- [Hong Kong IPO mechanism guide](runtime/hkipo-next/references/ipo-mechanism.md)
- [Risk preferences guide](runtime/hkipo-next/references/risk-preferences.md)
- [AiPO market data source](https://aipo.myiqdii.com)
- [AAStocks IPO market page](https://www.aastocks.com/tc/stocks/market/ipo/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON, Markdown, and text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local profile, watchlist, parameter, and review records under ~/.hkipo-next.]

## Skill Version(s):

0.1.0 (source: frontmatter, pyproject.toml, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
