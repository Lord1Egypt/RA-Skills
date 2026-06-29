## Description: <br>
Synthesizes user-provided text into iFlytek Hyper TTS speech audio with selectable voices, speed, pitch, volume, sample rate, and MP3 output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflytek.skills](https://clawhub.ai/user/iflytek.skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert text or text files into speech through iFlytek's cloud text-to-speech service, then save the generated audio locally. It is intended for voice synthesis workflows where callers choose a supported voice and basic prosody parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text is sent to iFlytek's cloud TTS service and may include sensitive or regulated content if callers provide it. <br>
Mitigation: Use only approved text for external cloud processing, and avoid secrets, private customer data, regulated content, and confidential drafts unless that use is authorized. <br>
Risk: Generated audio is written to a caller-selected local path. <br>
Mitigation: Choose output paths deliberately and protect generated audio files according to the sensitivity of the source text. <br>
Risk: The skill requires iFlytek API credentials. <br>
Mitigation: Store XFEI credentials in environment variables or a secret manager and do not place them in prompts, source files, or generated audio metadata. <br>


## Reference(s): <br>
- [iFlytek Hyper TTS API documentation](https://www.xfyun.cn/doc/spark/super%20smart-tts.html) <br>
- [iFlytek Hyper TTS voice list](https://www.xfyun.cn/doc/spark/super%20smart-tts.html#%E5%8F%91%E9%9F%B3%E4%BA%BA%E5%88%97%E8%A1%A8) <br>
- [ClawHub skill page](https://clawhub.ai/iflytek.skills/iflytek-hyper-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Files, JSON] <br>
**Output Format:** [JSON status output plus a generated local MP3 audio file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, websocket-client, XFEI_APP_ID, XFEI_API_KEY, and XFEI_API_SECRET; text input is limited to 64KB.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
