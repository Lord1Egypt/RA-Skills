## Description:

Work with HashiCorp Vault using the `vault` CLI for authentication checks, KV secret reads and writes, listing paths, enabling and tuning secrets engines, policy inspection, token lookup, and operational troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimpang8](https://clawhub.ai/user/jimpang8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect Vault status, authentication, policies, mounts, and KV secrets, and to prepare Vault CLI commands for safe secret management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper scripts can use a local Vault token from ~/.vault-token against the default plain-HTTP lab address if VAULT_ADDR is not overridden.

Mitigation: Set VAULT_ADDR explicitly to the intended HTTPS Vault endpoint before use and avoid the default lab address when handling real credentials.

Risk: Vault get, list, and put commands can expose or modify sensitive secrets through command output and shell arguments.

Mitigation: Review commands before execution, confirm write operations, and redact tokens and secret values from logs, chat, and shared terminal output.

Risk: Installing an unexpected vault binary could route secret operations through untrusted tooling.

Mitigation: Verify the Vault CLI binary comes from HashiCorp or an approved package source before using the skill.

## Reference(s):

- [KV and troubleshooting](references/kv-and-troubleshooting.md)
- [HashiCorp Vault CLI releases](https://releases.hashicorp.com/vault/)
- [ClawHub skill page](https://clawhub.ai/jimpang8/skills/hashicorp-vault)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Vault CLI commands and troubleshooting guidance; users should redact secret values and tokens from shared output.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
