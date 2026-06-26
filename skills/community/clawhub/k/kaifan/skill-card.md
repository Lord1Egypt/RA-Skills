## Description: <br>
开饭 helps an agent search dining options, recommend meals, draft food orders, manage confirmation, and check delivery status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaifan](https://clawhub.ai/user/kaifan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users ask the agent for restaurant discovery, meal recommendations, group ordering, order drafts, payment confirmation support, and delivery status updates through the Kaifan service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dynamic setup with npx can execute publisher package code while handling a user binding secret. <br>
Mitigation: Install only if you trust the publisher and the kaifan-ai package; prefer an explicit account-linking flow when available. <br>
Risk: Binding phrases and fallback OpenAPI parameters are sensitive credentials. <br>
Mitigation: Treat these values as secrets, provide them only in a trusted session, avoid logging them, and rotate or revoke them if exposed. <br>
Risk: Ordering actions can lead to real payment or delivery changes if confirmation is mishandled. <br>
Mitigation: Keep orders as drafts, show the restaurant, items, total price, and warnings, and require explicit user approval before confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaifan/kaifan) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Natural language guidance with order summaries and inline shell commands when setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Order confirmation should remain draft-first and require explicit user approval before payment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
