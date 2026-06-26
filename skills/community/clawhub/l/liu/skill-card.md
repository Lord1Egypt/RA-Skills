## Description: <br>
Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lice2021](https://clawhub.ai/user/lice2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide ClawHub CLI workflows for finding, installing, updating, listing, and publishing agent skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Login and publish workflows involve credential and account context. <br>
Mitigation: Confirm the active ClawHub account before publishing and treat login steps as credential handling. <br>
Risk: Update --all, --force, and publish commands can change installed skills or release content. <br>
Mitigation: Review those commands before allowing an agent to run them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lice2021/liu) <br>
- [ClawHub registry](https://clawhub.com) <br>
- [Publisher profile](https://clawhub.ai/user/lice2021) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include ClawHub CLI commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
