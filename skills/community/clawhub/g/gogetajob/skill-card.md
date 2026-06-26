## Description: <br>
Open-source contribution workflow: find GitHub issues, implement fixes, submit PRs, track results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kagura-agent](https://clawhub.ai/user/kagura-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and open-source contributors use this skill to run a structured contribution loop: scan repositories for issues, study candidate work, delegate implementation, submit pull requests, sync review status, and record lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can operate with broad authority over code changes and GitHub publishing under the user's account. <br>
Mitigation: Use a dedicated worktree, least-privilege GitHub token, and require human review before pushes, pull requests, issue filing, cron setup, or reviewer replies. <br>
Risk: The skill describes `--approve-all` execution for delegated code work. <br>
Mitigation: Avoid broad approval mode unless the user explicitly accepts that risk and independently reviews generated changes and test results. <br>


## Reference(s): <br>
- [Workloop Overview](references/workloop-overview.md) <br>
- [Gogetajob ClawHub Release](https://clawhub.ai/kagura-agent/gogetajob) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide GitHub CLI, git, FlowForge, Claude Code, cron setup, and PR follow-up actions.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
