## Description: <br>
GitHub Operations helps agents manage GitHub repositories, branches, pull requests, issues, security cleanup workflows, and IM channel notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate GitHub repository administration, branch creation, pull request and issue workflows, repository cleanup tasks, and notification delivery through configured IM channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The history-cleaning workflow can rewrite and force-push all branches and tags. <br>
Mitigation: Use the clean/history feature only after backups, explicit operator review, and confirmation that force-pushing all branches and tags is acceptable. <br>
Risk: GitHub automation may use administrative repository permissions. <br>
Mitigation: Use least-privilege GitHub tokens and avoid delete or force-push permissions unless the specific task requires them. <br>
Risk: IM integrations can send content to external webhook or API destinations. <br>
Mitigation: Verify Feishu, WeCom, WeChat, and Slack destinations before sending messages or deploying configured secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edwardwason/gitskills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured GitHub and IM credentials from environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
