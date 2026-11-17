## Description:

Analyze PDF files using MiniMax API with text extraction, keyword search, and image-based VLM analysis after converting PDF pages to images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlin53882](https://clawhub.ai/user/jlin53882)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and document reviewers use this skill to extract text from PDFs, search for relevant snippets, and request MiniMax VLM analysis of PDF pages rendered as images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential PDF content may be sent to a third-party MiniMax API when vision mode uploads rendered page images and prompts.

Mitigation: Use vision mode only with documents approved for third-party processing, and prefer local extract or search mode for sensitive documents.

Risk: The package includes an undeclared MiniMax web search helper and a generic local-image upload helper beyond the advertised PDF workflow.

Mitigation: Review available helper commands before installation and restrict use of web search or image upload helpers unless they are explicitly intended.

Risk: Broad local file paths or sensitive images could be exposed through the image understanding helper.

Mitigation: Pass only specific approved image paths and avoid running the helper from directories containing unrelated confidential files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlin53882/skills/minimax-pdf-analysis-v2)
- [ClawHub publisher profile](https://clawhub.ai/user/jlin53882)
- [MiniMax platform](https://platform.minimaxi.com)
- [MiniMax Coding Plan VLM endpoint](https://api.minimax.io/v1/coding_plan/vlm)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Plain text, saved text files, PNG page images, JSON from helper tools, and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vision mode sends rendered PDF page images and prompts to the MiniMax API; extraction and search can run locally with PyMuPDF.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
