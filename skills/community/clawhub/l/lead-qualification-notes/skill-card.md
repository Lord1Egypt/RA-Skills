## Description:

Organizes sales lead information into a qualification judgment, key questions, risks, and recommended next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and go-to-market teams use this skill to turn lead background, pain points, budget, and timing into reviewable qualification notes, follow-up questions, risk items, and next-step recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script includes local audit and pattern-scanning modes beyond the stated lead-note generation purpose.

Mitigation: Review the script before deployment, scope execution to intended lead files, and avoid broad filesystem access unless those audit modes are explicitly needed and documented.

Risk: Lead inputs may contain sensitive customer, prospect, or personal information.

Mitigation: Use only necessary local inputs, redact sensitive material where practical, and avoid treating generated notes as authoritative CRM master data.

Risk: Generated qualification notes can be misleading if the source lead data is incomplete or uncertain.

Mitigation: Preserve the skill's review workflow by listing missing information, marking uncertain assumptions, and having a sales owner review notes before action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/lead-qualification-notes)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [README.md](artifact/README.md)
- [resources/spec.json](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown by default, with optional JSON output from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lead qualification notes with explicit missing-information and review sections.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
