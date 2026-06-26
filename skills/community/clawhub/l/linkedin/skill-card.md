## Description: <br>
LinkedIn automation via browser relay or cookies for messaging, profile viewing, and network actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biostartechnology](https://clawhub.ai/user/biostartechnology) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to operate an authenticated LinkedIn browser session for messages, profiles, search, and network actions while confirming account-changing steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an authenticated LinkedIn session and optionally references the li_at session cookie. <br>
Mitigation: Prefer browser login or relay flows, avoid copying the li_at cookie unless necessary, and keep any session credential out of chat and logs. <br>
Risk: Messages, connection requests, acceptances, and similar actions can change the user's LinkedIn account state. <br>
Mitigation: Require explicit user approval before each message, connection request, acceptance, or other account-changing action. <br>
Risk: Rapid automated LinkedIn activity may trigger rate limits, CAPTCHA, or account checks. <br>
Mitigation: Keep automation slow, follow the artifact's recommended action limits, and pause when rate limiting or CAPTCHA appears. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/biostartechnology/linkedin) <br>
- [LinkedIn](https://linkedin.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Browser tool commands, Guidance] <br>
**Output Format:** [Markdown with inline browser command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated LinkedIn session; user approval is expected before sending messages or changing network state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
