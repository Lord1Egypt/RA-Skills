## Description: <br>
RAG and semantic search via OpenViking Context Database MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZaynJarvis](https://clawhub.ai/user/ZaynJarvis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to set up and connect an OpenViking MCP server for document Q&A, semantic search, knowledge-base retrieval, and adding selected files, directories, or URLs to vector memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently index local files, directories, and URLs without clear scoping, retention, or deletion guidance. <br>
Mitigation: Use it only for documents intentionally meant to be indexed, avoid broad private directories and secrets, and define retention and deletion practices before use. <br>
Risk: The OpenViking configuration file stores API keys used for embeddings and answer generation. <br>
Mitigation: Protect ov.conf, avoid committing it, restrict local file access, and rotate keys if they may have been exposed. <br>
Risk: The MCP server exposes search and resource-ingestion tools over a local HTTP endpoint. <br>
Mitigation: Keep the server bound to localhost, do not expose the port to untrusted networks, and verify the upstream repository before running setup. <br>


## Reference(s): <br>
- [OpenViking project repository referenced by the skill](https://github.com/volcengine/OpenViking) <br>
- [Volcengine Ark console for required API keys](https://console.volcengine.com/ark) <br>
- [OpenViking ClawHub release](https://clawhub.ai/ZaynJarvis/openviking-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides local setup, MCP connection, document search, and resource indexing workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: skill.yaml and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
