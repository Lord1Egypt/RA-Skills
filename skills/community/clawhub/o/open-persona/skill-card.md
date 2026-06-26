## Description: <br>
Meta-skill for building and managing agent persona skill packs, including creating, installing, managing, and publishing personas through explicit user-approved CLI actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neiljo-gy](https://clawhub.ai/user/neiljo-gy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create, configure, install, manage, and publish persona skill packs for SKILL.md-compatible agents. It helps agents draft persona.json files, choose faculties and skills, run explicit OpenPersona CLI commands, and review generated persona behavior before activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help change local agent personas and alter how an agent behaves across future sessions. <br>
Mitigation: Review generated persona.json and SKILL.md files before installing, switching, or publishing a persona. <br>
Risk: Publish, register, contribute, search, and install flows may invoke external CLIs, registries, or network services. <br>
Mitigation: Approve these commands one by one, use dry-run modes when available, and only run them against registries and repositories you trust. <br>
Risk: Optional memory, heartbeat, economy, voice/avatar, ACN, wallet, and external skill features can involve sensitive credentials or personal data. <br>
Mitigation: Enable only the features and data sources you are comfortable sharing, keep credentials out of generated packs, and review local files before distribution. <br>


## Reference(s): <br>
- [OpenPersona ClawHub page](https://clawhub.ai/neiljo-gy/open-persona) <br>
- [OpenPersona repository](https://github.com/acnlabs/OpenPersona) <br>
- [Architecture reference](references/ARCHITECTURE.md) <br>
- [Preset catalog](references/PRESETS.md) <br>
- [Faculty catalog](references/FACULTIES.md) <br>
- [Evolution reference](references/EVOLUTION.md) <br>
- [Avatar faculty reference](references/AVATAR.md) <br>
- [Heartbeat reference](references/HEARTBEAT.md) <br>
- [Economy and vitality reference](references/ECONOMY.md) <br>
- [Contribution workflow](references/CONTRIBUTE.md) <br>
- [OpenPersona persona directory](https://openpersona.co/skills) <br>
- [OpenPersona dataset directory](https://openpersona.co/datasets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, generated configuration, and inline shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce persona.json content, SKILL.md guidance, and CLI commands for user-approved local execution.] <br>

## Skill Version(s): <br>
0.21.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
