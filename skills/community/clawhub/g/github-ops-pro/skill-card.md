## Description: <br>
Automates GitHub repository creation, code pushes, README updates, and release creation using git, curl, and a configured GitHub token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automate GitHub account actions such as repository creation, code pushes, README updates, and release creation. It requires git, curl, and a configured GITHUB_TOKEN. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make account-changing GitHub actions using stored credentials without clear approval gates. <br>
Mitigation: Use a dedicated least-privilege token and require explicit confirmation before creating repositories, pushing code, creating releases, or triggering deployments. <br>
Risk: Embedding tokens in git remotes can expose credentials. <br>
Mitigation: Avoid token-bearing remote URLs and prefer credential helpers or short-lived environment-scoped credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/github-ops-pro) <br>
- [OpenClaw homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, git, and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git, curl, and GITHUB_TOKEN; may create repositories, push code, update files, and create releases.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
