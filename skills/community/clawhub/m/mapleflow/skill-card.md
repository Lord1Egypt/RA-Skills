## Description:

Call MapleFlow for AI chat, image generation, masked image erase, speech, transcription, embeddings, translation, weather, currency, and face comparison using one API key and credit balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kalven22](https://clawhub.ai/user/kalven22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use MapleFlow’s hosted API to perform chat, image, audio, embedding, translation, weather, currency, and face-comparison tasks through a single API key and credit balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted content is sent to MapleFlow’s cloud services and may be processed by other providers.

Mitigation: Review MapleFlow’s privacy policy and avoid sending sensitive material unless its use is approved.

Risk: API calls consume credits and may incur usage costs.

Mitigation: Check the account balance and recent usage before making calls; create a checkout only when the user requests a purchase.

Risk: The optional local MCP server introduces a third-party package and local execution.

Mitigation: Review and pin the package version and limit its permissions.

Risk: An exposed API key could enable unauthorized account use.

Mitigation: Keep MAPLEFLOW_API_KEY out of messages and logs.

## Reference(s):

- [MapleFlow API documentation](https://api.mapleflow.io/docs)
- [MapleFlow OpenAPI specification](https://api.mapleflow.io/openapi.json)
- [MapleFlow model catalog](https://api.mapleflow.io/v1/models)
- [MapleFlow MCP endpoint](https://api.mapleflow.io/mcp)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with curl examples and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API results may include text, structured data, or encoded media, depending on the requested service.]

## Skill Version(s):

0.34.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
