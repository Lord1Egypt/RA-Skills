## Description:

Guaikei Video2text turns public or local video and audio inputs into cleaned transcripts, summaries, meeting minutes, scripts, translations, and social media copy through GuaiKei's cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert a single accessible video or audio source into reusable text, then optionally ask for summaries, meeting notes, content analysis, translations, or platform-specific copy. It is intended for completed public links or local files, not live streams, login-protected media, pure music, or high-concurrency batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provided media URLs or files are sent to GuaiKei's cloud service under the user's API token.

Mitigation: Use only public or approved media, and avoid sensitive internal recordings unless GuaiKei's privacy, retention, billing, and service terms are acceptable.

Risk: Use of the cloud transcription service may incur charges.

Mitigation: Confirm token ownership and billing expectations before use, and avoid unnecessary duplicate submissions or uncontrolled batch processing.

Risk: Transcript and generated copy quality can degrade with noisy audio, overlapping speakers, strong accents, background music, or specialized content.

Mitigation: Review outputs before relying on them, especially for medical, legal, financial, or other high-stakes material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-video2text-1-0-1)
- [GuaiKei Homepage](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown generated from a video transcript, optionally shaped by the user's prompt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and sends the provided media URL or file to GuaiKei's cloud service.]

## Skill Version(s):

1.0.1 (source: artifact/SKILL.md frontmatter; ClawHub release metadata version: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
