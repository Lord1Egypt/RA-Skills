## Description: <br>
Long-term memory plugin for OpenClaw: automatic recall, storage, and agent tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humanlike2026](https://clawhub.ai/user/humanlike2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this plugin to give agents long-term memory across sessions through automatic recall, automatic storage, and explicit memory search and store tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation content may be sent to plugin.human-like.me for long-term storage and retrieval. <br>
Mitigation: Install only when remote memory storage is acceptable, avoid storing secrets or regulated personal data, and start with addEnabled=false or recallEnabled=false for cautious use. <br>
Risk: Memories can be associated with the wrong person or agent if identifiers are reused. <br>
Mitigation: Configure a distinct userId for each real user and align agentId and scenario only when memory sharing is intentional. <br>
Risk: Platform metadata can expose platform-specific user identifiers when enabled. <br>
Mitigation: Keep stripPlatformMetadata=true unless cross-platform identity continuity is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/humanlike2026/humanlike-memory-plugin) <br>
- [Human-Like Memory service](https://plugin.human-like.me) <br>
- [npm package](https://www.npmjs.com/package/@humanlikememory/human-like-mem) <br>
- [Source repository](https://gitlab.ttyuyin.com/personalization_group/human-like-mem-openclaw-plugin) <br>
- [OpenClaw plugin schema](https://openclaw.io/schemas/plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Text and Markdown with OpenClaw configuration commands and agent tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API key and sends conversation content to a remote memory service when storage or recall is enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, package.json, openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
