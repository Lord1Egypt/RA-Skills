## Description:

Generates short or multi-segment videos from text and optional image frames using ZhipuAI CogVideoX-3, with helper scripts for continuation, frame extraction, and concatenation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baokui](https://clawhub.ai/user/baokui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative operators use this skill to plan and run text-to-video, image-to-video, and frame-guided video generation workflows. It is suited for generating approximately five-second clips or longer videos assembled from multiple generated segments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and provided images may be sent to ZhipuAI during generation.

Mitigation: Avoid sensitive prompts or images unless the user has approved sharing them with that service.

Risk: The workflow stores task metadata and result information locally.

Mitigation: Review output directories before sharing or retaining generated task files.

Risk: Concatenating media with untrusted or unusual filenames may be unsafe until the escaping issue is fixed.

Mitigation: Use trusted media files with simple filenames when running the concatenation script.

Risk: The skill depends on zai-sdk, ffmpeg, and a ZHIPU_API_KEY environment variable.

Mitigation: Use a virtual environment, pin or review dependencies, and configure credentials only in the intended runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baokui/skills/llm-video-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MP4 videos, PNG continuation frames, and JSON task/result metadata through the bundled scripts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
