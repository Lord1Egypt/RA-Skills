## Description:

Drafts interpretive comments for complex clinical laboratory panel results, including critical-value notation, delta-check comparison, specimen-quality notes, pattern recognition, and clinical-correlation language for licensed review before release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical laboratory scientists, pathologists, lab directors, and laboratory medicine trainees use this skill to draft interpretive comments for supported lab panels before licensed review, sign-out, or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive patient identifiers could be exposed if users paste full names, medical record numbers, or dates of birth into the agent conversation.

Mitigation: Use only accession or case references and avoid direct identifiers.

Risk: Generic reference ranges or critical-value thresholds may not match local laboratory policy.

Mitigation: Confirm all draft comments against institutional reference intervals, critical-value rules, and laboratory policy before use.

Risk: Drafted interpretive comments could be mistaken for final clinical guidance or released without appropriate review.

Mitigation: Require licensed pathologist or authorized-provider review and approval before sign-out, result release, or provider notification.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/interpretive-lab-comment-drafter)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft interpretive comment with review block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft only; must be reviewed by a licensed pathologist or authorized provider before release.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact changelog, released 2026-05-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
