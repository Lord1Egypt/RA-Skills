## Description:

The Hailuo Video Generator helps agents use MiniMax Hailuo S2V-01 to generate subject-reference videos, check task status, and retrieve generated video files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinr](https://clawhub.ai/user/kylinr)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to guide MiniMax Hailuo video generation workflows, including API-key configuration, subject-reference request construction, status polling, and generated video retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video prompts, reference image URLs, task metadata, and retrieval requests are sent to MiniMax.

Mitigation: Use the skill only when external MiniMax processing is intended, and avoid sensitive personal, proprietary, or regulated content unless it is approved for that service.

Risk: The MiniMax API key is required for operation.

Mitigation: Store the API key in the MINIMAX_API_KEY environment variable or the intended local OpenClaw configuration, and keep it out of shared files, prompts, and logs.

## Reference(s):

- [MiniMax Platform](https://platform.minimax.com)
- [MiniMax Video Generation API](https://api.minimax.chat/v1/video_generation)
- [MiniMax Video Task Status API](https://api.minimax.chat/v1/query/video_generation?task_id=xxx)
- [MiniMax File Retrieval API](https://api.minimax.chat/v1/files/retrieve?file_id=xxx)
- [ClawHub Skill Page](https://clawhub.ai/kylinr/skills/hailuo-video-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MiniMax task IDs, file IDs, polling guidance, API error-code explanations, and download instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
