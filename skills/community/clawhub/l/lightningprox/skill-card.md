## Description:

Call AI models (Claude, GPT, Gemini, DeepSeek, Mistral and more) through LightningProx (lightningprox.com), paid per request in Bitcoin Lightning sats instead of provider API keys. Anthropic (/v1/messages) and OpenAI (/v1/chat/completions) formats, tool calling, streaming. Payment is L402 or an optional LightningProx spend token. Use it when the user wants a model answer billed through LightningProx and agrees to pay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request model responses through the LightningProx gateway and pay per request in Bitcoin Lightning sats. It supports Anthropic and OpenAI request formats, streaming, and tool calling when the selected model supports it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, conversation content, tool definitions and results, and image URLs are sent to LightningProx and forwarded to downstream model providers.

Mitigation: Only send content the user is comfortable sharing with those services; exclude secrets and personal data.

Risk: Paid requests use Lightning sats, and a spend token is a bearer credential.

Mitigation: Confirm the model and cost before a request, protect the token, fund a small budget, and check current pricing and expiry terms before paying.

## Reference(s):

- [LightningProx documentation](https://lightningprox.com/docs)
- [Live model list](https://lightningprox.com/v1/models)
- [Model pricing and capabilities](https://lightningprox.com/api/capabilities)
- [LightningProx ClawHub release](https://clawhub.ai/unixlamadev-spec/skills/lightningprox)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Model response text; API request and response JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Streaming and tool-call formats depend on the selected endpoint and model.]

## Skill Version(s):

4.1.0 (source: frontmatter, CHANGELOG.md; released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
