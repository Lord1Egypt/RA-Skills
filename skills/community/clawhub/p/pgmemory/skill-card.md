## Description: <br>
Persistent semantic memory for OpenClaw agents using PostgreSQL and pgvector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jbushman](https://clawhub.ai/user/jbushman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use pgmemory to set up, query, maintain, and synchronize persistent semantic memory for OpenClaw agents across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can capture sensitive project details and may send memory text to the configured embedding provider. <br>
Mitigation: Avoid storing secrets or regulated data, choose local embeddings such as Ollama for sensitive projects, and review memory contents before writing them. <br>
Risk: Setup can make lasting changes such as running a local database, modifying AGENTS.md, configuring cron, or changing host setup. <br>
Mitigation: Run setup interactively, review AGENTS.md and configuration changes before relying on them, and avoid setup.py --yes unless those host changes are acceptable. <br>
Risk: pgmemory.json may contain an embedding API key. <br>
Mitigation: Protect the config file, limit file access, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [Pgmemory skill page](https://clawhub.ai/jbushman/pgmemory) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [pgvector](https://github.com/pgvector/pgvector) <br>
- [Voyage AI](https://www.voyageai.com) <br>
- [OpenAI platform](https://platform.openai.com) <br>
- [Ollama](https://ollama.ai) <br>
- [Schema reference](references/schema.sql) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; scripts emit plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PostgreSQL with pgvector and a configured embedding provider.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
