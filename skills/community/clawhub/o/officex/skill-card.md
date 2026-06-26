## Description: <br>
OfficeX helps agents guide consumers and developers through the OfficeX REST API for marketplace apps, billing, installations, webhooks, embedded apps, and AI chat integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mevdragon](https://clawhub.ai/user/mevdragon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, app vendors, and OfficeX consumers use this skill to call the OfficeX cloud API, build or publish marketplace apps, manage installs and wallets, implement credit billing, handle webhooks, and integrate OfficeX context with AI chat agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers billing, payouts, deletion, wallet, key-rotation, and admin workflows that can affect funds or account state. <br>
Mitigation: Require explicit human approval before executing billing, payout, deletion, wallet, key-rotation, or admin actions. <br>
Risk: The skill discusses API keys, install secrets, master keys, admin secrets, and agent-visible credential context. <br>
Mitigation: Keep raw secrets out of agent-visible context; prefer backend-held secrets or short-lived scoped tokens. <br>
Risk: The artifact includes URL-parameter patterns for install secrets that are not appropriate for production secrets. <br>
Mitigation: Avoid URL parameters for production secrets and use secure server-side session or token exchange patterns. <br>


## Reference(s): <br>
- [OfficeX ClawHub Skill Page](https://clawhub.ai/mevdragon/officex) <br>
- [OfficeX Developer Portal](https://officex.app/store/en/developer/) <br>
- [OfficeX Production REST API](https://cloud.officex.app/v1) <br>
- [OfficeX Production Chat Stream](https://chat.cloud.officex.app/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with REST endpoint examples, JSON schemas, TypeScript snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OfficeX API request patterns, credential handling guidance, billing workflows, webhook examples, iframe integration notes, and error references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
