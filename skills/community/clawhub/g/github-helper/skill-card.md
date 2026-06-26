## Description: <br>
Local GitHub repository helper for search, clone, sync, and issue/PR inspection workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dandandujie](https://clawhub.ai/user/dandandujie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage a local GitHub repository directory, maintain a searchable repository knowledge base, and inspect repositories, issues, and pull requests with local-first workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to inspect a local GitHub directory and summarize repository README files. <br>
Mitigation: Use it only on repository directories the user intends the agent to inspect, and review sensitive local content before sharing outputs. <br>
Risk: The skill can rewrite the local CLAUDE.md knowledge base and includes behavior for changing the configured repository path. <br>
Mitigation: Back up any existing CLAUDE.md and require explicit user confirmation before persistent local configuration or knowledge base edits. <br>
Risk: The skill can invoke GitHub CLI or MCP access and propose cloning or syncing repositories. <br>
Mitigation: Confirm repository targets and authentication scope before running networked GitHub commands or cloning repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dandandujie/github-helper) <br>
- [Publisher profile](https://clawhub.ai/user/dandandujie) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file updates, repository scans, Git clone commands, GitHub CLI queries, and knowledge base changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
