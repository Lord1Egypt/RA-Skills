## Description:

MiniMax PDF OCR converts PDF pages to images and sends them to the MiniMax Vision API to produce Chinese and English OCR text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chongjie-ran](https://clawhub.ai/user/chongjie-ran)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to extract text from PDFs or images into Markdown while preserving basic page structure and formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input documents and generated page images are sent to MiniMax for OCR processing.

Mitigation: Use only documents approved for external OCR processing and avoid sensitive PDFs unless MiniMax use is authorized.

Risk: The security evidence reports a local command-injection risk in the pdftoppm spawn call.

Mitigation: Disable shell execution for the pdftoppm spawn call before using the skill on file paths supplied by other people.

Risk: The install instructions ask users to install packages that are not declared or used by package.json.

Mitigation: Correct or remove the unnecessary npm install instruction before release or deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chongjie-ran/skills/minimax-pdf-ocr)
- [MiniMax API Key Page](https://platform.minimaxi.com/user-center/basic-information/interface-key)
- [MiniMax Chat Completion API Endpoint](https://api.minimax.chat/v1/text/chatcompletion_v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown files and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and poppler; writes OCR results to a Markdown file.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
