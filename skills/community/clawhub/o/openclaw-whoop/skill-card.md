## Description:

Connects to the official WHOOP Developer Platform with OAuth, stores and refreshes local tokens, fetches WHOOP v2 health and activity data, and renders daily or weekly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinchengcool](https://clawhub.ai/user/gavinchengcool)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to authorize WHOOP access, fetch recovery, sleep, strain, workout, profile, and body measurement data, normalize it, and generate text or Markdown summaries for chat or scheduled delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive WHOOP health data and OAuth tokens on the local machine.

Mitigation: Use a deliberate WHOOP_TOKEN_PATH, restrict token and output file permissions, and avoid writing health outputs to /tmp.

Risk: Default OAuth scopes can grant broad WHOOP read access.

Mitigation: Set WHOOP_SCOPES to the minimum scopes required for the intended summary or workflow.

Risk: Scheduled or external chat delivery can expose health summaries outside the local session.

Mitigation: Require explicit user confirmation of destination, cadence, and content before sending or scheduling WHOOP summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gavinchengcool/skills/openclaw-whoop)
- [WHOOP API quick reference](references/whoop_api.md)
- [WHOOP OpenAPI specification](references/openapi.json)
- [Normalized output schema](references/output_schemas.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can format summaries for generic, Slack, Discord, WhatsApp, or Telegram-style chat output; normalized fields may be null when API data or scopes are unavailable.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
