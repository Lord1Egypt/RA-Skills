## Description: <br>
Lightweight agent productivity toolkit: semantic code search with embeddings and a categorized prompt library. Two services, ~200MB RAM, zero cloud dependencies. Your agent searches code by meaning (not grep) and reuses proven prompts instead of writing from scratch every time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to set up local semantic code search and a reusable prompt library for faster repository navigation and prompt reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local services can repeatedly index private source code. <br>
Mitigation: Use the skill only on trusted local repositories, define narrow index roots, and exclude secrets, credentials, dependency folders, generated files, and private data. <br>
Risk: The SQLite code-search database may contain sensitive repository content or summaries. <br>
Mitigation: Protect the database with filesystem permissions and delete old indexes when they are no longer needed. <br>
Risk: PM2 services and the cron re-index job can keep running after evaluation. <br>
Mitigation: Document how to stop PM2 services, remove the cron job, and clean up generated indexes before installation in shared environments. <br>


## Reference(s): <br>
- [Ops Deck Lite ClawHub release](https://clawhub.ai/solomonneas/ops-deck-lite) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, JavaScript, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and integration guidance for FastAPI, Express, SQLite, Ollama, PM2, and cron-based indexing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
