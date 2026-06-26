## Description: <br>
Boost developer productivity with Gitai: An AI-powered Git automation tool that analyzes code changes and generates semantic Conventional Commits instantly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leandrosilvaferreira](https://clawhub.ai/user/leandrosilvaferreira) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to invoke Gitai for analyzing repository changes, generating Conventional Commit messages, and optionally committing or pushing Git changes after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke an external Git automation CLI that may commit or push repository changes. <br>
Mitigation: Review diffs and generated commit messages before committing, and use `--push` only after explicitly confirming the target branch and remote. <br>
Risk: The configured AI provider may receive repository change context while generating commit messages. <br>
Mitigation: Use only approved providers for the repository and avoid sensitive codebases unless the provider and configuration are approved for that code. <br>
Risk: The skill depends on a preinstalled and configured `gitai` CLI. <br>
Mitigation: Confirm `gitai` is available and `~/.gitai` exists before operation; stop and ask the user to configure the tool if either prerequisite is missing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leandrosilvaferreira/gitai-skill) <br>
- [Publisher profile](https://clawhub.ai/user/leandrosilvaferreira) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run the external gitai CLI after prerequisite checks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
