## Description: <br>
Homework Grader helps teachers OCR math homework, compare student answers to a provided answer key, and generate Excel and PDF error-analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhy123456lhy](https://clawhub.ai/user/lhy123456lhy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teachers use this skill to grade batches of math homework from images, confirm OCR-recognized answers, identify common mistakes, and produce class-level reports for review or instruction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can contain sensitive student information. <br>
Mitigation: Use student numbers or pseudonyms when possible, process only authorized homework data, and store or delete generated reports according to school or organization privacy rules. <br>
Risk: OCR or answer parsing errors can lead to incorrect grading results. <br>
Mitigation: Have the teacher review the recognized answer key and spot-check grading results before relying on the Excel or PDF reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lhy123456lhy/homework-grader) <br>
- [Answer format reference](references/answer_format.md) <br>
- [Output format reference](references/output_format.md) <br>
- [Tesseract OCR Windows installer reference](https://github.com/UB-Mannheim/tesseract/wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated JSON, Excel, and PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python dependencies and Tesseract OCR; the default key-question error-rate threshold is 40%.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
