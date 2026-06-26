## Description: <br>
Use this skill when assisting with FortressQuant's peerberry-sdk for PeerBerry investor automation, P2P lending education, and alternative-investment onboarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FortressQuant](https://clawhub.ai/user/FortressQuant) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to build and debug Python workflows for PeerBerry account access, portfolio and loan analysis, guarded purchase automation, exports, and SDK troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Guidance can lead to real-money PeerBerry purchase actions. <br>
Mitigation: Start with read-only calls, keep DRY_RUN enabled for first runs, set hard order caps, check available funds, and require clear manual confirmation before any live purchase. <br>
Risk: Credentials, TOTP seeds, access tokens, exports, or logs may expose sensitive account or financial data. <br>
Mitigation: Keep secrets and exports private, avoid logging sensitive values, use secure token storage, and redact account data before sharing outputs. <br>
Risk: PeerBerry API behavior can change and break automation or produce misleading operational assumptions. <br>
Mitigation: Validate scripts with read-only checks before live use, catch specific SDK exceptions, and review generated purchase or export logic before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FortressQuant/peerberry-sdk) <br>
- [PeerBerry website](https://peerberry.com/) <br>
- [API quick reference](references/api-quickref.md) <br>
- [P2P lending primer](references/p2p-primer.md) <br>
- [Task recipes](references/task-recipes.md) <br>
- [Docs index](https://github.com/FortressQuant/peerberry-sdk/tree/main/docs) <br>
- [Client API reference](https://github.com/FortressQuant/peerberry-sdk/blob/main/docs/api/client.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only analysis, guarded automation snippets, SDK method guidance, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
