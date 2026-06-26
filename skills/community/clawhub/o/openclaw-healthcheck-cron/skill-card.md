## Description: <br>
Create and run a reusable OpenClaw deep healthcheck automation using a cron job plus a script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up scheduled OpenClaw health audits, run read-only status checks, and report concise verdicts with artifact paths for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A recurring cron job can keep running after the original setup intent changes. <br>
Mitigation: Review the schedule and timezone before enabling it, and confirm that the job can be paused or deleted. <br>
Risk: Healthcheck logs and summaries are written to local temporary storage by default. <br>
Mitigation: Review generated artifacts under /tmp/openclaw-healthcheck or set HEALTHCHECK_OUTPUT_DIR to an approved location. <br>
Risk: Status checks may produce warnings when OpenClaw commands are unavailable or the gateway is not reachable. <br>
Mitigation: Run the script manually once before scheduling and verify that the summary verdict and issue list are actionable. <br>


## Reference(s): <br>
- [Cron job example](references/cron-job-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON cron configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a cron job pattern, a shell healthcheck workflow, local report artifact paths, and concise status summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
