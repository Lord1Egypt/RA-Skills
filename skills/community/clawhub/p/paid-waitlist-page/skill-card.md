## Description:

Creates and deploys a hosted waitlist, landing, or preorder page with persisted signups and optional checkout through SettleMesh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[structureintelligence](https://clawhub.ai/user/structureintelligence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to create a hosted signup, waitlist, landing, preorder, or paywall page that persists submitted emails and can optionally charge for early access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unintended hosted or metered infrastructure deployment.

Mitigation: Install only for workflows that explicitly need a live SettleMesh waitlist or preorder deployment, and require confirmation before deploy, payment, or billed actions.

Risk: Credential misuse or overbroad platform access through SETTLE_API_KEY.

Mitigation: Use a least-privileged API key, keep credentials out of generated code and logs, and rotate the key if exposure is suspected.

Risk: Supply-chain drift from installing the latest settlemesh CLI.

Mitigation: Prefer a pinned, reviewed settlemesh CLI version before executing deployment commands.

## Reference(s):

- [Paid Waitlist Page on ClawHub](https://clawhub.ai/structureintelligence/skills/paid-waitlist-page)
- [structureintelligence publisher profile](https://clawhub.ai/user/structureintelligence)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and deployment JSON from SettleMesh]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a live hosted URL, managed database, and optional checkout when the generated commands are executed; requires settlemesh and SETTLE_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
