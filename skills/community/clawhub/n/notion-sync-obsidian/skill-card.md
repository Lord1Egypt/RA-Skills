## Description: <br>
Automatically syncs Notion articles into a local Obsidian directory with scheduled checks, full content export, and smart title extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hawkvan](https://clawhub.ai/user/hawkvan) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and Obsidian users use this skill to configure and run a Notion-to-Obsidian sync workflow that exports recently edited Notion content into local Markdown notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Notion integration token can grant access to connected Notion pages or databases if it is exposed. <br>
Mitigation: Use a narrowly scoped Notion integration, connect only the pages or databases needed for sync, and keep config.json private and out of version control. <br>
Risk: The timer can run ongoing background syncs that write local Markdown notes and logs. <br>
Mitigation: Test with a dedicated Obsidian subfolder first and start the timer only when ongoing background sync is intended. <br>
Risk: Logs or terminal output may disclose operational details from the connected workspace. <br>
Mitigation: Avoid sharing sync logs, terminal output, or configuration files without reviewing them for sensitive content. <br>


## Reference(s): <br>
- [Notion API Guide](references/NOTION_API_GUIDE.md) <br>
- [Notion API Documentation](https://developers.notion.com) <br>
- [Notion Integrations](https://notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command guidance, with JSON configuration and exported Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run recurring background syncs and write Markdown notes plus logs under the configured local Obsidian path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
