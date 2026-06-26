## Description: <br>
Generate MiniMax Hailuo videos from text prompts or first and last frame image URLs, then query generation status and download completed videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to run MiniMax Hailuo video generation workflows from an agent environment, including prompt-based generation, first-frame/last-frame transitions, task status checks, and local video download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and referenced frame-image URLs are sent to MiniMax when generation scripts are run. <br>
Mitigation: Use the skill only with content that is appropriate to share with MiniMax and with an approved MiniMax API key. <br>
Risk: MiniMax API use may consume account quota or incur billing usage. <br>
Mitigation: Confirm account limits and monitor generated tasks before running repeated or automated requests. <br>
Risk: The download script writes generated video files to the output path supplied by the user. <br>
Mitigation: Choose explicit output paths and review destinations before downloading files. <br>


## Reference(s): <br>
- [MiniMax Video Generator on ClawHub](https://clawhub.ai/hongjiahao371-pixel/minimax-video-gen) <br>
- [Publisher profile](https://clawhub.ai/user/hongjiahao371-pixel) <br>
- [MiniMax video generation endpoint](https://api.minimaxi.com/v1/video_generation) <br>
- [MiniMax video generation status endpoint](https://api.minimaxi.com/v1/query/video_generation) <br>
- [MiniMax file retrieval endpoint](https://api.minimaxi.com/v1/files/retrieve) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts call the MiniMax API, print task or file identifiers, and can save generated video files to a user-provided local path.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
