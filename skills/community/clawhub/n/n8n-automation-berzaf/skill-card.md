## Description:

Trigger n8n workflows using natural language to automate lead nurturing, email sequences, CRM updates, social media posting, meeting follow-ups, competitor monitoring, and invoice reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beraiautomation](https://clawhub.ai/user/beraiautomation)

### License/Terms of Use:

MIT-0

## Use Case:

External users, automation agencies, content creators, solo founders, and operators use this skill to trigger preconfigured n8n workflows from an agent through natural-language requests. It supports business workflows such as lead nurture, social posting, meeting follow-up, CRM updates, competitor reports, invoice reminders, content repurposing, and daily briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real n8n workflows that send email, post to social platforms, update CRMs, or process business data.

Mitigation: Review each proposed action before execution, require user confirmation, and test workflows against a staging n8n instance before enabling production endpoints.

Risk: The skill requires an n8n API key and webhook base URL, and webhook calls may send business data to an external n8n instance.

Mitigation: Use a dedicated least-privilege n8n API key, restrict webhook hosts to HTTPS, and avoid exposing credentials or webhook URLs in chat or logs.

Risk: Status and validation commands can POST test payloads to configured webhook endpoints.

Mitigation: Run diagnostics only against expected webhook targets and verify that diagnostic endpoints cannot cause irreversible production actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beraiautomation/skills/n8n-automation-berzaf)
- [Publisher profile](https://clawhub.ai/user/beraiautomation)
- [n8n workflow templates](references/n8n-workflow-templates.md)
- [Setup guide](references/setup-guide.md)
- [Usage examples](references/examples.md)
- [Publishing guide](references/publishing-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON responses with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger external n8n webhook calls and return workflow status, generated reports, or content drafts.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
