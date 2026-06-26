## Description: <br>
Triage Issues uses a configured Gitee MCP server to fetch open repository issues, classify them, prioritize them, identify duplicates, and prepare issue updates after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oschina](https://clawhub.ai/user/oschina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and repository maintainers use this skill to organize open Gitee issues into actionable priority, type, duplicate, and information-needed groups. After reviewing the generated report, they can approve label, priority, assignment, or comment updates through the configured Gitee MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk issue updates could apply incorrect labels, priorities, assignments, or comments to repository issues. <br>
Mitigation: Review the generated triage report and the exact proposed updates before approving any bulk changes. <br>
Risk: The skill depends on a Gitee MCP server that can read and update repository issues. <br>
Mitigation: Use the skill only with a trusted Gitee MCP server configured for the intended repository. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oschina/gitee-triage-issues) <br>
- [Publisher profile](https://clawhub.ai/user/oschina) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, API Calls] <br>
**Output Format:** [Markdown triage report with optional Gitee MCP tool actions after user confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured, trusted Gitee MCP server and repository owner/name inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
