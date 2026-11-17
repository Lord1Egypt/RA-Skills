## Description:

Generate speech or audio from text using OATDA's unified audio API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devcsde](https://clawhub.ai/user/devcsde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and accessibility-focused users use this skill through an agent to generate spoken audio, narration, voiceovers, and other text-to-speech outputs from text with OATDA-supported providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command template can mishandle arbitrary user text and may allow command injection if text is pasted directly into JSON payloads.

Mitigation: Build request JSON with a proper encoder such as jq --arg, validate output paths, and avoid reusing shell snippets with unsanitized user input.

Risk: The skill reads an OATDA API key and sends provided text to OATDA for speech generation.

Mitigation: Use the skill only when that data flow is acceptable, verify credential presence without printing the full key, and avoid sending sensitive text unless authorized.

## Reference(s):

- [OATDA Homepage](https://oatda.com)
- [OATDA Audio Models Endpoint](https://oatda.com/api/v1/llm/models?type=audio)
- [OATDA Speech Endpoint](https://oatda.com/api/v1/llm/speech)
- [ClawHub Skill Page](https://clawhub.ai/devcsde/skills/oatda-generate-speech)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with bash commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, OATDA_API_KEY, and safe JSON construction for user-provided text.]

## Skill Version(s):

1.1.0 (source: evidence.release.version and target metadata; artifact _meta.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
