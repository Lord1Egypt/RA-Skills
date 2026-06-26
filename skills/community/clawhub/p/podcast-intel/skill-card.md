## Description: <br>
Transcribes, segments, summarizes, and scores podcast episodes from RSS feeds to generate ranked recommendations and maintain a local consumption diary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexSpaceiosdev](https://clawhub.ai/user/nexSpaceiosdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Podcast listeners, researchers, and agents use this skill to turn configured podcast feeds or specific episode URLs into briefings, summaries, relevance scores, and listening recommendations. It can also display a local diary of prior podcast briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podcast audio and transcript text can be sent to OpenAI-compatible services unless local transcription mode is used. <br>
Mitigation: Use trusted feeds, review OPENAI_BASE_URL before use, and enable local mode when external processing is not appropriate. <br>
Risk: Transcripts, cached analyses, and listening-history summaries are stored locally and may contain sensitive interests or consumption history. <br>
Mitigation: Use --dry-run when diary writes are not desired and clear the podcast-intel cache or diary when stored history is sensitive. <br>


## Reference(s): <br>
- [Podcast Intel ClawHub release](https://clawhub.ai/nexSpaceiosdev/podcast-intel) <br>
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text) <br>
- [RSS 2.0 Specification](https://www.rssboard.org/rss-spec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance, files] <br>
**Output Format:** [Markdown, JSON, or TTS-ready text; diary entries are stored as JSONL and markdown notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are ranked by worth-your-time scoring and may update local cache, diary, and memory files unless dry-run or cache-only modes are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
