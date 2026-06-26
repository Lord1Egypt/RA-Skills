## Description: <br>
Best-practice management for recording verified solutions, reusing them across projects, and avoiding repeated troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexxxiong](https://clawhub.ai/user/alexxxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to capture, search, list, apply, update, and delete reusable best-practice notes stored locally. It helps teams or individuals reuse validated solutions across projects while keeping entries under their own local best-practices folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Best-practice entries are stored persistently in a local folder and may later be copied into projects. <br>
Mitigation: Do not save secrets or customer-sensitive data in entries, and review each entry before applying or copying it into a project. <br>
Risk: Copying an entry into docs/references/{id}.md can overwrite or conflict with an existing project reference file. <br>
Mitigation: Check whether docs/references/{id}.md already exists before copying an entry into project documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexxxiong/inspirai-bp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Markdown best-practice entries and index updates under $HOME/.inspirai/best-practices/ when the user chooses capture, update, copy, or delete workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
