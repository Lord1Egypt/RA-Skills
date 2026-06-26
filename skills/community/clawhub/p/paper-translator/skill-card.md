## Description: <br>
Translates academic PDFs from English to Chinese while preserving formulas and layout, producing bilingual and Chinese-only PDFs plus a glossary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xing-xing-coder](https://clawhub.ai/user/xing-xing-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and technical readers use this skill to translate English academic PDFs into Chinese while retaining formulas, layout, bilingual output, monolingual output, and glossary artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-run dependency installation can fetch and persist local tools from the internet. <br>
Mitigation: Review the install path before use and prefer manually installing trusted, pinned versions of uv and pdf2zh-next. <br>
Risk: The QQBot sharing step can expose PDFs outside the local workflow if sensitive files are copied to the upload directory. <br>
Mitigation: Copy only the exact PDFs intended for sharing and avoid confidential, unpublished, copyrighted, or sensitive documents. <br>


## Reference(s): <br>
- [Paper Translator on ClawHub](https://clawhub.ai/xing-xing-coder/paper-translator) <br>
- [Advanced pdf2zh-next arguments](references/advanced-args.md) <br>
- [pdf2zh-next](https://pdf2zh-next.com/) <br>
- [PDFMathTranslate-next](https://github.com/PDFMathTranslate-next/PDFMathTranslate-next) <br>
- [pdf2zh-next advanced documentation](https://pdf2zh-next.com/advanced/advanced.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown instructions with shell commands; generated PDF and CSV files when the command is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written beside the input PDF by default, with optional arguments for language, page range, cache behavior, bilingual or monolingual output, and output directory.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
