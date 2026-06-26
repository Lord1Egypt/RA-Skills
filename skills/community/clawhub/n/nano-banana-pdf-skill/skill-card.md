## Description: <br>
Edits PDF pages and slides from natural-language instructions by guiding an agent to run the nano-pdf CLI with Google Gemini image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ps06756](https://clawhub.ai/user/ps06756) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI-agent users use this skill to make visual changes to PDF decks or reports, such as fixing typos, updating charts, changing branding, or adding slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF page content may be sent to Google Gemini during editing. <br>
Mitigation: Use the skill only for documents approved for third-party AI processing, and avoid confidential, regulated, or customer documents unless policy permits it. <br>
Risk: PDF edits can alter important content or produce incorrect visual results. <br>
Mitigation: Keep backups of originals and review edited PDFs before sharing or relying on them. <br>
Risk: Commands rely on external CLI dependencies, file paths, page numbers, output paths, and context flags. <br>
Mitigation: Verify dependencies and command arguments before execution, including selected pages, output file, and context/search options. <br>
Risk: Gemini API use can incur cost through the configured API key. <br>
Mitigation: Use a dedicated Gemini API key with appropriate billing controls and spending limits. <br>


## Reference(s): <br>
- [Skill homepage](https://github.com/ps06756/nano-banana-pdf-skill) <br>
- [Nano-PDF](https://github.com/gavrielc/Nano-PDF) <br>
- [Google AI Studio API keys](https://aistudio.google.com/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline shell commands and generated PDF file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires nano-pdf dependencies and GEMINI_API_KEY; output PDF quality depends on prompt specificity, resolution, OCR, and model behavior.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
