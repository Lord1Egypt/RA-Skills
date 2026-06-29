## Description: <br>
Pre-implementation gate covering think-first, simplicity, surgical edits, and verifiable goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill as a pre-flight and self-audit guide for coding tasks, code review, and training workflows that benefit from explicit assumptions, narrow scope, surgical edits, and verifiable success criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill influences how an agent plans, reasons, and verifies work, so generated assumptions or verification plans could still be incomplete or misleading. <br>
Mitigation: Review the agent's assumptions, scope rationale, diff trace, and verification plan before relying on them. <br>
Risk: The guidance can over-constrain trivial, exploratory, documentation-only, prototype, or emergency work if applied mechanically. <br>
Mitigation: Use the artifact's tradeoff guidance to skip or adapt the gate when the cost of slowing down is higher than the risk of the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-karpathy-principles) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown guidance with checklists and worked examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credential handling, hidden execution, persistence, or exfiltration was identified in the server security evidence.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
