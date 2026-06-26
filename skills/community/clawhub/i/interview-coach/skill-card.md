## Description: <br>
面试助手 helps users analyze resumes and job descriptions, generate targeted interview questions with answer guidance, and produce JD-specific resume optimization suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzw6](https://clawhub.ai/user/jzw6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers, career coaches, and recruiting-support users use this skill to prepare for interviews from a resume and job description, or to refine a resume for a target role without adding unsupported experience. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install Python parsing libraries when its file parser is first used. <br>
Mitigation: Review the skill and run it only in environments where installing Python packages at first use is acceptable. <br>
Risk: Image files and scanned PDFs may be sent to a configured PaddleOCR endpoint for OCR processing. <br>
Mitigation: Prefer pasted text, Word files, text files, or text-based PDFs for sensitive resumes and job descriptions; use OCR only when the configured service is acceptable for the data. <br>


## Reference(s): <br>
- [Question Types Reference](references/question-types.md) <br>
- [Resume Optimization Reference](references/resume-optimization.md) <br>
- [PaddleOCR AIStudio](https://aistudio.baidu.com/paddleocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured interview questions, resume-edit suggestions, and inline shell commands for optional file parsing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May parse PDF, Word, image, and text inputs before producing advice; OCR for images and scanned PDFs requires PADDLEOCR_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
