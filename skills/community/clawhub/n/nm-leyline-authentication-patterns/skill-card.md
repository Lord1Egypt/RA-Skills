## Description: <br>
Provides auth patterns for API keys, OAuth, and token management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent authors use this skill to implement or review authentication flows for external services, including API keys, OAuth, token refresh, credential verification, and clear failure handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication examples can mishandle credentials if tokens are stored in shared locations, logged, or left active longer than needed. <br>
Mitigation: Keep cache directories private, avoid logging tokens, prefer least-privilege short-lived credentials in CI, and clear or rotate cached credentials when no longer needed. <br>
Risk: Subprocess-based authentication checks can become unsafe if user-controlled service names are passed directly into commands. <br>
Mitigation: Use fixed or allowlisted service names and review adapted command examples before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-authentication-patterns) <br>
- [Leyline plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Authentication methods module](modules/auth-methods.md) <br>
- [Interactive authentication module](modules/interactive-auth.md) <br>
- [Verification patterns module](modules/verification-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python, shell, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; users adapt examples to their service, CLI, and credential environment.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
