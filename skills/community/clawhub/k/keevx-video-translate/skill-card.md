## Description:

Translate videos into a specified target language using the Keevx API, with support for audio-only translation, subtitle generation, dynamic duration adjustment, language lookup, and task status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-xiling](https://clawhub.ai/user/baidu-xiling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to translate or dub videos through Keevx, query supported target languages, submit long-running translation tasks, and check task status until completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local videos are uploaded to Keevx for processing.

Mitigation: Use the skill only for videos that are appropriate to send to Keevx.

Risk: Callback URLs can expose task-completion data to an endpoint.

Mitigation: Use callback_url only with an endpoint the user controls.

Risk: The example bash workflow interpolates user-controlled values into JSON.

Mitigation: Harden JSON construction before automating the workflow with untrusted inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baidu-xiling/skills/keevx-video-translate)
- [Keevx API docs - supported languages](https://docs.keevx.com/api-reference/endpoint/ListSupportedLanguages)
- [Keevx API docs - submit translation](https://docs.keevx.com/api-reference/endpoint/SubmitVideoTranslate)
- [Keevx API docs - check status](https://docs.keevx.com/api-reference/endpoint/GetTranslationStatus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Keevx task IDs, status values, translated video URLs, and subtitle URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
