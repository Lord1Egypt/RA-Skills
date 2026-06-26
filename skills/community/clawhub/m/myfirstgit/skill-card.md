## Description: <br>
Interact with GitHub through the GitHub CLI to list repositories, issues, and pull requests, and to create new issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[M3159](https://clawhub.ai/user/M3159) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent inspect GitHub repositories, issues, and pull requests, or prepare issue creation through an authenticated GitHub CLI session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub operations use the currently authenticated GitHub CLI account and its repository permissions. <br>
Mitigation: Before creating an issue, confirm the active GitHub account, target repository, title, and body. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/M3159/myfirstgit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline GitHub CLI commands and command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on the active GitHub CLI account, repository permissions, and local authentication state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
