## Description: <br>
Openclaw Twitter Post Engage helps agents search X/Twitter profiles, tweets, and trends and perform OAuth-approved posting, likes, follows, and related workflows through the AISA relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to research X/Twitter content or perform approved public write and engagement actions without sharing passwords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform public Twitter/X write or engagement actions from an OAuth-authorized account. <br>
Mitigation: Confirm the final content or target before every post, like, follow, or unfollow, and require the documented confirmation flag for the action. <br>
Risk: The skill depends on AISA_API_KEY and OAuth authorization for relay-backed actions. <br>
Mitigation: Use a dedicated or easily rotated AISA key and revoke OAuth access when the skill is no longer needed. <br>
Risk: Relay-backed actions can fail or target the wrong account if the target is ambiguous. <br>
Mitigation: Ask for account or target confirmation when matches are ambiguous and report success only when the relay response indicates success. <br>


## Reference(s): <br>
- [OpenClaw Twitter OAuth](references/post_twitter.md) <br>
- [OpenClaw Twitter Engagement](references/engage_twitter.md) <br>
- [ClawHub skill listing](https://clawhub.ai/aisadocs/openclaw-twitter-post-engage) <br>
- [Publisher profile](https://clawhub.ai/user/aisadocs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON relay responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and explicit confirmation flags for public write and engagement actions.] <br>

## Skill Version(s): <br>
2.0.4 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
