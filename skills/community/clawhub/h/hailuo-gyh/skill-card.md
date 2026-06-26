## Description: <br>
Generates MiniMax Hailuo videos in text-to-video, image-to-video, start/end-frame, and subject-reference modes using a user-supplied MINIMAX_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skydream9527-ctrl](https://clawhub.ai/user/skydream9527-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and developers use this skill to generate short MiniMax Hailuo video clips from prompts, source images, start/end frames, or subject-reference face images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image references, and subject-reference face images are sent to MiniMax for generation. <br>
Mitigation: Use non-sensitive inputs, obtain consent for face images, and review MiniMax data-handling terms before use. <br>
Risk: Some artifact wording says an API key is built in, but the authoritative security evidence says users should rely on their own MiniMax API key. <br>
Mitigation: Set MINIMAX_API_KEY in the environment and avoid embedding secrets in skill files, prompts, or shared command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skydream9527-ctrl/hailuo-gyh) <br>
- [MiniMax platform](https://platform.minimax.com) <br>
- [MiniMax API host](https://api.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands; script execution produces MP4 video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, requests, and MINIMAX_API_KEY; generated videos are downloaded to the requested output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
