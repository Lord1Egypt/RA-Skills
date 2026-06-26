## Description: <br>
Pay for APIs, tools, and services from your agent's Kash wallet, with autonomous spending below the configured threshold and explicit user confirmation required above it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DevFaraaz](https://clawhub.ai/user/DevFaraaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an OpenClaw agent pay for metered APIs, tools, searches, data purchases, or other paid services from a Kash wallet while enforcing local and server-side budget controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to spend from a Kash wallet, including autonomous spends below the configured confirmation threshold. <br>
Mitigation: Use a dedicated low-budget Kash agent and configure KASH_BUDGET plus KASH_SPEND_CONFIRMATION_THRESHOLD according to risk tolerance. <br>
Risk: The KASH_KEY credential could authorize wallet spending if exposed. <br>
Mitigation: Keep KASH_KEY out of chat and logs, and provide it only through the skill environment. <br>
Risk: Changing KASH_API_URL could redirect payment requests away from the intended service during development. <br>
Mitigation: Leave KASH_API_URL unset except for local development; the artifact documents an allowlist for api.kash.dev, localhost, and 127.0.0.1. <br>


## Reference(s): <br>
- [Kash homepage](https://kash.dev) <br>
- [ClawHub skill page](https://clawhub.ai/DevFaraaz/kash) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration guidance] <br>
**Output Format:** [String tool responses and markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KASH_KEY and KASH_AGENT_ID; optional local budget and spend-confirmation threshold settings control agent spending behavior.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
