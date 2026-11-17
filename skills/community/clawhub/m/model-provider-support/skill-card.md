## Description:

Answer official-doc-grounded support questions about Claude, OpenAI/GPT, and Gemini model availability across Bedrock, Vertex AI, Azure, OpenAI, and Gemini API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derekhsu529](https://clawhub.ai/user/derekhsu529)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use this skill to answer provider-specific model support questions across Claude, OpenAI/GPT, and Gemini hosted surfaces. It helps keep answers conservative by requiring official provider documentation for model availability, regions, API surfaces, and capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted model support can change as providers update models, regions, and API versions.

Mitigation: Check the current official provider documentation for the exact model, hosted surface, API version, region, and capability before relying on a support conclusion.

Risk: First-party model documentation can be mistaken for proof that a hosted cloud-provider surface supports the same feature.

Mitigation: Use first-party documentation only for first-party API claims or comparison context, and require hosting-provider documentation for hosted support claims.

Risk: Unavailable, stale, or conflicting documentation can lead to overconfident answers.

Mitigation: State the documentation access or conflict clearly and mark the capability as unknown when current official docs do not confirm it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/derekhsu529/skills/model-provider-support)
- [Capability Taxonomy](references/capability-taxonomy.md)
- [Provider Differences](references/provider-differences.md)
- [QA Cases](references/qa-cases.md)
- [Source Registry](references/source-registry.json)
- [Anthropic Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock)
- [Anthropic Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai)
- [Amazon Bedrock supported models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [Amazon Bedrock Anthropic Claude messages parameters](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html)
- [Vertex AI Claude partner models](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude)
- [Azure OpenAI model docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models)
- [Azure OpenAI API reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference)
- [OpenAI model docs](https://platform.openai.com/docs/models)
- [OpenAI API reference](https://platform.openai.com/docs/api-reference)
- [Vertex AI Gemini models](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models)
- [Gemini API docs](https://ai.google.dev/gemini-api/docs)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text answers with citations and conservative status labels when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require live official-documentation checks because provider support can change.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
