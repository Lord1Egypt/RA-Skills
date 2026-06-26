## Description: <br>
Manages and standardizes product requirement documents by organizing project folders, reading the latest relevant files, and keeping project overview documents updated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinqianfei](https://clawhub.ai/user/jinqianfei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, analysts, and project teams use this skill to keep requirement, design, development, testing, and release documents in a consistent ProductManagement folder structure. It helps agents find the current project context and latest versioned documents before performing review, analysis, design, development, testing, or project-management tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create, move, or update local project documentation files in user-selected folders. <br>
Mitigation: Ask the agent to preview exact paths and proposed file changes before applying them, especially in important project or document folders. <br>
Risk: The skill depends on versioned filenames and folder conventions to choose the latest project documents. <br>
Mitigation: Confirm that document names, SemVer values, and ProductManagement directory structure follow the documented conventions before relying on automated document selection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinqianfei/project-doc-management) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jinqianfei) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file paths, directory structures, configuration snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, move, read, or update local project documentation files when the user authorizes those actions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
