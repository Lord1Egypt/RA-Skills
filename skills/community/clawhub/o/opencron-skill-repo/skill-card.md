## Description:

Visual cron job dashboard for OpenClaw with live countdown timers, run history, and calendar view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firstfloris](https://clawhub.ai/user/firstfloris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy and operate an OpenClaw cron dashboard that shows job status, upcoming runs, run history, and related cron metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron job names, prompts, schedules, outputs, and run metadata may reveal sensitive operational details.

Mitigation: Treat dashboard data as sensitive, redact prompts and secrets before serving, and limit access to trusted local users or authenticated viewers.

Risk: Dashboard links include gateway tokens in URLs and may be exposed through logs, browser history, or sharing.

Mitigation: Remove tokenized public URLs from routine output and use authentication that does not place secrets in query parameters.

Risk: The local HTTP server allows wildcard CORS and can bind on all interfaces, broadening data exposure on shared or networked hosts.

Mitigation: Bind locally by default, remove wildcard CORS, and place any external access behind an authenticated reverse proxy with rate limits and security headers.

Risk: The deploy script fetches dashboard HTML from a mutable remote URL at install or update time.

Mitigation: Pin, vendor, or checksum the dashboard asset before deployment so reviewers know exactly what code will run.

Risk: The background sync is documented as a nohup loop without lifecycle, status, or stop controls.

Mitigation: Run synchronization under a managed process supervisor with explicit start, status, restart, and stop behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/firstfloris/skills/opencron-skill-repo)
- [OpenCron dashboard repository](https://github.com/firstfloris/opencron)
- [OpenCron skill repository](https://github.com/firstfloris/opencron-skill)
- [Dashboard overview image](https://raw.githubusercontent.com/firstfloris/opencron/master/docs/overview.png)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and an OpenClaw cron data directory; dashboard content and cron-data JSON may be written under the user's OpenClaw canvas directory.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
