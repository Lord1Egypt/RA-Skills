## Description: <br>
Provides authentication patterns for API keys, OAuth, and token management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when designing or reviewing service authentication, credential verification, token refresh, OAuth flows, and CI-friendly authentication checks. It is most useful for agent workflows that need consistent auth failure handling and practical examples for API keys, tokens, and service CLIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential examples could be copied into shared files with plaintext long-lived secrets. <br>
Mitigation: Prefer environment variables or managed secret stores, avoid committing local secret files, and set restrictive permissions on any local credential cache or secret file. <br>
Risk: Service command examples may execute unintended commands if adapted with untrusted service names. <br>
Mitigation: Restrict supported service commands to a trusted allowlist before using the patterns in production workflows. <br>
Risk: The skill references external leyline plugin scripts for interactive authentication. <br>
Mitigation: Review external plugin scripts before sourcing them and verify they match the expected authentication behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-authentication-patterns) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Authentication methods module](artifact/modules/auth-methods.md) <br>
- [Interactive authentication module](artifact/modules/interactive-auth.md) <br>
- [Verification patterns module](artifact/modules/verification-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python, Bash, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-oriented output; no bundled executable code.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
