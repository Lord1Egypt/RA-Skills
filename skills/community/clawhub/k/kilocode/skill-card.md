## Description: <br>
AI coding agent CLI tool for generating code from natural language, automating tasks, and running terminal commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weinguyen1224-glitch](https://clawhub.ai/user/weinguyen1224-glitch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate the Kilo CLI for code generation, refactoring, debugging, terminal automation, and CI/CD coding workflows from natural language prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Kilo CLI can read and write files, run terminal commands, and interact with browser workflows. <br>
Mitigation: Run it only in projects where code edits and command execution are acceptable, and review proposed changes before relying on the results. <br>
Risk: Autonomous mode can execute without permission prompts. <br>
Mitigation: Reserve `kilo run --auto` for trusted CI/CD or disposable environments. <br>
Risk: Prompts or code context may be sent through the configured provider authentication profile. <br>
Mitigation: Review which provider profile is active and confirm the `kilo` CLI comes from a trusted source before installation or use. <br>


## Reference(s): <br>
- [Kilo documentation](https://kilo.ai) <br>
- [ClawHub skill page](https://clawhub.ai/weinguyen1224-glitch/kilocode) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include interactive, non-interactive, and autonomous CLI invocation patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
