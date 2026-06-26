## Description: <br>
PDF-API.io helps agents inspect templates and render PDFs through an OOMOL-connected PDF-API.io account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to list accessible PDF templates, inspect template variables, and render template-backed PDFs through an OOMOL-connected PDF-API.io account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF generation can produce a temporary hosted PDF URL from user-provided data. <br>
Mitigation: Confirm the template, payload, and sensitivity of the data before running render_pdf. <br>
Risk: The skill requires a connected OOMOL account and PDF-API.io credentials. <br>
Mitigation: Install only when the user is comfortable using OOMOL's oo CLI and the connected PDF-API.io account. <br>


## Reference(s): <br>
- [PDF-API.io ClawHub listing](https://clawhub.ai/oomol/oo-pdf-api-io) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [PDF-API.io homepage](https://pdf-api.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return JSON connector responses and temporary hosted PDF URLs when rendering PDFs.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
