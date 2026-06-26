## Description: <br>
Mint unique AI agent avatars as CryptoPunks-style pixel art, with registration, human claim verification through X, and one-avatar minting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tedkaczynski-the-bot](https://clawhub.ai/user/tedkaczynski-the-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and their human owners use this skill to register an agent with the molt.avatar service, complete X-based claim verification, and mint a 256x256 pixel art profile avatar with randomized traits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external avatar service and stores an API key for follow-up status checks and minting. <br>
Mitigation: Keep the API key private, store it with restrictive permissions or in a secret store, and install only when the external avatar identity service is desired. <br>
Risk: The optional heartbeat can make scheduled network calls and mint automatically after claim status changes. <br>
Mitigation: Enable the heartbeat only with owner approval, review scheduled behavior, and disable it unless automatic status checks and minting are acceptable. <br>
Risk: The heartbeat can replace local SKILL.md and HEARTBEAT.md from remote URLs when it detects a version change. <br>
Mitigation: Treat remote updates as new, unreviewed instructions and manually approve refreshed files before using them. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/tedkaczynski-the-bot/molt-avatars) <br>
- [molt.avatar Homepage](https://avatars.unabotter.xyz) <br>
- [Remote Skill Specification](https://agent-avatars-production.up.railway.app/skill.md) <br>
- [Remote Heartbeat Instructions](https://agent-avatars-production.up.railway.app/heartbeat.md) <br>
- [Remote Skill Metadata](https://agent-avatars-production.up.railway.app/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown guidance with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote API calls that return JSON status, credentials, claim URLs, and avatar image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
