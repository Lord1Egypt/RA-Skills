## Description:

Save, inspect, activate, and compare Hong Kong IPO scoring parameter versions across weights, thresholds, and cost assumptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackstoic](https://clawhub.ai/user/hackstoic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and IPO-analysis agents use this skill to manage versioned Hong Kong IPO scoring parameters before generating recommendations. It supports inspecting active settings, saving tuned candidates, activating defaults, and comparing parameter versions on representative symbols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled runtime exposes broader HK IPO workflows than the parameter-manager description, including scraping, scoring, profile, watchlist, review, and suggestion commands.

Mitigation: Run only explicit params commands for parameter management, and review any use of score, review, apply-suggestions, profile, or watchlist commands before execution.

Risk: Parameter versions are stored in the user's HKIPO runtime data directory by default.

Mitigation: Use an isolated HKIPO_HOME or test environment when evaluating the skill, especially before activating a parameter version for later scoring.

Risk: The runtime is executed through uv and depends on bundled Python code and dependencies.

Mitigation: Prefer a locked dependency install and review the included runtime before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hackstoic/skills/hkipo-parameter-manager)
- [hkipo-next README](runtime/hkipo-next/README.md)
- [API Guide](runtime/hkipo-next/references/api-guide.md)
- [Risk Preferences](runtime/hkipo-next/references/risk-preferences.md)
- [AiPO API](runtime/hkipo-next/references/aipo-api.md)
- [AAStocks IPO market page](https://www.aastocks.com/tc/stocks/market/ipo/)
- [AiPO data source](https://aipo.myiqdii.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command blocks and JSON-oriented output cues]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parameter commands may read or write version data under ~/.hkipo-next/data/hkipo.db unless HKIPO_HOME is isolated.]

## Skill Version(s):

0.1.0 (source: frontmatter, pyproject.toml, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
