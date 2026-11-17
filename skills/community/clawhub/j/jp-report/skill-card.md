## Description:

Generate a formal Japanese corporate-style HTML document and PDF from source material for business reports, compliance documents, security overviews, or Japanese-language reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken-chy129](https://clawhub.ai/user/ken-chy129)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external business users, and developers use this skill to turn source material into formal Japanese corporate HTML and PDF reports with structured chapters, cover page, table of contents, and A4 pagination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill renders source material into HTML and PDF, so untrusted HTML or attacker-supplied markup could affect generated output or local rendering behavior.

Mitigation: Use trusted source material, sanitize or review pasted markup before generation, and run PDF rendering in a hardened or network-restricted environment for sensitive workflows.

Risk: The PDF export depends on local headless Chrome execution.

Mitigation: Confirm Chrome is installed and patched before use, and review the generated HTML before invoking PDF export when handling confidential reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ken-chy129/skills/jp-report)
- [README](README.md)
- [HTML Components](docs/components.md)
- [Design Rules](docs/design-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated self-contained HTML files, PDF files, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a paginated A4 HTML report and invokes the bundled PDF export script when Chrome is available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
