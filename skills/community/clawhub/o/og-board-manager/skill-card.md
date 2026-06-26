## Description: <br>
Use when you need to delegate, track, or review work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jatin-31](https://clawhub.ai/user/jatin-31) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Managers and agents use this skill to create, assign, review, and update OpenGoat task-board work while keeping delegation, blockers, artifacts, and worklogs tracked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The placeholder agent ID may be used unchanged, causing task operations to run under the wrong identity. <br>
Mitigation: Replace the placeholder with the active agent ID before using task-list, task-create, or task-update calls. <br>
Risk: Tasks may be assigned outside the intended reportee scope. <br>
Mitigation: Confirm the organization context with the agent-info tool and assign only to valid direct or indirect reportees, or to yourself. <br>
Risk: Task descriptions, artifacts, blockers, or worklogs may contain secrets or sensitive information. <br>
Mitigation: Avoid placing secrets or sensitive data in task-board content and review entries before submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jatin-31/og-board-manager) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jatin-31) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown with OpenGoat tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task-board operating guidance and structured tool-call patterns; it does not require API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
