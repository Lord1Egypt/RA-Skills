## Description: <br>
金石知识库管理技能。监控钉钉多维表格中的项目管理事项状态，当事项状态为已完成时自动归档并生成知识文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxs13278](https://clawhub.ai/user/maxs13278) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Project teams using DingTalk use this skill to monitor completed project-management items, archive them, and generate knowledge-base documents such as issue reports, requirement notes, task summaries, and incident reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read business records from a DingTalk MCP endpoint and persist generated documents locally. <br>
Mitigation: Install only with a trusted DingTalk MCP endpoint, use a least-privileged account, and review generated documents before sharing or relying on them. <br>
Risk: Broad triggers or scheduled execution could archive records unexpectedly. <br>
Mitigation: Narrow invocation triggers, require explicit invocation where appropriate, and confirm how scheduled execution is enabled or disabled. <br>
Risk: Record-derived filenames and document content may contain sensitive project information. <br>
Mitigation: Validate output filenames and restrict access to the generated documents directory when using sensitive project records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maxs13278/jinshi-knowledge-base) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documents with local JSON archive state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, mcporter, and DINGTALK_MCP_URL for DingTalk MCP access.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
