## Description: <br>
CEO/founder-mode plan review that challenges premises, reviews strategy, and helps users choose between scope expansion, selective expansion, hold-scope rigor, and scope reduction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loocor](https://clawhub.ai/user/loocor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, founders, and product decision-makers use this skill to pressure-test implementation plans, surface edge cases, choose a scope posture, and turn strategic review into concrete next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect repository history and working context during plan review. <br>
Mitigation: Run it only in repositories where that review scope is acceptable, and review any findings before acting on them. <br>
Risk: The skill may propose or create planning documents, TODO updates, or promoted design docs. <br>
Mitigation: Approve file changes only when those documents should be added to the repository, and review the diff before committing. <br>
Risk: The skill is intentionally opinionated and may recommend broader scope or more rigorous implementation than requested. <br>
Mitigation: Use the explicit mode selection and option prompts to accept, defer, skip, or reduce scope deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loocor/gstack-plan-ceo-review) <br>
- [Publisher profile](https://clawhub.ai/user/loocor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown with structured review sections, option prompts, tables, ASCII diagrams, and inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or create planning documents and TODO updates when the user approves those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
