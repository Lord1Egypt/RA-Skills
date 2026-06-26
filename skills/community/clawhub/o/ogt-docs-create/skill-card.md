## Description: <br>
Create new documentation entities in the docs-first system. Routes to specialized creation sub-skills for tasks, definitions, rules, features, and social content. Use when adding any new documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EduardoU24](https://clawhub.ai/user/EduardoU24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to create docs-first project entities such as tasks, definitions, rules, feature docs, social content, and changelog updates with consistent folders, templates, and signal files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell snippets can create or modify documentation files in the active repository. <br>
Mitigation: Run them only in the intended repository and review generated paths and diffs before accepting changes. <br>
Risk: The batch creation example can create several files and folders at once. <br>
Mitigation: Use extra care with batch inputs and inspect the resulting documentation tree before committing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and document templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local documentation creation guidance; shell snippets may create files and folders in the active repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
