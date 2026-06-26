## Description: <br>
MiniMax video generation skill for text-to-video, image-to-video, frame-to-frame, and subject-reference video workflows using MiniMax-Hailuo-2.3, with local MP4 download support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silingyuan0](https://clawhub.ai/user/silingyuan0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent operators use this skill to submit MiniMax video generation jobs, check asynchronous task status, and download generated MP4 files for approved workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced image URLs are sent to MiniMax's cloud API. <br>
Mitigation: Use only content approved for MiniMax processing and set MINIMAX_REGION explicitly when data residency matters. <br>
Risk: Generated videos are downloaded to local file paths and can be misplaced or overwrite prior outputs if paths are reused. <br>
Mitigation: Save downloads to a dedicated output folder and choose explicit filenames for generated media. <br>
Risk: The skill depends on a MiniMax API key and external service availability. <br>
Mitigation: Store MINIMAX_API_KEY in the environment, avoid committing credentials, and handle failed or long-running tasks through status polling. <br>


## Reference(s): <br>
- [MiniMax Video API Reference](artifact/references/api.md) <br>
- [MiniMax China API endpoint](https://api.minimaxi.com/v1) <br>
- [MiniMax International API endpoint](https://api.minimax.io/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with shell commands; API responses as JSON; generated videos as MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and optional MINIMAX_REGION; video generation is asynchronous and downloads may be saved locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
