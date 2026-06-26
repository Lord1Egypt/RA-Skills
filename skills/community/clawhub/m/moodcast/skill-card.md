## Description: <br>
Transform any text into emotionally expressive audio with ambient soundscapes using ElevenLabs v3 audio tags and Sound Effects API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashutosh887](https://clawhub.ai/user/ashutosh887) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, content creators, writers, podcasters, and developers use MoodCast to convert text, stories, scripts, articles, and briefings into emotionally expressive speech with optional ambient soundscapes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected text and sound prompts to ElevenLabs and uses the user's ElevenLabs API key and credits. <br>
Mitigation: Use only with text and prompts that are acceptable to process through ElevenLabs, and configure the API key in an environment where its use can be monitored. <br>
Risk: The script may automatically install the unpinned elevenlabs Python package at runtime if it is missing. <br>
Mitigation: Install dependencies from the reviewed requirements file in an isolated Python environment before running the skill. <br>


## Reference(s): <br>
- [MoodCast ClawHub Page](https://clawhub.ai/ashutosh887/moodcast) <br>
- [MoodCast Homepage](https://github.com/ashutosh887/moodcast) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [Moltbot](https://molt.bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Files, Configuration] <br>
**Output Format:** [Enhanced text, generated audio files, command-line output, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY; can save speech and ambient audio as MP3 files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
