## Description: <br>
OKKI Go helps agents perform B2B prospect discovery and outreach through the Okki Go platform, including company search, contact email discovery, cold outreach, email status checks, and credit or plan queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okki-op](https://clawhub.ai/user/okki-op) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, business development, and growth users use this skill to find target companies, review prospect results, unlock company details, find decision-maker contact emails, draft or send outreach, and check email or credit status through Okki Go. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles an Okki Go API key. <br>
Mitigation: Use only a user-approved secure save path, avoid printing or logging keys, and keep the default HTTPS endpoint. <br>
Risk: Some actions consume paid credits or EDM quota. <br>
Mitigation: Require explicit user confirmation before paid unlocks, contact searches, or email sending. <br>
Risk: Email workflows can send real outbound messages. <br>
Mitigation: Review recipient lists and email content carefully before confirming send actions. <br>
Risk: Local batches or artifacts may contain contact lists, email bodies, or company details. <br>
Mitigation: Periodically delete saved raw batches and artifacts that contain sensitive prospect or outreach data. <br>
Risk: Optional update notifications install a recurring OpenClaw cron reminder. <br>
Mitigation: Enable update notifications only when recurring local reminders are desired. <br>


## Reference(s): <br>
- [OKKI Go skill page](https://clawhub.ai/okki-op/skills/okki-go) <br>
- [API Reference](references/api-reference.md) <br>
- [Authentication](references/authentication.md) <br>
- [Output Contracts](references/output-contracts.md) <br>
- [Paid Actions](references/paid-actions.md) <br>
- [Search Fast Path](references/search-fast-path.md) <br>
- [Okki Go](https://go.okki.ai) <br>
- [Okki Go Pricing](https://go.okki.ai/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown responses with script-rendered tables, JSON payloads, and shell command invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local batch or detail artifacts and uses Okki Go API credentials for authenticated requests.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence; target metadata agrees) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
