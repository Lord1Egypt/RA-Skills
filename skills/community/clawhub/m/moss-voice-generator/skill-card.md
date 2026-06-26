## Description: <br>
Generates WAV speech from text and a natural-language voice-style instruction using MOSI Studio's moss-voice-generator model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkkb473](https://clawhub.ai/user/mkkb473) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to synthesize one-off spoken audio by describing both the text and desired voice style instead of selecting a preset voice ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text and voice-style prompts are sent to MOSI Studio for processing. <br>
Mitigation: Avoid sending confidential, personal, or regulated content unless MOSI Studio's handling terms are acceptable. <br>
Risk: Passing the API key as a command-line argument can expose it through shell history or process listings. <br>
Mitigation: Prefer providing MOSI_TTS_API_KEY through the environment. <br>
Risk: Instruction-based voice generation can vary between runs and may not produce a stable brand voice. <br>
Mitigation: Review generated audio before use and lower the temperature when a more conservative result is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mkkb473/moss-voice-generator) <br>
- [MOSI Studio](https://studio.mosi.cn) <br>
- [MOSI Studio speech API endpoint](https://studio.mosi.cn/api/v1/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration guidance] <br>
**Output Format:** [WAV audio file with command-line status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOSI_TTS_API_KEY and Unix tools curl, jq, and base64.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
