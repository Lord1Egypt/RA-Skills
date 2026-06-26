## Description: <br>
MiniMax Hailuo video generation skill for creating subject-reference videos with the S2V-01 model, querying task status, and downloading generated video files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kylinr](https://clawhub.ai/user/Kylinr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to call MiniMax Hailuo APIs for subject-reference video generation, monitor generation jobs, and retrieve completed video files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts and reference image URLs to MiniMax using the user's MiniMax API key. <br>
Mitigation: Use a revocable key where possible, store it in an environment variable or protected config file, and review prompts and image URLs before submission. <br>
Risk: The sample download command writes to video.mp4, which could overwrite an existing file. <br>
Mitigation: Change the output filename before downloading when video.mp4 already exists or when preserving prior outputs matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Kylinr/hailuo-video-generator) <br>
- [MiniMax platform](https://platform.minimax.com) <br>
- [MiniMax video generation API endpoint](https://api.minimax.chat/v1/video_generation) <br>
- [MiniMax video generation status endpoint](https://api.minimax.chat/v1/query/video_generation?task_id=xxx) <br>
- [MiniMax file retrieval endpoint](https://api.minimax.chat/v1/files/retrieve?file_id=xxx) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a MiniMax API key from MINIMAX_API_KEY or ~/.openclaw/openclaw.json and may download generated video files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
