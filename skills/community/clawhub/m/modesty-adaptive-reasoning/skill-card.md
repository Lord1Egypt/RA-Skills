## Description: <br>
Automatically assesses task complexity and adjusts an agent's reasoning level before answering complex requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill as an always-on preprocessing guide to decide when a request needs fast, standard, or deeper reasoning before composing a response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently choose deeper reasoning and change response behavior for complex or ambiguous requests. <br>
Mitigation: Use it only where adaptive reasoning behavior is acceptable; avoid it for workflows that require explicit approval before session behavior changes. <br>
Risk: Visible reasoning indicators and deeper reasoning may interfere with strict output formatting or minimal-token workflows. <br>
Mitigation: Avoid this skill for strict-format automation, low-token tasks, or contexts where appended indicators would break downstream parsing. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/modestyrichards/modesty-adaptive-reasoning) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown instructions for agent response behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append a visible reasoning indicator to the final response when the skill judges a request complex.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
