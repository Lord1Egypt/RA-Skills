## Description:

Drafts an ICH E2D and EU GVP Module VI-aligned ICSR narrative packet for a single adverse-event case, including valid-case checks, reportability clocks, MedDRA prompts, follow-up questions, and required safety-physician or QPPV review before submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Drug-safety processors, pharmacovigilance scientists, medical reviewers, QPPV staff, safety officers, and PV vendors use this skill to convert one adverse-event case into a de-identified draft ICSR narrative packet. The packet supports review of case validity, reportability timing, seriousness, expectedness, causality, follow-up needs, and unresolved gaps before any regulatory transmission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft ICSR content could affect regulated pharmacovigilance decisions if used without qualified review.

Mitigation: Require safety-physician or QPPV review for every draft before any submission, as stated in the security guidance and artifact behavior.

Risk: Regional reporting rules, clocks, or routing expectations may differ or change.

Mitigation: Users should verify current regional reporting rules in approved safety systems before relying on any reportability clock or route.

Risk: Source case materials can contain protected health information.

Mitigation: Keep source PHI in approved safety systems and use the skill's de-identification boundaries that refuse full patient identifiers in the narrative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/pharmacovigilance-icsr-narrative)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown narrative packet with structured tables, draft labels, follow-up questions, and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only output requiring safety-physician or QPPV review before transmission.]

## Skill Version(s):

0.1.1 (source: server release and artifact changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
