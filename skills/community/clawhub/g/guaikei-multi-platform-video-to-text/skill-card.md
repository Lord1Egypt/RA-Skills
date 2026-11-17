## Description:

Converts video and audio files or public video links into cleaned transcripts and prompt-directed summaries, rewrites, translations, and other written content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, teams, and developers use this skill to transcribe recorded video or audio and turn it into meeting notes, summaries, scripts, or social media copy. It accepts a local file, a public link, or an existing task ID and requires a GuaiKei API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, prompts, task IDs, and related metadata are sent to GuaiKei and its upload storage provider; data-handling scope is not fully constrained.

Mitigation: Review before use, avoid confidential media unless you independently trust the provider's retention and deletion promises, and invoke only with explicit media paths, URLs, or task IDs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-multi-platform-video-to-text)
- [GuaiKei website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or prompt-directed structured prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results go to standard output; progress messages go to standard error.]

## Skill Version(s):

1.0.0 (source: ClawHub release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
