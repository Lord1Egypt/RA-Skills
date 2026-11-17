## Description:

秒秒AI助理 invokes a Link-AI multi-capability assistant for chat, weather, news, package tracking, image generation, web search, summarization, charts, maps, and train-ticket queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agleameal](https://clawhub.ai/user/agleameal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send natural-language requests to a third-party Link-AI assistant that selects practical services such as chat, weather, news, package tracking, search, summarization, charts, maps, train-ticket lookup, and image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private prompts, documents, locations, shipment numbers, travel plans, or account-sensitive data may be sent to an external assistant.

Mitigation: Use the skill only when the user clearly intends to call the external assistant and avoid sending sensitive data unless approved for that deployment.

Risk: Broad auto-triggering can invoke the assistant for many unrelated requests.

Mitigation: Review trigger behavior before installation and constrain invocation to explicit user requests for the listed services.

Risk: Debug logging can expose request payloads or responses.

Mitigation: Keep debug logging disabled in normal use and avoid collecting logs that contain prompts, credentials, or service results.

Risk: A configurable API destination can redirect requests to an untrusted host.

Mitigation: Do not set MIAOMIAO_API_URL to untrusted hosts; validate the destination before deployment.

Risk: Documentation references LINKAI_* variables while the SDK uses MIAOMIAO_* variables.

Mitigation: Reconcile environment variable names before deployment so credentials are configured intentionally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agleameal/skills/miaomiao-ai)
- [Link-AI platform](https://link-ai.tech)
- [Link-AI chat completions endpoint](https://api.link-ai.tech/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown or plain text responses, with Python code examples and environment variable configuration when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return service-specific content for weather, news, package tracking, web search, summaries, charts, maps, train-ticket lookup, and image generation through the external Link-AI assistant.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is v1.2.0 dated 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
