## Description:

金石知识库管理技能。监控钉钉多维表格中的项目管理事项状态，当事项状态为已完成时自动归档并生成知识文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxs13278](https://clawhub.ai/user/maxs13278)

### License/Terms of Use:

MIT-0

## Use Case:

Project teams use this skill to monitor DingTalk project-management table records and archive completed issues, requirements, tasks, and incidents as knowledge-base Markdown documents. It is intended for the Jinshi/Jingu Trust DingTalk workspace configured in the artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads project-management records from a DingTalk table and can archive business information into local Markdown files.

Mitigation: Install only in the intended DingTalk/Jinshi environment, confirm that the connected table may be archived locally, and apply explicit permissions and retention controls before enabling automation.

Risk: Security evidence reports weak scoping and filename controls for local file generation.

Mitigation: Narrow triggers and validate item types, record IDs, and resolved output paths so generated files remain under the intended docs directory.

Risk: The release depends on the mcporter command and a DingTalk MCP endpoint.

Mitigation: Confirm mcporter is trusted and configure DINGTALK_MCP_URL only for the approved MCP server before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxs13278/skills/jinshi-knowledge-base)
- [SKILL.md](artifact/SKILL.md)
- [Generated archive state](artifact/archived-items.json)
- [Sample generated knowledge documents](artifact/docs/)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files plus command-line status output and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, mcporter, and DINGTALK_MCP_URL; generated documents are saved under the skill docs directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
