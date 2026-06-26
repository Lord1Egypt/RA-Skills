## Description: <br>
Clarifies vague Chinese user requests, rewrites formal or technical text into casual language, and formats multi-agent task handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to turn ambiguous Chinese requests into actionable prompts, casual rewrites, or structured delegation notes before another agent executes work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation on vague or ambiguous phrasing may trigger clarification behavior when the user expected direct execution. <br>
Mitigation: Review whether clarification is useful for the current task and ask the user for missing goals, scope, resources, timing, and constraints before handing work to another agent. <br>
Risk: The skill's casual Chinese rewriting style may be unsuitable for formal documents or precise multi-agent handoffs. <br>
Mitigation: Preserve the original meaning first, reduce playful style in formal contexts, and confirm translated or delegated outputs before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/lobster-translator) <br>
- [Template library](templates/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON-shaped fields and handoff templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No tool execution, installation steps, binaries, or credential access are described by the release evidence.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
