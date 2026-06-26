## Description: <br>
GitHub automation toolset for multi-account management, pull request creation and cleanup, code review workflows, and notification delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrzhangkris](https://clawhub.ai/user/mrzhangkris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to automate GitHub account switching, pull request creation, review actions, branch cleanup, and repository event notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live repository changes, including pushing branches, merging pull requests, deleting remote branches, and changing pull request state. <br>
Mitigation: Use it only with GitHub accounts and repositories where live mutation is acceptable, verify target repositories and branch lists before execution, and run cleanup commands with --dry-run first. <br>
Risk: Notification commands can send project details to Discord, Dingtalk, Telegram, or Slack webhooks. <br>
Mitigation: Configure chat webhooks only for approved destinations and do not send private or regulated repository data unless that disclosure is approved. <br>
Risk: Multi-account management stores GitHub account metadata on the local machine. <br>
Mitigation: Limit access to local account configuration files, remove stale account entries, and validate the active GitHub account before running repository-changing commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrzhangkris/laomo-github) <br>
- [Publisher profile](https://clawhub.ai/user/mrzhangkris) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and shell-script driven actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GitHub CLI, git, jq, and optional chat webhook environment variables.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
