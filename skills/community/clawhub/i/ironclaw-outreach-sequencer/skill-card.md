## Description: <br>
Create and manage multi-step outreach sequences across LinkedIn, cold email, and follow-ups with per-lead personalization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aspenas](https://clawhub.ai/user/aspenas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, recruiting, and business-development operators use this skill to design, schedule, and execute personalized LinkedIn and email outreach sequences while tracking lead status and follow-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send LinkedIn and Gmail outreach on a recurring schedule without clear approval gates or account scoping. <br>
Mitigation: Require a dry-run preview of recipients, message bodies, channels, sending account, and schedule, then require explicit approval before any message is sent. <br>
Risk: Automated outreach can contact opted-out or inappropriate recipients and create spam, policy, or compliance issues. <br>
Mitigation: Confirm the lead source, opt-out handling, daily send limits, CAN-SPAM fields, and a pause or stop process before enabling cron-based sends. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aspenas/ironclaw-outreach-sequencer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with outreach templates, SQL snippets, shell commands, and JSON cron configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce personalized message bodies, sequence schedules, DuckDB status updates, Gmail CLI commands, browser action guidance, and run summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
