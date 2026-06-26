## Description: <br>
Proflow guides agents through a standardized project delivery workflow from requirement brainstorming through planning, execution, documentation, status tracking, and reset operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1232023](https://clawhub.ai/user/luis1232023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use Proflow to standardize feature delivery, including requirement IDs, staged planning, execution records, and generated project documentation. It is most useful when an agent should follow explicit phase commands such as full, brainstorm, plan, execute, spec, status, and reset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may write project documentation, create local state files, modify .gitignore, and change code without a clear approval gate. <br>
Mitigation: Keep the project under version control, invoke explicit Proflow subcommands, and review diffs after each run. <br>
Risk: The workflow depends on separate openspec and superpowers skills. <br>
Mitigation: Review and install those required skills separately before relying on Proflow output. <br>


## Reference(s): <br>
- [Proflow on ClawHub](https://clawhub.ai/luis1232023/proflow) <br>
- [Publisher profile](https://clawhub.ai/user/luis1232023) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command names, file paths, generated documentation, status files, and local script invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates project documentation, logs, status markers, and standardized filenames in the working repository.] <br>

## Skill Version(s): <br>
2.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
