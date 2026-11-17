## Description:

Trades a Simmer-indexed market when your estimated probability diverges from the live market price, with dry-run on sim by default, context checks, reasoning tags, and optional live execution on Polymarket through ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssj124](https://clawhub.ai/user/ssj124)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill when they already have a probability estimate for a Simmer-indexed market and need a configurable execution wrapper that compares the estimate to market price before deciding whether to trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run as a managed task every 15 minutes for a financial trading workflow.

Mitigation: Verify or disable the cron automaton before installation and only enable recurring execution when continuous trading is intended.

Risk: Live execution can place trades on a prediction-market venue when explicitly enabled.

Mitigation: Keep dry-run mode as the default, pass live mode only intentionally, and set conservative trade size and edge thresholds.

Risk: The skill requires a Simmer API key and depends on external Python packages.

Mitigation: Use a restricted API key, keep secrets out of prompts and logs, and review dependency versions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssj124/skills/polymarket-divergence-trader)
- [Publisher profile](https://clawhub.ai/user/ssj124)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Markdown guidance with bash examples and operator text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print JSON trade results during live execution; defaults to dry-run unless live mode is explicitly enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
