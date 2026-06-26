## Description: <br>
Creem payment store assistant that queries subscriptions, customers, transactions, products, runs heartbeat checks, and manages a payment store through a local Laravel HTTP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romansh](https://clawhub.ai/user/romansh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw to a local Laravel Creem Agent service for payment store status, subscriptions, customers, transactions, products, monitoring checks, checkout creation, subscription cancellation, and store switching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route broad prompts into sensitive store reads and store-changing actions without a clear confirmation boundary. <br>
Mitigation: Review before production use, restrict who can send OpenClaw commands, and add service-side authentication, audit logging, and confirmation checks for cancellation, checkout creation, store switching, and monitoring actions. <br>
Risk: The skill depends on trusting a local Laravel Creem Agent endpoint for payment-store data and actions. <br>
Mitigation: Use only with a trusted local endpoint and verify that the Laravel app is running and reachable before relying on responses. <br>


## Reference(s): <br>
- [Laravel Creem Agent homepage](https://github.com/nicepkg/laravel-creem-agent) <br>
- [OpenClaw Telegram channel documentation](https://docs.openclaw.ai/channels/telegram) <br>
- [ClawHub skill page](https://clawhub.ai/romansh/openclaw-laravel-creem-agent-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and JSON examples; runtime responses are relayed as text from the local endpoint.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a reachable local Laravel endpoint at http://127.0.0.1:8000/creem-agent/chat.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
