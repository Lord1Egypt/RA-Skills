## Description: <br>
Access OlaXBT Nexus cryptocurrency data APIs for market data, news, KOL tracking, technical indicators, and trading insights using a wallet-linked JWT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OlaXBT-Dev](https://clawhub.ai/user/OlaXBT-Dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to query OlaXBT Nexus crypto data APIs, monitor markets, news, sentiment, and KOL activity, and retrieve trading insight signals through Python or HTTP-backed workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes private-key wallet-signing code despite JWT-only framing. <br>
Mitigation: Do not provide Ethereum private keys to this package; obtain the JWT outside the skill and use only NEXUS_JWT. <br>
Risk: A wallet-linked JWT can grant access to OlaXBT Nexus API data and may be exposed through logs or displayed token fragments. <br>
Mitigation: Treat NEXUS_JWT and any token fragments as sensitive, avoid printing them, and rotate or revoke credentials if exposure is suspected. <br>
Risk: Custom API URL overrides can redirect authenticated requests to endpoints the user does not control. <br>
Mitigation: Use the documented default endpoints unless the replacement endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/OlaXBT-Dev/olaxbt-nexus-data) <br>
- [Nexus Skills API specification](https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md) <br>
- [Project homepage](https://github.com/olaxbt/olaxbt-nexus-data) <br>
- [Support](https://github.com/olaxbt/olaxbt-nexus-data/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, API calls] <br>
**Output Format:** [Python objects, JSON-like API responses, Markdown guidance, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_JWT; optional NEXUS_AUTH_URL and NEXUS_DATA_URL override API endpoints.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; artifact pyproject.toml, CHANGELOG, and clawhub.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
