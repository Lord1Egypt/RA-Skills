## Description: <br>
This skill helps agents use Powerdrill to upload and manage datasets, run natural-language data analysis queries, and retrieve charts, tables, and insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javainthinking](https://clawhub.ai/user/javainthinking) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to connect an assistant to Powerdrill for dataset upload, session management, natural-language querying, and data exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected datasets, file contents, prompts, and analysis artifacts are sent to Powerdrill's external service. <br>
Mitigation: Use only approved data, avoid secrets or regulated data unless approved, and confirm the intended files and questions before upload or analysis. <br>
Risk: Cleanup and delete operations can remove remote Powerdrill sessions, datasets, and data sources. <br>
Mitigation: Confirm destructive actions with the user and verify dataset or session identifiers before deletion. <br>
Risk: Powerdrill credentials are required for API access. <br>
Mitigation: Keep credentials in environment variables, avoid hardcoding or logging API keys, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [Powerdrill](https://chat.powerdrill.ai/) <br>
- [Powerdrill API endpoint](https://ai.data.cloud/api) <br>
- [Powerdrill Teamspace setup tutorial](https://www.youtube.com/watch?v=I-0yGD9HeDw) <br>
- [Powerdrill API credentials tutorial](https://www.youtube.com/watch?v=qs-GsUgjb1g) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON API responses, Python code, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Powerdrill job responses may include expiring table and chart URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
