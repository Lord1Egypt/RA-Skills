## Description:

Generate video from supplied image using Veo-3.0 async API. Gemini vision analyzes image, Veo creates video via predictLongRunning. All outputs in ~/.openclaw/workspace/tibetanProc/ with yymmddHHMM prefix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to turn an input image into a short cinematic MP4 by having an agent analyze the image, build a motion prompt, call Google's Veo API, poll for completion, and save the generated outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and prompts are uploaded to Google services.

Mitigation: Use only media and prompt content that the operator is permitted to send to Google; avoid confidential, regulated, or sensitive inputs.

Risk: The Google API key may be exposed during API calls or video downloads.

Mitigation: Use a dedicated, tightly restricted Google API key and review request handling before installing or running the skill.

Risk: The video download step appends the API key to a returned URI.

Mitigation: Validate the returned URI host and redirect behavior before attaching the API key or downloading generated media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/image-to-video-gen)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)
- [Google Generative Language Veo endpoint used by the skill](https://generativelanguage.googleapis.com/v1beta/models/veo-3.0-generate-001:predictLongRunning)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline Python and shell code blocks; generated runtime files include prompt text, JSON API responses, and MP4 video.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_API_KEY and writes timestamp-prefixed outputs under ~/.openclaw/workspace/tibetanProc/.]

## Skill Version(s):

3.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
