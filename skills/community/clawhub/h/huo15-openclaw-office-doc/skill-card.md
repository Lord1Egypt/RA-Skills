## Description:

Generates enterprise Word and PDF documents from markdown-style content across business formats, including contracts, reports, plans, API docs, deployment docs, resumes, quotes, and press releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Employees, external business users, and developers can use this skill to draft structured Chinese enterprise documents and convert markdown-style source content into Word or PDF deliverables. It is suited for contracts, project and operations reports, technical documentation, and administrative documents where format presets and company branding are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The document generators can use local company metadata and may fall back to Odoo credentials when that path is enabled.

Mitigation: Use explicit --company-name and --logo-path values, or run with --no-odoo unless the credential flow and target Odoo instance have been reviewed.

Risk: The bundled OpenClaw configuration generator can create persistent identity and memory files in the selected output directory.

Mitigation: Run it first against a temporary review directory and copy only approved files into an active OpenClaw workspace.

Risk: Generated business, HR, security, or legal documents can be incomplete or incorrect if the prompt content or templates are not reviewed.

Mitigation: Require human review before using generated contracts, policies, incident materials, or customer-facing documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-office-doc)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)
- [Template README](templates/README.md)
- [OpenOffice PDF export reference](https://wiki.openoffice.org/wiki/API/Tutorials/PDF_export)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands that can create .docx and .pdf files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents may depend on local company metadata, logo files, fonts, and optional conversion backends.]

## Skill Version(s):

7.9.4 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
