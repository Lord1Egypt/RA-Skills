## Description: <br>
PDF.co lets an agent inspect, convert, merge, split, compress, and create PDFs through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to handle PDF.co-backed document workflows from an agent, including PDF inspection, conversion, compression, splitting, merging, and account balance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a connected PDF.co account through OOMOL and may consume account credits or require sensitive account access. <br>
Mitigation: Install and use it only for an intended OOMOL-connected PDF.co account; run login or connection setup only after an authentication or connection failure. <br>
Risk: PDF processing can send document URLs, page content, or generated documents to PDF.co and OOMOL-connected services. <br>
Mitigation: Review payloads before execution and avoid processing sensitive documents unless the user has approved that data flow. <br>
Risk: Write-tagged actions such as PDF merging create or modify generated PDF outputs. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>


## Reference(s): <br>
- [PDF.co ClawHub Release](https://clawhub.ai/oomol/oo-pdf-co) <br>
- [PDF.co Homepage](https://pdf.co) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the pdf_co connector and typically return JSON responses containing data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: skill frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
