## Description:

Crypto market intelligence powered by Messari's REST API for AI-assisted analysis, market metrics, sentiment, news, research, stablecoins, exchanges, networks, protocols, token unlocks, fundraising, governance events, topics, and crypto X-user data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jds950](https://clawhub.ai/user/jds950)

### License/Terms of Use:


## Use Case:

Developers, analysts, and external agent users use this skill to route crypto market, protocol, sentiment, news, fundraising, governance, and token unlock questions to Messari REST API services. It helps an agent choose relevant endpoints and produce API-backed research guidance using a user-provided Messari API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto research queries and the Messari API key are sent to Messari's third-party service.

Mitigation: Install only when that data sharing is acceptable, keep the API key in the MESSARI_API_KEY environment variable, and avoid sending confidential personal or business data.

Risk: Prompts or API requests could accidentally include private keys, seed phrases, wallet credentials, or other sensitive crypto secrets.

Mitigation: Do not include private keys, seed phrases, wallet credentials, or confidential account material in prompts or API requests.

## Reference(s):

- [Messari REST API Services Reference](references/api_services.md)
- [Messari API](https://messari.io/api)
- [Messari API Base URL](https://api.messari.io)
- [ClawHub Skill Page](https://clawhub.ai/jds950/skills/messari-crypto)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided MESSARI_API_KEY; Messari AI completion endpoints require Messari AI credits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
