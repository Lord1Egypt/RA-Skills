## Description: <br>
Markdown2Doc converts Markdown files into PDF or DOCX documents with support for template themes, document structure preservation, heading hierarchy, and embedded images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoyt27](https://clawhub.ai/user/haoyt27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Markdown2Doc to convert local Markdown files into shareable PDF or DOCX documents, optionally applying DOCX themes and embedding referenced local images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown content and locally referenced image files are sent to lab.hjcloud.com for conversion. <br>
Mitigation: Use only documents appropriate for cloud processing; do not convert confidential documents, secrets, proprietary notes, private screenshots, or sensitive diagrams. <br>
Risk: Referenced local images may include files the user did not intend to send with the Markdown document. <br>
Mitigation: Review image references before converting and keep the Markdown source folder limited to files intended for upload. <br>


## Reference(s): <br>
- [Markdown2Doc ClawHub page](https://clawhub.ai/haoyt27/markdown2doc) <br>
- [Markdown2Doc conversion service](https://lab.hjcloud.com/llmdoc) <br>
- [Docchain skills support](https://github.com/wct-lab/docchain-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [PDF or DOCX files generated from Markdown, with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves the converted file beside the source Markdown file; DOCX output supports optional themes.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
