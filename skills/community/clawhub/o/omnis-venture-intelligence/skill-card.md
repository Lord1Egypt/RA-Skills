## Description: <br>
Discover and score venture opportunities with machine-first APIs using read-first workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HCS412](https://clawhub.ai/user/HCS412) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, analysts, and venture teams use this skill to query Omnis/Bamboosnow APIs for startup discovery, company scoring, service status, and catalog information while keeping billing actions outside agent execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Venture-discovery queries, company identifiers, and explicitly provided API keys may be sent to the Bamboosnow/Omnis service. <br>
Mitigation: Install only if that data sharing is acceptable; provide API keys explicitly in-session and avoid unrelated local credential discovery. <br>
Risk: Some API paths require prepaid balance or hosted checkout outside agent execution. <br>
Mitigation: Complete payment or funding steps yourself in the hosted checkout flow, then resume read calls after funding is confirmed. <br>
Risk: 402 or 429 responses can interrupt discovery and scoring workflows. <br>
Mitigation: Follow returned x-omnis recovery headers for funding guidance and wait for x-ratelimit-reset before retrying rate-limited calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HCS412/omnis-venture-intelligence) <br>
- [Omnis agents homepage](https://www.bamboosnow.co/agents) <br>
- [Omnis API OpenAPI specification](https://www.bamboosnow.co/docs/api/openapi.v1.yaml) <br>
- [Omnis agent manifest](https://www.bamboosnow.co/api/v1/agents/manifest) <br>
- [Omnis agent feed](https://www.bamboosnow.co/agent-feed.json) <br>
- [Omnis LLM index](https://www.bamboosnow.co/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown with API endpoint references and concise summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only API guidance; no billing POST actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
