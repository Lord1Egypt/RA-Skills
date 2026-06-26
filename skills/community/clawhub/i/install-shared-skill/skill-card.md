## Description: <br>
Installs named OpenClaw skills through the clawhub CLI and returns the command output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shifulegend](https://clawhub.ai/user/shifulegend) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install named ClawHub skills from an agent session through the clawhub CLI. It is best suited to trusted, simple skill names because it changes installed skills and returns terminal output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted skill name can cause the tool to run unintended shell commands. <br>
Mitigation: Use only trusted, simple skill names and prefer a version that validates skill slugs and executes commands with an argument array. <br>
Risk: The documented install scope is inconsistent, so users may misunderstand whether the skill installs globally or into the workspace. <br>
Mitigation: Confirm the install destination before use and review installed skill changes after the command completes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shifulegend/install-shared-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns stdout and stderr from the clawhub CLI; non-zero exits are surfaced as command output.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
