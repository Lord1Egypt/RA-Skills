## Description: <br>
Manage a Notion workspace by searching pages, reading content, creating pages in databases, appending blocks, and listing databases through the Notion REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrnsmh](https://clawhub.ai/user/mrnsmh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to operate on authorized Notion pages and databases from a CLI or importable Python module. It supports workspace search, page reads, database page creation, text appends, and database listing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an embedded Notion token when NOTION_TOKEN is not set. <br>
Mitigation: Remove the embedded token before installation, rotate any exposed token, and require NOTION_TOKEN to be set explicitly. <br>
Risk: The Notion integration can read, create, and append content anywhere it has workspace access. <br>
Mitigation: Grant the integration access only to the pages and databases the agent should manage. <br>


## Reference(s): <br>
- [Notion API quick reference](references/notion-api.md) <br>
- [ClawHub skill page](https://clawhub.ai/mrnsmh/openclaw-skill-notion-workspace) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and JSON from CLI commands, plus Python function return objects when imported as a module.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Notion integration token and access to the target pages or databases.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
