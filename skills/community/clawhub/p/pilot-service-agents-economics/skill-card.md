## Description:

Macroeconomic indicators from IMF DataMapper, World Bank, Eurostat SDMX, and Coinbase reference prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to discover and query Pilot Protocol economics service agents for country-level macroeconomic series, cross-country indicator comparisons, Eurostat dissemination data, IMF DataMapper data, World Bank metadata and indicators, and Coinbase spot reference prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and filters are sent through the Pilot Protocol service-agent overlay network.

Mitigation: Install only when that network path is acceptable, keep filters limited to intended data lookups, and verify agent contracts with /help before sending queries.

Risk: The /summary path returns Gemini-generated prose that may be less suitable than primary structured data for exact analysis.

Mitigation: Prefer /data for primary structured results and use /summary only when generated narrative output is acceptable.

Risk: The available economics-agent catalogue can change over time.

Mitigation: Run a fresh list-agents query before use and avoid hard-coding the snapshot in the artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-economics)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text]

**Output Format:** [Markdown guidance with bash commands, JSON request examples, JSON response envelopes, and optional prose summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses pilotctl to send /help, /data, and /summary messages; structured results are read from pilotctl inbox.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
