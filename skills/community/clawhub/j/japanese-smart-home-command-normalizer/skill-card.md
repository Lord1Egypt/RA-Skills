## Description:

Normalize short Japanese smart-home voice transcripts after STT into safe structured intents and slots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t0yohei](https://clawhub.ai/user/t0yohei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to normalize short Japanese smart-home transcripts into structured intents and slots before downstream device-control execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can emit fast-path smart-home intents beyond its stated scope.

Mitigation: Use it behind an explicit allowlist of permitted domains and intents before connecting results to automation.

Risk: Ambiguous, multi-device, contradictory, or undeclared-device commands may be mishandled.

Mitigation: Require downstream confirmation for these outputs and for low-confidence or incomplete results.

## Reference(s):

- [Design](references/design.md)
- [Domains](references/domains.md)
- [OpenClaw integration notes](references/openclaw-integration.md)
- [ClawHub skill page](https://clawhub.ai/t0yohei/skills/japanese-smart-home-command-normalizer)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-compatible structured intent and slot examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns confidence and needsConfirmation fields so downstream automation can require confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
