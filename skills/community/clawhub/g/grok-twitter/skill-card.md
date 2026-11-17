## Description:

Query and summarize Twitter/X trends, tweets, X platform content, and other Twitter-related information using Grok AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danetteceola](https://clawhub.ai/user/danetteceola)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to send Twitter/X-related prompts to Grok and receive summarized answers about trends, topics, tweets, or specific accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the bearer API key are sent to the configured third-party endpoint.

Mitigation: Use a narrowly scoped, revocable API key and set GROK_API_URL only to a trusted, organization-approved endpoint.

Risk: Sensitive prompt content may be exposed to the configured API provider.

Mitigation: Avoid sensitive prompts and review the endpoint's privacy and data-handling terms before use.

Risk: The default endpoint lacks enough disclosure and endpoint safeguards in the supplied evidence.

Mitigation: Prefer a version with host allowlisting, clear endpoint ownership, and explicit privacy disclosure.

## Reference(s):

- [Grok Twitter Query ClawHub Page](https://clawhub.ai/danetteceola/skills/grok-twitter)
- [Publisher Profile](https://clawhub.ai/user/danetteceola)
- [Default API Endpoint Configured by Skill](https://api.cheaprouter.club/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text responses from an API-backed command-line script, with setup guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GROK_API_KEY; optional GROK_API_URL and GROK_MODEL environment variables control the endpoint and model.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
