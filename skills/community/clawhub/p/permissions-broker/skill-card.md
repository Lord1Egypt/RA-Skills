## Description: <br>
Permissions Broker lets agents create user-approved requests to supported external providers through a Telegram approval flow when local credentials are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephancill](https://clawhub.ai/user/stephancill) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to request Google, GitHub, iCloud CalDAV, or Spotify data and actions through a user-controlled approval step. It is useful when a user wants external account access mediated by explicit Telegram approval instead of local credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broker requests can read from or act on connected external accounts after approval. <br>
Mitigation: Review each Telegram approval for URL, method, body, and consent reason before approving, especially for write, delete, Git push, playback-control, or broad data-read requests. <br>
Risk: PB_API_KEY is a secret used to create approval-gated broker requests. <br>
Mitigation: Store it only in a secrets store when the user explicitly consents to reuse, never place it in code, logs, or commits, and rotate it if it is lost or compromised. <br>
Risk: Upstream responses may contain sensitive account data and broker execution is one-time. <br>
Mitigation: Request only the data needed, avoid logging full responses, and parse or persist the needed result immediately after execution. <br>


## Reference(s): <br>
- [Permissions Broker Agent Reference](references/api_reference.md) <br>
- [iCloud CalDAV Templates](references/caldav.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON, code, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requests require user approval in Telegram; broker executions are one-time and responses should be parsed or saved immediately.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
