## Description: <br>
Perform Optical Character Recognition (OCR) to extract and recognize text from images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fchange](https://clawhub.ai/user/fchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill to extract text from local images or image URLs through the Gitee AI Vision API and present the OCR result with a brief prompt-based summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, image URLs, and prompts are sent to Gitee AI for OCR processing. <br>
Mitigation: Use only images and prompts approved for Gitee AI, avoid confidential or regulated documents unless that service is approved, and prefer the GITEEAI_API_KEY environment variable instead of command-line key arguments. <br>


## Reference(s): <br>
- [Gitee AI API](https://ai.gitee.com/v1) <br>
- [ClawHub skill page](https://clawhub.ai/fchange/moark-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown containing the extracted OCR text and a brief summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GITEEAI_API_KEY value or an explicit API key argument.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
