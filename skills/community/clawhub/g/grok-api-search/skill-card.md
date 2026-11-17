## Description:

Uses the Grok API to perform web searches, with a default relay endpoint intended to reduce cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xianyu110](https://clawhub.ai/user/xianyu110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to query real-time information through a Grok-compatible chat completions endpoint. It is intended for search-style prompts where concise answers with sources are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default relay endpoint can receive the user's API key and full search query text.

Mitigation: Set GROK_API_URL explicitly to the official xAI endpoint or another endpoint the user trusts before running the skill.

Risk: Sensitive prompts may be transmitted to the configured API endpoint.

Mitigation: Avoid sensitive searches and rotate any official key that may have been sent to the default relay.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xianyu110/skills/grok-api-search)
- [xAI API endpoint](https://api.x.ai/v1)
- [xAI console](https://console.x.ai/)
- [Default relay endpoint](https://apipro.maynor1024.live/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown returned by a shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GROK_API_KEY, GROK_API_URL, and GROK_MODEL environment variables; script requests up to 2000 output tokens.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
