## Description: <br>
Use when the user wants to practice LeetCode problems, submit solutions, or set up LeetCode integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SPerekrestova](https://clawhub.ai/user/SPerekrestova) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, interview candidates, and learners use this skill to connect a pinned LeetCode MCP server, practice problems with progressive hints, set up coding workspaces, submit solutions, and optionally authenticate for account-specific LeetCode actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the MCP server through npx downloads and executes third-party npm code. <br>
Mitigation: Ask for user consent before installation, use the pinned @sperekrestova/interactive-leetcode-mcp@3.1.1 package version, and review changelogs before updating. <br>
Risk: Saved LeetCode session cookies can authorize account-specific actions. <br>
Mitigation: Authenticate only when needed and with user consent, store credentials at ~/.leetcode-mcp/credentials.json with owner-only permissions, and delete the file when access is no longer needed. <br>
Risk: Full community solutions can bypass the intended learning flow. <br>
Mitigation: Use progressive hint levels before showing complete solutions, and fetch full solutions only at Level 4 or after an explicit user request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SPerekrestova/interactive-leetcode) <br>
- [Linked GitHub repository](https://github.com/SPerekrestova/interactive-leetcode-mcp) <br>
- [npm package](https://www.npmjs.com/package/@sperekrestova/interactive-leetcode-mcp) <br>
- [Linked GitHub releases](https://github.com/SPerekrestova/interactive-leetcode-mcp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user consent before installing the MCP server or saving LeetCode credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
