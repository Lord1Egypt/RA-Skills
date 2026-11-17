## Description:

Podcast Intel transcribes, segments, summarizes, scores, and recommends podcast episodes from RSS feeds while maintaining a local consumption diary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexspaceiosdev](https://clawhub.ai/user/nexspaceiosdev)

### License/Terms of Use:

MIT-0

## Use Case:

Podcast listeners, researchers, and developers use this skill to turn subscribed feeds or episode URLs into ranked listening recommendations, concise summaries, and a local record of consumed topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Podcast audio, transcript excerpts, and derived summaries may be sent to external AI providers.

Mitigation: Use only trusted podcast feeds and episode URLs, avoid processing sensitive audio, and review provider settings before enabling API-based transcription or analysis.

Risk: A custom OPENAI_BASE_URL can redirect audio, transcript, and summary data to an endpoint outside the expected provider.

Mitigation: Leave OPENAI_BASE_URL unset unless the endpoint is controlled and trusted.

Risk: Untrusted and model-derived podcast content can be stored in local diary, cache, and memory files.

Mitigation: Use dry_run while evaluating behavior, review generated diary and memory entries before relying on them, and clear local cache or diary files when content should not persist.

## Reference(s):

- [Podcast Intel ClawHub Release](https://clawhub.ai/nexspaceiosdev/skills/podcast-intel)
- [OpenClaw Skills Documentation](https://openclaw.ai/docs/skills)
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [Podcast Standards (RSS 2.0)](https://www.rssboard.org/rss-spec)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, or TTS-ready text; diary entries are JSONL and memory notes are Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local transcript, segmentation, analysis, cache, diary, and memory files; dry_run avoids diary writes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
