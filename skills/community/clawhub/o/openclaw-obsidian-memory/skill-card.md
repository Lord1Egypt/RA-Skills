## Description: <br>
OpenClaw Obsidian Memory helps an agent set up and use an Obsidian-style local vault for persistent memory, dual-channel retrieval, backlink management, and optional scheduled memory archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[masterxiaogu](https://clawhub.ai/user/masterxiaogu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure a local Obsidian vault as durable agent memory, retrieve notes before answering, create structured notes, and optionally schedule daily and weekly memory summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and configuration changes can modify AGENTS.md, MEMORY.md, and vault notes. <br>
Mitigation: Back up affected files and review generated patches before applying them. <br>
Risk: Unattended archival jobs can preserve sensitive conversations or keep running after they are no longer wanted. <br>
Mitigation: Enable cron jobs only intentionally, choose the timezone yourself, avoid storing secrets or sensitive conversations, and confirm you can inspect and remove stored notes and scheduled tasks. <br>
Risk: Local vault search and note creation can expose or retain sensitive knowledge over time. <br>
Mitigation: Limit vault access and keep secrets or private conversations out of the vault. <br>


## Reference(s): <br>
- [OpenClaw Obsidian Memory release page](https://clawhub.ai/masterxiaogu/openclaw-obsidian-memory) <br>
- [Note templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JavaScript script usage, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file updates, vault note creation, and scheduled archival tasks for user review.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
