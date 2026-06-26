## Description: <br>
Nex Skillmon monitors installed OpenClaw skills, estimates usage costs, identifies stale or flagged skills, checks for updates, and exports health reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, power users, and teams managing OpenClaw skill installations use this skill to inventory skills, review health and security signals, estimate API costs, manage budgets, and produce Markdown or JSON reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inventories installed skills and update or check commands may send installed skill names to the configured ClawHub API. <br>
Mitigation: Review before installing in sensitive environments, use a narrow skills directory, and run network-backed checks only when sharing skill names with ClawHub is acceptable. <br>
Risk: Configuration values are stored and logged locally, which could expose tokens, passwords, or internal endpoints if users place them in the config command. <br>
Mitigation: Avoid storing secrets or internal endpoints with the config command and review local files under ~/.nex-skillmon/ before sharing reports or logs. <br>
Risk: Security evidence marks the release for review rather than clean approval because VirusTotal was pending and artifact behavior includes local inventory and remote checks. <br>
Mitigation: Review and scan the artifact before deployment, especially in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-skillmon) <br>
- [Publisher profile](https://clawhub.ai/user/nexaiguy) <br>
- [Project homepage](https://nex-ai.be) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output with optional Markdown or JSON report exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and local configuration for SKILLS_BASE_DIR and CLAWHUB_API_URL. Stores monitoring data locally under ~/.nex-skillmon/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
