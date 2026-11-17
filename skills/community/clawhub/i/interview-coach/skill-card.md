## Description:

面试准备助手，支持根据简历和岗位 JD 生成针对性面试题、参考答案和答题要点，也支持针对 JD 输出个性化简历修改建议和修改原因。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzw6](https://clawhub.ai/user/jzw6)

### License/Terms of Use:

MIT-0

## Use Case:

External users and candidates use this skill to prepare for interviews by comparing a resume with a job description, generating focused interview questions, and improving resume phrasing without inventing new experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image and scanned-PDF parsing can upload sensitive resume or job-description content to PaddleOCR.

Mitigation: Prefer text PDFs, Word files, TXT files, or pasted text when possible, and use OCR only after confirming the documents are acceptable to send to that service.

Risk: A custom PADDLEOCR_SERVER_URL can redirect document content and the OCR token to an untrusted destination.

Mitigation: Leave PADDLEOCR_SERVER_URL unset unless the configured OCR endpoint is fully trusted.

Risk: The parser may install Python packages automatically into the system Python environment.

Mitigation: Run the skill in an isolated environment and review package installation behavior before use.

## Reference(s):

- [Question Types Reference](references/question-types.md)
- [Resume Optimization Reference](references/resume-optimization.md)
- [PaddleOCR AIStudio Access Token](https://aistudio.baidu.com/paddleocr)
- [ClawHub Skill Page](https://clawhub.ai/jzw6/skills/interview-coach)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with structured interview questions, reference answers, resume edit suggestions, and occasional shell commands for parsing files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May parse PDF, Word, image, or text inputs into plain text before analysis; OCR is only needed for images and scanned PDFs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
