## Description: <br>
Guides agents through implementing or refactoring code against an approved architecture package, including pre-flight checks, NFR feasibility review, functional coverage checks, and human confirmation gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inetgas](https://clawhub.ai/user/inetgas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill when a repository already has approved architecture artifacts and code must be implemented or refactored to conform to those decisions. It is intended to keep implementation plans, code changes, and verification steps aligned with approved architecture, NFR targets, selected patterns, and functional requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security guidance notes that related workflow capabilities can run privileged local commands or perform staff-level actions when invoked with appropriate credentials. <br>
Mitigation: Review the skill before use, restrict credentials to the minimum required scope, and review privileged shell commands or staff-level actions before execution. <br>
Risk: Using the skill without approved or internally consistent architecture artifacts could lead to implementation work that conflicts with intended architecture decisions. <br>
Mitigation: Require the documented pre-flight checks, stop on architecture-binding gaps or mismatches, and obtain explicit human confirmation before planning or writing implementation code. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/inetgas/arch-compiler) <br>
- [ClawHub skill page](https://clawhub.ai/inetgas/implementing-architecture) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code changes, configuration edits, shell command snippets, and verification summaries when implementation proceeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires approved architecture artifacts and explicit human confirmation before moving from pre-flight checks into implementation planning.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
