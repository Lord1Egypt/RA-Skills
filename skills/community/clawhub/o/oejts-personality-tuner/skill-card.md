## Description:

Administer and score the Open Extended Jungian Type Scales (OEJTS 1.2), map results to MBTI-style interaction preferences, and propose or apply personality-aware tuning updates to USER.md and SOUL.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salvagedeck](https://clawhub.ai/user/salvagedeck)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to run an OEJTS-style questionnaire, calculate an MBTI-style preference profile, and convert the result into assistant behavior guidance. It can preview or apply managed preference blocks for USER.md and SOUL.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently add or replace managed personality-tuning blocks in USER.md and SOUL.md.

Mitigation: Run dry-run mode first, review the proposed blocks, and apply only when the user wants those assistant preference files changed.

Risk: OEJTS results could be treated as a fixed identity rather than a preference signal.

Mitigation: Use the profile as adjustable guidance, keep user override available, and prefer live user feedback when it conflicts with test output.

## Reference(s):

- [OEJTS 1.2 Reference](references/oejts-1.2.md)
- [Behavior Mapping](references/behavior-mapping.md)
- [ClawHub Skill Page](https://clawhub.ai/salvagedeck/skills/oejts-personality-tuner)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and plain text with optional managed file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in dry-run mode to preview USER.md and SOUL.md changes before writing managed blocks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
