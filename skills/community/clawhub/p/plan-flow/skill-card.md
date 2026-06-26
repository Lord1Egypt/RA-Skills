## Description: <br>
Structured AI-assisted development workflows - discovery, planning, execution, code reviews, and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunoscardoso](https://clawhub.ai/user/brunoscardoso) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure AI-assisted software work through discovery, planning, execution, review, and testing workflows with persistent project notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and modify repository files as part of planning, execution, review, and testing workflows. <br>
Mitigation: Review generated files and diffs before committing, and run the workflow only in repositories where automated edits are acceptable. <br>
Risk: The project ledger stores persistent notes in flow/ledger.md and may capture project or preference details across sessions. <br>
Mitigation: Do not store secrets or sensitive business details in the ledger, and periodically review, prune, or remove ledger content. <br>
Risk: Autopilot mode can chain workflow steps for feature requests when enabled. <br>
Mitigation: Keep autopilot disabled unless automatic workflow chaining is explicitly desired, and require review of discovery and plan artifacts before execution. <br>
Risk: The contract workflow can fetch or read API documentation URLs supplied by the user. <br>
Mitigation: Use trusted documentation URLs and review generated contracts before relying on extracted schemas, authentication details, or examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brunoscardoso/plan-flow) <br>
- [Project homepage](https://github.com/brunoscardoso/plan-flow) <br>
- [Publisher profile](https://clawhub.ai/user/brunoscardoso) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions and generated project files, with inline shell commands and code examples when relevant.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates files under flow/ and may create .plan-flow.yml or flow/.autopilot when directed by the workflow.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
