## Description: <br>
LinkedIn automation skill for searching people and companies, fetching profiles, sending messages and InMails, managing connections, creating posts, reacting, commenting, and using Sales Navigator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vprudnikoff](https://clawhub.ai/user/vprudnikoff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate a connected LinkedIn account through the Linked API CLI for prospecting, profile and company research, messaging, content posting, engagement, account management, Sales Navigator, and custom workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad authority over a real LinkedIn account, including messages, InMails, connection changes, posts, comments, reactions, resets, and custom workflows. <br>
Mitigation: Require explicit user approval before any account-changing action and confirm the target account, recipient, content, and intended effect. <br>
Risk: Linked API tokens and identification tokens can expose account access if pasted into chat, logs, or shared files. <br>
Mitigation: Handle tokens outside chat when possible, avoid logging credentials, verify how to revoke access, and reset credentials if exposure is suspected. <br>
Risk: Installing and using the third-party CLI depends on the npm package and Linked API provider. <br>
Mitigation: Verify the npm package, publisher, and provider account before installation or authentication. <br>
Risk: Automation runs through real LinkedIn operations that may queue, take minutes, hit rate limits, or affect subscriptions and account status. <br>
Mitigation: Check command success fields, monitor workflow status, respect account limits, and stop automation when account or rate-limit errors occur. <br>


## Reference(s): <br>
- [Linked API dashboard](https://app.linkedapi.io) <br>
- [Linked API workflow schema documentation](https://linkedapi.io/docs/building-workflows/) <br>
- [ClawHub skill listing](https://clawhub.ai/vprudnikoff/linkedapi-linkedin) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can perform live LinkedIn account actions, require Linked API tokens, and may take 30 seconds to several minutes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
