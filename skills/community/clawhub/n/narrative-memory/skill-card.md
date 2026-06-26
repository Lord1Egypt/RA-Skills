## Description: <br>
Narrative Memory captures meaningful life moments, applies a three-layer filter to keep salient memories, and supports pattern recognition and decision reflection for milestones, decisions, value judgments, emotional turns, first experiences, and deep reflection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoguoqiang-hub](https://clawhub.ai/user/zhaoguoqiang-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to identify meaningful personal events, store narrative memories, review timelines, and analyze recurring topics, emotions, and values. It can also process proactive-engine signals for automatic capture of important moments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive life events, moods, values, reflections, and raw source text locally. <br>
Mitigation: Review stored files under ~/.openclaw/workspace/.soul, redact or delete sensitive records before sharing the workspace, and avoid entering information that should not be retained. <br>
Risk: Automatic signal processing may capture more personal context than the user intended. <br>
Mitigation: Enable proactive capture only after reviewing trigger behavior and keep manual review, deletion, and backup practices in place. <br>
Risk: The current artifacts do not document encryption or automatic data minimization for the local memory files. <br>
Mitigation: Treat the local storage location as sensitive, apply host-level access controls or encryption as appropriate, and avoid assuming records are minimized by default. <br>


## Reference(s): <br>
- [Narrative Memory Guidelines](references/narrative-guidelines.md) <br>
- [Narrative Templates](references/templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaoguoqiang-hub/narrative-memory) <br>
- [Publisher Profile](https://clawhub.ai/user/zhaoguoqiang-hub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text and JSON-backed local memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes narrative records and configuration under the local .openclaw workspace when invoked.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
