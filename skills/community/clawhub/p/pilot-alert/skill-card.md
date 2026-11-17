## Description:

Configurable alerting on event patterns with webhook and message delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Pilot Alert to subscribe to Pilot Protocol events, trigger alerts from patterns or thresholds, deliver webhook notifications, and escalate critical events to on-call agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alert payloads may expose sensitive event data to external webhook recipients.

Mitigation: Redact or minimize payload fields and avoid sending secrets to third-party webhooks.

Risk: Broad event subscriptions or unrestricted webhook destinations can cause unintended alert delivery.

Mitigation: Restrict subscribed topics and webhook destinations before production use.

Risk: Example shell snippets that construct JSON manually can produce malformed or unsafe payloads.

Mitigation: Build JSON payloads with jq and review shell snippets before deployment.

Risk: The example deduplication cache uses /tmp, which may be unsuitable for production state.

Mitigation: Replace the /tmp cache with a private locked state directory.

## Reference(s):

- [Pilot Protocol Network](https://pilotprotocol.network)
- [Pilot Alert ClawHub Page](https://clawhub.ai/teoslayer/skills/pilot-alert)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Bash command blocks and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl, jq, curl, a running daemon, and trust with source agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
