## Description: <br>
Detects a Node.js version requirement from a project's package.json engines.node field and helps switch to a matching Node version with nvm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piaolingwuyu](https://clawhub.ai/user/piaolingwuyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when setting up or entering Node.js projects that declare an engines.node requirement, so an agent can run or recommend the appropriate nvm-based version switch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the Bash script can download and execute the nvm installer from GitHub and change the user's local Node.js environment. <br>
Mitigation: Install nvm manually first or inspect the script and installer before execution, then run it only in environments where changing Node versions is acceptable. <br>
Risk: The skill documentation advertises Windows PowerShell usage, but the artifact only includes the Bash implementation. <br>
Mitigation: Do not rely on the advertised Windows command unless a PowerShell script is separately provided and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/piaolingwuyu/nvm-auto-switch) <br>
- [nvm installer referenced by the skill](https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local shell commands that inspect package.json, install nvm, install Node.js, and switch the active Node version.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
