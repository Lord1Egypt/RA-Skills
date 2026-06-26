## Description: <br>
Generates videos with the MiniMax Nuwa API from text, image, start/end frame, or subject-reference inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superluanxu](https://clawhub.ai/user/superluanxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit MiniMax video-generation jobs, poll for completion, download MP4 outputs, and return generated videos to users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and face-reference URLs are sent to MiniMax for video generation. <br>
Mitigation: Avoid confidential prompts and private image URLs, and only use face-reference images with the subject's permission. <br>
Risk: MiniMax API use may consume credits or create billing exposure. <br>
Mitigation: Use a dedicated API key where possible and monitor billing or credits during use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superluanxu/nuwa-video-gen) <br>
- [MiniMax API key management](https://platform.minimaxi.com) <br>
- [MiniMax API documentation](https://platform.minimaxi.com/docs/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated MP4 video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; prompts and image URLs are sent to MiniMax; generated videos are saved to the requested output path.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
