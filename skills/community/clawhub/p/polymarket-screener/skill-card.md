## Description:

Filter Polymarket prediction markets and track probabilities. Use when screening bets, drafting analyses, outlining trends, tracking price movements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, traders, and developers use this skill to screen Polymarket markets, compare odds, identify possible value bets, and maintain local watchlists for analysis. It provides analysis only and does not place trades or manage positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an unrelated content-writing command that can retain user prompts or topics in a local history file.

Mitigation: Install only after the publisher removes or clearly documents the unrelated script and explains local data retention controls.

Risk: The documented Polymarket command names and packaged scripts do not fully match, which can lead users to run behavior they did not intend.

Mitigation: Verify the installed entrypoint and command behavior before execution, and require corrected documentation from the publisher.

Risk: Prediction market analysis can be mistaken for betting advice and may involve real-money financial loss.

Mitigation: Treat output as analysis only, do independent research, and apply user-defined position and loss limits outside the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/skills/polymarket-screener)
- [BytesAgain Homepage](https://bytesagain.com)
- [Polymarket Gamma Markets API](https://gamma-api.polymarket.com/markets?closed=false&limit={}&order={})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash command examples, terminal text output, and local JSON cache or watchlist files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Polymarket public API reads and local user-directory cache or history files.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
