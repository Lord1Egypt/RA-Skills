## Description:

Your personal Garmin and AI health coach analyzes sleep and biometric data daily for actionable functional medicine insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daasai](https://clawhub.ai/user/daasai)

### License/Terms of Use:

MIT-0

## Use Case:

External users configure the skill to connect Garmin wearable data and receive daily wellness reports with sleep, activity, HRV, stress, and body battery insights. It also guides first-time setup for NotebookLM, Garmin authorization, health concerns, and scheduled report timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive wearable health metrics, health concerns, Garmin account identifiers, and local history/log files.

Mitigation: Install only when comfortable with that data handling, protect the local machine, and review stored files under the OpenClaw data and log directories.

Risk: Health metrics and concerns are sent through external Garmin and Google/NotebookLM pathways despite privacy claims in the artifact.

Mitigation: Authenticate only with trusted accounts, review NotebookLM and Garmin data-sharing expectations, and avoid entering sensitive medical details beyond what is needed for wellness guidance.

Risk: The install and setup flow can install Python packages, download Playwright Chromium, and configure daily scheduled report execution.

Mitigation: Review dependency installation before running it and disable or adjust the daily cron schedule if automatic execution is not desired.

Risk: The reset command removes configuration but may not remove all local health history or logs.

Mitigation: Manually inspect and delete retained health history and log files when removing the skill or clearing sensitive data.

Risk: Generated wellness recommendations could be mistaken for clinical advice.

Mitigation: Treat reports as general wellness guidance only and consult a qualified professional for medical concerns or clinical decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daasai/skills/health-coach)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [garth Garmin API Client](https://github.com/matin/garth)
- [notebooklm-py CLI](https://github.com/teng-lin/notebooklm-py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style instant-message report with setup prompts and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily reports combine Garmin metrics, recent local history, and NotebookLM-generated wellness recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
