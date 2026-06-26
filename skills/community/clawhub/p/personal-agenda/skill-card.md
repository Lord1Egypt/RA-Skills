## Description: <br>
个人日程秘书 helps an agent record, update, archive, and review personal tasks across local task files, an index, a log, and a browser-friendly dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reckonlee](https://clawhub.ai/user/reckonlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals use this skill when they want an agent to maintain a local personal agenda: ingesting inbox items, creating structured task files, marking tasks done or cancelled, adding notes, refreshing dashboard data, and archiving older completed work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to write and reorganize local task-management files. <br>
Mitigation: Use explicit task-focused prompts and review proposed file changes before allowing large dashboard, archive, or task-directory updates. <br>
Risk: The skill has a broad trigger for processing inbox and agenda updates. <br>
Mitigation: Keep the intended inbox and workspace scope clear when invoking it so unrelated files are not treated as task inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reckonlee/personal-agenda) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/reckonlee) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown task files, YAML frontmatter, JSON dashboard data, JavaScript archive data, HTML dashboard updates, and concise status summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates local task-management files including tasks/, index.md, log.md, and views/dashboard.html.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
