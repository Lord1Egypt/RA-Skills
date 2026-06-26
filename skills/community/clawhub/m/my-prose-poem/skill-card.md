## Description: <br>
A literary listening and writing skill that uses layered questions to help users turn real experiences, feelings, travel memories, life fragments, inner monologues, or photos into restrained prose diary entries without fabricating details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justzerox](https://clawhub.ai/user/justzerox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to organize real experiences, emotions, reflections, and optional photo context into concise prose diary entries. The agent asks focused follow-up questions, preserves user-provided details, and avoids inventing events, dialogue, relationships, causes, or emotional states. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Photos can contain EXIF timestamps, GPS coordinates, and device details. <br>
Mitigation: Process photos only when the user chooses photo-based writing, use EXIF only as objective timeline or scene context, and fall back to asking for approximate time or place when metadata is unavailable or sensitive. <br>
Risk: Optional auto-install can fetch Python packages at runtime. <br>
Mitigation: Leave auto-install disabled unless the user is comfortable installing Pillow; otherwise use the manual fallback workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/justzerox/my-prose-poem) <br>
- [Style anchors](references/style-anchors.md) <br>
- [Writing rules](references/writing-rules.md) <br>
- [Writing samples](references/writing-samples.md) <br>
- [Pillow 10.0.0](https://pypi.org/project/Pillow/10.0.0/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Conversational prompts and Markdown prose, with optional JSON EXIF summaries from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional local photo metadata processing can sort images by EXIF time and use DateTime, GPSParsed, and camera model as objective context.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
