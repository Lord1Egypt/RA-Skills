## Description: <br>
Audits Rust code for unsafe blocks, ownership issues, and Cargo dependency risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Rust changes for ownership, error handling, concurrency, unsafe code, dependency security, and idiomatic implementation issues before merging or releasing code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad Rust-related triggers and may activate for general Rust discussion or review contexts. <br>
Mitigation: Confirm the task is a Rust code review before applying its checklist or recommendations. <br>
Risk: The skill may suggest cargo install, cargo audit, or other long-running audit commands. <br>
Mitigation: Review proposed commands and their runtime impact before allowing an agent to execute them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-pensive-rust-review) <br>
- [Publisher Profile](https://clawhub.ai/user/athola) <br>
- [Skill Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive) <br>
- [The Cost of Concurrency Coordination](https://youtube.com/watch?v=tND-wBBZ8RY) <br>
- [Concurrency Costs](https://travisdowns.github.io/blog/2020/07/06/concurrency-costs.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown review findings with inline shell commands and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review guidance and action items; any suggested cargo or audit commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
