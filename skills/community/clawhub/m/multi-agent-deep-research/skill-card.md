## Description: <br>
Coordinate deep, source-verifiable research projects in OpenClaw using AgentSkills-compatible folders, local artifact tracking, and explicit evidence ledgers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZZXX-bit](https://clawhub.ai/user/ZZXX-bit) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, researchers, and research leads use this skill to run auditable deep research workflows with local source ledgers, claim tracking, handoffs, and final reports. It supports both single-agent use and explicitly requested multi-agent delegation with bounded file ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally writes research state, ledgers, handoffs, and drafts into the user's workspace. <br>
Mitigation: Use a clearly scoped project directory and review generated or modified files before relying on them. <br>
Risk: Optional multi-agent workflows can create conflicting edits if agents are not assigned clear file ownership. <br>
Mitigation: Use delegation only when requested, assign disjoint write scopes, and require handoffs that list completed work, verified facts, open issues, and next steps. <br>


## Reference(s): <br>
- [Project Layout](references/project-layout.md) <br>
- [Delegation Patterns](references/delegation-patterns.md) <br>
- [Evidence Standards](references/evidence-standards.md) <br>
- [Starter Templates](references/templates.md) <br>
- [OpenClaw Platform Notes](references/platform-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file templates and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local research ledgers, handoffs, checks, and report drafts in the user's workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
