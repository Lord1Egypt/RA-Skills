## Description: <br>
Connects agents to Geocodio (geocod.io) for address geocoding and coordinate reverse-geocoding through the OOMOL oo CLI instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to geocode addresses or reverse geocode latitude and longitude through an OOMOL-connected Geocodio account, including single and batch lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Geocodio account with server-side credentials. <br>
Mitigation: Use it only when the account connection is expected; do not request or expose raw API keys, and run connection steps only after matching auth or connection errors. <br>
Risk: Geocoding and reverse-geocoding requests can send address or coordinate data to Geocodio through the connector. <br>
Mitigation: Review payloads for sensitive location data before execution and use the live connector schema to send only required fields. <br>
Risk: Setup and billing recovery commands can affect the local environment or the connected OOMOL account. <br>
Mitigation: Run setup or billing steps only when the documented failure condition occurs, and confirm with the user before any action that changes state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-geocodio) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Geocodio homepage](https://www.geocod.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects with data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
