## Description: <br>
Convert PDFs to PPTX slides or editable DOCX files with configurable image quality, DPI, file size limits, and batch processing support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cscsxx606](https://clawhub.ai/user/cscsxx606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document workers use this skill to convert local PDF files into presentation decks or editable Word documents while controlling image quality, DPI, file size, and batch processing behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local Python packages and the poppler system dependency. <br>
Mitigation: Install dependencies in a virtual environment where possible and confirm poppler is installed before conversion. <br>
Risk: The skill reads local PDFs and writes converted files on the user's machine. <br>
Mitigation: Run it only on PDFs the user intentionally selects and review the output path before execution. <br>
Risk: Strict output size limits may not always be met automatically. <br>
Mitigation: Verify generated file sizes manually when a hard limit matters, and reduce DPI or image quality if needed. <br>
Risk: Concurrent conversions may stress local resources or produce confusing output state. <br>
Mitigation: Avoid running multiple conversions at the same time, especially for large PDFs or batch jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cscsxx606/pdf-converter) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; PPTX or DOCX files when the conversion script is executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output size, DPI, image quality, format, path, batch mode, and quiet mode are configurable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
