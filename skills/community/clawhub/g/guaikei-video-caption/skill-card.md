## Description:

Transcribes video or audio from a local file or public link and can generate summaries, rewrites, translations, and other structured text from the content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, editors, and teams use this skill to turn recordings and video links into transcripts, summaries, meeting notes, and adapted copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, links, and prompt text are sent to the provider for processing.

Mitigation: Use only media and prompts approved for external processing; avoid confidential videos and internal URLs unless the upload is intended.

Risk: The GUAIKEI_API_TOKEN is sent to the provider to authenticate requests, and online media links may be downloaded locally before upload.

Mitigation: Use a dedicated token and review the selected link before running the skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-video-caption)
- [Guaikei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or structured Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs a cleaned transcript by default or prompt-directed content; progress messages go to stderr.]

## Skill Version(s):

1.0.0 (source: server release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
