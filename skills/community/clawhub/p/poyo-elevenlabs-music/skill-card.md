## Description: <br>
Helps agents prepare and submit PoYo ElevenLabs Music text-to-music jobs, including text briefs, structured composition plans, output formats, callbacks, and task status retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolhackboy](https://clawhub.ai/user/coolhackboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare text briefs or structured composition plans for PoYo ElevenLabs Music, submit trusted server-side generation requests, and guide retrieval of task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music prompts, lyrics, callback URLs, task IDs, generated audio URLs, and API keys may be sensitive when sent to PoYo or retained in logs. <br>
Mitigation: Keep POYO_API_KEY in a server-side secret store, review payload files before submission, and avoid logging private prompts, callback URLs, task IDs, generated audio URLs, or API keys. <br>


## Reference(s): <br>
- [PoYo ElevenLabs Music API Reference](artifact/references/api.md) <br>
- [PoYo ElevenLabs Music docs](https://docs.poyo.ai/api-manual/music-series/elevenlabs-music) <br>
- [PoYo ElevenLabs Music model page](https://poyo.ai/models/elevenlabs-music) <br>
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-elevenlabs-music) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON payloads and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model selection, input path choice, generation payloads, task IDs, and next-step retrieval guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
