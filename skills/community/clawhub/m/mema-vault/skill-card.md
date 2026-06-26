## Description: <br>
Secure credential manager using AES-256 (Fernet) encryption. Stores, retrieves, and rotates secrets using a mandatory Master Key. Use for managing API keys, database credentials, and other sensitive tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to store, retrieve, list, and rotate local credentials such as API keys, database credentials, and sensitive tokens through a command-line vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passwords can be passed as command-line arguments when storing credentials. <br>
Mitigation: Do not enter high-value passwords through shared shells, CI jobs, or logged terminals; use the vault only in private, controlled sessions. <br>
Risk: The master key controls all vault read and write operations. <br>
Mitigation: Protect MEMA_VAULT_MASTER_KEY, avoid storing it in plaintext, and rotate secrets if the environment variable or shell environment may have been exposed. <br>
Risk: Encrypted credentials and unencrypted metadata are stored in a local workspace database. <br>
Mitigation: Restrict filesystem access to the skill data directory and assume service names, usernames, and metadata may be visible to anyone who can read the local database. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1999AZZAR/mema-vault) <br>
- [Publisher profile](https://clawhub.ai/user/1999AZZAR) <br>
- [Security Policy: Mema Vault](references/security-policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Command-line text output with masked secrets by default] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMA_VAULT_MASTER_KEY and the Python cryptography package; --show can print raw secrets when explicitly requested.] <br>

## Skill Version(s): <br>
1.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
