## Description:

Monitors a configured GitLab project for new commits, prepares pending commit data, and guides an agent to generate and send code review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhanghaiyu0511](https://clawhub.ai/user/zhanghaiyu0511)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to configure scheduled GitLab commit monitoring and receive code review reports for new commits on a selected branch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a GitLab personal access token in workspace/.env and reuses it through an hourly background job.

Mitigation: Use a dedicated least-privilege read_api token, restrict access to workspace/.env, and rotate or revoke the token when monitoring is no longer needed.

Risk: The configured GitLab URL determines where the token is sent during API calls.

Mitigation: Configure only a trusted HTTPS GitLab URL and review the configuration before enabling scheduled monitoring.

Risk: The cron job continues accessing the selected GitLab project until it is removed.

Mitigation: Periodically review the cron configuration and remove the job when scheduled code review is no longer required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhanghaiyu0511/skills/gitlab-code-review)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and generated review-report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates pending review JSON, review state JSON, and Markdown code review reports in workspace memory when configured.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
