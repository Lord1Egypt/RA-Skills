## Description:

Provides templates, checklists, and decision-support frameworks for medical OCR, liability determination, anti-fraud assessment, and claims reporting, with human review required for all claim decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance professionals and analysts can use the skill's advisory frameworks to structure receipt review, liability and fraud assessment, and claims report drafts. A licensed insurance professional must review and confirm all claim decisions.

### Deployment Geography for Use:

China-focused; validate insurance and data-protection requirements for other jurisdictions.

## Known Risks and Mitigations:

Risk: Claim approvals, denials, payout estimates, or fraud labels could be mistaken for final decisions.

Mitigation: Require a licensed insurance professional to review every output and verify it against policy terms and source records before acting.

Risk: Medical and claimant records may contain sensitive personal information.

Mitigation: Obtain consent, minimize and redact data, confirm OCR vendor retention and transfer terms, and prefer private processing for production use.

Risk: The benign security verdict has medium confidence and incomplete coverage, with a manifest parse issue and three missing references.

Mitigation: Review the manifest and unresolved references before installation, and treat the scan as partial evidence rather than full verification.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gechengling/skills/insurance-claims-intelligence)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text, Code]

**Output Format:** [Markdown checklists, decision trees, report drafts, and illustrative Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory drafts only; requires licensed human review; includes no executable models or production OCR integration.]

## Skill Version(s):

5.0.8 (source: server-resolved release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
