## Description: <br>
七阶段多角色工作坊技能：先澄清任务、再选角讨论、最后产出并执行 plan，附带可执行 orchestrator。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[349840432m-dev](https://clawhub.ai/user/349840432m-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to run a structured multi-role workshop for complex requirements: clarify the deliverable, choose task-specific roles, capture discussion, draft a plan, and execute only after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow writes local workshop state and may use subagents, which can capture sensitive task context in generated files. <br>
Mitigation: Use the skill only in an approved workspace, review generated state and plan files before sharing, and avoid placing confidential requirements in workshop artifacts unless that storage is acceptable. <br>
Risk: The optional JD search feature can send role, industry, and task query terms to Serper. <br>
Mitigation: Use JD search only for non-confidential tasks, redact sensitive terms before searching, and configure SERPER_API_KEY only when this external lookup is acceptable. <br>
Risk: The JD search script has an unsafe TLS fallback when certificate support is unavailable. <br>
Mitigation: Install and use proper certificate validation support, or avoid the JD search feature until the TLS fallback is fixed. <br>
Risk: The cleanup and configuration utilities can edit OpenClaw session state or configuration outside the workshop directory. <br>
Mitigation: Review target paths and backups before running cleanup or configuration commands, and avoid these utilities when the broader OpenClaw state must remain untouched. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/349840432m-dev/multi-agent-workshop) <br>
- [README](README.md) <br>
- [Role card from JD guide](references/role-card-from-jd.md) <br>
- [Role card skeleton](references/role-card-skeleton.md) <br>
- [Anti-drift rules](references/anti-drift.md) <br>
- [Debate protocol](references/debate-protocol.md) <br>
- [Subagent closure guide](references/subagent-closure.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plans and workshop state, role-card drafts, Python and shell command invocations, configuration edits, and final deliverable files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes workshop artifacts under workshops/<session_id>/; optional JD search uses SERPER_API_KEY; execution is gated on user approval of plan.md.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
