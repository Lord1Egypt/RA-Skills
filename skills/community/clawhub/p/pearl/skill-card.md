## Description: <br>
Pearl lets agents connect a user's Pearl wallet, check balances and transactions, and route paid skill calls while preserving user approval and spending controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misteeka](https://clawhub.ai/user/misteeka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Pearl to set up wallet credentials for paid ClawHub skills, inspect wallet balance and transaction history, and let Pearl-powered skills request charge approval through user-controlled limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Pearl credentials connect this machine to a user's wallet. <br>
Mitigation: Run setup only for users who intend to use Pearl, keep ~/.pearl/config.json user-only, and remove or revoke the credentials when the machine should no longer be connected. <br>
Risk: Paid skill providers receive a limited skill token and may initiate charge approval flows. <br>
Mitigation: Use Pearl-powered skills only from trusted providers and review Pearl dashboard approvals and spending limits before accepting charges. <br>
Risk: Calling a paid skill URL shares the limited skill token with that provider. <br>
Mitigation: Use HTTPS domain URLs from trusted providers; the artifact rejects non-HTTPS URLs, IP addresses, localhost, and redirects. <br>


## Reference(s): <br>
- [Pearl ClawHub listing](https://clawhub.ai/misteeka/pearl) <br>
- [Pearl homepage](https://pearlcash.ai) <br>
- [Publisher profile](https://clawhub.ai/user/misteeka) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Plain text CLI output, local JSON configuration, and returned paid-skill response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; setup writes Pearl credentials and pending-charge state under ~/.pearl.] <br>

## Skill Version(s): <br>
0.0.14 (source: server release metadata and artifact _meta.json; package.json lists client package 0.0.15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
