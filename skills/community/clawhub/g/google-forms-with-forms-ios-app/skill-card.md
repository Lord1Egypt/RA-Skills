## Description: <br>
Forms for Google Drive lets agents use a managed Google Forms API integration to create forms, add questions, list and retrieve forms, summarize responses, and export response data to Excel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dfaaa](https://clawhub.ai/user/dfaaa) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage Google Forms through an agent, including creating surveys, reviewing responses, summarizing results, and exporting response data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Google Forms API key and calls a hosted Forms API. <br>
Mitigation: Store GFORMS_API_KEY only as an environment variable, never expose the key in messages, and regenerate it if disclosure is suspected. <br>
Risk: Authenticated API calls can create, modify, or delete Google Forms. <br>
Mitigation: Confirm with the user before creating or modifying a form, and confirm twice before deleting any form. <br>
Risk: Response exports can expose form response data through temporary download links. <br>
Mitigation: Return export links only to the intended user and remind them that each download link expires in 10 minutes. <br>


## Reference(s): <br>
- [Forms for Google Drive on ClawHub](https://clawhub.ai/dfaaa/google-forms-with-forms-ios-app) <br>
- [Forms for Google Drive App](https://apps.apple.com/us/app/forms-for-google-drive/id6468928038) <br>
- [Google Forms API Reference](https://developers.google.com/workspace/forms/api/reference/rest) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with Python, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and GFORMS_API_KEY for authenticated API use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
