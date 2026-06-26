## Description: <br>
Review what is due, capture new tasks, build projects from notes, and organize OmniFocus from natural language in OpenClaw on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doannminh](https://clawhub.ai/user/doannminh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users on macOS use this skill to read, triage, create, edit, and organize OmniFocus tasks, projects, folders, tags, and perspectives through the upstream OmniFocus MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change local OmniFocus data through macOS automation. <br>
Mitigation: Install it only when that access is intended, start with read-only queries, and review proposed edits before applying them. <br>
Risk: Bulk edits or deletions can affect many OmniFocus items. <br>
Mitigation: Confirm ambiguous destructive requests and review bulk changes carefully before execution. <br>
Risk: macOS automation permission lets the host process operate OmniFocus on the user's behalf. <br>
Mitigation: Grant automation permission only to trusted host processes and revoke it if the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/doannminh/omnifocus-mcp-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/doannminh) <br>
- [OmniFocus-MCP upstream homepage](https://github.com/themotionmachine/OmniFocus-MCP) <br>
- [omnifocus-mcp npm package](https://www.npmjs.com/package/omnifocus-mcp) <br>
- [OmniFocus scripting documentation](https://support.omnigroup.com/documentation/omnifocus/mac/3.12/en/print/) <br>
- [query_omnifocus reference](references/query_omnifocus.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed OmniFocus reads, writes, or setup checks for the user to review.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
