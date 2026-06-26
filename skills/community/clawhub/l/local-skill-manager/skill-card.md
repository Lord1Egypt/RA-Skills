## Description: <br>
Manages local Skill directories by listing installed skills, checking versions, scaffolding new skills, and safely deleting unneeded skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChenChen913](https://clawhub.ai/user/ChenChen913) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect and maintain local skill installations, create new skill scaffolds, and remove old skills with confirmation and dry-run safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Create and delete operations can modify local Skill directories, including permanent deletion when force options are used. <br>
Mitigation: Confirm the exact target skill before execution, prefer dry-run mode before deletion, and keep backups or version control. <br>
Risk: The skill depends on parsing SKILL.md frontmatter and may produce incomplete listings if metadata is malformed or dependencies are not installed. <br>
Mitigation: Install the declared pyyaml dependency and review script output before acting on version or inventory results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChenChen913/local-skill-manager) <br>
- [Publisher profile](https://clawhub.ai/user/ChenChen913) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Python scripts that read, create, or delete Skill directories.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
