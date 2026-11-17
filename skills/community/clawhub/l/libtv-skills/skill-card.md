## Description:

libtv-skills lets agents create LibTV sessions, upload reference media, send image or video generation and editing requests, poll progress, and download generated results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[316530790](https://clawhub.ai/user/316530790)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to route AI image and video generation or editing requests to LibTV, monitor sessions, upload reference media, and retrieve finished media assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected local media files, and session requests are sent to the configured LibTV endpoint.

Mitigation: Use only trusted OPENAPI_IM_BASE or IM_BASE_URL values and avoid submitting confidential media unless approved.

Risk: The download and upload helpers are loosely scoped and may fetch, write, or upload more than users expect.

Mitigation: Confirm local file paths before upload, avoid arbitrary --urls values, avoid path-like --prefix values, and choose an explicit output directory.

Risk: The script's media and size checks are weak.

Mitigation: Manually verify media type and size before upload, including the documented 200 MB limit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/316530790/skills/libtv-skills)
- [LibTV OpenAPI endpoint](https://im.liblib.tv)
- [LibTV canvas URL pattern](https://www.liblib.tv/canvas?projectId=)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with JSON command outputs, media URLs, project links, and downloaded files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and LIBTV_ACCESS_KEY; optional OPENAPI_IM_BASE or IM_BASE_URL can change the LibTV endpoint.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
