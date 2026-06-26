## Description: <br>
PDFMonkey lets an agent read PDFMonkey account, document, and template data and create documents through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate PDFMonkey from an agent: inspect action schemas, read account, document, and template data, list document cards, and create documents after confirming write payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through the connected PDFMonkey/OOMOL account. <br>
Mitigation: Use it only in workspaces where that account access is appropriate and review requested permissions before installation. <br>
Risk: The create_document action changes PDFMonkey state. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running write actions. <br>


## Reference(s): <br>
- [PDFMonkey homepage](https://pdfmonkey.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub PDFMonkey skill page](https://clawhub.ai/oomol/oo-pdfmonkey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include connector execution results returned as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
