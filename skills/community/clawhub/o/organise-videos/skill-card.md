## Description:

Organize a video folder by cleaning non-video files, removing short/bad videos, and classifying videos into numbered subfolders using AI vision analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lemondepat](https://clawhub.ai/user/lemondepat)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to reorganize local video folders by removing or isolating unwanted files, analyzing representative frames, and moving videos into clear category folders. It is useful when a video collection needs quick cleanup and content-based grouping before review, editing, or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move or delete files in the user-provided video folder.

Mitigation: Review every deletion or move prompt carefully, and prefer moving files to _misc or _rejected when unsure.

Risk: Extracted video frames may contain sensitive visual content and are written to a temporary frame directory during analysis.

Mitigation: Avoid using the skill on highly sensitive videos unless frame extraction is handled in a private per-run temporary directory and cleaned up after analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lemondepat/skills/organise-videos)
- [Publisher profile](https://clawhub.ai/user/lemondepat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with summary tables, user prompts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces folder organization plans, category labels, quality notes, and file move or deletion commands for user-approved execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
