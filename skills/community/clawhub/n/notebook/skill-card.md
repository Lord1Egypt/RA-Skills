## Description: <br>
Local-first personal knowledge base for tracking ideas, projects, tasks, habits, and any object type you define. YAML-based with no cloud lock-in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to set up and operate a local, YAML-backed notebook for user-defined object types such as ideas, projects, tasks, habits, books, and people. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local notebook records may contain sensitive personal or project information. <br>
Mitigation: Avoid storing secrets or credentials in notebook entries and review local file permissions before use. <br>
Risk: Delete operations remove notebook objects from local storage. <br>
Mitigation: Keep backups of the notebook folder and manually confirm the target object before deleting until confirmation or soft-delete behavior is added. <br>
Risk: Loose type names or paths can make local file handling harder to review. <br>
Mitigation: Use simple type names made from letters, numbers, hyphens, and underscores. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheSethRose/notebook) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, files] <br>
**Output Format:** [Markdown guidance with notebook CLI commands and local YAML/JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local notebook object/type data in the workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
