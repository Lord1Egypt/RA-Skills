## Description: <br>
Convert multi-page PDFs into a single vertical long image by concatenating all pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kieferHuan](https://clawhub.ai/user/kieferHuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users use this skill to turn a multi-page PDF into one vertically concatenated PNG for sharing, visual review, or scrolling summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python code and processes user-selected PDF files, so users should only run it on files they are permitted to process. <br>
Mitigation: Review the command and input path before execution, install dependencies from trusted package sources, and run in a controlled environment when handling sensitive documents. <br>
Risk: Large PDFs or high scale settings can create very large image files and consume significant memory or disk space. <br>
Mitigation: Use the default scale first, increase scale only when needed, and verify available memory and output disk space before processing long documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kieferHuan/pdf2image) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with bash commands; generated artifact is a PNG image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts an input PDF path, optional output PNG path, and optional render scale.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
