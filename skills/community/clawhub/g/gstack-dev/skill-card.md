## Description: <br>
Gstack AI虚拟工程团队 turns one AI assistant into a role-based engineering team for sprint planning, implementation, review, testing, release, and reflection workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangbotaochn](https://clawhub.ai/user/wangbotaochn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure complex software work as a multi-stage sprint with product thinking, architecture review, implementation, code review, E2E testing, deployment, and retrospective outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can guide broad code changes, real-environment testing, merges, deployments, or production access without enough explicit consent boundaries. <br>
Mitigation: Use it on local or staging projects by default and require explicit approval before file writes, destructive tests, merges, deployments, or production access. <br>
Risk: Cross-model review and memory-oriented workflows may share proprietary code, secrets, customer data, or regulated data with external systems. <br>
Mitigation: Do not use cross-checking or memory updates with sensitive data unless the external sharing and retention implications have been reviewed and accepted. <br>
Risk: Generated engineering plans, code, commands, and release steps may be incorrect or incomplete. <br>
Mitigation: Review outputs before execution, run project tests and security scans, and keep deployment and rollback decisions under human control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangbotaochn/gstack-dev) <br>
- [Garry Tan gstack methodology reference](https://github.com/garrytan/gstack) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, checklists, implementation guidance, code or test changes, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [High-autonomy workflows may propose or perform staged code changes, tests, releases, and cross-model review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
