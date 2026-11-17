## Description:

Conservative World Cup fixture-trading workflow for ClawHub: discover a market, validate the matchup, price the edge, and trade only when safe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[natekohisbetterthanryan](https://clawhub.ai/user/natekohisbetterthanryan)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to evaluate World Cup fixture-style prediction markets, normalize team names, compare fair value with market price, and either submit a paper/live trade or return a clear pass reason.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit paper trades by default and live trades when explicitly run with --live and credentials.

Mitigation: Keep default paper mode for validation, scope credentials carefully, and require explicit operator review before any live run.

Risk: Market-context warnings or recommendations can be reported without stopping execution.

Mitigation: Before live use, treat any context warning or recommendation other than TRADE as a pass condition.

Risk: The live trade path may submit the requested amount while reporting a risk-adjusted amount.

Mitigation: Correct and verify the live submitted amount so it matches the risk-adjusted trade amount before using live mode.

Risk: Dependency and venue behavior can change trade discovery, context, and execution outcomes.

Mitigation: Pin dependencies, verify Simmer venue behavior, and test against dry-run or paper-trading flows before release use.

## Reference(s):

- [Automated Slate Scan Notes](references/automated-slate-scan.md)
- [Session Notes](references/session-notes.md)
- [Simmer SDK Compatibility Notes](references/simmer-sdk-compat.md)
- [Stake Sizing Guidance](references/stake-sizing-guidance.md)
- [Team-Name Normalization Notes](references/team-name-normalization.md)
- [World Cup Market Discovery](references/world-cup-market-discovery.md)
- [International Football Results Dataset](https://raw.githubusercontent.com/martj42/international_results/master/results.csv)
- [FotMob Match Details API](https://www.fotmob.com/api/data/matchDetails)
- [FotMob Fixtures API](https://www.fotmob.com/api/data/pageableFixtures)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON decision reports, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Simmer-compatible market APIs and can submit paper trades by default or live trades only when explicitly run with live credentials.]

## Skill Version(s):

1.0.20 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
