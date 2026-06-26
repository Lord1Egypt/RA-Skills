## Description: <br>
AI-native configuration and setup guides for OpenClaw <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxzyma](https://clawhub.ai/user/maxzyma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to apply OpenClaw setup guides for multi-agent operation, memory optimization, monitoring, provider routing, and cost controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guides can enable autonomous background agents, heartbeat checks, cron jobs, persistent memory, and broad OpenClaw configuration changes. <br>
Mitigation: Review generated openclaw.json and AGENTS.md changes before applying them, keep cron, heartbeat, and autoSpawn disabled until needed, and require human review for worker code changes. <br>
Risk: Provider routing, webhook notifications, and environment-variable setup can expose sensitive API keys or route prompts to unintended services. <br>
Mitigation: Store API keys only in the protected ~/.openclaw/.env file, verify webhook destinations, and confirm provider-routing privacy implications before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maxzyma/ohmyopenclaw) <br>
- [Publisher Profile](https://clawhub.ai/user/maxzyma) <br>
- [Setup Guides Index](guides/_index.md) <br>
- [Agent Swarm Architecture Guide](guides/agent-swarm.md) <br>
- [Memory Optimization Guide](guides/memory-optimized.md) <br>
- [Proactive Monitoring Guide](guides/monitor.md) <br>
- [Chinese Providers Guide](guides/chinese-providers.md) <br>
- [Cost Optimization Guide](guides/cost-optimization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown setup guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to OpenClaw configuration, AGENTS.md, workspace task directories, monitoring settings, provider routing, and environment variable setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
