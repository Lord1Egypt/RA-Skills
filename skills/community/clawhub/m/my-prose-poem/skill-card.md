## Description:

My Prose Poem helps users turn real experiences, daily reflections, travel memories, and photo-supported moments into restrained prose diary entries through layered questioning without fabricating details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justzerox](https://clawhub.ai/user/justzerox)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record daily experiences, travel memories, emotional reflections, and photo-based recollections as prose diary entries. The skill asks focused follow-up questions, preserves user-provided facts and phrasing, and avoids inventing relationships, dialogue, causality, or emotions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Photo processing may expose sensitive timestamps, GPS coordinates, device model information, or other EXIF metadata.

Mitigation: Use only photos intended for journaling, remove unnecessary EXIF fields before use when privacy matters, and avoid sharing generated EXIF summaries beyond the intended conversation.

Risk: Optional auto-install behavior can install an unpinned Pillow package at runtime.

Mitigation: Leave --auto-install and MY_PROSE_POEM_AUTO_INSTALL disabled unless runtime installation is acceptable; install dependencies from requirements.txt in a controlled environment and pin Pillow if stricter dependency control is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justzerox/skills/my-prose-poem)
- [README](artifact/README.md)
- [Style anchors](artifact/references/style-anchors.md)
- [Writing rules](artifact/references/writing-rules.md)
- [Writing samples](artifact/references/writing-samples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose, brief conversational prompts, optional shell command suggestions, and optional JSON EXIF summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt diary length to the amount of user-provided material; optional photo handling may use EXIF DateTime, GPS, and camera model as factual context.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
