## Description:

Agent memory with ALMA meta-learning, LLM fact extraction, and full-text search, where Observer calls remote LLM APIs (OpenAI/Anthropic/Gemini) and ALMA and Indexer work offline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arosstale](https://clawhub.ai/user/arosstale)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to add memory workflows for evolving memory designs, extracting structured facts from conversations, and searching Markdown-based workspace memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A credential-handling flaw can send an API key to the wrong LLM provider when relying on fallback environment variables.

Mitigation: Use explicit provider-specific apiKey values and avoid passing private conversation history to Observer unless the selected LLM provider is approved for that data.

Risk: Observer sends conversation history to remote LLM APIs when extraction is enabled.

Mitigation: Use Observer only with approved providers and data classes; keep ALMA and Indexer for offline-only memory workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arosstale/skills/openclaw-memory-2)
- [Publisher Profile](https://clawhub.ai/user/arosstale)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration, Guidance]

**Output Format:** [TypeScript API outputs including structured observations, memory design records, and ranked search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Observer may call remote LLM APIs when configured; ALMA and Indexer operate offline.]

## Skill Version(s):

2.0.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
