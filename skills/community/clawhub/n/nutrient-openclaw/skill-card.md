## Description:

Nutrient OpenClaw routes document conversion, OCR, extraction, redaction, watermarking, signing, and local credit-ledger requests to the pinned Nutrient OpenClaw plugin with external-transfer, credit-estimation, and confirmation safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdrhyne](https://clawhub.ai/user/jdrhyne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and operate a pinned Nutrient document-processing plugin for conversion, OCR, extraction, redaction, watermarking, signing, and local credit-ledger inspection. It is intended for workflows that need explicit external-transfer disclosure, bounded credit estimates, user confirmation, source preservation, and careful handling of credentials and high-risk document outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Most document-processing operations send selected files or pages to Nutrient DWS and consume credits.

Mitigation: State the external transfer, provide a numeric or bounded credit estimate from official pricing, and obtain explicit confirmation for each unchanged invocation.

Risk: A Nutrient API key could be exposed through chat, command arguments, logs, or configuration examples.

Mitigation: Configure credentials only through protected settings or an approved secrets manager, and verify readiness from redacted status and tool availability.

Risk: Redaction outputs may permanently remove content or miss sensitive information.

Mitigation: Prefer deterministic redaction when presets fit, preserve the source, treat AI-redacted output as a candidate, and require human review of every affected page before distribution.

Risk: Signing output may not establish signer identity, authority, consent, certificate custody, or legal sufficiency.

Mitigation: Confirm the signing boundary and route regulated or certificate-controlled signing needs to an approved workflow with human or legal approval.

Risk: The local credit checker can report stale prior ledger state rather than a live quote or reservation.

Mitigation: Use local credit status only as context and never as a substitute for current pricing-based estimates or per-call authorization.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jdrhyne/skills/nutrient-openclaw)
- [Reviewed Plugin Contract](references/plugin-contract.md)
- [Pinned Plugin Source](https://github.com/PSPDFKit-labs/nutrient-openclaw)
- [npm Package](https://www.npmjs.com/package/@nutrient-sdk/nutrient-openclaw)
- [OpenClaw Skills](https://docs.openclaw.ai/skills)
- [OpenClaw Secrets](https://docs.openclaw.ai/gateway/secrets)
- [OpenClaw Tool Plugins](https://docs.openclaw.ai/plugins/tool-plugins)
- [Nutrient Credit Calculation](https://www.nutrient.io/guides/dws-processor/pricing/calculate-credit-usage/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with confirmation blocks and shell commands when installation is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bounded credit estimates and explicit yes/no confirmation before each credit-consuming external processing call.]

## Skill Version(s):

1.3.0 (source: evidence release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
