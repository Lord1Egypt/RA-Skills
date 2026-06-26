## Description: <br>
Recognizes text in PDFs and images with the MiniMax Vision API and writes OCR results as Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chongjie-ran](https://clawhub.ai/user/chongjie-ran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users can use this skill to convert PDF pages to images, send them to MiniMax for OCR, and collect the recognized Chinese or English text in Markdown output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processed PDF page images are sent to a third-party MiniMax API. <br>
Mitigation: Use only documents approved for external processing, and avoid confidential, regulated, customer, or financial documents unless that processing is authorized. <br>
Risk: PDF conversion invokes a shell command using user-provided file paths. <br>
Mitigation: Review file paths before running the skill and avoid passing untrusted or unexpected paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chongjie-ran/minimax-pdf-ocr) <br>
- [MiniMax API key setup](https://platform.minimaxi.com/user-center/basic-information/interface-key) <br>
- [MiniMax chat completion endpoint](https://api.minimax.chat/v1/text/chatcompletion_v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and a local pdftoppm binary from poppler; document page images are sent to the MiniMax API for recognition.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
