## Description:

Transparent API proxy for ZhenInsure AI insurance consultation, enabling agents to create conversations, send messages, and request human advisor handoff with a user-provided API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to conduct ZhenInsure insurance consultations, including starting chat sessions, sending insurance questions, and requesting handoff to a human advisor. It is suited for insurance brokerage workflows that can safely handle API-key authenticated calls to the ZhenInsure service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be configured to send the user's API key and sensitive insurance consultation data to an arbitrary base URL.

Mitigation: Install only if the publisher is trusted, verify that ZHENINSURE_BASE_URL is unset or restricted to an approved ZhenInsure origin, and protect the API key as a production secret.

Risk: Insurance consultations may include health, financial, or customer data.

Mitigation: Avoid sending real personal or customer data unless users have consent and understand ZhenInsure's data handling terms.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhenstaff/skills/insurance-broker)
- [ZhenInsure API documentation](https://www.zhenins.com/docs/api)
- [ZhenInsure homepage](https://www.zhenins.com)
- [ZhenInsure console](https://console.zhenrobot.com/zhenins)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Synchronous JSON response objects with status fields, returned API data, error details, costs, and management or billing action links when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ZHENINSURE_API_KEY secret; the action accepts an allowlisted endpoint, POST method, and optional endpoint-specific JSON body.]

## Skill Version(s):

2.0.2 (source: server release metadata, package.json, skill.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
