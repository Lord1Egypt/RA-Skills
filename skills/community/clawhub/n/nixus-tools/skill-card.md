## Description:

Nixus Agentic Tools helps agents call unauthenticated novelty endpoints on nixus.pro for Magic 8-Ball answers, roasts, confessional text, last words, and Deadpool predictions with a 30 requests/minute rate limit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassh100k](https://clawhub.ai/user/cassh100k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call free interactive API tools for lightweight entertainment or novelty interactions without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted questions, names, confessions, last words, or predictions are sent to the external nixus.pro service.

Mitigation: Do not send secrets, API keys, private conversations, system prompts, personal data, or proprietary information.

Risk: The API is rate-limited to 30 requests per minute per IP.

Mitigation: Throttle requests and handle rate-limit or service failures before relying on responses in an agent workflow.

## Reference(s):

- [Nixus Tools API Catalog](https://nixus.pro/api/tools)
- [ClawHub Skill Page](https://clawhub.ai/cassh100k/skills/nixus-tools)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline bash code blocks and API response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [External HTTP calls to nixus.pro; no API key required; 30 requests/minute per IP.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
