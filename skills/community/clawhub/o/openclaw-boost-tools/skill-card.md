## Description: <br>
Provides OpenClaw productivity tools for cost tracking, memory retrieval, context compaction, permission checks, tool tracking, task coordination, slash-command status, token budgeting, and feature flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bw520333](https://clawhub.ai/user/bw520333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local cost, token, memory, compaction, and tool status; retrieve or inject relevant local memories; review permission rules; and manage feature flags for productivity workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toolkit can persist or inject local memory and log contents, which may expose sensitive project or user information. <br>
Mitigation: Use it only on trusted machines and review memory files before using memory injection, especially in shared workspaces or projects containing secrets. <br>
Risk: Permission checks include broad allow rules for Python, Node, and curl patterns and do not automatically block all high-impact commands. <br>
Mitigation: Do not connect the permission manager to automatic approvals until the allow rules are narrowed and high-impact commands require explicit review. <br>
Risk: Dream consolidation can modify long-term memory files and remove processed log files when run outside dry-run mode. <br>
Mitigation: Back up ~/.openclaw before enabling consolidation and test with safe status or dry-run workflows before running destructive modes. <br>


## Reference(s): <br>
- [OpenClaw Boost Tools on ClawHub](https://clawhub.ai/bw520333/openclaw-boost-tools) <br>
- [Publisher profile: bw520333](https://clawhub.ai/user/bw520333) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact version metadata](artifact/version.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with bash and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write local OpenClaw memory, logs, feature flags, and permission configuration under ~/.openclaw/bw-openclaw-boost.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact/version.json reports current 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
