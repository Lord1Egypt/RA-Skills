## Description: <br>
Answer official-doc-grounded support questions about Claude, OpenAI/GPT, and Gemini model availability across Bedrock, Vertex AI, Azure, OpenAI, and Gemini API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derekhsu529](https://clawhub.ai/user/derekhsu529) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support teams use this skill to answer model availability and capability questions across Claude, OpenAI/GPT, and Gemini provider surfaces with official documentation. It is intended for provider-specific guidance where hosted model support, regions, API versions, and capabilities may differ. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider-hosted model support can differ from first-party model documentation or change after release, which can lead to incorrect availability or capability claims. <br>
Mitigation: Check the official documentation for the exact provider surface, model version, API version, and region; mark unsupported or unclear claims as unknown_needs_live_check. <br>
Risk: Registry edits could introduce stale or unofficial sources into future support answers. <br>
Mitigation: Run scripts/check-sources.mjs after registry changes and keep source entries limited to official provider documentation. <br>


## Reference(s): <br>
- [Capability Taxonomy](references/capability-taxonomy.md) <br>
- [Provider Differences](references/provider-differences.md) <br>
- [QA Cases](references/qa-cases.md) <br>
- [Source Registry](references/source-registry.json) <br>
- [Anthropic Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock) <br>
- [Anthropic Claude on Vertex AI](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai) <br>
- [AWS Bedrock Supported Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) <br>
- [AWS Bedrock Anthropic Claude Messages Parameters](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-anthropic-claude-messages.html) <br>
- [Google Cloud Vertex AI Claude Partner Models](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) <br>
- [Azure OpenAI Models](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models) <br>
- [Azure OpenAI API Reference](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference) <br>
- [OpenAI Models](https://platform.openai.com/docs/models) <br>
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference) <br>
- [Google Cloud Vertex AI Gemini Models](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models) <br>
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with official-source citations and conservative status labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May mark unverified capabilities as unknown_needs_live_check when current official docs are unavailable or conflicting] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
