## Description: <br>
Train a custom iFlytek voice clone model from audio samples and synthesize speech with the cloned voice using a Python standard-library command-line workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingzhe2020](https://clawhub.ai/user/qingzhe2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run the iFlytek voice cloning workflow: collect training text, create and submit a voice training task, poll for the resulting voice resource, and synthesize speech from text or files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends selected voice recordings, text, and iFlytek API-backed requests to iFlytek. <br>
Mitigation: Use only recordings and text you have permission to process, review iFlytek data-handling terms, and avoid submitting sensitive material unless the service terms and your policy allow it. <br>
Risk: The security summary flags sensitive voice data and API credentials with insecure transport settings. <br>
Mitigation: Use trusted networks, protect IFLY_APP_ID, IFLY_API_KEY, and IFLY_API_SECRET, and prefer a version that keeps normal TLS verification enabled. <br>
Risk: Voice cloning can create speech that sounds like a real person. <br>
Mitigation: Clone only voices with clear authorization and apply consent, disclosure, and misuse controls appropriate for the deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qingzhe2020/ifly-voiceclone-tts) <br>
- [iFlytek Voice Clone API documentation](https://www.xfyun.cn/doc/spark/voiceclone.html) <br>
- [iFlytek console](https://console.xfyun.cn) <br>
- [iFlytek one-sentence voice clone service](https://console.xfyun.cn/services/oneSentenceV2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Files] <br>
**Output Format:** [Markdown guidance with shell command examples and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses iFlytek API credentials from environment variables and can write synthesized audio output such as MP3, PCM, Speex, or Opus files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
