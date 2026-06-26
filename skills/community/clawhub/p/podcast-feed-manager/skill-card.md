## Description: <br>
Manage personal podcast feeds through the fixed user-scoped huisheng.fm API from an installed skill package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quentinzhang](https://clawhub.ai/user/quentinzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect and manage their own huisheng.fm podcast feeds and episodes through a user-scoped API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent could expose the user's HUISHENG_API_TOKEN if credentials are pasted into chat or printed in output. <br>
Mitigation: Provide HUISHENG_API_TOKEN through a trusted environment and avoid showing the full token in user-facing output. <br>
Risk: Create, update, and delete commands can modify user-owned podcast feeds and episodes. <br>
Mitigation: Review requested API actions and JSON payloads before authorizing changes. <br>


## Reference(s): <br>
- [huisheng.fm API Skill Reference](references/api.md) <br>
- [Podcast Feed Manager on ClawHub](https://clawhub.ai/quentinzhang/podcast-feed-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and HUISHENG_API_TOKEN for API requests; create, update, and delete operations act on user-scoped feeds and episodes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
