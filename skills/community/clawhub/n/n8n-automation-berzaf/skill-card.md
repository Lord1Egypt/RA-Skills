## Description: <br>
Trigger n8n workflows using natural language for lead nurturing, email sequences, CRM updates, social media posting, meeting follow-ups, competitor monitoring, invoice reminders, content repurposing, and daily briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beraiautomation](https://clawhub.ai/user/beraiautomation) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, automation agencies, content creators, solo founders, and operators use this skill to trigger configured n8n workflows from agent chat for routine business automation. It helps users validate required inputs, confirm actions, run webhook-backed workflows, and report workflow results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Status and validator checks can POST ping or test payloads to configured n8n webhook endpoints and may trigger live workflows. <br>
Mitigation: Use only trusted HTTPS n8n instances and run status or validation checks against production workflows only after confirming each workflow safely ignores ping and test payloads. <br>
Risk: Email, social posting, CRM update, invoice reminder, and briefing workflows can perform real business actions or expose sensitive account data. <br>
Mitigation: Require explicit user confirmation before execution, verify required fields and recipient details, and avoid sending test data to production webhooks without approval. <br>
Risk: The skill depends on an n8n API key and webhook base URL for live operation. <br>
Mitigation: Store credentials in a protected environment or secret manager and do not print API keys, webhook URLs, or other secrets in chat or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beraiautomation/n8n-automation-berzaf) <br>
- [README](README.md) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [n8n Workflow Templates](references/n8n-workflow-templates.md) <br>
- [Usage Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON/text command output, with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires N8N_WEBHOOK_BASE_URL and N8N_API_KEY; scripts can call live n8n webhook endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
