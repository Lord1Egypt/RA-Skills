## Description: <br>
Use MiniMax API for image generation and text-to-speech (TTS), supporting the image-01 model for images and speech-2.8-hd for voice synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlin53882](https://clawhub.ai/user/jlin53882) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images and synthesize speech through the MiniMax API, saving generated PNG and MP3 files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, TTS text, request metadata, and the API key are sent to MiniMax or the configured MiniMax-compatible endpoint. <br>
Mitigation: Use a revocable API key, avoid submitting secrets or regulated data unless approved, and keep MINIMAX_BASE_URL unset unless the alternate endpoint is trusted. <br>


## Reference(s): <br>
- [MiniMax Platform](https://platform.minimax.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/jlin53882/minimax-media-james) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON responses with generated PNG image files or MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; MINIMAX_BASE_URL can point to an alternate trusted MiniMax-compatible endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
