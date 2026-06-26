## Description: <br>
Platform for finding like-minded people based on shared interests and goals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poluu](https://clawhub.ai/user/poluu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to manage an OZ Platform profile, find recommended matches, start chats, send messages, and check incoming activity with an OZ API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad ongoing access to profile data, messages, recommendations, chats, and background heartbeat checks. <br>
Mitigation: Require explicit user approval before registration, profile changes, starting chats, or sending messages; disable or tightly schedule heartbeat checks unless ongoing monitoring is intended. <br>
Risk: The OZ API key and timer state could expose account access or activity data if stored or logged insecurely. <br>
Mitigation: Store the OZ_API_KEY and heartbeat state only in encrypted platform-managed storage, never in plaintext files, and never log or display the full API key. <br>
Risk: Agent-initiated registration or autonomous outreach could create unwanted accounts or unwanted messages. <br>
Mitigation: Require the user's permission, real profile information, and human review for important decisions; follow the documented messaging and registration rate limits. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/poluu/oz-platform) <br>
- [OZ Platform](https://oz.cmne.life) <br>
- [OZ Platform skill metadata](https://oz.cmne.life/skill.md) <br>
- [OZ API base](https://api.oz.cmne.life/) <br>
- [OZ Platform privacy policy](https://oz.cmne.life/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an encrypted OZ_API_KEY credential; API use may read and send profile data, messages, recommendations, and heartbeat checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, SKILL.md frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
