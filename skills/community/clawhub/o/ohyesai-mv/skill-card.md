## Description:

Generate music videos from uploaded audio with AI-driven storyboarding, image generation, and video synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bajie-git](https://clawhub.ai/user/bajie-git)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit an audio file to OhYesAI, choose a visual style and aspect ratio, and return a generated music video link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected audio file is sent to OhYesAI for processing.

Mitigation: Avoid private, confidential, or rights-sensitive audio unless the user accepts OhYesAI's handling of the file.

Risk: The documented API requests place OHEYSAI_API_KEY in URL query strings.

Mitigation: Use a limited and rotatable API key, and avoid exposing request URLs in logs, chat transcripts, or shared screenshots.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bajie-git/skills/ohyesai-mv)
- [OhYesAI homepage](https://ohyesai.com)

## Skill Output:

**Output Type(s):** [text, markdown, api calls, shell commands, guidance]

**Output Format:** [Markdown or plain text responses with progress updates and a final video preview link or download URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an audio file under 50MB, OHEYSAI_API_KEY, curl, sleep, and polling until success, failure, or timeout.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
