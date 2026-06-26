## Description: <br>
Converts an HTML file, report, or webpage snapshot to PDF using headless Chrome through Puppeteer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[owenrao](https://clawhub.ai/user/owenrao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn local HTML reports or webpage snapshots into single-page poster-style PDFs or paginated A4/Letter documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering untrusted HTML in Chromium can execute page JavaScript and load remote resources during conversion. <br>
Mitigation: Use a low-privilege isolated environment, block network access for sensitive documents, and review HTML inputs before conversion. <br>
Risk: The bundled Chromium launch configuration disables sandboxing for Docker and CI compatibility. <br>
Mitigation: Prefer container or VM isolation, avoid privileged execution, and enable Chromium sandboxing where the runtime supports it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/owenrao/html2pdf) <br>
- [Publisher profile](https://clawhub.ai/user/owenrao) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown instructions with command-line examples and bundled JavaScript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a PDF file from an HTML input when the bundled Node.js script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
