## Description: <br>
PDF parsing tool for AI/RAG that converts PDF files to Markdown, JSON, HTML, text, rebuilt PDF, and image-aware Markdown outputs with layout preservation, bounding boxes, and image extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wtjjacobj](https://clawhub.ai/user/wtjjacobj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to extract structured text, layout, image, and table content from PDFs for AI processing, RAG pipelines, and document analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parsed outputs may contain sensitive content from source PDFs. <br>
Mitigation: Use the skill only on PDFs you are allowed to process, enable or apply sanitization when needed, and review extracted content before sharing it or adding it to AI/RAG systems. <br>
Risk: Installing or invoking the wrong package could run code outside the intended trust boundary. <br>
Mitigation: Confirm that `opendataloader-pdf` is the intended package before installation and execution. <br>
Risk: Generated files may be written to an unintended location. <br>
Mitigation: Choose output directories deliberately and review generated Markdown, JSON, HTML, PDF, text, and image files before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wtjjacobj/opendataloader-pdf-wuxie) <br>
- [Project homepage from metadata](https://github.com/opendataloader-project/opendataloader-pdf) <br>
- [Test script](references/test_script.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON, HTML, Text, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated document outputs may be Markdown, JSON, HTML, text, PDF, and extracted image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports page ranges, image directories, structure-tree parsing, table detection options, reading-order options, hybrid mode, sanitization, and stdout output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
