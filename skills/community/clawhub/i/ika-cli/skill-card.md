## Description: <br>
Guide for using the Ika CLI tool for dWallet operations, validator management, system deployment, and network administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omersadika](https://clawhub.ai/user/omersadika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators working with Ika and Sui use this skill to choose CLI commands for dWallet creation, signing, presigning, key management, validator operations, network setup, and structured JSON queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers high-value crypto operations involving seed, mnemonic, decryption-key, secret-key, and secret-share material. <br>
Mitigation: Keep secret material out of chat, shell history, CI logs, telemetry, source control, and shared files; store secret files with restrictive permissions. <br>
Risk: CLI commands may affect wallet assets, validator state, or share visibility if run against the wrong wallet, network, object ID, or transaction. <br>
Mitigation: Before running commands, confirm the active wallet, network, object IDs, and transaction effects. <br>
Risk: Unverified CLI binaries or skipped confirmations can increase the chance of executing unintended signing, validator, or share-visibility changes. <br>
Mitigation: Install only verified Ika and Sui CLI binaries, and avoid using --yes for signing, validator, or share-visibility changes unless the transaction has been independently reviewed. <br>


## Reference(s): <br>
- [Ika](https://ika.xyz) <br>
- [Ika CLI Command Reference](references/commands.md) <br>
- [Ika CLI JSON Output Schemas](references/json-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI command examples and JSON schema snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Ika and Sui CLI commands, object ID placeholders, and JSON output examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
