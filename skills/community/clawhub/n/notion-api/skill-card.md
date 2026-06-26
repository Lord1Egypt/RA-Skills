## Description: <br>
Generic Notion API CLI (Node) for search, querying data sources, creating pages, and reading or editing blocks with a Notion integration token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timenotspace](https://clawhub.ai/user/timenotspace) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to make authenticated Notion API calls for searching workspace content, querying data sources, creating database pages, and retrieving or updating block content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Notion workspace content when used with a Notion integration token. <br>
Mitigation: Use a dedicated least-privilege Notion integration and share only the pages or databases needed for the task. <br>
Risk: Create-page, append-blocks, and update-block commands can modify workspace content. <br>
Mitigation: Review mutation commands and their JSON bodies before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timenotspace/notion-api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON printed to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Notion integration token via NOTION_KEY or a local key file; NOTION_VERSION can override the default Notion API version header.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
