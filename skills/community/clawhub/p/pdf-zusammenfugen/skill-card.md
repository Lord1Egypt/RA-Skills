## Description: <br>
Provides a privacy-oriented workflow and local Python script for merging PDFs in a specified order, with guidance for German application document bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsgtcyx](https://clawhub.ai/user/wsgtcyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
German-speaking users and support agents use this skill to merge PDFs locally, confirm input order and output paths, and assemble application PDFs while considering data-protection expectations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The output file may replace an existing PDF if overwrite is used unintentionally. <br>
Mitigation: Confirm the output path before execution and use --overwrite only when replacement is intended. <br>
Risk: Installing or using PDF dependencies can affect the local Python environment. <br>
Mitigation: Prefer installing pypdf in a virtual environment before running the helper script. <br>
Risk: Sensitive PDFs may be exposed if an external website is used instead of the local workflow. <br>
Mitigation: Use the local script for sensitive PDFs and only use the linked external site when it is independently trusted for the documents involved. <br>


## Reference(s): <br>
- [pdfzus.de PDF merge reference](https://pdfzus.de/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash command examples and a Python helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local helper script can produce a merged PDF file when executed with user-selected input files and an output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
