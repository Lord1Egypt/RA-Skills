## Description: <br>
Google Workspace Bridge (Gmail, Drive, Sheets, Calendar) via local API at http://127.0.0.1:8787 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spinzerus](https://clawhub.ai/user/spinzerus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and assistants use this skill to inspect Gmail messages, search Drive files, read or update Sheets ranges, and list or create Calendar events through a trusted local bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify sensitive Google Workspace data through an external local bridge. <br>
Mitigation: Install only when you operate and trust the bridge, verify the Google account and OAuth scopes, and keep the bridge bound to localhost. <br>
Risk: Write-capable actions can update Sheets, create Calendar events, or forward email. <br>
Mitigation: Require explicit user confirmation before Sheets writes, Calendar creation, or email forwarding. <br>
Risk: Bridge access may expose OAuth-backed account actions if the local endpoint is weakly protected. <br>
Mitigation: Use a strong bridge secret when supported and verify token storage and bridge authentication before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spinzerus/gmail-bridge) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/spinzerus) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON bridge responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, and optionally BRIDGE_SECRET when the local bridge enforces a secret header.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
