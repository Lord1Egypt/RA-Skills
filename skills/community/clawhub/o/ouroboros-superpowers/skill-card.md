## Description: <br>
Guides coding agents through triggered workflows for interviewing, specification writing, implementation planning, execution, and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tty444](https://clawhub.ai/user/tty444) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to turn unclear coding requests into a concise spec, plan implementation tasks, execute changes, and verify results. It is intended for explicit workflow triggers such as ouroboros, superpowers, or full-flow requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated specs, plans, or code changes may not match the user's intent or project constraints. <br>
Mitigation: Review the generated spec, plan, execution mode, diffs, and commits before approving or relying on changes. <br>
Risk: Broad workflow triggers can lead the agent into planning, editing, testing, or commit behavior when the user expected a narrower response. <br>
Mitigation: Use explicit triggers such as ouroboros, superpowers, or full-flow requests, and confirm the selected workflow mode before execution. <br>


## Reference(s): <br>
- [Ouroboros + Superpowers on ClawHub](https://clawhub.ai/tty444/ouroboros-superpowers) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with optional code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose specs, plans, file changes, tests, execution modes, and commits for user review.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
