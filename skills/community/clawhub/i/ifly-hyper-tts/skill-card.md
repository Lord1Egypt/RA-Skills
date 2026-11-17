## Description:

Ifly Hyper TTS converts text into iFlytek hyper-realistic speech with selectable voices, prosody settings, and MP3 output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingzhe2020](https://clawhub.ai/user/qingzhe2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to synthesize user-provided text into speech through iFlytek's TTS service. It supports common TTS controls such as voice selection, speed, volume, pitch, sample rate, and output file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis is sent to iFlytek's service using the user's API credentials.

Mitigation: Avoid sensitive text unless iFlytek terms, retention practices, and organizational data-handling requirements have been reviewed.

Risk: The skill depends on local iFlytek credential environment variables.

Mitigation: Provide credentials through environment variables only, keep them out of skill files and logs, and rotate them if exposed.

Risk: The current script may fail during synthesis because it references an undefined omni_params variable.

Mitigation: Fix and test that variable path before relying on the skill for production synthesis.

Risk: Dependency hygiene depends on the locally installed websocket-client package.

Mitigation: Use a virtual environment and pin a reviewed websocket-client version before deployment.

## Reference(s):

- [iFlytek Hyper-Realistic TTS API Documentation](https://www.xfyun.cn/doc/spark/super%20smart-tts.html)
- [iFlytek Voice List](https://www.xfyun.cn/doc/spark/super%20smart-tts.html#%E5%8F%91%E9%9F%B3%E4%BA%BA%E5%88%97%E8%A1%A8)
- [ClawHub Skill Page](https://clawhub.ai/qingzhe2020/skills/ifly-hyper-tts)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Files, JSON]

**Output Format:** [Markdown guidance with bash commands; runtime execution returns JSON status and writes an audio file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XFEI_APP_ID, XFEI_API_KEY, and XFEI_API_SECRET; sends synthesis text to iFlytek and defaults to MP3 output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
