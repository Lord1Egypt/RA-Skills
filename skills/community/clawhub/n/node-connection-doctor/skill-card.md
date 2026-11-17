## Description:

Diagnoses OpenClaw node connection issues, generates repair guidance, and can optionally run local fixes such as token reset and gateway restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huoxinjiang](https://clawhub.ai/user/huoxinjiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to troubleshoot node pairing, gateway status, VPN/Tailscale, and configuration issues, then receive specific commands or an optional guided repair flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests system:cron permission even though the provided diagnostic and repair scripts do not show a scheduled-check requirement.

Mitigation: Remove the cron permission or document the scheduled behavior before installation or publication.

Risk: Repair mode can change OpenClaw configuration by clearing pairing tokens, generating new tokens, and restarting the gateway.

Mitigation: Require an explicit preview and user confirmation, back up relevant configuration first, and provide rollback guidance before applying fixes.

Risk: Documentation mentions silent or automatic repair behavior for system-changing operations.

Mitigation: Avoid silent repair mode until the skill reliably confirms changes and supports recovery if a token reset or gateway restart fails.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huoxinjiang/skills/node-connection-doctor)
- [Validation Guide](artifact/references/validation-guide.md)
- [FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text, Markdown documentation, CLI command suggestions, and optional HTML or JSON diagnostic reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can execute local OpenClaw CLI repair steps when fix mode is confirmed by the user.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
