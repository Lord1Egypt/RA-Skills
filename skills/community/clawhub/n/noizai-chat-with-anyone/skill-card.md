## Description:

Chat With Anyone helps an agent create synthetic roleplay speech by finding public reference audio for a named character or designing a voice from a provided image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksuriuri](https://clawhub.ai/user/ksuriuri)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to create voice-based roleplay interactions that return synthesized speech and accompanying text. The workflow covers target clarification, public reference-audio collection or image-based voice design, reference extraction, and speech generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create synthetic voice audio that may be mistaken for genuine speech.

Mitigation: Use it only with consent or clearly permissible public-figure and media cases, inform users that audio is synthetic, and decline deceptive, harassing, defamatory, or private-person impersonation requests.

Risk: The skill may download public speech and upload selected images or descriptions to Noiz.

Mitigation: Review source media rights and privacy expectations before use, avoid sensitive or non-consensual images, and share only the minimum material needed for the requested voice workflow.

Risk: The skill handles API credentials and exposes a configurable API base URL.

Mitigation: Protect NOIZ_API_KEY, prefer trusted default endpoints, pin dependencies where possible, and do not use or expose custom base URLs unless the endpoint is fully trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ksuriuri/skills/noizai-chat-with-anyone)
- [Noiz API Endpoint](https://noiz.ai/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown instructions with inline shell commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce WAV audio files, selected reference clips, voice preview files, and a reusable voice ID.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
