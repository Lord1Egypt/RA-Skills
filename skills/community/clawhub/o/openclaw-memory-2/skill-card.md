## Description: <br>
Agent memory with ALMA meta-learning, LLM fact extraction, and full-text search. Observer calls remote LLM APIs (OpenAI/Anthropic/Gemini). ALMA and Indexer work offline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arosstale](https://clawhub.ai/user/arosstale) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to add memory workflows for OpenClaw agents, including offline memory design exploration, structured fact extraction from conversations, and search across Markdown memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Observer can send full conversation text to the configured external LLM provider. <br>
Mitigation: Use Observer only with conversations approved for that provider and review provider data handling before deployment. <br>
Risk: Observer may use a fallback environment API key if an explicit key is not supplied. <br>
Mitigation: Pass the intended provider-specific apiKey explicitly and avoid relying on environment fallback. <br>
Risk: Indexer searches local memory directories selected by the caller. <br>
Mitigation: Point Indexer only at workspaces and memory directories intended for search. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/arosstale/openclaw-memory-2) <br>
- [Publisher profile](https://clawhub.ai/user/arosstale) <br>
- [Project source link from skill text](https://github.com/arosstale/openclaw-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and structured memory observations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Observer may return structured observation objects; ALMA returns proposed and evaluated memory designs; Indexer returns ranked search results from local Markdown memory files.] <br>

## Skill Version(s): <br>
2.0.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
