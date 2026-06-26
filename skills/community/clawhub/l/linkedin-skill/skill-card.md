## Description: <br>
LinkedIn automation skill - search people and companies, fetch profiles, send messages and InMails, manage connections, create posts, react, comment, and use Sales Navigator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vprudnikoff](https://clawhub.ai/user/vprudnikoff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, recruiting, marketing, and developer users can ask an agent to operate LinkedIn through the Linked API CLI for profile and company research, messaging, connection management, posting, engagement, and Sales Navigator workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a real LinkedIn account, including sending messages or InMails, creating posts, commenting, reacting, changing connections, switching accounts, resetting configuration, and running workflows. <br>
Mitigation: Confirm every account-changing or public action with the user before execution, and review workflow JSON before running it. <br>
Risk: The skill handles Linked API and identification tokens. <br>
Mitigation: Treat tokens as secrets and avoid exposing them in chat, command history, logs, or generated artifacts. <br>
Risk: The server security summary reports broad automation power without enough safety boundaries. <br>
Mitigation: Install only when the user intentionally wants an agent to operate LinkedIn through Linked API, and keep use limited to authorized accounts and actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vprudnikoff/linkedin-skill) <br>
- [Linked API workflow documentation](https://linkedapi.io/docs/building-workflows/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI operations return structured JSON when called with --json -q; real browser-backed actions can take 30 seconds to several minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
