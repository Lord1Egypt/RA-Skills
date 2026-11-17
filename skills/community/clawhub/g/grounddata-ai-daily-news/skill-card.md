## Description:

Fetches current or date-specific AI news, synchronizes available analysis capabilities, and helps agents produce AI-news briefings, workflow artifacts, and automation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finleyfu](https://clawhub.ai/user/finleyfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, analysts, product teams, and investors use this skill to retrieve AI and machine-learning news, personalize briefings, generate workflow-specific artifacts, and prepare scheduled delivery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remotely supplied news, sponsor, survey, and update content can affect agent replies.

Mitigation: Review this skill before installing and use it only if the AI Daily News service is trusted for that content.

Risk: Identifiers or access tokens may be sent to configurable service endpoints.

Mitigation: Set AINEWS_ACCESS_TOKEN only when Pro features are needed, and use AINEWS_SERVICE_URL or --base-url only with a trusted HTTPS endpoint.

Risk: Generated automation or cron scripts may run commands or send rendered content to external destinations.

Mitigation: Inspect any generated automation or cron script before running or scheduling it, and perform a test run before relying on delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/finleyfu/skills/grounddata-ai-daily-news)
- [Publisher Profile](https://clawhub.ai/user/finleyfu)
- [Automation Prompt Template](references/automation-prompt.md)
- [AI Daily News API Endpoint](https://api.ainewparadigm.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include automation-safe markdown, context-only markdown, feedback or survey submission results, and generated workflow artifacts.]

## Skill Version(s):

1.3.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
