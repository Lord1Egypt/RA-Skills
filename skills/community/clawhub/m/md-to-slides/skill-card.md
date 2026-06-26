## Description: <br>
Converts Markdown content into PowerPoint-compatible slide decks, with a fallback HTML presentation output when python-pptx is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and business users can use this skill to turn Markdown notes or outlines into presentation files for reports, lessons, and meetings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fallback HTML output can include unsanitized content from Markdown input. <br>
Mitigation: Use trusted Markdown only for HTML fallback output, or install python-pptx and generate .pptx output instead. <br>
Risk: Expected .pptx output is not produced when python-pptx is unavailable. <br>
Mitigation: Install python-pptx before relying on PowerPoint output, and confirm generated files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darbling/md-to-slides) <br>
- [Publisher profile](https://clawhub.ai/user/darbling) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with command examples; generated presentation files are .pptx or fallback .html] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports file-based input and theme selection; .pptx output depends on python-pptx being installed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
