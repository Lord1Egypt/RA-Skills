## Description: <br>
Your card stays on your PC with no SaaS, login, or external account, and credentials inject directly while staying out of the AI's context window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tpemist](https://clawhub.ai/user/tpemist) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent fill billing details and request constrained card injection during online checkout while applying local spend policy and guardrail checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can reach real-money checkout with automatic card injection and human approval disabled by default. <br>
Mitigation: Set POP_REQUIRE_HUMAN_APPROVAL=true, consider POP_AUTO_INJECT=false, and configure tight per-transaction, daily, and vendor/category limits before use. <br>
Risk: A checkout page or merchant flow could still mislead the agent about the merchant, cart, amount, or final order action. <br>
Mitigation: Manually verify the merchant, cart contents, amount, and final submit button before any purchase is submitted. <br>
Risk: Optional LLM guardrails or webhook notifications can send transaction-related data to the user's chosen API provider or endpoint. <br>
Mitigation: Use the default keyword guardrail for local-only checks unless external processing is intentional, and configure only trusted webhook endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tpemist/pop-pay-python) <br>
- [Publisher profile](https://clawhub.ai/user/tpemist) <br>
- [Project homepage](https://github.com/TPEmist/Point-One-Percent) <br>
- [PyPI package](https://pypi.org/project/pop-pay/) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell snippets, JSON configuration, and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing tool responses include approval or rejection status and reasons; approved checkout fields are injected locally rather than returned to the agent.] <br>

## Skill Version(s): <br>
0.6.23 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
