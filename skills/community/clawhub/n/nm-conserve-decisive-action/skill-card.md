## Description: <br>
Guides agents on when to ask clarifying questions versus proceed autonomously, reducing unnecessary questions when intent is clear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when clarification is necessary and when to proceed with clear, reversible work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages more autonomous action for clear, reversible tasks, which could lead to proceeding when a task is actually destructive, production-sensitive, security-critical, or ambiguous. <br>
Mitigation: Require explicit confirmation for destructive, production, security-critical, or ambiguous work, and prefer previews or dry runs before taking action. <br>


## Reference(s): <br>
- [Conserve Plugin Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance with decision matrices, checklists, and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution or external service calls; effectiveness depends on the agent applying the guidance to the current task context.] <br>

## Skill Version(s): <br>
1.9.13 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
