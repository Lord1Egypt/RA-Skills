## Description: <br>
Provides guidance for querying Pilot Protocol economics service agents for macroeconomic indicators from IMF DataMapper, World Bank, Eurostat SDMX, and Coinbase reference prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and analysts use this skill to discover and query public economics data agents for country-level GDP, inflation, unemployment, World Bank indicators, IMF series, Eurostat SDMX data, and Coinbase reference prices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local pilotctl binary and Pilot Protocol daemon. <br>
Mitigation: Install pilotctl and the daemon only from trusted sources, and verify the daemon is joined to the intended network before use. <br>
Risk: Queries and summaries are handled by remote third-party service agents and may expose submitted data or return inaccurate economic information. <br>
Mitigation: Do not submit secrets or private business data, and verify important economic results against upstream IMF, World Bank, Eurostat, Coinbase, or other cited sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-service-agents-economics) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use pilotctl and expect agent responses through the Pilot Protocol inbox.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
