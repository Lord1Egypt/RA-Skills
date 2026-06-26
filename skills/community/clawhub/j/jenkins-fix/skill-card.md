## Description: <br>
Jenkins Fix helps an agent list Jenkins jobs, trigger builds for default or specified branches and tags, check build status, and return build results or artifact links while using environment-variable-based Jenkins authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitboy123](https://clawhub.ai/user/gitboy123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release operators use this skill to operate Jenkins from agent chat: listing jobs, starting builds for requested projects and branches, checking completion, and returning build results or artifact links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger real Jenkins CI/CD builds from broad chat prompts without a built-in confirmation step. <br>
Mitigation: Require human confirmation before running builds or deployments and restrict the Jenkins credential to least-privilege jobs and branches. <br>
Risk: Jenkins credentials and endpoint settings are required for operation. <br>
Mitigation: Use a dedicated Jenkins API token via environment variables and avoid storing credentials in source or chat history. <br>
Risk: The DingTalk helper uses a fixed local script path that may not match the deployment. <br>
Mitigation: Update or remove the helper path before deploying the DingTalk integration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gitboy123/jenkins-fix) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with shell command snippets and Jenkins result/status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Jenkins build numbers, console-log summaries, and artifact download URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
