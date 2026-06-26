## Description: <br>
PingCode API integration for the PingCode research and development management platform, supporting work item queries, weekly reports, project progress management, team collaboration, and data analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaohenanhai](https://clawhub.ai/user/zhaohenanhai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering managers, and project teams use this skill to automate PingCode project workflows, inspect work items and team data, manage comments, sprints, and workloads, and generate weekly reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports apparent exposed PingCode client credentials. <br>
Mitigation: Rotate or remove exposed credentials before use and provide workspace-specific least-privilege PingCode app credentials. <br>
Risk: The skill can delete PingCode work items, comments, and workload records without an extra confirmation safeguard. <br>
Mitigation: Grant delete permissions only in workspaces where the agent is explicitly allowed to modify or remove PingCode data. <br>
Risk: The skill can read and modify project, member, sprint, comment, and workload data through PingCode APIs. <br>
Mitigation: Use it only in authorized workspaces and scope PingCode app permissions to the minimum data and actions required. <br>


## Reference(s): <br>
- [PingCode Open API Documentation](https://open.pingcode.com/) <br>
- [PingCode API Reference](references/api_docs.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaohenanhai/pingcode-skills-zhaohenanhai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Command-line output, JSON responses, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PingCode client credentials through PINGCODE_CLIENT_ID and PINGCODE_CLIENT_SECRET.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
