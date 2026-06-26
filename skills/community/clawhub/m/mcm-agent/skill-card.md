## Description: <br>
MCM Agent helps users save and recall AI memories across devices through a cloud memory account, syncing only when the user explicitly asks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoxuan0820-ctrl](https://clawhub.ai/user/xiaoxuan0820-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage selected AI memory across devices, including personality notes, preferences, chat history, and long-term memory. The skill requires an API key and user consent before syncing to the cloud service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill syncs selected AI memory to a third-party cloud service using a user-provided API key. <br>
Mitigation: Review the provider, retention and deletion controls before use, and only provide an API key for accounts approved for this type of memory storage. <br>
Risk: Synced memories may include sensitive chat details if users choose to save them. <br>
Mitigation: Avoid syncing secrets or highly sensitive information, and require explicit user consent before saving or retrieving cloud memories. <br>
Risk: Memories saved on other devices could affect future agent behavior when recalled. <br>
Mitigation: Prompt the user before applying cross-device memories and keep saved content categorized by personality, preferences, chat history, and long-term memory. <br>


## Reference(s): <br>
- [MCM Agent ClawHub release](https://clawhub.ai/xiaoxuan0820-ctrl/mcm-agent) <br>
- [MCM Agent service homepage](https://clawsafe.vip) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with setup steps and memory handling instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided API key and explicit user consent before cloud sync.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
