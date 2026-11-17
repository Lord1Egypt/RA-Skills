## Description:

Helps detect install-then-update attacks, where a skill passes initial review and later introduces malicious behavior through an update; v1.1 adds cryptographic chain-of-custody checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud)

### License/Terms of Use:


## Use Case:

Developers, security reviewers, and agent operators use this skill to assess whether skill updates introduce undeclared behavior, permission expansion, suspicious timing, rollback gaps, or broken update chain of custody.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may need access to version history or installed skill metadata to assess update-window risk.

Mitigation: Keep checks user-directed and grant only the local or network access needed for the specific assessment.

Risk: Behavioral deltas, timing anomalies, and missing chain-of-custody metadata are signals rather than proof of malicious behavior.

Mitigation: Use the report to prioritize manual review of suspicious update content before taking enforcement action.

Risk: Registries that do not preserve older versions, signatures, or content hashes can leave parts of the assessment without a reliable signal.

Mitigation: Treat absent history or cryptographic metadata as an evidence gap and document the uncertainty in the final review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skills/install-then-update-trap-detector)
- [ClawHub publisher profile](https://clawhub.ai/user/andyxinweiminicloud)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown trap detection report with scores, findings, a risk verdict, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assessments are stronger when version history, installed skill metadata, signing records, and content hashes are available.]

## Skill Version(s):

1.1.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
