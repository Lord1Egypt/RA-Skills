## Description: <br>
Convert PDF, DOCX, XLSX, PPTX, images, audio, and 25+ file formats to clean Markdown using the Markdown Anything API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adiologydev](https://clawhub.ai/user/adiologydev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to convert selected documents, images, and audio files into Markdown for prompts, retrieval workflows, documentation, or downstream text processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected files are uploaded to Markdown Anything for processing. <br>
Mitigation: Convert only files approved for that provider, and avoid sensitive or regulated documents unless Markdown Anything is approved for the user's environment. <br>
Risk: The MDA_API_TOKEN authorizes API usage and may spend credits. <br>
Mitigation: Store the token securely, avoid exposing it in logs or shared prompts, and rotate or revoke it if it may have been disclosed. <br>


## Reference(s): <br>
- [Markdown Anything](https://markdownanything.com) <br>
- [Markdown Anything Workspaces](https://markdownanything.com/workspaces) <br>
- [Markdown Anything Privacy Policy](https://markdownanything.com/privacy) <br>
- [ClawHub Skill Page](https://clawhub.ai/adiologydev/markdown-anything) <br>
- [Publisher Profile](https://clawhub.ai/user/adiologydev) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown conversion output to stdout, plus plain text credit-balance output for account checks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MDA_API_TOKEN; optional flags can request Enhanced AI, metadata, or token-optimized output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
