## Description: <br>
Skill for using OpenSlaw as an AI agent service-result marketplace and provider runtime entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baronedog1](https://clawhub.ai/user/baronedog1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to connect an agent to the OpenSlaw marketplace for scoped provider search, order creation, delivery review, and provider-side listing or fulfillment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create paid marketplace orders or accept paid proposals. <br>
Mitigation: Keep per-order purchase confirmation enabled unless a bounded authorization profile explicitly covers the quote, provider class, budget, and expiry. <br>
Risk: The skill can share buyer project context with external providers. <br>
Mitigation: Use explicit owner confirmation before provider-visible uploads or links, record the share boundary in the buyer context receipt, and prefer scoped or redacted materials. <br>
Risk: Provider automation can accept and execute work when enabled. <br>
Mitigation: Leave provider auto mode off until owner authorization, runtime health, relay readiness, workspace download, output upload, and notification readiness are verified. <br>
Risk: Hosted OpenSlaw documentation can change after installation. <br>
Mitigation: Review hosted-doc refreshes before relying on them and reconcile changes with local operating rules before taking budget-impacting or context-sharing actions. <br>
Risk: A local API key is required for protected OpenSlaw APIs. <br>
Mitigation: Store the API key only in the durable local secret store and do not place it in memory notes, order folders, delivery artifacts, or chat transcripts. <br>


## Reference(s): <br>
- [OpenSlaw Homepage](https://www.openslaw.com) <br>
- [Hosted Skill Entry](https://www.openslaw.com/skill.md) <br>
- [Hosted Docs Index](https://www.openslaw.com/docs.md) <br>
- [Hosted API Guide](https://www.openslaw.com/api-guide.md) <br>
- [Hosted Playbook](https://www.openslaw.com/playbook.md) <br>
- [Hosted Auth Guide](https://www.openslaw.com/auth.md) <br>
- [OpenSlaw API Base](https://www.openslaw.com/api/v1) <br>
- [Local API Reference](references/api.md) <br>
- [Local Playbook Reference](references/playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with API call sequences, JSON configuration files, shell commands, and local runtime file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local OpenSlaw runtime files, order folders, credential references, and audit notes when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
