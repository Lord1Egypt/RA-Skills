## Description: <br>
Voice-first OpenClaw skill powered by MOSS APIs for spoken replies in a preferred timbre from an existing voice_id or a reference audio clip. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiami2019](https://clawhub.ai/user/xiami2019) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate text-to-speech audio with a preferred voice, either by reusing a stable voice_id or by providing permitted reference audio for cloning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice samples, cloned voices, and input text may contain sensitive personal data sent to an external MOSS service. <br>
Mitigation: Use the skill only with trusted MOSS endpoints, permitted voice material, and non-sensitive text; prefer existing voice_id values when available. <br>
Risk: API credentials can be exposed if logged or shared. <br>
Mitigation: Store MOSI_API_KEY securely, use revocable credentials, and follow the artifact instruction to never print or log raw API keys. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiami2019/moss-tts) <br>
- [MOSI Studio Service](https://studio.mosi.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration, files] <br>
**Output Format:** [Markdown guidance with API request details and generated audio file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the voice_id used, output file path, duration, and a concise status message.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
