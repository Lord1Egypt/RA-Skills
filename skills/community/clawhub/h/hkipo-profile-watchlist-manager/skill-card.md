## Description:

Manage Hong Kong IPO user preferences and watchlists, including risk profile, default output, budget, financing preference, and tracked symbols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackstoic](https://clawhub.ai/user/hackstoic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain personalized Hong Kong IPO risk preferences, output defaults, budget, financing preference, and tracked symbols for later IPO decision workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled runtime exposes broader IPO decision-support, network, scoring, review-history, suggestion-application, and persistence capabilities beyond profile and watchlist management.

Mitigation: Review the bundled commands before use, run the skill in a minimally privileged environment, and install only when the broader CLI behavior is acceptable.

Risk: The runtime stores profile and watchlist configuration under ~/.hkipo-next.

Mitigation: Avoid placing unrelated secrets in that directory and review generated profile or watchlist files before sharing logs or artifacts.

Risk: Dependency resolution may change without a reviewed lockfile.

Mitigation: Prefer a reviewed lockfile or pinned environment before using the bundled runtime in a sensitive workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hackstoic/skills/hkipo-profile-watchlist-manager)
- [AiPO data source](https://aipo.myiqdii.com)
- [AAStocks IPO market data](https://www.aastocks.com/tc/stocks/market/ipo/)
- [API guide](runtime/hkipo-next/references/api-guide.md)
- [Risk preferences](runtime/hkipo-next/references/risk-preferences.md)
- [Analysis guide](runtime/hkipo-next/references/analysis-guide.md)
- [IPO mechanism](runtime/hkipo-next/references/ipo-mechanism.md)
- [AiPO API documentation](runtime/hkipo-next/references/aipo-api.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, text, markdown, JSON, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON, text, or markdown command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile and watchlist state is stored under ~/.hkipo-next when commands are executed.]

## Skill Version(s):

0.1.0 (source: frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
