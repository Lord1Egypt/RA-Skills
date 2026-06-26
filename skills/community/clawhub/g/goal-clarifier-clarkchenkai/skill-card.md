## Description: <br>
Goal Clarifier turns vague or solution-shaped requests into executable briefs by clarifying the real goal, constraints, success criteria, scope boundaries, and safe next step before design or execution begins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarkchenkai](https://clawhub.ai/user/clarkchenkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill when a request names a tool, dashboard, agent, automation, or process before the desired outcome is clear. It produces a structured brief that makes goals, constraints, success criteria, scope boundaries, ambiguities, and the next safe action explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Implicit invocation may cause the agent to ask clarifying questions during ordinary planning conversations. <br>
Mitigation: Disable implicit invocation or call the skill manually when clarification should be opt-in. <br>
Risk: For high-stakes or irreversible workflows, an unclear goal can lead to premature automation or misplaced decision ownership. <br>
Mitigation: Require explicit success criteria, identify the human-owned decision boundary, and keep execution planning separate from the clarified brief. <br>


## Reference(s): <br>
- [Aristotle Reference](references/aristotle.md) <br>
- [High-Risk Signals](references/high-risk.md) <br>
- [Question Patterns](references/patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/clarkchenkai/goal-clarifier-clarkchenkai) <br>
- [Publisher Profile](https://clawhub.ai/user/clarkchenkai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown six-part brief] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses fixed headings for goal, constraints, success criteria, scope boundary, key ambiguities, and recommended next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
