## Description: <br>
Build, run, and visualize multi-step AI generation workflows using natural-language workflow architecture and the muapi CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anil-matcha](https://clawhub.ai/user/Anil-matcha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover, create, edit, execute, and inspect multi-step muapi.ai generation workflows for image, video, audio, enhancement, and editing pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to reinstall an external local muapi CLI at the start of each session. <br>
Mitigation: Install only from a trusted local muapi CLI source and require explicit user confirmation before running the installation step. <br>
Risk: Workflow create, edit, rename, delete, execute, download, and webhook actions can mutate remote state or move data outside the workspace. <br>
Mitigation: Require explicit user confirmation before workflow mutation, execution, downloads, or webhook URL use, and review inputs before sending them to the CLI. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Anil-matcha/muapi-workflow-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger muapi CLI workflow creation, mutation, execution, output download, and webhook usage when a user authorizes those actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
