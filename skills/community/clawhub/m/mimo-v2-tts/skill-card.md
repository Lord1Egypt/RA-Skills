## Description: <br>
Converts text to speech using Xiaomi MiMo-V2-TTS with emotional style control, Chinese dialect support, role voices, and singing synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddpie](https://clawhub.ai/user/ddpie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to synthesize text into audio through Xiaomi's MiMo-V2-TTS API, including styled speech, Chinese dialects, role voices, and singing-style output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can automatically install the Python requests package at runtime. <br>
Mitigation: Use an environment where runtime pip installation is acceptable, or preinstall and pin requests before running the skill. <br>
Risk: Synthesis text is sent to Xiaomi's cloud API. <br>
Mitigation: Avoid synthesizing confidential or regulated text unless Xiaomi's data handling is acceptable for the use case. <br>
Risk: API keys can be exposed when passed as command-line arguments. <br>
Mitigation: Use a dedicated MiMo API key and prefer the MIMO_API_KEY environment variable over the --api-key argument. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ddpie/mimo-v2-tts) <br>
- [Xiaomi MiMo Platform](https://platform.xiaomimimo.com) <br>
- [Xiaomi MiMo API base URL](https://api.xiaomimimo.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Audio files] <br>
**Output Format:** [Markdown usage guidance with bash command examples; the helper script writes an audio file such as MP3, WAV, PCM, OPUS, or FLAC.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiMo API key through MIMO_API_KEY or an explicit API-key argument; sends synthesis text to Xiaomi's cloud API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
