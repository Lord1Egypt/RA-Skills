## Description: <br>
Sets up a local Mac Mini knowledge base and RAG search workflow with document parsing, Ollama embeddings, scheduled analysis, and optional Feishu summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seairteng](https://clawhub.ai/user/seairteng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical operators use this skill to configure a local Mac Mini knowledge base, parse common document formats, generate searchable summaries, and register OpenClaw scheduled analysis jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill parses files placed in the local knowledge directory and writes plaintext summaries. <br>
Mitigation: Avoid placing confidential files in the knowledge directory unless plaintext local summaries are acceptable. <br>
Risk: The setup enables OpenClaw exec/process tools, installs local dependencies, and creates scheduled jobs. <br>
Mitigation: Review the setup script and scheduled job commands before installation, and enable only the permissions required for the deployment. <br>
Risk: Optional Feishu delivery may send generated summaries outside the local machine. <br>
Mitigation: Skip or remove the Feishu cron setup when external notification delivery is not appropriate. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seairteng/macmini-knowledge-base) <br>
- [Ollama download](https://ollama.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup guidance and scripts for document analysis, catalog generation, scheduled jobs, and optional Feishu notifications.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
