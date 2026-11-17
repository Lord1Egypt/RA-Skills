## Description:

Upload a video or image to memories.ai with capture time and location metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memories-ai-official](https://clawhub.ai/user/memories-ai-official)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to upload selected video or image files to Memories.ai/Luci as visual memory. The agent should probe media metadata first, then ask for missing capture time or location before upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may upload any readable local file path provided to it, including file contents and filename.

Mitigation: Use it only with explicit media files the user intends to send, and add or require a confirmation step before upload.

Risk: Uploads can include capture timestamp and location metadata, and named locations may be sent to a geocoding service.

Mitigation: Confirm the time and location with the user when metadata is missing or sensitive, and avoid broad or ambiguous upload requests.

Risk: The current artifact does not enforce media-type validation before upload.

Mitigation: Validate file type and extension before invoking the upload path, especially for user-supplied paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/memories-ai-official/skills/memoriesai-upload)
- [memories.ai upload service](https://mavi-backend.memories.ai)
- [Nominatim geocoding endpoint](https://nominatim.openstreetmap.org/search?{params})

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, API Calls]

**Output Format:** [Markdown with inline bash commands and JSON/text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEMORIES_AI_KEY and python3; ffprobe is required for automatic media metadata extraction.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
