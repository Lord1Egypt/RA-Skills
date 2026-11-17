## Description:

Set up and use Bitwarden CLI (bw) for installing the CLI, unlocking a vault, and reading or generating secrets with BW_SESSION session management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimihford](https://clawhub.ai/user/jimihford)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install and operate the Bitwarden CLI, maintain authenticated BW_SESSION state in tmux, and retrieve or generate secrets through focused bw commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vault contents or secrets can be exposed if full item JSON, pane captures, logs, or chat output include sensitive values.

Mitigation: Avoid the documented pane-capture access test for real vault data, retrieve only the specific field needed, and keep commands explicit and user-approved.

Risk: An unlocked vault session can remain available through BW_SESSION in a weakly scoped tmux setup.

Mitigation: Use a dedicated trusted local tmux session for authenticated bw commands, then lock the vault and kill the session when work is complete.

Risk: The Vaultwarden testing setup includes sample credentials and an admin token.

Mitigation: Replace sample secrets before use and keep any Vaultwarden test deployment local-only.

## Reference(s):

- [Bitwarden CLI documentation](https://bitwarden.com/help/cli/)
- [Vaultwarden test server](https://github.com/dani-garcia/vaultwarden)
- [ClawHub skill page](https://clawhub.ai/jimihford/skills/openclaw-bitwarden)
- [ClawHub publisher profile](https://clawhub.ai/user/jimihford)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Bitwarden CLI commands, tmux session setup, BW_SESSION handling steps, and secret-handling guardrails.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
