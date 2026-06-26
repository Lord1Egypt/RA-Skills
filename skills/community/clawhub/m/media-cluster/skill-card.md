## Description: <br>
Crawls Chinese social media by keyword, summarizes collected posts, writes a Markdown report, and can generate a short voice summary with SenseAudio TTS. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[q1lin570](https://clawhub.ai/user/q1lin570) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect keyword-based results from supported Chinese social platforms, summarize themes and representative posts, and optionally produce a spoken summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and run an unpinned third-party crawler and install dependencies. <br>
Mitigation: Review or pin the MediaCrawler commit before setup, and run the workflow in an isolated, low-privilege environment. <br>
Risk: The crawler may use logged-in social-media sessions and store crawl results locally. <br>
Mitigation: Use a separate low-privilege social-media account where possible, follow platform terms, protect local data, and clear cached sessions after use. <br>
Risk: Voice generation can send summary text to an external TTS service. <br>
Mitigation: Enable TTS only for summaries suitable for sharing with SenseAudio and keep API keys in environment variables. <br>


## Reference(s): <br>
- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) <br>
- [SenseAudio API Documentation](https://senseaudio.cn/docs/) <br>
- [SenseAudio Text-to-Speech API](https://senseaudio.cn/docs/text_to_speech_api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Text, Audio] <br>
**Output Format:** [Markdown report, plain-text voice script, optional MP3 audio, and inline shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local MediaCrawler data files and report/audio files; optional TTS requires SENSEAUDIO_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
