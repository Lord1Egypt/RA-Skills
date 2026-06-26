## Description: <br>
Maiat Trust API helps agents register an on-chain identity, check agent and token trust signals, protect wallet transactions, and report outcomes through Maiat APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JhiNResH](https://clawhub.ai/user/JhiNResH) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to integrate Maiat trust checks, passport registration, token safety checks, outcome reporting, and optional wallet-guard workflows into agent transaction decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-linked trust, token, outcome, and threat-report data may be sent to Maiat. <br>
Mitigation: Disclose the data flow to users and require explicit approval before registration, outcome reporting, or threat reporting. <br>
Risk: Outcome and threat reports can affect reputation signals or blocking decisions. <br>
Mitigation: Submit reports only from verified user intent, keep an audit trail, and avoid automated reporting without confirmation. <br>
Risk: The optional wallet-guard package can influence transaction execution. <br>
Mitigation: Review the package and configuration before granting transaction authority, and set conservative trust thresholds for wallet actions. <br>


## Reference(s): <br>
- [Maiat App](https://app.maiat.io) <br>
- [Maiat API Base](https://app.maiat.io/api/v1) <br>
- [Maiat Skill Source](https://app.maiat.io/skill.md) <br>
- [Passport Portal](https://passport.maiat.io) <br>
- [Maiat API Docs](https://app.maiat.io/docs) <br>
- [8004scan](https://www.8004scan.io) <br>
- [Maiat Protocol](https://github.com/JhiNResH/maiat-protocol) <br>
- [Maiat Guard](https://github.com/JhiNResH/maiat-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with curl commands, JSON examples, and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API endpoints, request examples, response examples, trust score thresholds, package names, and contract addresses.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
