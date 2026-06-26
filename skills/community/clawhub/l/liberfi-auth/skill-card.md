## Description: <br>
LiberFi Auth helps agents register or log in to LiberFi, manage local session state, and verify assigned EVM and Solana wallet addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombmod](https://clawhub.ai/user/bombmod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to authenticate a CLI or agent with LiberFi through key-based or email OTP login, then check session status and wallet assignment before LiberFi operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to install the global @liberfi.io/cli package. <br>
Mitigation: Review and approve the package source and install command before allowing a global npm install. <br>
Risk: Authentication can create persistent local session and key files containing sensitive material. <br>
Mitigation: Protect ~/.liberfi/session.json and ~/.liberfi/keys/default.json, restrict access to the local user, and avoid logging or sharing their contents. <br>
Risk: Local logout clears the session file but may not revoke server-side access. <br>
Mitigation: Use this skill only when LiberFi authentication is intended, and follow LiberFi account or server-side revocation procedures when access must be terminated. <br>


## Reference(s): <br>
- [LiberFi homepage](https://liberfi.io) <br>
- [ClawHub skill page](https://clawhub.ai/bombmod/liberfi-auth) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should use --json; authentication may write local session and key files under ~/.liberfi.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
