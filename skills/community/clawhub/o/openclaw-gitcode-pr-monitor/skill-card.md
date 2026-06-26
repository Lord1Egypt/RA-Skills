## Description: <br>
Monitor GitCode PRs for one or more repos, auto-run AI review via OpenClaw Gateway, post PR comments, and send notifications (DingTalk + WeCom). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingyang1996](https://clawhub.ai/user/mingyang1996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to monitor GitCode pull requests, trigger OpenClaw-based code reviews, post Markdown review comments, and notify configured DingTalk and WeCom recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended automation can post AI-generated PR comments and send full review reports to chat services without a human review step. <br>
Mitigation: Add a manual approval or dry-run step before posting comments or sending report attachments. <br>
Risk: The skill uses a GitCode token and repository and chat target configuration. <br>
Mitigation: Use a dedicated least-privilege GitCode token, restrict monitored repositories and chat targets, and avoid sensitive or private repositories unless external sharing is approved. <br>


## Reference(s): <br>
- [Configuration](references/CONFIG.md) <br>
- [ClawHub skill page](https://clawhub.ai/mingyang1996/openclaw-gitcode-pr-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review reports with shell-script driven PR comments and notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run unattended when scheduled; uses a GitCode token and configured repository and chat targets.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
