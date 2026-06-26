## Description: <br>
Parse text and coordinates from images with SoMark, including character, word, and line positions on the original image for OCR-first image understanding where location matters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soul-code](https://clawhub.ai/user/soul-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract OCR text with bounding-box coordinates from receipts, invoices, screenshots, forms, scanned pages, and other images. It supports downstream field extraction, regional lookup, and layout-aware automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images may contain sensitive content and are sent to SoMark for processing. <br>
Mitigation: Use the skill only for images you are comfortable processing with SoMark, especially for receipts, invoices, screenshots, and forms. <br>
Risk: Providing the API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer the SOMARK_API_KEY environment variable and avoid pasting secrets into chat or command arguments. <br>
Risk: Use can consume SoMark quota or paid billing capacity. <br>
Mitigation: Monitor quota and billing before large parsing runs. <br>


## Reference(s): <br>
- [Image Parser Skill Page](https://clawhub.ai/soul-code/image-parser) <br>
- [Soul-Code Publisher Profile](https://clawhub.ai/user/soul-code) <br>
- [SoMark](https://somark.tech) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON and Markdown files with text, bounding boxes, page numbers, roles, and a results index] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOMARK_API_KEY and sends selected images to SoMark for processing.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
