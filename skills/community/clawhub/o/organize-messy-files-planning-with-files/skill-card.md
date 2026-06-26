## Description: <br>
Helps agents plan complex work by creating and maintaining local task_plan.md, findings.md, and progress.md files in the active project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to preserve task plans, findings, decisions, progress, and errors across multi-step work. It is most useful for research, implementation, and troubleshooting tasks that need persistent working notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Planning files can contain task details, research notes, errors, file paths, and other sensitive project context. <br>
Mitigation: Review task_plan.md, findings.md, and progress.md before committing, publishing, or sharing them. <br>
Risk: The skill creates and updates local markdown planning files in the current project directory. <br>
Mitigation: Run it only in the intended workspace and inspect generated planning files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/organize-messy-files-planning-with-files) <br>
- [Reference: Manus Context Engineering Principles](artifact/reference.md) <br>
- [Examples: Planning with Files in Action](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown planning files with concise shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and checks local planning files in the active project directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 2.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
