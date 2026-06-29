## Description: <br>
InferSports provides read-only football and basketball odds, schedules, scores, fair probabilities, value scans, odds conversion, and finished results through bundled scripts over the InferSports REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infersports-dev](https://clawhub.ai/user/infersports-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer football and basketball schedule, score, odds, fair probability, value-detection, odds-conversion, and results questions. The skill is informational and read-only; it relays numbers and does not place bets or recommend wagers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A custom API base can receive the optional InferSports API key. <br>
Mitigation: Leave INFERSPORTS_API_BASE unset unless the target host is trusted, and leave INFERSPORTS_API_KEY unset for keyless free-tier use. <br>
Risk: Live network calls may be undesirable during review or offline validation. <br>
Mitigation: Set INFERSPORTS_MOCK=1 to use the bundled fixtures for deterministic offline checks. <br>
Risk: Host-agent behavior can add interpretation beyond the read-only script output. <br>
Mitigation: Relay the script's numbers without adding betting recommendations, stake sizing, or external odds sources. <br>


## Reference(s): <br>
- [InferSports full API reference](references/full-api.md) <br>
- [InferSports API documentation](https://docs.infersports.dev) <br>
- [InferSports OpenAPI documentation](https://api.infersports.dev/docs) <br>
- [InferSports agent map](https://api.infersports.dev/llms.txt) <br>
- [InferSports remote MCP endpoint](https://api.infersports.dev/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Concise plain text lines, with optional JSON when detailed output is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only, keyless by default, and offline-verifiable with bundled mock fixtures.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and VERSION file) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
