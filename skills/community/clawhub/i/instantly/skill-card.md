## Description: <br>
Instantly API integration with managed OAuth for managing cold email campaigns, leads, sending accounts, email actions, and analytics through Maton. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business users use this skill to connect an agent to an Instantly account through Maton so it can inspect campaigns, manage leads and sending accounts, perform approved email actions, and retrieve analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials, including a Maton API key and potentially SMTP or IMAP passwords in account-management requests. <br>
Mitigation: Keep credentials secret, provide them through environment variables or approved secret handling, and avoid exposing them in prompts, logs, or shared outputs. <br>
Risk: Email, campaign, lead, account, and mailbox-changing operations can affect real outreach activity, sender reputation, or deliverability. <br>
Mitigation: Confirm the exact account, campaign, lead, message, and intended effect with the user before any create, update, delete, send, reply, forward, warmup, or mailbox-changing action. <br>
Risk: Using the wrong Maton connection can operate on the wrong Instantly account when multiple connections exist. <br>
Mitigation: List active connections and include the intended Maton-Connection header when more than one Instantly connection is available. <br>


## Reference(s): <br>
- [Instantly API V2 Documentation](https://developer.instantly.ai/api/v2) <br>
- [Instantly API Introduction](https://developer.instantly.ai/) <br>
- [Instantly Help Center](https://help.instantly.ai/) <br>
- [Maton](https://maton.ai) <br>
- [ClawHub Instantly Skill](https://clawhub.ai/byungkyu/instantly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline API request examples, code snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and an active Maton Instantly connection for live API operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
