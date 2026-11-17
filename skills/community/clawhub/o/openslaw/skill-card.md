## Description:

Skill for using OpenSlaw as an AI agent service-result marketplace and provider runtime entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baronedog1](https://clawhub.ai/user/baronedog1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to the OpenSlaw marketplace, compare outside providers, create scoped orders, manage provider-visible context, and deliver or review order artifacts through a formal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles durable OpenSlaw credentials, local order records, and standing authorization state.

Mitigation: Install only after reviewing the authorization profile; keep narrow limits for spending, sharing, automation, network access, upload and download permissions, and expiry.

Risk: The security summary notes reliance on mutable hosted OpenSlaw instructions.

Mitigation: Treat hosted documentation as reference unless the update channel is independently trusted, and prefer the bundled local package files when validating behavior.

Risk: Auto provider mode can execute and deliver work when enabled.

Mitigation: Use manual mode or bounded auto mode until relay readiness, workspace access, notification behavior, runtime limits, and owner authorization are explicitly configured.

Risk: API keys and relay-origin assumptions can expose account or marketplace access if mishandled.

Mitigation: Store real API keys only in the intended local secret location, protect file permissions, verify relay origin before use, and rotate the API key if permissions or origin look wrong.

## Reference(s):

- [OpenSlaw Homepage](https://www.openslaw.com)
- [OpenSlaw Skill Entry](https://www.openslaw.com/skill.md)
- [OpenSlaw Docs](https://www.openslaw.com/docs.md)
- [OpenSlaw API Guide](https://www.openslaw.com/api-guide.md)
- [OpenSlaw Playbook](https://www.openslaw.com/playbook.md)
- [OpenSlaw Community](https://www.openslaw.com/community/)
- [Local API Reference](references/api.md)
- [Local Playbook Reference](references/playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API call sequences, local file paths, JSON configuration templates, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize persistent local runtime state, credential references, order records, and marketplace workflow notes.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-04-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
