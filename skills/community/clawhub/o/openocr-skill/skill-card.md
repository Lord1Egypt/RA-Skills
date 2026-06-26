## Description: <br>
Extracts text, formulas, tables, and document structure from images, scanned documents, and PDFs using OpenOCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Topdu](https://clawhub.ai/user/Topdu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to choose OpenOCR tasks and produce OCR, formula recognition, table extraction, and document parsing outputs from local images, scanned documents, and PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Demo launch examples can expose OCR interfaces over the network, which may reveal sensitive source documents or generated OCR output. <br>
Mitigation: Avoid --share, share=True, and 0.0.0.0 unless remote access is intentional and protected by network controls. <br>
Risk: OCR inputs and generated text, Markdown, JSON, or visualizations may contain sensitive document content. <br>
Mitigation: Run the skill only in trusted environments and handle generated outputs according to the sensitivity of the source files. <br>


## Reference(s): <br>
- [OpenOCR GitHub](https://github.com/Topdu/OpenOCR) <br>
- [OpenOCR PyPI Package](https://pypi.org/project/openocr-python/) <br>
- [UniRec Documentation](https://github.com/Topdu/OpenOCR#unirec) <br>
- [OpenDoc Documentation](https://github.com/Topdu/OpenOCR#opendoc) <br>
- [Model Zoo and Configs](https://github.com/Topdu/OpenOCR/tree/main/configs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe OCR confidence scores, bounding boxes, Markdown exports, JSON exports, and visualization files depending on the selected OpenOCR task.] <br>

## Skill Version(s): <br>
0.1.6 (source: ClawHub release evidence; artifact frontmatter lists 0.1.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
