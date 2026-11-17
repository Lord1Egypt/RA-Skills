## Description:

LrshuAI Text To Speech converts text prompts into natural-sounding speech through configured TTS models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrshu](https://clawhub.ai/user/lrshu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to generate speech from text prompts using Gemini, Doubao, or Keling text-to-speech models. Operation requires Python and a TEAM_API_KEY for the remote model service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script can upload local image or video files to an external endpoint even though the release is presented as text-to-speech.

Mitigation: Use the skill only with trusted endpoints and avoid providing sensitive local image or video paths.

Risk: The script can operate as a broader remote model proxy beyond the advertised TTS workflow.

Mitigation: Prefer a version that limits execution to disclosed TTS models and clearly documents all data sent externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lrshu/skills/lrshuai-text-to-speech)
- [Publisher profile](https://clawhub.ai/user/lrshu)
- [Default remote model endpoint](https://dlazy.com/api/ai/tool)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Command-line output containing JSON or status text from the remote model service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit asynchronous generation jobs and poll for completion before returning results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
