## Description:

Helps agents turn handover or project-transition notes into structured, reviewable Markdown that preserves explicit and tacit knowledge while flagging risks and missing information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, and operations teams use this skill to prepare personnel-offboarding, project-handoff, and knowledge-transfer packs from local input notes. It produces reviewable drafts and checklists covering responsibilities, contacts, tacit knowledge, unresolved items, risks, and handover recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input handover notes may contain plaintext secrets, privileged information, or unnecessary personal data.

Mitigation: Replace sensitive values with references or locations, redact unnecessary personal data, and review generated Markdown before sharing.

Risk: Generated Markdown from untrusted input may carry misleading, sensitive, or unsafe content into downstream review workflows.

Mitigation: Treat generated Markdown as untrusted content, verify facts against source materials, and avoid opening or publishing it in privileged contexts without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/handover-memory-pack)
- [README](artifact/README.md)
- [Skill specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration]

**Output Format:** [Markdown or JSON, with optional local shell command usage for file-based generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with python3 and standard-library dependencies; output is intended to be reviewed before sharing or acting on it.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
