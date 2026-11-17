## Description:

Gemini image generation, image editing, and search-grounded image creation via gemini-3.1-flash-image-preview (Nano Banana 2).

This skill is ready for commercial/non-commercial use.

## Publisher:

[frank-bot07](https://clawhub.ai/user/frank-bot07)

### License/Terms of Use:


## Use Case:

Developers and creative technical users use this skill to generate new images, edit local PNG/JPEG images, or create search-grounded visuals through Gemini. It provides command templates and setup guidance for saving generated PNG outputs into a project-local .nano-banana/ directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to GEMINI_API_KEY, and documented echo-based checks can expose the key in shell output.

Mitigation: Use a boolean, length-only, or prefix-only environment check; avoid printing the full key and keep .env files ignored before committing.

Risk: Prompts and source images are sent to Google services for generation or editing.

Mitigation: Do not include credentials, confidential business data, PII, or sensitive personal images unless the user has appropriate authorization and consent.

Risk: The declared curl and unrestricted python3 command permissions are broader than needed for normal use.

Mitigation: Narrow command permissions to the Gemini endpoint and expected local output paths before deployment.

Risk: Search-grounded generation may incorporate untrusted third-party web content.

Mitigation: Treat search-grounded text responses as commentary only and review generated images before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frank-bot07/skills/nano-banana-2-gemini)
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey)
- [Gemini image generation API endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Python and Bash command templates; generated PNG files saved under .nano-banana/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images use timestamped filenames; prompts and source images are sent to Google Gemini services.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
