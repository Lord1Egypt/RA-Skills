## Description:

Ask questions and get AI-synthesized answers backed by live web search, via Kagi's FastGPT API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelazar](https://clawhub.ai/user/joelazar)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to ask factual or current-information questions and receive a synthesized answer with cited web references through Kagi FastGPT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper may download and run a latest prebuilt binary from the publisher's GitHub releases on first use.

Mitigation: Prefer building from the included Go source or independently verify a pinned release artifact before running the skill.

Risk: Queries are sent to the Kagi FastGPT API and may include sensitive user-provided text.

Mitigation: Do not send secrets, credentials, private URLs, or confidential internal content as FastGPT queries.

Risk: The skill depends on a Kagi account, API key, billing setup, and external API availability.

Mitigation: Confirm KAGI_API_KEY is configured and that account billing and service availability meet the deployment requirements.

## Reference(s):

- [Kagi FastGPT API documentation](https://help.kagi.com/kagi/api/fastgpt.html)
- [Kagi API portal](https://kagi.com/settings/api)
- [ClawHub skill listing](https://clawhub.ai/joelazar/skills/kagi-fastgpt)

## Skill Output:

**Output Type(s):** [Text, JSON, References, Shell commands, Guidance]

**Output Format:** [Plain text with numbered references, or structured JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token usage and API balance are emitted to stderr when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
