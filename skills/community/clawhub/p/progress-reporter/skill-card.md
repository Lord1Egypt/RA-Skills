## Description:

Automatically reports task progress every 10 minutes during execution, including current status, recent work, overall progress, and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenmejiang-commits](https://clawhub.ai/user/zenmejiang-commits)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to monitor long-running agent tasks by generating recurring Markdown progress reports and short notification summaries while a task is active.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled reporting can continue after it is no longer needed.

Mitigation: Enable the cron job only when recurring reports are desired, document the installed crontab entry, and remove it when reporting should stop.

Risk: Progress reports may expose task descriptions or log snippets that contain sensitive information.

Mitigation: Run the reporter as a least-privileged user, restrict access to task and memory directories, and avoid using it for sensitive tasks unless redaction and retention controls are added.

Risk: Reports are stored without built-in retention controls.

Mitigation: Define a cleanup process for old progress reports, notifications, and reporter logs before enabling scheduled execution.

## Reference(s):

- [Progress Reporter ClawHub listing](https://clawhub.ai/zenmejiang-commits/skills/progress-reporter)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Configuration]

**Output Format:** [Markdown progress reports, Markdown notification summaries, and plain-text log lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are intended to be generated on a recurring schedule while a task is running.]

## Skill Version(s):

1.0.0 (source: release metadata, skill.json, skill.yaml, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
