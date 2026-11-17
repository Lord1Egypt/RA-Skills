## Description:

Converts local videos and video links into edited transcripts or prompt-guided summaries, rewrites, translations, and other text using a cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, editors, and teams use this skill to transcribe videos or audio and create summaries, meeting notes, translations, or social media copy from local files or video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local or downloaded media, prompts, task IDs, and the GUAIKEI token are sent to a cloud service.

Mitigation: Use only authorized media, avoid confidential or regulated recordings without approval, and confirm that sharing the token and prompts with the service is acceptable.

Risk: The skill can download supplied URLs, including destinations beyond its narrow stated network scope.

Mitigation: Confirm each URL and local path before use, and prefer public media URLs over internal or private-network links.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-video-text-converter)
- [guaikei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcripts or prompt-guided copy are written to stdout; progress is written to stderr.]

## Skill Version(s):

1.0.0 (source: ClawHub release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
