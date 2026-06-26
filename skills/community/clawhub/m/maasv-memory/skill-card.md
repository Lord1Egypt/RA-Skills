## Description: <br>
Provides structured long-term memory for OpenClaw agents with semantic, keyword, and knowledge graph retrieval, entity extraction, temporal versioning, and experiential learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ascottbell](https://clawhub.ai/user/ascottbell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to add self-hosted long-term memory to OpenClaw conversations, including recall, storage, deletion, graph search, and decision-history lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The memory server stores conversation-derived memories locally and can persist sensitive information. <br>
Mitigation: Install only when long-term memory is desired, review captured data, protect the local database, and use memory deletion tools when information should not persist. <br>
Risk: Entity extraction and semantic search may call the user's configured LLM or embedding provider. <br>
Mitigation: Keep provider API keys private and use local providers such as Ollama for conversations that should not be sent to cloud services. <br>
Risk: The skill depends on external maasv and @maasv/openclaw-memory packages. <br>
Mitigation: Review the referenced packages and install them only from trusted package indexes before enabling automatic recall or capture. <br>


## Reference(s): <br>
- [maasv Memory on ClawHub](https://clawhub.ai/ascottbell/maasv-memory) <br>
- [@maasv/openclaw-memory on npm](https://www.npmjs.com/package/@maasv/openclaw-memory) <br>
- [maasv on PyPI](https://pypi.org/project/maasv/) <br>
- [maasv source](https://github.com/ascottbell/maasv) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides setup of a local memory server, OpenClaw memory plugin configuration, and memory-related agent tools.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
