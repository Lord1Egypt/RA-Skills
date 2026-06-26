## Description: <br>
YouTube and Bilibili video transcript extraction and AI-powered summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcdowell8023](https://clawhub.ai/user/mcdowell8023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to extract transcripts from YouTube or Bilibili videos, summarize individual videos, scan channels for recent content, and generate daily video digest JSON for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Chrome browser cookies for Bilibili downloads. <br>
Mitigation: Use a dedicated browser profile or explicit cookie file, avoid private accounts, and review cookie access before running Bilibili workflows. <br>
Risk: Transcript and video metadata may be sent to external LLM providers. <br>
Mitigation: Set an explicit trusted LLM provider and avoid processing private, confidential, or sensitive videos. <br>
Risk: The setup script installs dependencies and configures local behavior. <br>
Mitigation: Review setup.sh and dependency installation steps before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mcdowell8023/oc-youtube-summarizer) <br>
- [Publisher Profile](https://clawhub.ai/user/mcdowell8023) <br>
- [Repository](https://github.com/mcdowell8023/oc-youtube-summarizer) <br>
- [Original Skill Acknowledgment](https://github.com/happynocode/openclaw-skill-youtube) <br>
- [innertube](https://github.com/tombulled/innertube) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON containing video metadata, transcript status, Markdown summaries, statistics, and optional local transcript or frame file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports text-only, auto-insert, and ai-review modes; Bilibili processing may produce local transcript and key-frame files.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
