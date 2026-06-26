## Description: <br>
Extract text from images, documents and scanned PDFs using OpenOCR - supports text detection, recognition, universal VLM recognition, and document parsing with layout analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Topdu](https://clawhub.ai/user/Topdu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-processing teams use this skill to extract text, formulas, tables, and document structure from images, scanned documents, and PDFs with OpenOCR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR output may expose confidential content when extracted text, Markdown, JSON, text, or visualization files are saved locally. <br>
Mitigation: Process confidential documents only in an appropriate agent environment and review output folder handling before use. <br>
Risk: OpenOCR may download model or package artifacts during setup or execution. <br>
Mitigation: Use local model paths or disable automatic downloads when controlled or offline operation is required. <br>
Risk: Launching Gradio demos with share mode can expose a demo link outside the local environment. <br>
Mitigation: Avoid Gradio share mode unless external access is intended. <br>


## Reference(s): <br>
- [OpenOCR GitHub](https://github.com/Topdu/OpenOCR) <br>
- [OpenOCR PyPI Package](https://pypi.org/project/openocr-python/) <br>
- [UniRec Documentation](https://github.com/Topdu/OpenOCR#unirec) <br>
- [OpenDoc Documentation](https://github.com/Topdu/OpenOCR#opendoc) <br>
- [Model Zoo and Configs](https://github.com/Topdu/OpenOCR/tree/main/configs) <br>
- [ClawHub Skill Page](https://clawhub.ai/Topdu/opencr-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OCR text, layout-aware document outputs, JSON output guidance, and visualization file guidance.] <br>

## Skill Version(s): <br>
0.1.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
