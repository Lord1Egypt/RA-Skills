## Description:

Public market data for crypto spot prices, FX rates, order books, and macro indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agents use this skill to discover and query Pilot Protocol finance service agents for public market data such as crypto prices, FX rates, currency conversion, and market snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The finance catalog includes market, macroeconomic, and SEC-related agents, so users may choose an agent outside the intended finance-data scope.

Mitigation: Verify each selected agent with /help before querying it, and use dedicated government-finance or economics skills when domain separation matters.

Risk: The skill connects to public read-only data sources whose availability, coverage, or freshness can vary by upstream service.

Mitigation: Cross-check important values across available providers and treat returned data as public market information rather than brokerage or portfolio data.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-finance)
- [Publisher Skill Index](https://teoslayer.github.io/pilot-skills/)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include ACK envelopes, inbox entries, item arrays, counts, pagination fields, truncation flags, and upstream URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
