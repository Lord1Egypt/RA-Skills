## Description: <br>
Manages PARA-based personal knowledge management systems by helping agents scaffold, organize, validate, archive, and generate navigation for Projects, Areas, Resources, and Archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killerapp](https://clawhub.ai/user/killerapp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, knowledge workers, and agent users use this skill to create and maintain PARA knowledge bases, decide where content belongs, generate AI navigation files, validate structure, and archive completed projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File-changing scripts can overwrite local output files or delete the source project file during archiving. <br>
Mitigation: Back up the knowledge base first, run commands from the intended KB root, and verify archive and output paths before execution. <br>
Risk: Absolute paths or ../ traversal can target files outside the intended PARA knowledge base. <br>
Mitigation: Use relative paths inside the KB whenever possible and reject paths that leave the expected Projects, Areas, Resources, or Archives tree. <br>


## Reference(s): <br>
- [PARA Method Principles](references/para-principles.md) <br>
- [PARA Decision Guide](references/decision-guide.md) <br>
- [Common PARA Patterns](references/common-patterns.md) <br>
- [AI Navigation Best Practices](references/ai-navigation.md) <br>
- [Forte Labs PARA Method](https://fortelabs.com/blog/para/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local files when scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local knowledge-base files such as README.md, AGENTS.md, archives, and PARA directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
