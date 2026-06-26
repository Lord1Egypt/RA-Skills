## Description: <br>
Helps users create structured notes with Cornell, Zettelkasten, mind map, meeting, lecture, and note-organization templates, with an included local task-list helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to generate reusable note-taking templates and manage lightweight terminal task notes. It is suited to class notes, meeting notes, structured study notes, quick capture, and local task review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task-list use can leave local note data and command history on disk. <br>
Mitigation: Avoid storing secrets or highly sensitive notes, set NOTE_TAKER_DIR deliberately when needed, and delete local data and history when they are no longer required. <br>
Risk: The package mixes note-template behavior with a task-list command script, which may make the active entrypoint unclear. <br>
Mitigation: Confirm which installed command or script is being run before relying on its behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bytesagain3/note-taker) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown templates and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Task-list commands may store local data and command history under NOTE_TAKER_DIR or XDG_DATA_HOME.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence; artifact frontmatter and scripts report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
