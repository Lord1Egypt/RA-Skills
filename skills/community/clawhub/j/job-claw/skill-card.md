## Description:

JobClaw automates job searches across LinkedIn and Indeed, scores postings against a user's profile, and maintains a local CSV tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixijia](https://clawhub.ai/user/weixijia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use JobClaw to configure automated job searches, rank ML/AI job postings against a personal profile, track results in CSV, and receive optional daily summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled local automation searches job sites, writes CSV and log files, and archives records.

Mitigation: Review configuration, JOBCLAW_DIR, scheduler settings, and dry-run output before enabling recurring runs or committed archiving.

Risk: Remote job data and arbitrary URLs can influence local processing.

Mitigation: Fix the URL-validation issue identified in the security guidance and review job URLs before enabling URL checks or manual job intake.

Risk: Notification paths may expose tokens or job-search summaries through Telegram or OpenClaw.

Mitigation: Store Telegram tokens in a secret store or locked-down config file, and keep notifications disabled unless needed.

Risk: Dependency setup can install unpinned packages and may use --break-system-packages.

Mitigation: Use a virtual environment, pin dependencies, and avoid --break-system-packages before routine use.

Risk: The daily runner uses heredoc-based command invocation flagged by the security guidance.

Mitigation: Fix the heredoc injection issue before enabling scheduled execution.

## Reference(s):

- [JobClaw Commands Reference](references/commands.md)
- [JobClaw Keyword Reference](references/keywords.md)
- [JobClaw Screening Guide](references/screening_guide.md)
- [ClawHub JobClaw Release Page](https://clawhub.ai/weixijia/skills/job-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses with inline shell and Python commands, JSON configuration, CSV job records, and notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local files under JOBCLAW_DIR or ~/Documents/JobClaw; can perform network searches and optional outbound notifications.]

## Skill Version(s):

1.0.20260329-142ceea (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
