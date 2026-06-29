## Description: <br>
Gxpcode Translator helps an agent translate text and PDF inputs with terminology support, producing bilingual HTML and Markdown outputs for PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gxpcode-hezhong](https://clawhub.ai/user/gxpcode-hezhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate text or PDF documents while preserving configured terminology. It is especially oriented toward domain-specific documents where the user supplies a field, optional subdomain, and terminology dictionary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that full original and translated content may be retained in local log files. <br>
Mitigation: Avoid confidential or regulated documents unless logging is disabled, changed, or reviewed for the deployment environment. <br>
Risk: The security scan reports cloud OCR usage and local PaddleOCR token storage for PDF processing. <br>
Mitigation: Use the PDF route only when the OCR path is acceptable, protect the token, and consider a local OCR path for sensitive documents. <br>


## Reference(s): <br>
- [Source repository](https://github.com/Gxpcode-hezhong/Gxpcode-translator) <br>
- [Source commit](https://github.com/Gxpcode-hezhong/Gxpcode-translator/tree/756769d10bcfdd4e378585fbf88aa3fb799dbfc5) <br>
- [ClawHub skill page](https://clawhub.ai/gxpcode-hezhong/skills/gxpcode-translator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain translated text for text requests; generated bilingual HTML and Markdown files for PDF requests; JSON-backed configuration for local settings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PDF workflows can create local logs, intermediate files, and bilingual output files under the configured output directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
