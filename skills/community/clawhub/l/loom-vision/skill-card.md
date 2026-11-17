## Description:

Process a Loom share URL into multimodal context: a downloaded video, sampled frames, and the auto-generated transcript.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrollinondubs](https://clawhub.ai/user/scrollinondubs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and support teams use this skill to turn Loom walkthroughs, bug repros, demos, and design reviews into transcript-plus-frame context that an agent can inspect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download Loom recordings and retain local copies of videos, transcripts, and sampled frames.

Mitigation: Use it only for recordings suitable for local processing, set a private OUTPUT_ROOT for sensitive material, and delete generated files after review.

Risk: The skill relies on an unpinned loom-dl downloader dependency.

Mitigation: Prefer a pinned and reviewed loom-dl version before using the skill in sensitive or repeatable workflows.

## Reference(s):

- [Loom Vision ClawHub Skill Page](https://clawhub.ai/scrollinondubs/skills/loom-vision)
- [Behalf.bot](https://behalf.bot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated local media, transcript, and frame files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local output directory containing video.mp4, transcript.json, transcript.vtt, transcript.txt, and sampled frame_NNN.jpg files.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
