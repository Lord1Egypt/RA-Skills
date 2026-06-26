## Description: <br>
Sets up and operates a personal knowledge system using Supabase pgvector and OpenRouter to capture, classify, route, and semantically search thoughts, people, projects, ideas, and admin tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justfinethanku](https://clawhub.ai/user/justfinethanku) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and personal-knowledge users use this skill to configure an agent-backed second brain that stores captured notes, classifies them with an LLM, routes them into structured tables, and retrieves them with semantic search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores private notes in Supabase and sends captured text and search queries to OpenRouter or model providers for AI processing. <br>
Mitigation: Use a dedicated personal Supabase project, protect and rotate the Supabase service-role key and OpenRouter key, avoid capturing secrets or highly sensitive third-party communications, and review OpenRouter and model-provider data policies before use. <br>


## Reference(s): <br>
- [Conceptual Framework](artifact/references/concepts.md) <br>
- [First-Time Setup](artifact/references/setup.md) <br>
- [Database Schema](artifact/references/schema.md) <br>
- [Ingest Pipeline](artifact/references/ingest.md) <br>
- [Retrieval Operations](artifact/references/retrieval.md) <br>
- [OpenRouter API Patterns](artifact/references/openrouter.md) <br>
- [Project homepage](https://natebjones.com) <br>
- [ClawHub listing](https://clawhub.ai/justfinethanku/nate-jones-second-brain) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash, SQL, JSON, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, and OPENROUTER_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
