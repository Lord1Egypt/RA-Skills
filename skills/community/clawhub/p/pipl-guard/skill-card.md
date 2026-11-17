## Description:

PIPL Guardrail is a local runtime guardrail that detects, masks, or blocks personal information in AI application input and output text before it reaches a model or user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI application teams use this skill to add a China PIPL-oriented runtime guardrail that checks user input and model output for personal information, then returns a pass, masked, blocked, or inspect-only decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detect mode can return the original input in its output, which may expose plaintext personal information if passed onward or logged.

Mitigation: Use mask or block mode on production input and output paths, and avoid logging detect-mode results that may contain plaintext.

Risk: Rule-based personal-information detection can miss data or produce false positives and does not provide legal advice or compliance proof.

Mitigation: Use the skill as one control in a broader compliance process, review high-impact decisions, and consult qualified legal or privacy specialists for compliance determinations.

## Reference(s):

- [PIPL Guardrail README](artifact/README.md)
- [PIPL Guardrail Skill Definition](artifact/SKILL.md)
- [PIPL Guardrail Changelog](artifact/CHANGELOG.md)
- [ClawHub Skill Page](https://clawhub.ai/wwumit/skills/pipl-guard)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or structured JSON guardrail decisions with masked or blocked output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports detect, mask, and block actions; detect mode can include the original input in the output field.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
