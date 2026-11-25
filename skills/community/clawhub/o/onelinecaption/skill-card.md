## Description:

Transcribes MP4 videos and creates summaries, rewrites, quotes, storyboards, and translations from custom prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Creators, editors, and teams use this skill to transcribe local MP4 files or direct MP4 links, then turn the spoken content into summaries, meeting notes, promotional copy, quotes, storyboards, or translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports a download weakness that could reach private services, and some responses may be sent to cloud storage; analysis is incomplete.

Mitigation: Review the download and upload behavior before use, and only provide MP4 links and video content that are intended for processing by the service.

Risk: The security assessment reports an undisclosed token requirement; the skill documentation requires GUAIKEI_API_TOKEN for service access.

Mitigation: Set the token through the documented environment variable, keep it private, and review service billing and data handling before submitting videos.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/engheng-art/skills/onelinecaption)
- [一键台词 service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or Markdown generated from video transcription or a custom prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One video per command; accepts local MP4 files or direct MP4 links.]

## Skill Version(s):

1.0.1 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
