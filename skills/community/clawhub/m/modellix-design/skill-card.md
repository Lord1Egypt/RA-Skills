## Description:

Integrates Modellix's unified API for AI image, video, and audio generation and editing, speech synthesis, transcription, and related media workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modellix](https://clawhub.ai/user/modellix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to check Modellix model schemas and run image, video, and audio workflows through the available Modellix tools. It helps them select an execution path and retrieve task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may change a shared global CLI or clear a saved CLI profile beyond the media workflow's stated purpose.

Mitigation: Review the installation and profile behavior before use, especially on shared systems.

Risk: Prompts and media inputs may be sent to Modellix during a task.

Mitigation: Review privacy implications and avoid sending sensitive prompts or data unless authorized.

## Reference(s):

- [Modellix AI Onboarding](https://docs.modellix.ai/get-started.md)
- [Modellix REST API](https://docs.modellix.ai/ways-to-use/api.md)
- [Modellix CLI package](https://www.npmjs.com/package/modellix-cli)
- [Modellix skill release](https://clawhub.ai/modellix/skills/modellix-design)

## Skill Output:

**Output Type(s):** [Generated media, JSON, Text, Shell commands, Guidance]

**Output Format:** [Generated media files or task result links, with JSON results and Markdown guidance or commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Media tasks run asynchronously; result links may expire after about seven days.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
