## Description: <br>
记忆索引管理器维护长期项目记忆索引，按明确的回忆触发词读取历史上下文，并在后台整理索引与整合文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxc159620352](https://clawhub.ai/user/zxc159620352) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to recover project context from long-running conversations and keep memory topics indexed over time. It supports explicit recall, daily memory archival, and topic consolidation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic memory maintenance can archive and reorganize conversation memory without clear opt-in or disable controls. <br>
Mitigation: Confirm the daily flush and index update behavior before installation, and verify that indexed or archived memory entries can be disabled or deleted. <br>
Risk: Scheduled daily flush behavior may create or rely on local automation that affects stored memory outside explicit recall requests. <br>
Mitigation: Review any scheduled job setup before use, including the referenced daily flush script and launch agent configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxc159620352/memory-index-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown instructions with file-path conventions, workflow steps, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory index and consolidation files when used in an OpenClaw memory workflow.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
