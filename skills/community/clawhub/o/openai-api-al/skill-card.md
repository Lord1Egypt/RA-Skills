## Description: <br>
Access OpenAI API capabilities for text generation, reasoning, embeddings, images, audio, and moderation with cost-conscious, safe, and model-appropriate guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to decide when and how to call OpenAI API tools for generation, embeddings, images, audio, moderation, structured extraction, and RAG workflows while controlling cost and handling errors safely. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive OpenAI credentials. <br>
Mitigation: Read the API key only from the environment or a secrets manager, never accept it as a tool argument, and never print the key or Authorization header. <br>
Risk: Paid OpenAI calls can create avoidable cost. <br>
Mitigation: Choose the cheapest capable model, set max_tokens or max_output_tokens on text calls, batch embeddings, cache repeat work, avoid uncontrolled loops, and report usage. <br>
Risk: Untrusted inputs or model outputs can create safety and prompt-injection issues. <br>
Mitigation: Moderate untrusted input before paid calls, refuse or sanitize flagged content, validate structured output, and do not execute returned code, commands, or URLs blindly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simonpierreboucher02/openai-api-al) <br>
- [OpenAI API reference](https://platform.openai.com/docs/api-reference) <br>
- [README](artifact/README.md) <br>
- [Model reference](artifact/reference/models.md) <br>
- [Endpoint reference](artifact/reference/endpoints.md) <br>
- [Parameter reference](artifact/reference/parameters.md) <br>
- [Best practices](artifact/reference/best-practices.md) <br>
- [Common errors](artifact/reference/common-errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with JSON examples, checklists, and reusable prompt templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes token caps, model selection, moderation, credential handling, caching, and usage reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
