## Description: <br>
Manages connected social media accounts through PostSyncer using REST and/or MCP for scheduling, posting, media management, comments, labels, campaigns, analytics, and platform-specific video cover workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdulmejidshemsuawel](https://clawhub.ai/user/abdulmejidshemsuawel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage PostSyncer-connected social accounts, including scheduling or drafting posts, uploading media, replying to comments, organizing campaign assets, and checking analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive PostSyncer API token with access to connected social accounts. <br>
Mitigation: Install only when PostSyncer is trusted, store POSTSYNCER_API_TOKEN securely, and use the narrowest token abilities needed. <br>
Risk: The skill can post externally or publish content across social platforms. <br>
Mitigation: Review posts before publishing and prefer drafts for new automations or uncertain content. <br>
Risk: The skill can delete posts, media, folders, comments, labels, and connected accounts. <br>
Mitigation: Require explicit confirmation before destructive operations and state the affected resource before execution. <br>
Risk: The skill includes public X/Twitter analysis and analytics workflows that may affect how public content is interpreted. <br>
Mitigation: Treat analysis outputs as decision support and review conclusions before using them for campaign, moderation, or customer-facing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abdulmejidshemsuawel/postsyncer) <br>
- [PostSyncer OpenClaw and MCP](https://postsyncer.com/openclaw) <br>
- [PostSyncer API documentation](https://docs.postsyncer.com/api-reference/introduction) <br>
- [PostSyncer API authentication](https://docs.postsyncer.com/essentials/authentication) <br>
- [PostSyncer dashboard](https://app.postsyncer.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses POSTSYNCER_API_TOKEN and may produce PostSyncer REST or MCP request guidance for social media operations.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
