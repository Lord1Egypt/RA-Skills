## Description: <br>
Work with Notion databases, pages, and APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to query Notion databases, create and update pages, retrieve page content, and automate workflows against Notion resources shared with their integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided Notion token to read and modify shared Notion content. <br>
Mitigation: Use a least-privilege Notion integration, share only the required pages or databases, and keep NOTION_TOKEN out of logs and committed files. <br>
Risk: Create and update commands can change Notion pages or databases if the wrong target ID or properties are supplied. <br>
Mitigation: Review database IDs, page IDs, and JSON properties before running create or update operations. <br>


## Reference(s): <br>
- [Notion Integration examples](references/examples.md) <br>
- [Notion integrations setup](https://www.notion.so/my-integrations) <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/notion-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Notion API operations through scripts/notion.py when NOTION_TOKEN and target page or database IDs are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
