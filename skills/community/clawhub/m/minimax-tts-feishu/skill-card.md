## Description: <br>
Generates natural Chinese speech with MiniMax, applies emotion and pause preprocessing, and sends the resulting audio to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiang92229](https://clawhub.ai/user/lixiang92229) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to convert Chinese text or recent Feishu chat messages into natural speech, choose or design MiniMax voices, and deliver generated audio into Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MiniMax and Feishu credentials can authorize TTS generation and bot actions if exposed. <br>
Mitigation: Store MINIMAX_API_KEY, FEISHU_APP_ID, and FEISHU_APP_SECRET only in environment or secret storage, use minimal scopes and billing limits, and rotate credentials if exposed. <br>
Risk: Chat text and generated audio may contain confidential content and are sent to MiniMax and Feishu during normal operation. <br>
Mitigation: Use the skill only for content approved for those services and avoid converting sensitive or regulated chat messages. <br>
Risk: Generated audio can be delivered to an unintended Feishu recipient if the recipient Open ID is misconfigured. <br>
Mitigation: Set the recipient deliberately and verify FEISHU_USER_OPEN_ID or command parameters before triggering delivery. <br>
Risk: Recent message text and generated audio may be cached locally in /tmp. <br>
Mitigation: Run the skill in an environment with appropriate local file access controls and clear temporary files when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lixiang92229/minimax-tts-feishu) <br>
- [Project Homepage](https://github.com/lixiang92229/lx-minimax-tts-feishu) <br>
- [MiniMax Platform](https://platform.minimaxi.com) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Audio files, Feishu messages, Text, Shell commands] <br>
**Output Format:** [WAV audio, Feishu audio messages, and command-line text or JSON status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured MiniMax and Feishu credentials; may write generated audio and recent message cache files under /tmp.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
