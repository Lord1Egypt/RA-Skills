## Description: <br>
Manage Mac disk space by checking usage, cleaning junk, finding large files, and removing duplicates with explicit confirmation before deletions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wukongsheld](https://clawhub.ai/user/wukongsheld) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Mac storage, run CleanerCat disk cleanup workflows, identify large or duplicate files, and remove selected items only after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs the agent to download and persistently enable a third-party executable before helping the user. <br>
Mitigation: Review and verify the downloaded CleanerCat MCP executable before installation, and only use the skill if the user accepts the third-party executable and persistent plugin setup. <br>
Risk: The skill can request disk cleanup or file deletion actions. <br>
Mitigation: Require explicit confirmation before cleanup or deletion, inspect listed paths and categories first, and avoid approving actions unless the files are clearly safe to remove. <br>


## Reference(s): <br>
- [MacCleaner ClawHub release](https://clawhub.ai/wukongsheld/mac-cleanup-skill) <br>
- [CleanerCat MCP executable source](https://raw.githubusercontent.com/wukongsheld/cleanercat-mac/main/bin/cleanercat-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with tables, confirmation prompts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CleanerCat MCP tool calls when available and requires explicit user confirmation before cleanup or file deletion actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
