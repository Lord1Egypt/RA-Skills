## Description: <br>
Fetches the latest news using news-aggregator-skill, formats it into a podcast script in Markdown format, and uses the tts skill to generate a podcast audio file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ksuriuri](https://clawhub.ai/user/Ksuriuri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users ask an agent to turn current news into a concise dual-host podcast briefing. The skill guides the agent through fetching public news, drafting a Markdown script, generating speech audio, and returning the script, audio file path, and included headlines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local dependency skills for news retrieval and text-to-speech generation. <br>
Mitigation: Install only after reviewing the local news and TTS dependency skills and their network behavior. <br>
Risk: Podcast text and optional reference audio may be sent to the configured TTS backend. <br>
Mitigation: Use guest-mode voices when possible, avoid sensitive source material, and provide NOIZ_API_KEY only when voice-cloning behavior is acceptable. <br>
Risk: Generated podcast files are written into the current workspace. <br>
Mitigation: Run the skill in an appropriate working directory and review or remove podcast_script.md, line_*.wav, list.txt, and podcast_output.wav after use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown script, command guidance, generated WAV files, and a concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes podcast_script.md, line_*.wav, list.txt, and podcast_output.wav in the current workspace; optional reference audio may be sent to the configured TTS backend.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
