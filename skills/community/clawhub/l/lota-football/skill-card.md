## Description:

Lota Football helps agents query football match lists and compact single-match feature reports, including free historical World Cup reports and structured prompts for football match analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingvergil](https://clawhub.ai/user/kingvergil)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Lota football match data, compact feature reports, and local cached match files for agent-assisted football analysis. It can also guide agents in formatting match analysis outputs from the returned feature text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and match queries may be sent to the Lota service, and the default API base URL in the artifact uses HTTP.

Mitigation: Review before installing and set LOTA_API_BASE_URL to an HTTPS endpoint before using a real API key.

Risk: The artifact suggests placing LOTA_API_KEY directly in a persistent cron command for scheduled cache refresh.

Mitigation: Avoid putting the key directly in crontab; use a safer secret-loading mechanism and remove scheduled jobs when automatic refresh is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingvergil/skills/lota-football)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON or plain-text API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local cache files under lota_data when scheduled refresh is configured.]

## Skill Version(s):

2.1.0 (source: server release metadata, artifact _meta.json, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
