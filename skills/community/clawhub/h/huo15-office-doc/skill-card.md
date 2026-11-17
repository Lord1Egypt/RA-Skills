## Description:

Huo15 Office Doc helps agents generate enterprise Word documents in rule-based or template-based modes, including document metadata, formatting, version history, approvals, headers, footers, and tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business users use this skill to draft or export Chinese enterprise Word documents such as contracts, proposals, reports, and meeting minutes from plain text or a .docx template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports under-disclosed credential-backed network access.

Mitigation: Review the package before installing, require explicit opt-in for remote Odoo lookup, and use normal TLS verification.

Risk: The security evidence reports an unrelated workspace configuration generator that can persist agent instructions and memory.

Mitigation: Separate Word document generation from OpenClaw configuration generation and clearly disclose credential access, network calls, and home-directory writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-office-doc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, plain text document content, shell commands, configuration files, and .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce Word documents and may write local configuration or memory files when the bundled configuration generator is used.]

## Skill Version(s):

3.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
