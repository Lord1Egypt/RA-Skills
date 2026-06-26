## Description: <br>
Secure credential and secrets management for OpenClaw agents using Locker Secrets Manager, with read-only and read-write vault access, in-memory caching, vault-reference patterns, and safeguards against credential leakage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moskoweb](https://clawhub.ai/user/moskoweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to give OpenClaw agents structured access to secrets for integrations, cron jobs, and configuration. It guides agents to store vault references instead of raw credential values and to use least-privilege read-only or read-write vault modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan summary says the skill includes unsafe install and credential-handling patterns that users should review before trusting it with real secrets. <br>
Mitigation: Review before installing, install the Locker CLI only through a verified signed or checksummed source, and avoid raw piping, broad environment export, inline cron credential examples, and .env-based secret handling. <br>
Risk: Read-write vault mode can create, update, or delete secrets. <br>
Mitigation: Prefer read-only Locker access for normal agents and enable read-write mode only for agents that truly need to rotate or manage secrets. <br>


## Reference(s): <br>
- [Locker Vault on ClawHub](https://clawhub.ai/moskoweb/locker-vault) <br>
- [Locker CLI Reference](references/cli-reference.md) <br>
- [Vault Patterns](references/vault-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a zero-dependency Node.js vault client wrapper and vault-reference patterns for agent configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
