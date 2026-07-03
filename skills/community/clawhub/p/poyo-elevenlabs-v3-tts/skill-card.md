## Description: <br>
Helps agents prepare and submit PoYo elevenlabs-v3-tts text-to-speech jobs, including payload fields, server-side curl examples, and task-status retrieval guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare text-to-speech requests for PoYo, choose voice and request options, submit trusted payloads with curl, and track asynchronous task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text, callback URLs, task IDs, generated audio URLs, or other sensitive data may be exposed to PoYo or logs during text-to-speech workflows. <br>
Mitigation: Use only trusted server-side environments, keep POYO_API_KEY secret, review payload files before submission, and avoid sending private or customer data unless policy allows it. <br>


## Reference(s): <br>
- [PoYo ElevenLabs V3 TTS documentation](https://docs.poyo.ai/api-manual/music-series/elevenlabs-v3-tts) <br>
- [PoYo ElevenLabs V3 TTS model page](https://poyo.ai/models/elevenlabs-v3-tts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a PoYo task ID when the user explicitly requests a live submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
