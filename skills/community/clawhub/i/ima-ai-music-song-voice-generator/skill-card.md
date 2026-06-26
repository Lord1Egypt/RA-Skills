## Description: <br>
IMA AI Music & Voice Generator helps agents generate music-oriented audio such as songs, background soundtracks, jingles, beats, and instrumental compositions with IMA-supported models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dai-shuo](https://clawhub.ai/user/dai-shuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route text prompts to IMA music models for generated songs, background music, jingles, beats, and instrumental compositions. It is suited for agent workflows that need user-facing audio generation with status updates and generated media links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Music prompts are sent to IMA and the configured IMA API key may consume credits. <br>
Mitigation: Avoid sensitive prompt text and use scoped or test keys when available. <br>
Risk: Local preference and log files may retain model choices, task IDs, timestamps, and HTTP status history. <br>
Mitigation: Delete ~/.openclaw/memory/ima_prefs.json and ~/.openclaw/logs/ima_skills/ when local history should not be retained. <br>
Risk: Changing the API base URL could redirect requests to an untrusted service. <br>
Mitigation: Keep the default IMA endpoint unless the replacement endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/dai-shuo/ima-ai-music-song-voice-generator) <br>
- [IMA Studio homepage](https://imastudio.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text updates and JSON metadata containing task ID, generated audio URL, duration, model, and credit use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is returned as a remote media URL; the skill requires an IMA API key and may retain local preference and log history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
