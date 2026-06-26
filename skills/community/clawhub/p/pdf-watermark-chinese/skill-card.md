## Description: <br>
PDF watermark addition and removal support for text and image watermarks, with Chinese-language documentation and tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pwcy1978-boop](https://clawhub.ai/user/pwcy1978-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document operators can use this skill to add text or image watermarks to local PDF files, including Chinese text watermarks. Users should verify PDF outputs themselves and should not rely on the advertised removal path to sanitize or declassify documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises PDF watermark removal, but the security evidence says the current removal path copies the PDF unchanged, so sensitive marks may remain. <br>
Mitigation: Use the skill for local watermark addition only unless removal results are manually inspected and independently verified; do not use it for sanitization, anonymization, declassification, or legal redaction. <br>
Risk: The security verdict is suspicious for this release. <br>
Mitigation: Install only when local PDF watermarking is required, review the skill and generated outputs before operational use, and keep original documents backed up. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pwcy1978-boop/pdf-watermark-chinese) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce modified local PDF files when the generated commands or scripts are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
