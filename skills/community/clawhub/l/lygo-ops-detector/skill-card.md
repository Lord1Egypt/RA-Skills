## Description:

LYGO Ops Detector provides local, consent-gated heuristics for reviewing operator-supplied text and public metadata for evasion, coordination, saturation, and policy-refusal signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO Sovereign License v2.0

## Use Case:

Developers and analysts use this skill when explicitly asked to run AETHON D9 or evasion-index style review on text supplied by the user. The skill produces heuristic review signals and boundaries, not identity, guilt, affiliation, legal, or medical determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic scores could be mistaken for proof about a person, nationality, affiliation, or wrongdoing.

Mitigation: Treat outputs as review signals only and require human review before any reputational, employment, legal, or social action.

Risk: Private or local files could be analyzed without proper authority.

Mitigation: Use only text and metadata the operator has authority to analyze; file inputs require explicit --i-consent.

Risk: Country or public metadata fields could be misused as nationality guilt.

Mitigation: Use public metadata only as weighted context; a country label alone cannot clear the operational threshold.

Risk: Calibration results could be presented as production-grade performance claims.

Mitigation: Keep the documented distinction between operational review thresholds and low-threshold calibration suite ranking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-ops-detector)
- [ClawHub release page](https://clawhub.ai/deepseekoracle/lygo-ops-detector)
- [Metadata homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-ops-detector)
- [Quickstart](artifact/examples/quickstart.md)
- [AETHON D9 blueprint](artifact/references/AETHON_D9_BLUEPRINT.md)
- [Security and ethics](artifact/references/SECURITY.md)
- [SkillSpector audit](https://clawhub.ai/deepseekoracle/skills/lygo-ops-detector/security-audit)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI examples and optional JSON detector output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local stdlib CLI behavior; file reads require --i-consent; evaluation writes are limited to tests/.]

## Skill Version(s):

1.4.0 (source: evidence release metadata, claw.json, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
