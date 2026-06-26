## Description: <br>
Use MiniMax image-01 model to generate images from text prompts, save PNG output locally, and return the generated image URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlin53882](https://clawhub.ai/user/jlin53882) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to call MiniMax image generation from a Python command, producing a local PNG file path and a generated image URL from a text prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports an undocumented text-to-speech path that sends text to MiniMax and saves audio files. <br>
Mitigation: Use only when comfortable sending prompts or text to MiniMax/Hailuo infrastructure; avoid sensitive text, review or remove the TTS path, and keep MINIMAX_BASE_URL pointed at a trusted MiniMax endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jlin53882/minimax-img) <br>
- [MiniMax platform](https://platform.minimax.io) <br>
- [MiniMax API endpoint](https://api.minimax.io) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [JSON response from a Python CLI, including local media paths, generated media URLs, and byte counts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and writes generated media files locally; MINIMAX_BASE_URL can override the default MiniMax endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
