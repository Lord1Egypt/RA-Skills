## Description:

Secure key management for AI agents handling private keys, API secrets, wallet credentials, and systems that need agent-controlled funds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allprogramming9999](https://clawhub.ai/user/allprogramming9999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to apply safer patterns for agent access to secrets, wallet credentials, and bounded session keys. It provides guidance for secure storage, leak prevention, prompt injection defense, and incident response around high-impact secret workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples for wallet and secret workflows could expose credentials if copied with real private keys or session keys in shell commands.

Mitigation: Use concealed prompts, stdin, or another 1Password-supported secret input path, and replace valid-format sample private keys with impossible placeholders before reuse.

Risk: The skill addresses high-impact wallet and secret workflows where incorrect application can lead to credential exposure or unauthorized transactions.

Mitigation: Review the guidance before execution, use bounded session keys instead of master keys, and keep human operators responsible for issuing, revoking, and monitoring access.

## Reference(s):

- [Bagman ClawHub Skill Page](https://clawhub.ai/allprogramming9999/skills/master-skills)
- [Project Homepage](https://numbergroup.xyz)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the 1Password CLI (`op`) for workflows that retrieve secrets at runtime.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
