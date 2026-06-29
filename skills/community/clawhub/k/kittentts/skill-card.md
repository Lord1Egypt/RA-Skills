## Description: <br>
Generate local TTS audio with KittenTTS using selectable voices and model sizes for quality or speed tradeoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredguile](https://clawhub.ai/user/fredguile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local KittenTTS speech generation with voice and model-size choices, including OpenClaw workflows that send generated audio through Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated speech audio may leave the local machine when the OpenClaw Telegram integration is used. <br>
Mitigation: Use the skill only with non-confidential text unless the Telegram account, chat destination, and configuration have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fredguile/kittentts) <br>
- [KittenTTS package release](https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide WAV audio generation with selectable voices and model sizes; Telegram delivery may transmit generated audio outside the local machine.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
