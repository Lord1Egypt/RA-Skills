## Description: <br>
Query and manage GitHub repositories, including listing repositories, checking CI status, creating issues, searching repositories, and viewing recent activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyzx](https://clawhub.ai/user/gyzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an OpenClaw assistant inspect GitHub repositories, summarize repository activity, check CI status, and create repository resources from conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live GitHub account changes when configured with broad credentials. <br>
Mitigation: Use the narrowest practical GitHub token scopes and require confirmation of repository names, visibility, issue bodies, and pull-request details before write actions. <br>
Risk: The pull-request creation action is under-documented in the public skill materials. <br>
Mitigation: Review the action behavior before enabling it and confirm title, source branch, target branch, repository, and body before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gyzx/openclaw-github-assistant-2-0-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured action results from GitHub API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live GitHub read and write actions when configured with a GitHub token.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
