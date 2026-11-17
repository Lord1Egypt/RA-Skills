## Description:

Compares a contest submission fingerprint with supplied known fingerprints and returns a JSON decision-support report, not a definitive plagiarism finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Contest participants and reviewers use supplied fingerprints to screen submissions against a known-hashes list before human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instructions may prompt users to share unpublished submission content even though the checker only compares fingerprints.

Mitigation: Provide only precomputed hashes and a known-hashes list; do not paste unpublished work into the skill.

Risk: A limited or absent comparison set cannot establish originality, and similarity results may be misleading.

Mitigation: Use findings only as decision support and require human review before any contest decision.

## Reference(s):

- [Originality Check on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/originality-check)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes comparison results, warnings, and status codes; a missing comparison corpus produces a warning.]

## Skill Version(s):

1.0.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
