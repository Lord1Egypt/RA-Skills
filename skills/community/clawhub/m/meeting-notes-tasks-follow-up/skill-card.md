## Description: <br>
Lightweight meeting-notes productivity workflow for turning transcripts or raw meeting notes into clean summaries, extracted key points, and simple action lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaelbuenobarthe](https://clawhub.ai/user/gaelbuenobarthe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, team leads, and operations users use this skill to turn meeting transcripts, call notes, workshop notes, or internal sync notes into a concise recap, key points, simple tasks, and open questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting notes and transcripts may contain sensitive business or personal information. <br>
Mitigation: Process only appropriate local inputs, review outputs before sharing, and avoid placing confidential transcript content in unintended destinations. <br>
Risk: The bundled scripts write output files and could overwrite files if pointed at an existing path. <br>
Mitigation: Use deliberate input and output paths, and write to a new or disposable output location before replacing important files. <br>
Risk: Generated tasks may omit context or misread lightly implied follow-up items. <br>
Mitigation: Review extracted tasks against the original notes before treating owners, statuses, or next steps as commitments. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/gaelbuenobarthe/meeting-notes-tasks-follow-up) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON summary and CSV task files from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow keeps owners and due dates blank or unassigned when they are not present in the source notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
