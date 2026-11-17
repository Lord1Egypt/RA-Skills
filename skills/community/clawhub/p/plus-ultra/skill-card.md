## Description:

Run a Byzantine 2+1 plan before consequential work and a fresh, plan-blind reality check afterward.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill for bounded consequential agent work where a mistaken plan or unverified outcome would be costly, such as deployment configuration changes, data-processing repairs, or shared interface updates. It guides two read-only proposal passes, arbitration, one implementation pass, and a fresh reality check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Claude Code hook broadly intercepts agent events and can retain blocked command text in local audit logs.

Mitigation: Review hook configuration before enabling it, avoid placing secrets in commands, and prefer manual or pinned installation.

Risk: The hook is a workflow gate, not a sandbox or complete shell parser.

Mitigation: Use operating-system permissions, isolated worktrees or containers, and credential boundaries for real enforcement.

Risk: Recorded plan and reality verdicts do not prove that independent agents actually ran or that the verifier checked the right observable.

Mitigation: Review the recorded verdicts and verification evidence before treating a task as complete.

## Reference(s):

- [Plus Ultra on ClawHub](https://clawhub.ai/antreasantoniou/skills/plus-ultra)
- [Agent Orchestra](https://github.com/AntreasAntoniou/agent-orchestra)
- [Grade-A Pipeline](https://github.com/AntreasAntoniou/grade-a-pipeline)
- [Agent Collaboration Control](https://github.com/AntreasAntoniou/agent-collaboration-control)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON hook configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces candidate plans, an arbitration decision, an implementation path, and a reality-verification verdict; the optional Claude Code hook can write local session state and audit events.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
