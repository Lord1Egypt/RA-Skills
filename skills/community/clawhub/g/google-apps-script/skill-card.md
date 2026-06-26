## Description: <br>
Google Apps Script API integration with managed OAuth for managing Apps Script projects, deployments, versions, script execution, and process monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to create, update, deploy, inspect, and run Google Apps Script projects through Maton-managed OAuth connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and a connected Google account to access Apps Script projects. <br>
Mitigation: Keep MATON_API_KEY secret, install only if Maton is trusted for this account, and connect only the intended Google account. <br>
Risk: Create, update, deploy, delete, and script-run actions can change Apps Script projects or trigger side effects. <br>
Mitigation: Review the target project, selected connection, and intended effect before approving write operations or script execution. <br>
Risk: Multiple active Google Apps Script connections can send requests to the wrong account. <br>
Mitigation: Specify the intended connection when more than one account is connected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/byungkyu/google-apps-script) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton homepage](https://maton.ai) <br>
- [Google Apps Script API overview](https://developers.google.com/apps-script/api) <br>
- [Google Apps Script API reference](https://developers.google.com/apps-script/api/reference/rest) <br>
- [Google Apps Script deployments guide](https://developers.google.com/apps-script/api/how-tos/manage-deployments) <br>
- [Google Apps Script execution guide](https://developers.google.com/apps-script/api/how-tos/execute) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Google Apps Script OAuth account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
