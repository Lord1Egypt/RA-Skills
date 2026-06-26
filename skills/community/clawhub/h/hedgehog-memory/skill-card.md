## Description: <br>
Radial memory architecture for AI agents - infinite persistent memory with hierarchical compression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vvxer](https://clawhub.ai/user/vvxer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use HedgehogMemory to give agents durable cross-session memory, retrieve relevant prior work, and drill from compact summaries to recoverable full context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to retain recoverable session history indefinitely in origin.json. <br>
Mitigation: Use a dedicated HEDGEHOG_MEMORY_PATH, review stored memory regularly, and redact or delete sensitive content according to the deployment's data retention policy. <br>
Risk: Configured OpenAI or LiteLLM summarizers can send memory content to external LLM providers. <br>
Mitigation: Prefer the built-in local keyword summarizer for confidential work, or approve provider use only after confirming data handling requirements. <br>
Risk: Stored full-context memory may include secrets, raw transcripts, file paths, environment details, or other sensitive operational data. <br>
Mitigation: Do not commit origin.json, avoid saving secrets in session logs, and treat memory backups as sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vvxer/hedgehog-memory) <br>
- [Publisher profile](https://clawhub.ai/user/vvxer) <br>
- [GitHub repository](https://github.com/vvxer/HedgehogMemory) <br>
- [GitHub issues](https://github.com/vvxer/HedgehogMemory/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Python API return values, JSON-backed memory files, and Markdown/code guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores durable memory in origin.json; can use local keyword summarization by default or external LLM summarizers when configured.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
