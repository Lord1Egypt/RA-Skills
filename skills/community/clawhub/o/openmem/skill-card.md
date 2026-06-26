## Description: <br>
SQLite long-term memory compression system for extended memory life. Adds tools for agents to control their memory functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danavfrost](https://clawhub.ai/user/danavfrost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use OpenMem to preserve selected long-term memories across agent sessions, search them later, and inject top memories into new sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can install recurring automation that reads private session transcripts and may overwrite older session logs after compression. <br>
Mitigation: Install only when persistent memory is intended; consider disabling the cron job, running compression with --no-wipe, and keeping backups of session logs. <br>
Risk: Selected memories and the cache are stored locally in plaintext. <br>
Mitigation: Avoid storing secrets or personal data, and review, protect, export, or delete the local database and cache as needed. <br>


## Reference(s): <br>
- [OpenMem ClawHub listing](https://clawhub.ai/danavfrost/openmem) <br>
- [OpenMem database schema](references/schema.md) <br>
- [OpenAuto integration](https://clawhub.ai/halthelobster/openauto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [MCP tool responses, CLI text, and Markdown bootstrap context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores selected memory records in a local SQLite database and plaintext cache.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and skill heading) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
