## Description: <br>
Agent memory with ALMA meta-learning, LLM fact extraction, and full-text search. Observer calls remote LLM APIs (OpenAI/Anthropic/Gemini). ALMA and Indexer work offline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arosstale](https://clawhub.ai/user/arosstale) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to add memory workflows for evolving memory designs, extracting structured facts from conversations, and searching workspace Markdown memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Observer can send conversation content to third-party LLM APIs. <br>
Mitigation: Use Observer only on chats and memory files that are appropriate to share with the selected provider, and add separate redaction controls for secrets, regulated data, or private user information. <br>
Risk: Observer may choose an environment API key fallback that does not match the intended provider. <br>
Mitigation: Pass an explicit apiKey for the selected provider instead of relying on environment-variable fallback. <br>


## Reference(s): <br>
- [Openclaw Memory on ClawHub](https://clawhub.ai/arosstale/openclaw-memories) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown and TypeScript API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Observer may return structured observations from LLM extraction; ALMA returns candidate memory designs and scores; Indexer returns ranked memory chunks.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
