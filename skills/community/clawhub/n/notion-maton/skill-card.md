## Description: <br>
Access and manage Notion workspaces through Maton-managed OAuth to search, query databases and data sources, manage pages and blocks, and list users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otman-ai](https://clawhub.ai/user/otman-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to prepare authenticated Notion API requests for workspace search, data source and database work, page and block management, user lookup, and Maton connection administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent read, create, update, archive, or delete Notion workspace content through a third-party OAuth gateway. <br>
Mitigation: Use a least-privileged or test Notion workspace first and require explicit confirmation before write, archive, delete, or connection-management requests. <br>
Risk: MATON_API_KEY authorizes the gateway and could expose workspace access if shared or logged. <br>
Mitigation: Keep MATON_API_KEY private, avoid placing it in shared transcripts or logs, and rotate it if exposure is suspected. <br>
Risk: Notion OAuth access is brokered by Maton rather than a direct Notion integration. <br>
Mitigation: Install only if you trust Maton with the connected Notion workspace and are comfortable with the gateway proxying Notion API requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/otman-ai/notion-maton) <br>
- [Maton account settings](https://maton.ai/settings) <br>
- [Maton connection management](https://ctrl.maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and Notion-Version headers; write, archive, delete, and connection-management requests should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
