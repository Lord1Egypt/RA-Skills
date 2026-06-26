## Description: <br>
Manage macOS Reminders.app from Docker via a local HTTP bridge for creating, listing, updating, completing, and deleting reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MasteRyuuuu](https://clawhub.ai/user/MasteRyuuuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users run this skill when an AI agent in Docker needs to manage native macOS Reminders through a host-side listener. It supports reminder creation, listing, updates, completion toggles, deletion, list discovery, and listener health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local HTTP bridge can read and change macOS Reminders. <br>
Mitigation: Install only when this capability is intended, run the listener on a trusted Mac, and confirm the agent should have access before enabling it. <br>
Risk: Default access controls may allow clients on broad local or Docker networks to call the bridge without a shared secret. <br>
Mitigation: Set BRIDGE_SECRET, restrict BRIDGE_ALLOWED_IPS to exact trusted clients, and keep port 5000 off public networks. <br>
Risk: Fuzzy delete, update, complete, or all-list operations may affect unintended reminders. <br>
Mitigation: Require explicit user confirmation before fuzzy matching, destructive changes, completion toggles, or broad listing operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MasteRyuuuu/mac-reminder-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/MasteRyuuuu) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Listener implementation](artifact/listener.py) <br>
- [macOS platform reference](https://www.apple.com/macos/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples, JSON request and response shapes, and concise user-facing confirmations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a host-side macOS listener on port 5000, curl in the agent environment, and optional X-Bridge-Secret authentication.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
