## Description: <br>
Convert Markdown to Notion blocks with full format support. Handles bold, italic, strikethrough, inline code, headings, lists, tables, callouts, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maweis1981](https://clawhub.ai/user/maweis1981) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to create or append Notion pages from Markdown content while preserving common formatting such as headings, lists, tables, code blocks, callouts, and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Notion integration token can grant access to workspace pages shared with the integration. <br>
Mitigation: Use a least-privilege Notion token, share only required pages with the integration, and protect or avoid the local API-key file. <br>
Risk: Markdown content processed by the skill may be stored in Notion. <br>
Mitigation: Avoid uploading sensitive documents unless they are intended to be stored in the connected Notion workspace. <br>


## Reference(s): <br>
- [Notion block API reference](https://developers.notion.com/reference/block) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>
- [ClawHub skill page](https://clawhub.ai/maweis1981/notion-md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Notion page content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NOTION_API_KEY and optional NOTION_PARENT_PAGE_ID for Notion workspace access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
