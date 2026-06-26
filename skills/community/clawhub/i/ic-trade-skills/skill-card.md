## Description: <br>
Connects local ERP inventory with the IC Trade Navigator API to return IC component quotes, risk scores, and trade advisories for MCP-compatible agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oppstie](https://clawhub.ai/user/oppstie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IC trading and procurement teams use this skill to query component market quotes, read local stock availability, and combine those signals into agent-readable recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector can send part numbers, requested quantities, language, and optional customer identifiers to a configured quote service. <br>
Mitigation: Use a dedicated API key, verify the quote API URL, and avoid passing real customer identifiers unless they are intended for the quote service. <br>
Risk: Local inventory data may be exposed to the local agent workflow even when pricing fields are blocked. <br>
Mitigation: Use a reduced inventory export that contains only fields approved for agent use. <br>
Risk: The evidence security verdict is suspicious because the privacy claims may understate some customer and inventory data exposure. <br>
Mitigation: Review before installing on sensitive ERP data and confirm the local column mapping and blocked fields match the intended data boundary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oppstie/ic-trade-skills) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summaries or JSON objects containing quote, inventory, risk, and recommendation fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP tools return single-part quotes, local inventory lookups, or combined market and ERP views.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
