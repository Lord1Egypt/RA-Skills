## Description:

Coordinate the end-to-end Hong Kong IPO workflow across discovery, snapshot extraction, personalization, scoring, and review optimization. Use when the user wants one skill to choose the next step across the full HK IPO research loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackstoic](https://clawhub.ai/user/hackstoic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and IPO researchers use this skill to coordinate a Hong Kong IPO research loop, selecting the next step across market discovery, snapshot extraction, profile and watchlist setup, scoring, decision-card generation, and review optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores watchlists, risk preferences, scoring parameters, decisions, notes, and outcomes under ~/.hkipo-next as local plaintext data.

Mitigation: Use it only on trusted machines, restrict filesystem permissions on ~/.hkipo-next, and treat exported review files as sensitive financial history.

Risk: The workflow contacts public market-data sites, so source availability or partial data can affect research quality.

Mitigation: Review degraded or partial data warnings and verify important IPO facts against source materials before acting.

Risk: Repeated score or batch jobs can create additional review records.

Mitigation: Confirm before running repeated scoring or batch operations when preserving a clean decision history matters.

## Reference(s):

- [hkipo-next README](runtime/hkipo-next/README.md)
- [AiPO API Documentation](runtime/hkipo-next/references/aipo-api.md)
- [Analysis Guide](runtime/hkipo-next/references/analysis-guide.md)
- [API Guide](runtime/hkipo-next/references/api-guide.md)
- [IPO Mechanism Reference](runtime/hkipo-next/references/ipo-mechanism.md)
- [Risk Preferences Reference](runtime/hkipo-next/references/risk-preferences.md)
- [AiPO Data Source](https://aipo.myiqdii.com)
- [AASTOCKS IPO Market Data](https://www.aastocks.com/tc/stocks/market/ipo/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON, text, or Markdown with concise shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route to companion HK IPO skills and may update local profile, watchlist, parameter, or review-history files when the user confirms state-changing steps.]

## Skill Version(s):

0.1.0 (source: frontmatter, pyproject.toml, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
