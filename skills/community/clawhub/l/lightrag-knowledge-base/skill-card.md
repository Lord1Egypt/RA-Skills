## Description: <br>
Deploy LightRAG as a shared knowledge graph for OpenClaw agents to query cross-agent knowledge, auto-index daily logs, and search entity relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mosoonpi-ai](https://clawhub.ai/user/mosoonpi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to deploy a shared LightRAG-backed knowledge graph so multiple OpenClaw agents can search historical decisions, daily logs, entities, and relationships across workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private agent files, secrets, or personal data could be indexed into a persistent cross-agent graph. <br>
Mitigation: Use explicit file allowlists, redact secrets and personal data before indexing, and document how to remove mistakenly indexed content. <br>
Risk: A shared memory service can expose stored knowledge to agents that should not read or write it. <br>
Mitigation: Protect API keys, decide which agents may access the service, keep credentials separate, and bind the service to localhost unless a reviewed network design requires otherwise. <br>
Risk: Automatic daily-log indexing can ingest new content before review. <br>
Mitigation: Keep cron-based indexing disabled until reviewed, then enable it only for approved workspaces and file patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mosoonpi-ai/lightrag-knowledge-base) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Docker Compose, environment, Python, Bash, and cron examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides setup of a persistent shared memory service; users must provide their own API keys, model endpoints, and file selection policy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
