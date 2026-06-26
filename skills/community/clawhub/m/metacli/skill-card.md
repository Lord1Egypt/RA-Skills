## Description: <br>
Meta Marketing CLI for authentication lifecycle, Graph API requests, campaign/ad/adset writes, insights reporting, and Instagram publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bilalbayram](https://clawhub.ai/user/bilalbayram) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run Meta ads and Instagram workflows from terminal commands, including authentication setup, account and campaign operations, reporting, and publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meta Ads or Instagram write commands can change campaigns, budgets, publishing state, or account data. <br>
Mitigation: Require explicit approval before campaign, budget, delete, or publishing commands; prefer dry runs and schema sync before writes. <br>
Risk: OAuth app secrets, access tokens, and redirect tunnels are sensitive and can expose account access if mishandled. <br>
Mitigation: Use a dedicated low-privilege Meta app and profile, keep OAuth tunnels short-lived, protect secrets and tokens, and redact them from command output. <br>
Risk: Installing the upstream CLI at a floating latest version can introduce unreviewed behavior changes. <br>
Mitigation: Pin or review the upstream CLI version before installation in managed environments. <br>


## Reference(s): <br>
- [ClawHub metacli page](https://clawhub.ai/bilalbayram/metacli) <br>
- [metacli project homepage](https://github.com/bilalbayram/metacli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should preserve fail-closed behavior, use machine-readable output where appropriate, and redact secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
