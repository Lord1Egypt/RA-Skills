## Description: <br>
Build, maintain, and extend Horus, a local-first technology and event intelligence terminal currently configured for MWC 2026 Barcelona event monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trungviet17](https://clawhub.ai/user/trungviet17) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and event-intelligence users use this skill to maintain Horus relay ingestion, local data stores, dashboard behavior, and agent chat workflows for MWC 2026 technology monitoring. The skill also guides user-facing summaries from Horus data across web and external chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates shared context across external chat channels and the Horus web dashboard, which may expose sensitive or stale information without clear consent boundaries. <br>
Mitigation: Use the skill only when shared cross-channel memory is intentional, review MEMORY.md periodically, and avoid storing secrets or unnecessary sensitive data in durable memory. <br>
Risk: The local agent bridge and relay can create unintended access paths if exposed beyond localhost without controls. <br>
Mitigation: Keep the relay bound to localhost or place it behind authentication before exposure, use revocable tokens, and sanitize bridge errors before returning them to users. <br>
Risk: The workflow depends on credentials for upstream services and OpenClaw session routing. <br>
Mitigation: Store credentials only in .env files, never commit tokens or runtime data, and rotate credentials after accidental exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trungviet17/mwc-2026-horus) <br>
- [Publisher profile](https://clawhub.ai/user/trungviet17) <br>
- [J7 credential onboarding Discord](https://discord.gg/CEcatgcq) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and concise user-facing summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local project memory files when notable announcements or architectural changes occur.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
