## Description:

Uploads local MP4 videos to VolcEngine ARK and analyzes them with a selected model and prompt to return structured video-script data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gnview](https://clawhub.ai/user/gnview)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to upload permitted MP4 videos to VolcEngine ARK, then request structured script, action, or scene analysis with a default or custom prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local videos are sent to a third-party cloud API.

Mitigation: Use only videos the user is allowed to send to VolcEngine ARK, and avoid sensitive or regulated footage unless the user's organization permits it.

Risk: API keys may be exposed when passed directly on the command line.

Mitigation: Prefer a protected environment variable or secret manager, and rotate any key that has appeared in shell history or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gnview/skills/gnview-script-extraction)
- [VolcEngine ARK file upload endpoint](https://ark.cn-beijing.volces.com/api/v3/files)
- [VolcEngine ARK responses endpoint](https://ark.cn-beijing.volces.com/api/v3/responses)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON responses from the script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Upload returns a video file ID; analysis returns formatted JSON from the selected VolcEngine ARK model.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
