## Description:

Generates Infoxmed VIP membership activation QR codes from natural-language requests by extracting card parameters, confirming them with the user, and calling the Infoxmed batch QR generation endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaochao](https://clawhub.ai/user/yaochao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to generate Infoxmed VIP or membership activation QR-code zip files after providing hospital, business channel, card type, and scan-count details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an API password in ways that could expose it in chat, logs, transcripts, shell history, or persistent profile files.

Mitigation: Use a secure secret manager or temporary environment variable, avoid pasting the password into chat, do not persist it in shell profiles, and rotate any password that may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yaochao/skills/infoxmed-qr-generator)
- [Infoxmed batch QR generation endpoint](https://api.infox-med.com/system/batchGenerateVipQr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and a generated zip file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local zip file containing generated QR codes after user confirmation and API execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
