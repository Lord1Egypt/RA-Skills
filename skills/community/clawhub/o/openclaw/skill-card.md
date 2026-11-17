## Description:

Secure key management for AI agents handling private keys, API secrets, wallet credentials, or systems that need agent-controlled funds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zscole](https://clawhub.ai/user/zscole)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design safer agent secret-handling and wallet-access workflows with secure storage, delegated session keys, leak prevention, and prompt-injection defenses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-paste examples may be unsafe when adapted directly for live credentials or funds.

Mitigation: Review and harden examples before production use, especially secret retrieval, confirmation flows, and incident-response commands.

Risk: Shell-based secret retrieval and bypassable pre-commit examples can weaken secret-handling controls.

Mitigation: Use argument-array execution where practical, remove bypass prompts from commit hooks, and test controls against non-production wallets first.

Risk: Wallet confirmations and emergency actions can be misapplied if they are not tied to a verified user, session, and exact operation.

Mitigation: Bind confirmations to authenticated sessions and operation details, and coordinate revocation or history-rewrite steps before executing them.

## Reference(s):

- [Secure Storage Patterns for Agent Secrets](artifact/references/secure-storage.md)
- [Session Keys for Agent Wallet Access](artifact/references/session-keys.md)
- [Leak Prevention for Agent Secrets](artifact/references/leak-prevention.md)
- [Prompt Injection Defense for Agent Key Operations](artifact/references/prompt-injection-defense.md)
- [Skill homepage](https://numbergroup.xyz)
- [ClawHub skill page](https://clawhub.ai/zscole/skills/openclaw)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell, Python, TypeScript, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation patterns and checklists; examples should be reviewed and hardened before use with live credentials or funds.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
