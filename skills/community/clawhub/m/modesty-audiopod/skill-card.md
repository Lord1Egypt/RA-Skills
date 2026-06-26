## Description: <br>
Use SkillBoss API Hub for audio processing tasks including AI music generation (text-to-music, instrumentals, samples), text-to-speech, speech-to-text transcription, stem separation, noise reduction, and speaker separation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent prepare SkillBoss API calls for music generation, text-to-speech, transcription, speaker diarization, stem separation, and audio cleanup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected prompts, lyrics, transcripts, URLs, audio files, and voice samples to SkillBoss as a third-party processor. <br>
Mitigation: Install only when SkillBoss processing is intended, and submit only content that is acceptable to share with SkillBoss under its terms. <br>
Risk: The skill requires a sensitive SkillBoss API key. <br>
Mitigation: Use a dedicated API key and avoid hardcoding, committing, or logging the key. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/modesty-audiopod) <br>
- [SkillBoss Setup Guide](https://skillboss.co/skill.md) <br>
- [Stem Separation Reference](references/stems.md) <br>
- [Text to Speech Reference](references/tts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and cURL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SkillBoss API request guidance and result-path handling; generated media, transcripts, and processed audio are returned by the external SkillBoss service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
