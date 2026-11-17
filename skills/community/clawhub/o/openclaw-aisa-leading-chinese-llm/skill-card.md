## Description:

Configure AIsa as an OpenClaw provider for production access to Chinese LLMs including Qwen, DeepSeek, Kimi K2.5, and Doubao.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure AIsa API access, select supported Chinese model IDs, compare model pricing, and troubleshoot provider setup. It is intended for production-oriented model provider onboarding when the user has an AISA_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed through command arguments, shell history, screenshots, terminal recordings, logs, or support transcripts.

Mitigation: Use the environment-variable or masked interactive onboarding flow, avoid commands that place the key directly in arguments, avoid printing the full key during troubleshooting, and rotate any exposed key.

Risk: Model pricing, availability, and versioned model IDs may change after the artifact's published reference data.

Mitigation: Confirm current pricing and available model IDs through AIsa's marketplace pricing page or models endpoint before relying on quoted rates or IDs.

Risk: Kimi K2.5 requests fail when callers set a temperature other than 1.0.

Mitigation: Use the model default or explicitly set temperature to 1.0 for Kimi K2.5.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/aisadocs/skills/openclaw-aisa-leading-chinese-llm)
- [AIsa Marketplace](https://marketplace.aisa.one)
- [AIsa Pricing](https://marketplace.aisa.one/pricing)
- [AIsa Models Endpoint](https://api.aisa.one/v1/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes model IDs, pricing notes, provider setup commands, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
