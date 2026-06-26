## Description: <br>
Multimodal document deep analysis tool based on Zhipu GLM-OCR, GLM-4.7, and GLM-4.6V. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baokui](https://clawhub.ai/user/baokui) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document-analysis users use this skill to extract document layout elements from PDFs or images, convert tables to Markdown, crop charts and figures, and generate semantic analysis for tables and images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs, images, and extracted context are sent to Zhipu cloud APIs for OCR and analysis. <br>
Mitigation: Process only documents approved for that external service, avoid confidential or regulated material unless sharing is authorized, and use a dedicated API key. <br>
Risk: Extracted text, analysis JSON, and cropped images are saved locally in the chosen output directory. <br>
Mitigation: Use a secure output directory with appropriate access controls and remove generated files when they are no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files] <br>
**Output Format:** [JSON report with Markdown table content, deep-understanding text, and local cropped image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY, writes extracted text and cropped images to the selected output directory, and processes the first page of multi-page PDFs by default.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
