## Description: <br>
MOSS TTSD 多人对话合成 helps agents generate a continuous WAV dialogue track from 1 to 5 speaker-tagged text segments using MOSI Studio voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkkb473](https://clawhub.ai/user/mkkb473) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn multi-speaker dialogue text into one continuous audio file for conversational voice workflows. It is useful when an agent needs concise shell guidance for MOSI Studio dialogue synthesis with speaker IDs, sampling controls, and WAV output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dialogue text and speaker IDs are sent to MOSI Studio for processing. <br>
Mitigation: Use the skill only with text and voice identifiers that are appropriate to send to MOSI Studio, and avoid sensitive or confidential content unless the service terms and data handling meet the user's requirements. <br>
Risk: The MOSI_TTS_API_KEY credential is required for API access. <br>
Mitigation: Keep the API key in the MOSI_TTS_API_KEY environment variable, avoid passing it with --api-key when possible, and do not include it in shared logs or prompts. <br>
Risk: The optional Feishu voice-message workflow is separate from the core dialogue synthesis script. <br>
Mitigation: Review the Feishu helper before using that workflow and confirm that audio delivery behavior is acceptable for the target chat. <br>


## Reference(s): <br>
- [MOSI Studio](https://studio.mosi.cn) <br>
- [MOSI speech API endpoint used by the skill](https://studio.mosi.cn/api/v1/audio/speech) <br>
- [ClawHub release page](https://clawhub.ai/mkkb473/moss-ttsd) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and generated WAV file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOSI_TTS_API_KEY and local curl, jq, and base64 tools; generated audio is WAV at 32 kHz, 16-bit, mono.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
