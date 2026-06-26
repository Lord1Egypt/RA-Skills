## Description: <br>
PDF Utils enables OCR of image-based PDFs, extraction of arXiv IDs from text or OCR output, and scriptable PDF tasks like merging, splitting, and rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwllu](https://clawhub.ai/user/wangwllu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to automate local PDF workflows, including OCR for scanned PDFs, arXiv reference mining, and repeatable merge, split, and page-rendering operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local scripts can read PDFs and write generated OCR text, rendered images, split PDFs, merged PDFs, or downloaded arXiv papers to user-selected paths. <br>
Mitigation: Run the skill in a virtual environment and use a dedicated output directory to avoid accidental overwrites or mixing generated files with source documents. <br>
Risk: OCR quality can be poor for handwritten, low-resolution, or very large scanned PDFs, which may lead to incomplete extracted text or references. <br>
Mitigation: Process large PDFs in page ranges, adjust OCR settings when needed, and manually review extracted references before relying on them. <br>
Risk: Optional arXiv downloading requires network access and saves downloaded PDFs locally. <br>
Mitigation: Use downloads only when network access is acceptable and direct output to a controlled folder. <br>


## Reference(s): <br>
- [PDF Utils usage reference](references/usage.md) <br>
- [ClawHub skill page](https://clawhub.ai/wangwllu/pdf-utils) <br>
- [Publisher profile](https://clawhub.ai/user/wangwllu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local PDF, text, and image files through user-run scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
