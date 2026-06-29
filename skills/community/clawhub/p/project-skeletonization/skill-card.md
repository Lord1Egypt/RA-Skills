## Description: <br>
Project Skeletonization guides an agent through converting a complete business project into a reusable base skeleton while preserving common framework capabilities and gating destructive changes on user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agilebuilder](https://clawhub.ai/user/agilebuilder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when turning an existing application into a reusable starter or template. It inventories the project, separates common framework capabilities from business-specific code, asks for confirmation on destructive changes, and guides verification of the resulting skeleton. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide deletion or refactoring of project files, which may remove reusable capabilities or business-critical code if project boundaries are misunderstood. <br>
Mitigation: Require the documented inventory, keep/remove lists, uncertain-items list, and user confirmation before any destructive transformation. <br>
Risk: Database, authentication, uploads, audit logs, scheduled jobs, and deployment configuration can be common framework capabilities or business-specific behavior depending on the project. <br>
Mitigation: Review these areas explicitly and approve retention or removal decisions before editing them. <br>


## Reference(s): <br>
- [Project Skeletonization on ClawHub](https://clawhub.ai/agilebuilder/skills/project-skeletonization) <br>
- [Publisher profile: agilebuilder](https://clawhub.ai/user/agilebuilder) <br>
- [Server-resolved source import: agilebuilder/agilebuilder-skills](https://github.com/agilebuilder/agilebuilder-skills/tree/master/skills/project-skeletonization) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks and command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Destructive transformations are confirmation-gated; final responses include verification results and unresolved concerns.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
