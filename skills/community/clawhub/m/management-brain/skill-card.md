## Description: <br>
Boss AI Agent is AI management middleware for connected workplace systems, mentor-guided decisions, AI C-suite analysis, automated management scenarios, and MCP clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonypk](https://clawhub.ai/user/tonypk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Managers and team leads use this skill to automate team check-ins, project health patrols, daily briefings, 1:1 preparation, signal scanning, knowledge capture, and emergency alerts across connected workplace tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can monitor employee communications, store employee profiles, and retain sentiment or management history. <br>
Mitigation: Inform affected employees, scope channel and project access narrowly, and review memory retention before enabling monitoring workflows. <br>
Risk: The skill can schedule recurring scans and send messages or alerts on the boss's behalf. <br>
Mitigation: Require explicit approval for schedules, message sending, alerts, and channel targets; regularly review and remove unneeded cron jobs. <br>
Risk: Optional cloud connectivity and knowledge-base writes can expand data exposure beyond local operation. <br>
Mitigation: Require explicit approval for cloud use and knowledge-base writes, and grant only the smallest necessary cloud, project, and integration permissions. <br>
Risk: Shell diagnostics can affect the host environment if granted too broadly. <br>
Mitigation: Avoid shell execution unless it is tightly controlled and separately approved for the specific diagnostic task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tonypk/management-brain) <br>
- [Publisher profile](https://clawhub.ai/user/tonypk) <br>
- [Boss AI Agent website](https://manageaibrain.com) <br>
- [MCP HTTP endpoint](https://manageaibrain.com/mcp) <br>
- [Cloud API base URL](https://api.manageaibrain.com) <br>
- [Cloud dashboard](https://app.manageaibrain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request tool-mediated messages, API calls, cron jobs, memory writes, file writes, and diagnostics when the host agent grants those tools.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
