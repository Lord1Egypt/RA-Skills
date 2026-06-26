## Description: <br>
一个文学气质的聆听者与记录者，通过分层提问帮用户把真实经历写成散文日记。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justzerox](https://clawhub.ai/user/justzerox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to turn personal experiences, daily reflections, travel memories, emotional notes, and optional photo context into concise literary diary prose. The skill guides the user with layered questions, preserves user-provided facts, and avoids inventing relationships, dialogue, causes, or emotions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Photo metadata may include EXIF timestamps, camera model information, or GPS coordinates that expose private location details. <br>
Mitigation: Strip EXIF from photos before use when location privacy matters, or provide time and place manually instead of sharing original image metadata. <br>
Risk: The optional EXIF helper can install Python image libraries when runtime auto-install is enabled. <br>
Mitigation: Install dependencies explicitly with requirements.txt and review dependency installation before allowing runtime auto-install. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justzerox/my-literary-moment) <br>
- [style-anchors.md](references/style-anchors.md) <br>
- [writing-rules.md](references/writing-rules.md) <br>
- [writing-samples.md](references/writing-samples.md) <br>
- [requirements.txt](requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown prose with occasional shell commands for optional EXIF extraction] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use optional photo EXIF metadata for chronology and scene context, while keeping the diary content grounded in user-provided text.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
