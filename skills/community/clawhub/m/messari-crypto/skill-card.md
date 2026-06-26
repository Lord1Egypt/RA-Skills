## Description: <br>
Messari provides crypto market intelligence through Messari's REST API, including AI chat completions, market metrics, social signal data, news, research, stablecoin, exchange, network, protocol, token unlock, fundraising, intel, topic, and X-user data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jds950](https://clawhub.ai/user/jds950) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users, crypto analysts, and developers use this skill to route crypto market questions to Messari services for token analysis, market metrics, sentiment, protocol research, news, stablecoin flows, token unlocks, fundraising, and governance or protocol events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires delegating a Messari API key to the agent environment. <br>
Mitigation: Use a key you are comfortable delegating, keep it out of prompts and logs, and rotate it if exposure is suspected. <br>
Risk: Messari AI and API usage can consume paid credits or quota. <br>
Mitigation: Monitor Messari usage and credit consumption before running broad or repeated research workflows. <br>
Risk: Prompts or requests may include sensitive trading plans, portfolio details, secrets, or other confidential information sent to a third-party API. <br>
Mitigation: Avoid sending secrets, sensitive trading details, or confidential portfolio information unless that use is approved. <br>
Risk: The skill routes requests to Messari service domains for crypto research. <br>
Mitigation: Verify the Messari service domain independently before configuring credentials or making API requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jds950/messari-crypto) <br>
- [Messari API](https://messari.io/api) <br>
- [Messari REST API Services Reference](references/api_services.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with service routing notes, API request examples, and configuration instructions for Messari API access.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MESSARI_API_KEY in the agent environment; AI chat completion endpoints also require Messari AI credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
