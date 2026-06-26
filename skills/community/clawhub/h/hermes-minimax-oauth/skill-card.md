## Description: <br>
Add MiniMax OAuth authentication support to Hermes Agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddieguan801-oss](https://clawhub.ai/user/eddieguan801-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers maintaining Hermes Agent use this skill to add MiniMax OAuth login support for Global and China regions, including PKCE user-code authorization, token refresh, authentication status checks, and CLI auth commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MiniMax OAuth credentials may be reusable if stored in ~/.hermes/auth.json. <br>
Mitigation: Protect ~/.hermes/auth.json with restrictive permissions, avoid shared machines, and ensure users know how to revoke or log out of MiniMax tokens. <br>
Risk: Incorrect MiniMax endpoints or client_id values could cause failed login flows or unintended authentication behavior. <br>
Mitigation: Review the resulting Hermes code changes and verify the MiniMax endpoints, client_id, scope, and OAuth flow before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eddieguan801-oss/hermes-minimax-oauth) <br>
- [MiniMax Global API Base](https://api.minimax.io) <br>
- [MiniMax China API Base](https://api.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown implementation guidance with code-oriented file changes and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes Hermes OAuth provider changes, CLI usage, endpoint configuration, PKCE flow behavior, and token storage considerations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
