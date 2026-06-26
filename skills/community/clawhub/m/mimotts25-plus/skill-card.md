## Description: <br>
小米 MiMo TTS 2.5 Plus — 增强版语音合成。兼容官方接口，支持预置音色/声音设计/克隆/导演模式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limingjing6666](https://clawhub.ai/user/limingjing6666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to synthesize speech with Xiaomi MiMo TTS 2.5 Plus, choosing preset voices, text-designed voices, cloned voices, or director-style prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MiMo API key and sends selected text to a configured MiMo endpoint. <br>
Mitigation: Keep MIMO_API_KEY secret, avoid submitting confidential text, and use only trusted MiMo endpoints. <br>
Risk: Voice cloning can upload user-selected voice samples. <br>
Mitigation: Use only recordings you own or have explicit permission to use. <br>
Risk: Custom API base URLs can change where requests and credentials are sent. <br>
Mitigation: Use the default endpoint or set MIMO_API_BASE and --base-url only to endpoints you control or trust. <br>


## Reference(s): <br>
- [MiMo TTS 2.5 Official API Docs](artifact/references/official-api-docs.md) <br>
- [Xiaomi MiMo Open Platform](https://platform.xiaomimimo.com/) <br>
- [ClawHub skill page](https://clawhub.ai/limingjing6666/mimotts25-plus) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/limingjing6666) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Audio files] <br>
**Output Format:** [Markdown guidance with bash commands and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MIMO_API_KEY; generated media is written to the configured output path, typically output.mp3.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
