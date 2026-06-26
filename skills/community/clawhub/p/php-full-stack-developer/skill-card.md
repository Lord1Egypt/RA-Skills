## Description: <br>
A senior, governance-backed PHP full-stack delivery OS for OpenClaw that emphasizes pre-flight analysis, safe data changes, explicit contracts, and reproducible verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sja-dev1](https://clawhub.ai/user/sja-dev1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to plan and execute PHP full-stack work with explicit pre-flight checks, risk classification, data-safety rules, API/UI contract review, and reproducible test instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace memory and log files could capture secrets or unnecessary personal data during governance logging. <br>
Mitigation: Keep secrets and unnecessary personal data out of OpenClaw memory and log files; record only scoped, task-relevant facts. <br>
Risk: Database, authorization, API, or deployment changes can affect production systems if accepted without review. <br>
Mitigation: Review proposed changes before applying them, require rollout and rollback notes for high-risk work, and stop when auth, data, contract, or runtime constraints are unclear. <br>
Risk: Delegating to a specialized agent can share project context beyond the current session. <br>
Mitigation: Approve specialized-agent delegation only when the shared context is appropriate and constrained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sja-dev1/php-full-stack-developer) <br>
- [README](artifact/README.md) <br>
- [Governance Kernel](artifact/INFO_GOVERNANCE.md) <br>
- [Runtime Integration](artifact/INFO_RUNTIME.md) <br>
- [Project Discovery Checklist](artifact/INFO_DISCOVERY.md) <br>
- [Templates](artifact/INFO_TEMPLATES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with checklists, templates, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pre-flight summaries, ADR-lite decisions, PR descriptions, rollout and rollback notes, and test instructions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
