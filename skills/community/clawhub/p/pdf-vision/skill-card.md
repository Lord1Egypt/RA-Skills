## Description: <br>
Extract text content from image-based/scanned PDFs using multiple vision APIs with automatic fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lpq6](https://clawhub.ai/user/lpq6) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and document-processing users use this skill to convert scanned or image-only PDF pages into extracted text, tables, summaries, or prompt-shaped structured output through configured vision model APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an unrelated GitHub repository creation script that looks for GitHub tokens. <br>
Mitigation: Remove or ignore that script unless repository creation is explicitly needed, and only run it with narrow-scope GitHub tokens. <br>
Risk: PDF page images and prompts are sent to third-party model providers for extraction. <br>
Mitigation: Avoid confidential or regulated documents unless the providers, data handling terms, and approval path are acceptable for the use case. <br>
Risk: Temporary image, payload, and response files may be written during processing. <br>
Mitigation: Use a private temporary directory and clean up generated payload, response, and image files after each run. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lpq6/pdf-vision) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or prompt-shaped structured text, optionally written to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes one PDF page per run by default and can use a selected model or automatic fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
