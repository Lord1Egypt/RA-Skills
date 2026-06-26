## Description: <br>
Jarvis Mission Control for OpenCLAW AIS v2.1.1 is a self-hosted command center for OpenCLAW AI systems with kanban, chat, session tracking, cost metrics, GitHub Issues sync, webhook monitoring, a CLI console, and dashboard guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asif2bd](https://clawhub.ai/user/asif2bd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up, configure, and operate a Mission Control dashboard for coordinating OpenCLAW agents, local tasks, agent status, deliverables, and optional MissionDeck.ai connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Linked self-hosted application code and dependencies may affect the user's local environment when cloned, installed, or run. <br>
Mitigation: Audit the GitHub repository and dependencies before running install or server commands. <br>
Risk: GitHub and MissionDeck credentials may be exposed if configured with excessive privileges or stored insecurely. <br>
Mitigation: Use least-privilege credentials, protect API keys, and avoid committing local configuration files. <br>
Risk: Dashboard, SOUL editor, and reset workflows can expose or modify operational agent data if made available to untrusted users. <br>
Mitigation: Keep the dashboard local or access-controlled, restrict editor access, and back up .mission-control before reset or bulk data operations. <br>


## Reference(s): <br>
- [Setup Guide - Self-Hosted Mission Control](references/1-setup.md) <br>
- [MissionDeck.ai Cloud Connection](references/2-missiondeck-connect.md) <br>
- [mc CLI Reference](references/3-mc-cli.md) <br>
- [Data Population Guide](references/4-data-population.md) <br>
- [MissionDeck.ai Live Demo](https://missiondeck.ai/mission-control/demo) <br>
- [GitHub Self-Hosted Source](https://github.com/Asif2BD/JARVIS-Mission-Control-OpenClaw) <br>
- [MissionDeck.ai Cloud](https://missiondeck.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no commands execute automatically from the skill package.] <br>

## Skill Version(s): <br>
2.1.1 (source: frontmatter, server release evidence, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
