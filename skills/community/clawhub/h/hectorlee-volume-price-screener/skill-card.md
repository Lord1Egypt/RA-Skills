## Description:

A Chinese-language A-share volume-price screening toolkit that detects six price-volume patterns, scores candidates across multiple factors and timeframes, supports intraday monitoring, and diagnoses individual stocks or position files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiyanjun](https://clawhub.ai/user/xiyanjun)

### License/Terms of Use:

MIT-0

## Use Case:

External users, finance analysts, and developers use this skill to run A-share market scans, inspect volume-price pattern matches, review risk filters, compare signal changes, and generate position diagnostics. The outputs support technical analysis workflows and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe pickle loading paths in model and backtest workflows.

Mitigation: Load only model or cache .pkl files that were generated locally or come from a trusted source; fix or replace pickle loading before using the skill in shared or higher-risk environments.

Risk: The security evidence notes broad finance, network, and MCP behavior, including sending stock codes or search terms to market-data providers and using a local WorkBuddy MCP proxy.

Mitigation: Review provider and proxy configuration before execution and run the skill only where disclosure of those stock codes, search terms, and MCP requests is acceptable.

Risk: Position diagnosis may process files containing cost basis and share counts.

Mitigation: Use trusted local position files, avoid sharing generated diagnostics outside the intended environment, and remove sensitive holdings data when it is not needed.

Risk: The artifact states that pure volume-price signals are not investment advice and that high scores do not guarantee price increases.

Mitigation: Treat results as technical-analysis signals for review, not as trading instructions; require independent financial judgment before acting on any output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiyanjun/skills/hectorlee-volume-price-screener)
- [Pattern rules](references/pattern_rules.md)
- [Scoring rules](references/scoring_rules.md)
- [Test cases](references/test_cases.md)
- [V2 backtest report](references/v2_backtest_report.md)
- [V2 portfolio report](references/v2_portfolio_report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands, tables, and JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local market databases and position JSON files, call market-data providers, use a local WorkBuddy MCP proxy, and write local scan logs or signal files when invoked.]

## Skill Version(s):

3.7.1 (source: SKILL.md frontmatter, manifest.yaml, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
