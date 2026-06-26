## Description: <br>
Helps agents read, create, edit, validate, and render PowerPoint presentations using PPTX XML workflows, PptxGenJS, and local Office tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Employees, external users, and developers use this skill when an agent must inspect or produce .pptx decks, adapt templates, generate slides from scratch, and run QA on presentation output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Office tooling and modify unpacked document directories. <br>
Mitigation: Run it in a sandbox or disposable workspace and review generated or modified files before using them. <br>
Risk: Untrusted Office files may expose ZIP, XML, and document-processing attack surface. <br>
Mitigation: Avoid processing untrusted Office files unless the environment is isolated and the parser risk is acceptable. <br>
Risk: The evidence reports under-disclosed Office-document capabilities and a native LibreOffice preload workaround. <br>
Mitigation: Review or remove the DOCX/XLSX and preload-shim paths if only PPTX support is needed. <br>


## Reference(s): <br>
- [Editing Presentations](artifact/editing.md) <br>
- [PptxGenJS Tutorial](artifact/pptxgenjs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with code snippets and generated or edited PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify unpacked Office document directories and create thumbnails, PDFs, or slide images for QA.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
