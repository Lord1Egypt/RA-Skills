## Description:

Weather forecast analysis for Polymarket prediction markets using multi-model ensemble forecasts to identify potentially mispriced temperature contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasnocodo](https://clawhub.ai/user/lucasnocodo)

### License/Terms of Use:

MIT-0

## Use Case:

External prediction market traders, weather enthusiasts, and analysts use this skill to scan Polymarket temperature markets, compare ensemble forecasts, and review potential positive-edge opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POLYMARKET_SCANNER_API_KEY can be sent to a host configured through POLYMARKET_SCANNER_HOST.

Mitigation: Avoid setting POLYMARKET_SCANNER_HOST unless you control the endpoint, and treat POLYMARKET_SCANNER_API_KEY as a credential.

Risk: Vague weather or trading questions may trigger scans or forecasts unintentionally.

Mitigation: Prefer explicit /scan and /forecast requests when invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lucasnocodo/skills/polymarket-weather-scanner)
- [Polymarket Weather Scanner scan endpoint](https://polymarket-scanner.fly.dev/scan/weather)
- [Polymarket Weather Scanner forecast endpoint](https://polymarket-scanner.fly.dev/forecast/{city})
- [Polymarket Weather Scanner cities endpoint](https://polymarket-scanner.fly.dev/cities)
- [Polymarket Weather Scanner tiers endpoint](https://polymarket-scanner.fly.dev/tiers)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON from shell scripts, typically summarized as Markdown tables or concise text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; optionally uses POLYMARKET_SCANNER_API_KEY for higher-tier access.]

## Skill Version(s):

1.1.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
