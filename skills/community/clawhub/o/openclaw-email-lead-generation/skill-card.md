## Description: <br>
OpenClaw Email Lead Generation is an outreach and pipeline-management skill that helps an agent set up lead records, create custom email sequences, score prospects, draft outreach, monitor replies, generate briefings, and optionally run cron-driven follow-up workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffjhunter](https://clawhub.ai/user/jeffjhunter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and business operators use this skill to manage sales leads, build personalized email sequences, track outreach status, and prepare follow-up actions through an agent-assisted workflow. It supports manual operation by default and optional email or cron automation after setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive lead records, reply content, audit logs, and temporary email-body files. <br>
Mitigation: Treat ~/workspace/leadgen and the temporary email-body file as sensitive, restrict local access, and prune audit logs according to the configured retention period. <br>
Risk: Email outreach can be sent unintentionally or at an inappropriate volume if automation is enabled without review. <br>
Mitigation: Review every email before sending unless auto-send is deliberately enabled, keep cron jobs opt-in, and enforce configured daily, hourly, per-domain, warmup, and unsubscribe limits. <br>
Risk: SMTP credentials or mail account secrets could be exposed if pasted into configuration or chat. <br>
Mitigation: Store mail credentials only in environment variables and avoid placing passwords in config files, lead records, templates, or messages. <br>
Risk: Cron-driven workflows may continue acting on stale configuration or stale lead data. <br>
Mitigation: Review created cron jobs, verify schedules and prompts after setup, and periodically inspect pipeline status before leaving automation unattended. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/jeffjhunter/openclaw-email-lead-generation) <br>
- [Publisher Homepage](https://jeffjhunter.com) <br>
- [Template Forge Reference](references/template-forge.md) <br>
- [Lead Scoring Reference](references/scoring-guide.md) <br>
- [Cron Automation Reference](references/cron-automation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON lead records, YAML configuration, email draft text, and report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates lead, template, sequence, draft, report, and audit-log files under ~/workspace/leadgen; optional email and cron automation require user setup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
