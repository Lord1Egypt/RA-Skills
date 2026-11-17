## Description:

Create and manage scheduled Korea metropolitan bus arrival alerts using Korea TAGO OpenAPI and Clawdbot cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsooooo](https://clawhub.ai/user/hsooooo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to register weekday, weekend, or daily bus arrival alerts for selected TAGO stops and routes. It helps agents build cron jobs, query bus arrival data, and deliver concise arrival summaries to the registering user's configured direct-message channel.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: Persistent scheduled-agent prompts could be registered from untrusted route, stop, or destination values.

Mitigation: Accept alert registration only from trusted users and confirm the generated cron payload, route list, stop identifier, channel, and direct-message destination before creating a job.

Risk: Direct-message-only delivery is described by the skill but depends on correct cron payload and Gateway delivery targeting.

Mitigation: Require explicit delivery target selection and verify that the cron job uses an isolated session with the registering user's direct-message channel before enabling delivery.

Risk: The setup helper can write a user systemd Gateway override and restart the Gateway service.

Mitigation: Run setup only on a trusted host after reviewing the selected systemd unit and environment file path; use manual environment configuration when service changes are not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hsooooo/skills/korea-metropolitan-bus-alerts)
- [TAGO API reference](references/api_reference.md)
- [Clawdbot cron recipe](references/cron_recipe.md)
- [TAGO bus stop information dataset](https://www.data.go.kr/data/15098534/openapi.do)
- [TAGO bus arrival information dataset](https://www.data.go.kr/data/15098530/openapi.do)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON cron job payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAGO_SERVICE_KEY for live TAGO lookups; generated cron jobs should use isolated sessions and direct-message delivery.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
