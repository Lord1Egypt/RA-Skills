## Description: <br>
Extract text and metadata from PDF files using PyMuPDF, supporting large files and outputting results in JSON format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to extract readable text and basic metadata from local PDF files, then write the extracted content to JSON for downstream review or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSON can contain sensitive text and metadata extracted from the source PDF. <br>
Mitigation: Treat output files as sensitive document derivatives and store or share them only in approved locations. <br>
Risk: Path checks rely on the current working directory and should not be treated as a strong sandbox, especially around symlinks. <br>
Mitigation: Run the script from a controlled working directory and avoid symlinks or untrusted file paths. <br>
Risk: The skill depends on PyMuPDF being installed in the execution environment. <br>
Mitigation: Install PyMuPDF from a trusted package source before use. <br>


## Reference(s): <br>
- [Pdfreader on ClawHub](https://clawhub.ai/nantes/pdfreader) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated JSON may contain extracted PDF text and metadata; extraction can be limited by page count.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
