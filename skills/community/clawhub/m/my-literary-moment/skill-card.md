## Description:

一个文学气质的聆听者与记录者，通过分层提问帮用户把真实经历写成不虚构的散文日记。

This skill is ready for commercial/non-commercial use.

## Publisher:

[justzerox](https://clawhub.ai/user/justzerox)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn diary prompts, travel memories, life fragments, emotional reflections, or photo-backed moments into concise prose diary entries after a short, layered interview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Photo EXIF metadata may include precise location, capture time, and device details.

Mitigation: Strip location metadata before sharing photos, or provide approximate time and place manually instead of allowing EXIF extraction.

Risk: The optional auto-install path can install Python packages during use.

Mitigation: Keep auto-install disabled unless the package source is trusted; install reviewed, pinned dependencies in an isolated environment.

Risk: Diary writing can place personal experiences and emotional content into the agent context.

Mitigation: Avoid submitting unnecessary sensitive details, and review generated text before sharing it outside the conversation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/justzerox/skills/my-literary-moment)
- [Skill instructions](artifact/SKILL.md)
- [Style anchors](artifact/references/style-anchors.md)
- [Writing rules](artifact/references/writing-rules.md)
- [Writing samples](artifact/references/writing-samples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose with optional shell commands for EXIF extraction]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can optionally read image EXIF metadata to help order photos by capture time; core diary writing works without external packages.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
