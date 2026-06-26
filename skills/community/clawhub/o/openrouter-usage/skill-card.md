## Description: <br>
Fetch real-time OpenRouter usage totals and historical per-model spend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosseyre](https://clawhub.ai/user/rosseyre) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, operators, and teams using OpenRouter can ask an agent to retrieve current spend, remaining credits, and recent per-model usage from their OpenRouter account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenRouter credentials may be exposed if stored in credentials.env or shared logs. <br>
Mitigation: Prefer environment variables, keep any credentials.env file out of version control, restrict file permissions, and avoid printing credential values. <br>
Risk: The management key enables model-level activity reporting beyond basic spend totals. <br>
Mitigation: Provide OPENROUTER_MGMT_KEY only when model-level activity reporting is needed. <br>


## Reference(s): <br>
- [OpenRouter Usage release page](https://clawhub.ai/rosseyre/openrouter-usage) <br>
- [OpenRouter key usage endpoint](https://openrouter.ai/api/v1/auth/key) <br>
- [OpenRouter activity endpoint](https://openrouter.ai/api/v1/activity) <br>
- [OpenRouter credits endpoint](https://openrouter.ai/api/v1/credits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Terminal text with concise Markdown-style sections and currency totals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes live daily, weekly, and monthly spend totals, credit balance, and an optional seven-day per-model breakdown when the management key is provided.] <br>

## Skill Version(s): <br>
1.1.3 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
