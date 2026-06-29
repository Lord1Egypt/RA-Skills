## Description: <br>
Audits Rust code for unsafe blocks, ownership issues, and Cargo dependency risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Rust changes for ownership, error handling, concurrency, unsafe and FFI usage, dependency risk, performance, idioms, tests, and security patterns before merging or shipping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad Rust-related terms and produce review guidance outside the intended scope. <br>
Mitigation: Confirm that the current task is a Rust code review before applying its findings. <br>
Risk: The skill may suggest cargo commands or tool installation commands during review. <br>
Mitigation: Review suggested commands before execution and run them only in a trusted development environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-rust-review) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown audit report with structured findings and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include recommendations and an approve, approve with actions, or block disposition.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
