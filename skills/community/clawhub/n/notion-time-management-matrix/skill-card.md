## Description: <br>
A Notion task-management skill that uses a Python script to connect to a configured Notion database and manage Eisenhower Matrix tasks, including creation, queries, search, status updates, due-date changes, and summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiangtaoxiao](https://clawhub.ai/user/xiangtaoxiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage Notion-based task lists with Eisenhower Matrix prioritization. It helps create, search, query, update, and summarize tasks from a configured Notion database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Notion integration and can cache task data locally. <br>
Mitigation: Use a Notion key scoped to the intended database, protect ~/.config/notion files, and periodically remove the local state cache if cached task data is no longer needed. <br>
Risk: Security evidence reports that the skill returns an instruction to alter future agent or tool behavior outside the task-management purpose. <br>
Mitigation: Ignore or remove the TOOLS.md prioritization instruction before use, and review script responses before allowing them to affect agent behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiangtaoxiao/notion-time-management-matrix) <br>
- [Notion API base URL used by the skill](https://api.notion.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown or chat-ready text derived from JSON script responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Python helper returns JSON with ok, action, message, and data fields; the agent formats those results for the user's chat surface.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact metadata lists 1.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
