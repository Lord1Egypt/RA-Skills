## Description:

Guide for using the Ika CLI tool for dWallet operations, validator management, system deployment, and network administration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omersadika](https://clawhub.ai/user/omersadika)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent for Ika CLI guidance, commands, and configuration steps for dWallet signing, presigning, key handling, validator operations, network setup, and Ika state queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides high-impact wallet, signing, presigning, validator, and network operations that can submit real transactions or expose signing authority.

Mitigation: Review each proposed command and transaction before execution, especially signing, presign, validator, protocol, and share operations.

Risk: Prompts, command arguments, shell history, logs, or JSON pipelines can expose mnemonics, seeds, secret shares, secret keys, or decryption keys.

Mitigation: Keep secrets in protected files or a keystore where possible, avoid pasting secret material into prompts, and avoid passing secrets directly on command lines.

Risk: Share publication or re-encryption workflows can change access to dWallet secret shares, including irreversible public-share behavior.

Mitigation: Confirm the target dWallet, destination address, share object IDs, and intended sharing posture before running make-public, re-encrypt, or accept commands.

## Reference(s):

- [Ika homepage](https://ika.xyz)
- [ClawHub skill page](https://clawhub.ai/omersadika/skills/ika-cli)
- [Ika CLI command reference](references/commands.md)
- [Ika CLI JSON output schemas](references/json-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command flags, required inputs, file paths, object IDs, and JSON output shapes for Ika CLI workflows.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
