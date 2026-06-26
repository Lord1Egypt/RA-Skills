## Description: <br>
HTTP client for IServ school platforms that logs in to an IServ instance and fetches mail, calendar, files, tasks, exercises, announcements, and other module data, with best-effort file operations and exercise submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finnbusse](https://clawhub.ai/user/finnbusse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent access an authenticated IServ school-platform account for mail, calendar, file, messenger, and exercise workflows. It is suited to account-assistant tasks where the operator trusts the agent with IServ credentials and reviews actions before sending, uploading, submitting, moving, renaming, or deleting data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad access to an authenticated IServ account, including mail, calendar, files, messenger, and exercises. <br>
Mitigation: Install only when the operator trusts the agent with the IServ account and server URL, and scope credentials to the intended account. <br>
Risk: Commands can send mail or messages and can upload, submit, rename, move, or delete remote content. <br>
Mitigation: Require exact user confirmation before any send, upload, submit, rename, move, or delete command. <br>
Risk: Credentials may be exposed if entered into shared shells, logs, or saved command history. <br>
Mitigation: Provide credentials only through protected ISERV_* environment variables and avoid shared terminals or logs. <br>
Risk: File downloads from unexpected or untrusted IServ instances may be unsafe until filename sanitization is fixed. <br>
Mitigation: Download only from trusted IServ instances and inspect downloaded filenames and paths before opening or sharing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finnbusse/iserv) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and command output that may include plain text, JSON-like API responses, and downloaded files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ISERV_* environment variables for the target IServ account and server URL.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
