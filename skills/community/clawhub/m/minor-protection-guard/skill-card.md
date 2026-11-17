## Description:

Minor Protection Guard checks product copy, feature descriptions, user agreements, and operations text for six high-frequency minor-protection compliance risk statements before publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, compliance reviewers, and agents use this skill to screen Chinese-language product, game, livestreaming, social, and education content for minor-protection wording risks before release. It provides local findings and remediation guidance for real-name verification, teen mode, anti-addiction controls, spending limits, child information consent, and harmful-content filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker is focused on PRC minor-protection wording and may not cover other jurisdictions or non-Chinese workflows.

Mitigation: Use it as a local pre-publication screen and add jurisdiction-specific review for releases outside the PRC-focused scope.

Risk: A clean result does not establish legal compliance or replace review of actual product controls such as real-name systems, teen mode, anti-addiction limits, payment controls, consent flows, and content filtering.

Mitigation: Escalate high-stakes or public releases to compliance and legal review, and verify the underlying product implementation separately from the text scan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/minor-protection-guard)
- [Publisher profile](https://clawhub.ai/user/wwumit)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON risk findings with categories, severity, matched terms, source positions, legal basis, and remediation suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python standard library only and no third-party runtime dependencies.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, package.json, CHANGELOG released 2026-08-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
