## Description: <br>
Routes contract review requests to the OpenClaw Contract Review Plugin through a single contract_review tool entry point. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renzhiping](https://clawhub.ai/user/renzhiping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to submit contract review requests, check task status, continue or cancel reviews, and retrieve results through the OpenClaw Contract Review Plugin. The skill constrains the agent to collect required review context before invoking the plugin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contract files may contain sensitive business or legal information and are processed by the underlying plugin. <br>
Mitigation: Install only after confirming trust in the OpenClaw Contract Review Plugin and its data-handling policy. <br>
Risk: A complete review submission can trigger a browser login flow and then continue automatically after user confirmation. <br>
Mitigation: Use the skill only for intentional review tasks, and cancel or log out if the pending review should not proceed. <br>
Risk: Incomplete submissions could otherwise start authentication or review before the user has supplied all required context. <br>
Mitigation: The artifact requires contract file, review position, review mode, and review requirements before any review tool call. <br>


## Reference(s): <br>
- [OpenClaw Contract Review Skill Page](https://clawhub.ai/renzhiping/openclaw-contract-review) <br>
- [OpenClaw Contract Review Plugin Skill Design](https://your-domain.example/docs/openclaw-contract-review-plugin-skill-design) <br>
- [Intent Routing Reference](artifact/references/intent-routing.md) <br>
- [Authentication Gate Reference](artifact/references/auth-gate.md) <br>
- [Execution Rules Reference](artifact/references/execution-rules.md) <br>
- [Interaction Examples](artifact/references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text responses with plugin tool invocations when a request passes the required gates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return login guidance, task status, follow-up prompts, or contract review result guidance through the plugin flow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
