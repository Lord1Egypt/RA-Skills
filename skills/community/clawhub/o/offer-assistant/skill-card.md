## Description:

简历全流程助手：传一份旧简历拆解为永久素材库，后续任意 JD 一键匹配生成定制简历 + 干净 PDF + 模拟面试。

This skill is ready for commercial/non-commercial use.

## Publisher:

[antiwork-lab](https://clawhub.ai/user/antiwork-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers and career-support agents use this skill to turn an existing resume into a reusable material library, analyze job descriptions, generate tailored resumes and PDFs, run mock interviews, and track applications or interview retrospectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume, contact, JD, application, and interview data may be extracted and persisted to Feishu-backed documents.

Mitigation: Confirm the Feishu account and destination folder before use, review extracted data before document creation, and minimize unnecessary personal or employer-sensitive information.

Risk: Helper scripts and dependency installation were flagged by the authoritative security evidence as needing review.

Mitigation: Inspect and fix the PDF generation and dependency setup scripts before installing or running them, and execute them in a controlled workspace.

Risk: OCR or parsed job-description data can be inaccurate, which may affect the material library, resume content, and interview preparation.

Mitigation: Require user confirmation for extracted company names, roles, dates, metrics, and other key facts before treating them as source material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antiwork-lab/skills/offer-assistant)
- [Resume parsing methodology](artifact/references/resume-parsing.md)
- [JD analysis and matching methodology](artifact/references/jd-methodology.md)
- [Resume writing methodology](artifact/references/resume-methodology.md)
- [Mock interview methodology](artifact/references/mock-interview.md)
- [Tracking and interview review methodology](artifact/references/tracking.md)
- [PDF generation methodology](artifact/references/pdf-generation.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown reports, generated HTML resume content, PDF files, shell commands, and configuration notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on Node.js, Chrome or Chromium, Tesseract OCR, the ws npm package, and optional CHROME_PATH or TESSERACT_LANG environment variables.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
