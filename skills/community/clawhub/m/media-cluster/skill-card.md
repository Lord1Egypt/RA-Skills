## Description:

Crawls Chinese social media platforms by keyword, summarizes the collected content, writes a Markdown report, and can generate a short voice summary through TTS.

This skill is for research and development only.

## Publisher:

[q1lin570](https://clawhub.ai/user/q1lin570)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run keyword-based crawls across supported Chinese social platforms and convert the collected posts into a concise report and optional voice summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically downloads and runs unpinned third-party crawler code and dependencies.

Mitigation: Run it only in an isolated environment or container, and pin MediaCrawler plus dependency versions to reviewed revisions before setup.

Risk: QR login can create authenticated platform session state during crawling.

Mitigation: Use dedicated test accounts where appropriate and review local session artifacts before reuse or sharing.

Risk: Crawler output may contain personal or copyrighted social-media content.

Mitigation: Review collected data before sharing reports and follow applicable platform terms, privacy requirements, and content-use policies.

Risk: Enabling voice summary sends generated summary text to SenseAudio.

Mitigation: Disable TTS for sensitive crawls and provide the SenseAudio key through an environment variable rather than command-line arguments.

## Reference(s):

- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)
- [SenseAudio API documentation](https://senseaudio.cn/docs/)
- [SenseAudio text-to-speech API](https://senseaudio.cn/docs/text_to_speech_api)
- [ClawHub skill page](https://clawhub.ai/q1lin570/skills/media-cluster)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report, short voice-summary text, optional MP3 file, and setup or crawl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local crawler output; optional TTS uses SENSEAUDIO_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
