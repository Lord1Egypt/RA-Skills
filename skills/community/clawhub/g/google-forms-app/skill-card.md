## Description: <br>
Google Forms API integration with managed OAuth for creating forms, adding questions, exporting responses to Excel, and summarizing response data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dfaaa](https://clawhub.ai/user/dfaaa) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage Google Forms through an agent: create surveys, add supported question types, list forms, export responses, and summarize collected response data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party Forms for Google Drive service and API key that may access Google Forms, response exports, and respondent data. <br>
Mitigation: Install only if you trust Forms for Google Drive and gformsfree.com, review the Google OAuth consent screen and scopes before connecting, and avoid highly sensitive respondent data unless provider privacy and retention practices are acceptable. <br>
Risk: The required GFORMS_API_KEY could expose account access if pasted into chat, committed to files, or logged in command output. <br>
Mitigation: Store GFORMS_API_KEY only in the agent environment, never reveal its value in responses, and revoke or regenerate it when access is no longer needed. <br>


## Reference(s): <br>
- [Forms for Google Drive App](https://gformsfree.com/app) <br>
- [Google Forms API Reference](https://developers.google.com/workspace/forms/api/reference/rest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell and Python code blocks, JSON API responses, form URLs, export links, and response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and GFORMS_API_KEY for authorized operations; exported download links expire after 10 minutes.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; SKILL.md metadata version is 1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
