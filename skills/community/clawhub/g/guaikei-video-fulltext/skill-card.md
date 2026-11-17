## Description:

Converts local video files or supported video links into cleaned transcripts and prompt-directed summaries, rewrites, translations, and other structured text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users working with courses, meetings, interviews, livestreams, or short-form video can create cleaned transcripts and prompt-directed summaries, translations, and reusable copy from local files or supported links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags a mismatch between stated network restrictions and video-transfer behavior, so privacy claims need review.

Mitigation: Confirm upload destinations and privacy terms before sending private recordings.

Risk: Source links may use unencrypted HTTP, and downloaded copies may remain locally until cleanup or manual removal.

Mitigation: Prefer HTTPS source links and remove local downloaded copies after processing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/guaikei-video-fulltext)
- [Guaikei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or prompt-directed structured text, written to standard output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One text stream per video task; a custom prompt determines whether the result is a transcript, summary, translation, rewrite, or other requested copy.]

## Skill Version(s):

1.0.0 (source: ClawHub release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
