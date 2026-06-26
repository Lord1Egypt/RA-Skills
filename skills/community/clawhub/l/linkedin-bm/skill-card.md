## Description: <br>
LinkedIn automation via browser relay or cookies for messaging, profile viewing, and network actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernhmueller](https://clawhub.ai/user/bernhmueller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent operate a logged-in LinkedIn browser session for messages, profile viewing, searches, and network actions with user confirmation for sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may expose a powerful LinkedIn session cookie if users copy or paste li_at into chat, files, or logs. <br>
Mitigation: Prefer browser relay or isolated browser login, avoid sharing li_at values, and log out of LinkedIn sessions or rotate credentials if a cookie is exposed. <br>
Risk: Agent actions in a logged-in LinkedIn session could send messages, issue connection requests, or repeat account actions without sufficient review. <br>
Mitigation: Require explicit user confirmation before messages, connection requests, or repeated account actions, and keep automation rates low. <br>


## Reference(s): <br>
- [LinkedIn](https://linkedin.com) <br>
- [ClawHub skill page](https://clawhub.ai/bernhmueller/linkedin-bm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with browser tool command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in LinkedIn session through browser relay, isolated browser login, or a securely handled session cookie.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
