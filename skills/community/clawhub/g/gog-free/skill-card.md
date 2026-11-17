## Description: <br>
Google Workspace command guide for agents that helps users configure OAuth credentials and run the gog CLI for Gmail search and Google Sheets read/append workflows with JSON-oriented examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users can use this skill to retrieve Gmail search results and perform lightweight Google Sheets reads or appends through guided gog CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides Gmail searches and Google Sheets reads/appends that may expose mailbox or spreadsheet data. <br>
Mitigation: Use a least-privilege Google account, review requested OAuth scopes, and avoid sharing returned mailbox or spreadsheet results with callback URLs you do not control. <br>
Risk: Sheet append commands can write data to a target spreadsheet. <br>
Mitigation: Review the sheet ID, range, and values before running append commands, especially in automated workflows. <br>
Risk: OAuth credentials and related environment values can be mishandled during setup. <br>
Mitigation: Keep credentials out of version control, avoid exporting unrelated API keys, and rotate credentials if they are exposed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Google Workspace command examples and structured JSON result examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
