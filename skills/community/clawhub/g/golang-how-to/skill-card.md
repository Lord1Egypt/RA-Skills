## Description: <br>
Golang How To helps AI coding agents choose and load relevant Go skills for coding, review, debugging, setup, disambiguation, and project configuration tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to route Go-related agent tasks to the most relevant Go skills, including related secondary skills for testing, security, performance, API work, and project setup. It can also guide configuration of project agent files so selected Go skills are loaded for future Go work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configure mode can change future Go-related agent behavior by adding always-loaded skills to project agent configuration files. <br>
Mitigation: Review the target files and selected skills before accepting configure-mode edits, and keep the always-loaded list limited to skills the project actually requires. <br>
Risk: Automatic loading of related Go skills may add prompt overhead or introduce guidance that is broader than the immediate task. <br>
Mitigation: Review the selected primary and secondary skills for fit, especially when disambiguating overlapping areas such as performance, troubleshooting, safety, and security. <br>


## Reference(s): <br>
- [Golang skills catalog by category](references/by-category.md) <br>
- [Competing clusters disambiguation](references/disambiguation.md) <br>
- [Configure mode project config workflow](references/project-config.md) <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-how-to) <br>
- [Project homepage from skill metadata](https://github.com/samber/cc-skills-golang) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands and configuration edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to load multiple Go skills for one task; configure mode can add a Required Go skills block to supported project agent files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
