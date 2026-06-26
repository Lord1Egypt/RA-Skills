## Description: <br>
Automatically monitors a GitLab project for new commits on a schedule, prepares pending commit data, and guides the agent to generate and send code review reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanghaiyu0511](https://clawhub.ai/user/zhanghaiyu0511) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to configure scheduled GitLab commit checks and receive code review reports for newly detected changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GitLab read_api token and stores configuration in workspace/.env. <br>
Mitigation: Use a dedicated least-privilege token with an expiration, keep workspace/.env private, and remove the token when automated review is no longer needed. <br>
Risk: The scheduled job fetches private commit diffs from the configured GitLab project. <br>
Mitigation: Verify the GitLab URL, project path, and branch before saving configuration, and restrict token access to only the intended project where possible. <br>
Risk: Automated hourly review continues until the cron job is removed. <br>
Mitigation: Review the configured cron job and remove it when scheduled code review is no longer required. <br>


## Reference(s): <br>
- [GitLab Code Review on ClawHub](https://clawhub.ai/zhanghaiyu0511/gitlab-code-review) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, JSON pending-review files, shell commands, and workspace configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates scheduled review state and pending-review files; sends reports only when new commits are found.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
