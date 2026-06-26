## Description: <br>
PM Skill guides an agent to scaffold and write structured Product Requirements Documents with BDD acceptance criteria and testing strategy guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leio9511](https://clawhub.ai/user/leio9511) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn product discussions into structured PRDs with problem statements, architecture notes, BDD acceptance criteria, and testing strategy guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt execution of local scripts and operational helpers that may change installed OpenClaw state. <br>
Mitigation: Review the helper scripts and only allow execution after confirming the target project, generated PRD path, and local OpenClaw installation changes. <br>
Risk: The skill writes PRD files based on conversation context, so incomplete or ambiguous requirements may produce misleading downstream planning input. <br>
Mitigation: Review the generated PRD for requirements, architecture assumptions, acceptance criteria, and testing strategy before using it as planner input. <br>


## Reference(s): <br>
- [PM Skill ClawHub Release](https://clawhub.ai/leio9511/pm-skill) <br>
- [Technical PM Skill Core Architecture PRD](docs/PRDs/PRD_001_PM_Skill_Core_Architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown PRD content and concise status guidance, with shell commands when invoking scaffold or audit helpers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates PRD files after a scaffold path is resolved.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
