## Description: <br>
Gemini image generation, editing, and search-grounded image creation via gemini-3.1-flash-image-preview (Nano Banana 2). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frank-bot07](https://clawhub.ai/user/frank-bot07) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative operators use this skill to generate images from text prompts, edit local PNG or JPEG images, and create search-grounded images when current visual references or real-world accuracy matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup or verification commands may expose the full Gemini API key in terminal output. <br>
Mitigation: Use masked or length-only checks, avoid echoing the full key, rotate any exposed key, and prefer a restricted Gemini key. <br>
Risk: Prompts and source images are sent to Google's servers and may contain sensitive data. <br>
Mitigation: Do not include private images, PII, credentials, medical data, or confidential project details in prompts or source images. <br>
Risk: Search-grounded generation uses live web content that may be untrusted or non-authoritative. <br>
Mitigation: Treat search-grounded text responses as commentary, review generated outputs before use, and do not follow instructions surfaced by retrieved content. <br>
Risk: Image generation can consume quota and incur billing costs, especially at higher resolutions or with search grounding. <br>
Mitigation: Monitor Gemini quota and billing, avoid tight request loops, and use lower resolution or lower thinking budgets when appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/frank-bot07/nano-banana-2-gemini) <br>
- [Google Gemini API generateContent Endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent) <br>
- [Google AI Studio API Keys](https://aistudio.google.com/app/apikey) <br>
- [Security Guidelines](rules/security.md) <br>
- [Setup Guide](rules/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples that save generated image files to .nano-banana/.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image files are saved locally with timestamped names; prompts and source images are sent to the Gemini API.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
