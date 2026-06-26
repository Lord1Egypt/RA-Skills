## Description: <br>
AutoSkills CLI detects project types, recommends matching AgentSkills, and can install or integrate selected skills through CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamwgp](https://clawhub.ai/user/adamwgp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to inspect a workspace, identify the project category, and get recommended AgentSkills for web, Python, academic, finance, marketing, or media workflows. It can also provide commands for installing and checking those skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run an external CLI that installs and activates other agent skills with limited scoping or rollback guidance. <br>
Mitigation: Run detection, list, or doctor commands first; inspect proposed downstream skills; avoid the default full integration flow unless those setup changes are intended; use a pinned package version or reviewed source where possible. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/adamwgp/our-autoskills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend or trigger downstream skill installation depending on the selected command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
