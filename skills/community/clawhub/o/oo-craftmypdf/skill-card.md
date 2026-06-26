## Description: <br>
CraftMyPDF helps an agent use the OOMOL `oo` CLI to inspect CraftMyPDF schemas, generate hosted PDFs from templates, and read account or template information through an OOMOL-connected CraftMyPDF account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to create PDFs from CraftMyPDF templates and inspect CraftMyPDF account or template data without handling raw API tokens directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The one-time `oo` CLI installer uses shell or PowerShell commands that should be reviewed before execution. <br>
Mitigation: Review the official install guide and installer script, or use a trusted package path, before running installation commands. <br>
Risk: PDF generation is a write action that can create hosted output from user-provided template data. <br>
Mitigation: Confirm the exact template ID, payload, and expected effect with the user before running `create_pdf`. <br>
Risk: The skill depends on OOMOL as the credential broker for CraftMyPDF. <br>
Mitigation: Install only when using OOMOL for credential mediation is acceptable, and reconnect CraftMyPDF only after authentication or connection failures. <br>


## Reference(s): <br>
- [CraftMyPDF homepage](https://craftmypdf.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [CraftMyPDF ClawHub listing](https://clawhub.ai/oomol/oo-craftmypdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent actions can return JSON responses from the `oo` CLI, including hosted PDF URLs and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
