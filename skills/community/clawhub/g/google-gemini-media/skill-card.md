## Description:

Use the Gemini API (Nano Banana image generation, Veo video, Gemini TTS speech and audio understanding) to deliver end-to-end multimodal media workflows and code templates for "generation + understanding".

This skill is ready for commercial/non-commercial use.

## Publisher:

[xsir0](https://clawhub.ai/user/xsir0)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to plan and implement Gemini API workflows for generating and understanding images, video, speech, and audio with Node.js or REST templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected media are sent to Google APIs.

Mitigation: Confirm the user intends to use Google Gemini services and avoid uploading sensitive, unauthorized, or rights-restricted media.

Risk: Model names, limits, quotas, costs, and retention behavior may change.

Mitigation: Check current Google documentation before production use and implement timeout, retry, download, and review steps for generated media workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xsir0/skills/google-gemini-media)
- [Google Gemini generateContent endpoint](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request templates, model-selection guidance, media I/O handling steps, and operational cautions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
