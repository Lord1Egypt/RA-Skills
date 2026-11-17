## Description:

Turns FAQ entries, chat logs, and scattered notes into reviewable SOP or Playbook drafts with exception branches and rollback steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, support, training, and knowledge-management users can use this skill to transform provided FAQ, chat, or procedure notes into structured SOP or playbook drafts. It is suited for reviewable documentation, not direct system changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script can read any file path supplied as input.

Mitigation: Review and scope input paths before use, and avoid passing sensitive or unrelated files.

Risk: The generated playbook content may be incomplete or incorrect if source notes are incomplete.

Mitigation: Treat outputs as reviewable drafts and require human approval before publishing or using them for operational changes.

Risk: Dormant audit and scanning code is present but not enabled by the shipped configuration.

Mitigation: Do not rely on audit or scanning behavior unless the publisher documents and scopes those modes clearly.

Risk: Inputs may contain personal information or sensitive operational details.

Mitigation: Sanitize or limit sensitive source material before processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/knowledge-to-playbook)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Output Template](artifact/resources/template.md)
- [Structured Spec](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown or JSON generated from local input files, with optional shell command usage for the bundled Python helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are reviewable drafts with sections for scenarios, standard steps, exception branches, rollback plans, upgrade paths, common pitfalls, missing information, and next steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
