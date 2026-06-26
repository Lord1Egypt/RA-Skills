## Description: <br>
Read and query Monday.com boards, items, workspaces, and users directly via the Monday.com GraphQL API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeninja23](https://clawhub.ai/user/codeninja23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect Monday.com project data, including account details, boards, board structure, items, workspaces, and users through authenticated GraphQL queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Monday API token can expose board contents, account details, and user emails available to that token. <br>
Mitigation: Use a least-privileged MONDAY_API_TOKEN and avoid broad listings in sensitive workspaces unless the results are appropriate to share in the agent session. <br>
Risk: Command output may include sensitive project or user data from Monday.com. <br>
Mitigation: Review command scope, board IDs, and limits before execution, and avoid pasting or retaining output that should not be visible in the agent session. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/codeninja23/native-monday) <br>
- [Monday.com GraphQL API endpoint](https://api.monday.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Terminal text and JSON emitted by Python CLI commands, with setup guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MONDAY_API_TOKEN and python3; the script pins the Monday API version to 2024-04.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
