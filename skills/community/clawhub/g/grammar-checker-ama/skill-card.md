## Description:

Grammar checking tool for AMA style medical writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and medical-writing teams use this skill to check supplied text for AMA-style grammar issues and receive correction suggestions with explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a draft local script intended for medical writing, so sensitive medical text should not be assumed safe for routine use without review.

Mitigation: Run it only in a trusted local workspace and verify behavior before using sensitive medical text.

Risk: The documentation describes broader AMA compliance and medical terminology validation than the current implementation demonstrates.

Mitigation: Review the current script behavior before relying on results, and align documentation or implementation before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/grammar-checker-ama)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires text input through the --text argument; current evidence shows local execution with no network access.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
