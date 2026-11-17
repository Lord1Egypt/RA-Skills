## Description:

Control Home Assistant smart home devices, run automations, and receive webhook events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

External Home Assistant users and developers use this skill to inspect entity state, control smart-home devices, run scenes, scripts, and automations, and receive Home Assistant webhook events through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue broad Home Assistant service calls that control devices, scenes, scripts, automations, covers, climate, and other smart-home entities.

Mitigation: Install only when broad smart-home control is acceptable, review commands before execution, and prefer a dedicated least-privilege Home Assistant account.

Risk: The skill uses long-lived bearer tokens that may be stored in a config file or environment variable.

Mitigation: Protect the token like a password, restrict config file permissions, use HTTPS or trusted local-only transport, and rotate the token if exposed.

Risk: Webhook and generic service-call workflows can trigger sensitive physical-world actions or automations if misconfigured.

Mitigation: Limit webhook exposure, validate entity and service names, and add confirmation or Home Assistant-side safeguards for sensitive actions.

## Reference(s):

- [Home Assistant REST API Reference](artifact/references/api.md)
- [ClawHub skill page](https://clawhub.ai/eohmig/skills/home-assistant-backup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, YAML, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl and ha.sh commands that require jq, curl, HA_URL, and HA_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
