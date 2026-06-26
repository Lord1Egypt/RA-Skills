## Description: <br>
Work with HashiCorp Vault using the `vault` CLI for authentication checks, KV secret reads and writes, listing paths, enabling and tuning secrets engines, policy inspection, token lookup, and operational troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimpang8](https://clawhub.ai/user/jimpang8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and operators use this skill to inspect Vault authentication, KV secrets, mounts, policies, and token state, then prepare safe `vault` CLI commands for troubleshooting or controlled changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can use a default plain-HTTP Vault address when the user has not set a Vault server. <br>
Mitigation: Set VAULT_ADDR explicitly to the correct trusted Vault endpoint, preferably HTTPS, before running helper scripts. <br>
Risk: Helper scripts can load VAULT_TOKEN from ~/.vault-token, which may target an unintended Vault environment. <br>
Mitigation: Verify the active token and target environment with read-only commands before running helper scripts or approving changes. <br>
Risk: Vault write, policy, and mount commands can alter secrets or access controls. <br>
Mitigation: Approve secret writes, policy changes, or mount changes only when the target path, environment, and intended effect are clear. <br>


## Reference(s): <br>
- [KV and troubleshooting](references/kv-and-troubleshooting.md) <br>
- [HashiCorp Vault CLI releases](https://releases.hashicorp.com/vault/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Vault CLI commands and environment variable settings; users should redact tokens and secret values from shared output.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
