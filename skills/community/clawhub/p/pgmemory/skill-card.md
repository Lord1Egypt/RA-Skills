## Description:

Persistent semantic memory for OpenClaw agents using PostgreSQL and pgvector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbushman](https://clawhub.ai/user/jbushman)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Pgmemory to give OpenClaw agents persistent, searchable semantic memory for decisions, constraints, infrastructure facts, preferences, task context, and sub-agent findings across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can make persistent local changes such as PostgreSQL or Docker setup, migrations, AGENTS.md scaffolding, and a decay cron job.

Mitigation: Review the setup flow before running it, prefer an existing secured local PostgreSQL service, and inspect AGENTS.md and cron changes before accepting them.

Risk: The Docker example uses a default database password and exposes PostgreSQL on a local host port.

Mitigation: Bind PostgreSQL to localhost only and replace default credentials with a generated password before storing useful or sensitive memories.

Risk: Memories and embedding requests can contain secrets, production connection details, or other sensitive context.

Mitigation: Do not store secrets or production credentials as memories; use local embeddings through Ollama for sensitive data when possible.

Risk: API keys may be stored directly in pgmemory.json.

Mitigation: Keep API keys out of pgmemory.json unless file permissions are locked down, or use environment variables for provider credentials.

## Reference(s):

- [Pgmemory reference schema](references/schema.sql)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [pgvector](https://github.com/pgvector/pgvector)
- [Voyage AI](https://www.voyageai.com)
- [OpenAI platform](https://platform.openai.com)
- [Ollama](https://ollama.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and script usage patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local scripts that write memories, query memories, manage PostgreSQL migrations, scaffold AGENTS.md, and configure decay jobs.]

## Skill Version(s):

1.2.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
