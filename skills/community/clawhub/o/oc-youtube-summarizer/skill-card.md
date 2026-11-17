## Description:

YouTube and Bilibili video transcript extraction and AI-powered summarization for individual videos, channel scans, and daily video digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcdowell8023](https://clawhub.ai/user/mcdowell8023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external agents use this skill to extract video transcripts, summarize YouTube and Bilibili videos, scan configured channels, and generate daily digest JSON for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video transcripts and metadata may be sent to configured or fallback external LLM providers.

Mitigation: Use only approved providers for sensitive content, disable external fallback behavior where needed, and avoid private, licensed, internal, or account-restricted videos unless data sharing is explicitly approved.

Risk: Bilibili processing may read Chrome browser cookies to access video content.

Mitigation: Run the skill only in environments where browser-cookie access is acceptable, and avoid account-restricted videos unless cookie use has been reviewed.

Risk: Dependency installation and media tooling can change behavior over time.

Mitigation: Pin dependencies, review the setup script before installation, and prefer a private temporary work directory for generated transcripts, audio, and frames.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcdowell8023/skills/oc-youtube-summarizer)
- [Repository metadata](https://github.com/mcdowell8023/oc-youtube-summarizer)
- [Publisher profile](https://clawhub.ai/user/mcdowell8023)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, configuration]

**Output Format:** [JSON containing video metadata, transcript status, Markdown summaries, statistics, and optional transcript or frame file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text-only, auto-insert, and AI-review output modes; Bilibili mode may produce local transcript and frame files.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
