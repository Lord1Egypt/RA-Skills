## Description:

Enables agents to create LibTV sessions, send image and video generation or editing requests, query progress, switch projects, upload reference media, and download generated results through LibTV APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haofanwang](https://clawhub.ai/user/haofanwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit natural-language image and video generation or editing tasks to LibTV, track the session until media is available, and return local downloads plus project links. It is also used to upload user-provided reference media before submitting an edit or generation request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a LibTV access key and uses it for authenticated API calls.

Mitigation: Install only when sharing a LibTV access key is acceptable, keep the key scoped appropriately, and avoid exposing it in logs or shared command output.

Risk: Configurable API base URLs can send credentials and media requests to a non-default endpoint.

Mitigation: Leave OPENAPI_IM_BASE and IM_BASE_URL unset unless intentionally using a trusted LibTV-compatible endpoint.

Risk: Uploaded reference media and downloaded result URLs may contain sensitive or proprietary content.

Mitigation: Review local file paths before upload, avoid sensitive media unless remote storage is acceptable, and inspect download destinations and direct URLs before automatic retrieval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haofanwang/skills/libtv-skill)
- [Publisher profile](https://clawhub.ai/user/haofanwang)
- [LibTV API base endpoint](https://im.liblib.tv)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and LIBTV_ACCESS_KEY; may return session identifiers, project URLs, media URLs, local file paths, and progress messages.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
