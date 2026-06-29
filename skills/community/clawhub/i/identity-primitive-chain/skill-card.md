## Description: <br>
Identity Primitive Chain is a prompt-only meta-skill that assesses task complexity, applies adaptive identity layering for simple tasks, and decomposes complex tasks into primitive execution chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to route work through task-complexity assessment, identity layering, primitive execution, chain orchestration, transparency control, and result delivery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary notes transparency ambiguity because the skill can influence how an agent decomposes and routes tasks while hiding execution details by default. <br>
Mitigation: Ask the agent to show concise execution summaries when using the skill, especially for complex or consequential tasks. <br>
Risk: The security guidance cautions against relying on this meta-skill for sensitive compliance, security, or high-impact decisions without review. <br>
Mitigation: Use it with human review for sensitive decisions and verify the applied steps before acting on the result. <br>


## Reference(s): <br>
- [Identity Primitive Chain on ClawHub](https://clawhub.ai/wangjiaocheng/identity-primitive-chain) <br>
- [Identity Primitive Chain Catalog](references/identity-primitive-chain-catalog.md) <br>
- [Identity Primitive Chain Requirements](references/identity-primitive-chain-requirements.md) <br>
- [Identity Primitive Chain Exemplars](references/exemplars.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown or plain text with optional structured execution summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only meta-skill; no tool, MCP, credential, or shell-command requirements were detected in the release evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
