## Description: <br>
Reads, extracts, merges, splits, and generates PDF files from local inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[droba07](https://clawhub.ai/user/droba07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run local PDF reading, table extraction, metadata inspection, merge, split, and HTML/Markdown-to-PDF generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing untrusted PDFs or HTML can expose the local workspace to risks in PDF and HTML rendering libraries. <br>
Mitigation: Run the scripts only on documents you choose, avoid privileged workspaces for untrusted inputs, and keep the Python dependencies patched. <br>
Risk: Metadata extraction can print document metadata such as title, author, creator, and producer. <br>
Mitigation: Review outputs before sharing them and avoid running metadata extraction on highly sensitive documents unless disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/droba07/pdf-rw-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, plus text, CSV, JSON, and PDF file outputs from local scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and local PDF-processing packages: pdfplumber, pypdf, and weasyprint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
