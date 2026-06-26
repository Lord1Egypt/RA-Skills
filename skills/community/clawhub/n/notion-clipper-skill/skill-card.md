## Description: <br>
Clip web pages to Notion. Fetches any URL via Chrome CDP, converts HTML to Markdown, then to Notion blocks, and saves to user-specified Notion database or page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EwingYangs](https://clawhub.ai/user/EwingYangs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and knowledge workers use this skill to save rendered web pages into a Notion database or page as structured Notion content. It is suited for clipping public pages and, with explicit user interaction, pages that require login or manual loading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Notion integration token grants access to connected pages or databases. <br>
Mitigation: Use a narrowly scoped Notion integration and share only the target database or page with that integration. <br>
Risk: The API key is stored in ~/.config/notion/api_key and could be exposed by local file access. <br>
Mitigation: Protect the key file with local filesystem permissions and rotate the Notion integration secret if exposure is suspected. <br>
Risk: Wait mode can capture logged-in, paywalled, or otherwise private page content from a persistent browser session. <br>
Mitigation: Use --wait only for content intended to be copied into Notion, and review the destination database or page permissions before saving. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EwingYangs/notion-clipper-skill) <br>
- [Notion Integrations](https://notion.so/my-integrations) <br>
- [Notion API](https://api.notion.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, markdown, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands; runtime output writes converted page content to Notion.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Chrome or Chromium, Node.js with tsx, and a Notion API key with access to the target database or page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
