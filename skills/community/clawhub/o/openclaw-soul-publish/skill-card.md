## Description: <br>
Openclaw Soul Publish deploys a persistent OpenClaw self-evolution framework with workspace files, memory structure, heartbeat configuration, identity evolution, and self-improvement support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kianzzz](https://clawhub.ai/user/Kianzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to bootstrap a self-evolving OpenClaw workspace with governance files, memory templates, dependency skills, and a guided first-run personality setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent memory, edits global OpenClaw configuration, and can modify SOUL-related files. <br>
Mitigation: Review the deployment plan before execution, keep backups of overwritten files, and require approval for identity or governance changes. <br>
Risk: External feeds, recurring network ingestion, and credential handling can expand the skill's access beyond the local workspace. <br>
Mitigation: Leave external feeds disabled unless needed, avoid pasting API tokens into setup, and review any shell-profile or credential storage before use. <br>
Risk: The security verdict is suspicious because of broad artifact behavior, even though static scan was clean and VirusTotal was pending. <br>
Mitigation: Scan and review the skill before deployment, then install it only in workspaces where a persistent self-evolving agent is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kianzzz/openclaw-soul-publish) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Preflight check script](artifact/scripts/preflight_check.py) <br>
- [OpenClaw agent template](artifact/references/agents-template.md) <br>
- [Bootstrap guide](artifact/references/bootstrap-guide.md) <br>
- [Self-Improving Agent reference](https://clawic.com/skills/self-improving) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown workspace files, JSON configuration, shell commands, and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates OpenClaw workspace files, memory directories, dependency skill directories, and heartbeat configuration after environment checks and backups.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
