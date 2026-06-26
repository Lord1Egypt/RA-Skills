## Description: <br>
2-agent collaborative software development workflow for OpenClaw <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChloePark85](https://clawhub.ai/user/ChloePark85) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and builders use this skill to turn project requests into implemented software by coordinating a PM agent that plans work and a Dev agent that writes, tests, documents, and commits code. It is aimed at landing pages, small web applications, prototypes, documentation sites, and similar code generation projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate agents that create and modify project files, run development commands, install packages, start processes, and make Git commits. <br>
Mitigation: Use a dedicated or backed-up project workspace and review generated changes before commits, pushes, or deployment. <br>
Risk: Repository or deployment credentials could give the agents broader access than the intended project. <br>
Mitigation: Provide GitHub or deployment credentials only for the specific repository or service the agents should modify. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ChloePark85/multi-agent-dev-team) <br>
- [Publisher profile](https://clawhub.ai/user/ChloePark85) <br>
- [UBIK Collective homepage](https://ubik.systems) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw) <br>
- [Skill guide](SKILL.md) <br>
- [Project specification template](templates/project-spec-template.md) <br>
- [PM Agent SOUL](agents/pm-agent/SOUL.md) <br>
- [Dev Agent SOUL](agents/dev-agent/SOUL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with task specifications, code deliverables, setup commands, configuration snippets, and completion summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify project files and Git commits when used by configured OpenClaw agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
