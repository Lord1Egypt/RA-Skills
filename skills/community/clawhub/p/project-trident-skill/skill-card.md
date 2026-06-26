## Description: <br>
Give your AI agent genuine continuity, identity, and resilience across every session and deployment with a four-tier persistent memory stack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shivaclaw](https://clawhub.ai/user/shivaclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Project Trident to add durable memory, signal routing, semantic organization, and recovery workflows to OpenClaw agents. It is intended for agents that need continuity across sessions, crashes, migrations, and deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and organize long-lived conversation and workspace data, including sensitive personal or business context. <br>
Mitigation: Define what may be remembered before enabling it, exclude secrets and sensitive data, and regularly inspect, edit, delete, or purge stored memory. <br>
Risk: Optional cron routing, semantic indexing, cloud models, Git backup, or VPS snapshots can process or move memory outside the immediate agent session. <br>
Mitigation: Use local models or private encrypted backups for sensitive work, disable optional networked components when not needed, and confirm how to stop scheduled jobs. <br>
Risk: Automated memory migration and routing can persist incorrect or unwanted context if enabled without review. <br>
Mitigation: Preview migrations with dry-run behavior where available, review generated memory files and routing prompts, and keep backups before applying changes. <br>


## Reference(s): <br>
- [Project Trident skill page](https://clawhub.ai/shivaclaw/project-trident-skill) <br>
- [Project Trident repository](https://github.com/ShivaClaw/project-trident) <br>
- [Project Trident issue tracker](https://github.com/ShivaClaw/project-trident/issues) <br>
- [Project homepage](https://github.com/ShivaClaw/shiva-memory) <br>
- [Trident Lite](references/trident-lite.md) <br>
- [Deployment Guide](references/deployment-guide.md) <br>
- [Platform Guide](references/platform-guide.md) <br>
- [Cost Calculator](references/cost-calculator.md) <br>
- [Cost Tuning](references/cost-tuning.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file paths, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce migration, cron, backup, and integrity-check instructions for persistent agent memory.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
