## Description: <br>
Search and manage knowledge bases using LightRAG API. Supports multiple servers, context-aware writing, and direct information retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RuslanLanket](https://clawhub.ai/user/RuslanLanket) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure LightRAG API servers, query knowledge bases in supported retrieval modes, and reuse returned context for writing or analysis tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper disables HTTPS certificate verification, which can expose queries and API keys to interception. <br>
Mitigation: Enable normal TLS certificate verification and use trusted certificates before sending API keys, private documents, or sensitive queries. <br>
Risk: Server configuration may include API keys stored in the local LightRAG config file. <br>
Mitigation: Protect the local config file with appropriate filesystem permissions and avoid sharing it with logs, prompts, or generated artifacts. <br>
Risk: Retrieved knowledge-base text may contain untrusted or misleading content. <br>
Mitigation: Treat retrieved context as reference material and review it before following instructions or using it in downstream work. <br>


## Reference(s): <br>
- [LightRAG API Reference](references/API_DOCS.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/RuslanLanket/lightrag) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command-line invocations and plain-text query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured LightRAG server alias; query output depends on the connected knowledge base.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
