## Description: <br>
Manages digital garden notes, link structures, and health metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and knowledge-base curators use this skill to organize living notes, maintain bidirectional links, track content maturity, and plan maintenance for digital gardens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may cause the skill to activate during general knowledge-base or documentation curation work. <br>
Mitigation: Use explicit prompts when requesting note edits or reorganization, and review proposed changes before applying them. <br>
Risk: Suggested commands and templates may not match a user's local garden layout or available scripts. <br>
Mitigation: Verify command availability with help or environment checks and adapt generated paths, YAML fields, and maintenance schedules to the local repository before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-memory-palace-digital-garden-cultivator) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace) <br>
- [artifact/modules/linking-patterns.md](artifact/modules/linking-patterns.md) <br>
- [artifact/modules/maintenance.md](artifact/modules/maintenance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose note structures, link patterns, maintenance schedules, and garden health metrics.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
