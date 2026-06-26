## Description: <br>
Bi-directional sync and management for Notion pages and databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robansuini](https://clawhub.ai/user/robansuini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and project teams use this skill to search, query, monitor, and synchronize Notion pages and databases with local Markdown workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A batch update can modify many Notion records at once. <br>
Mitigation: Run with --dry-run first, use a narrow --filter, and confirm the target pages before allowing writes. <br>
Risk: The Notion token can grant access to important business or shared workspace data. <br>
Mitigation: Use a least-privilege Notion integration shared only with required pages or databases, and protect token files with restrictive permissions. <br>
Risk: JSON monitoring output may contain workspace details that should not be broadly distributed. <br>
Mitigation: Send monitoring output only to approved chat, CI, logging, or alerting destinations. <br>


## Reference(s): <br>
- [Notion Sync API Reference](references/API-REFERENCE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/robansuini/notion-sync) <br>
- [Notion Integrations](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scripts emit JSON, Markdown files, and Notion API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a Notion integration token; local sync state may be stored under memory/.] <br>

## Skill Version(s): <br>
2.5.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
