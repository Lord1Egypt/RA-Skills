## Description:

Pg Setup helps agents guide first-time ProxyGate users through CLI installation, authentication with an API key or wallet keypair, and gateway verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwelten](https://clawhub.ai/user/jwelten)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and AI agents use this skill to set up ProxyGate for the first time, configure authentication, verify CLI access, and start routing API calls through the gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global CLI installation can introduce package-source and environment risks.

Mitigation: Verify the package source and prefer an isolated or pinned CLI install where possible.

Risk: API keys and wallet keypairs can be exposed through chat transcripts, shell history, or local configuration.

Mitigation: Use interactive login or protected secret storage, and avoid pasting real API keys or private wallet keys into chat or shell history.

Risk: Deposit, withdrawal, listing deletion, tunnel, or skill-install commands can change funds, access, or local agent behavior.

Mitigation: Dry-run when available and manually verify commands before executing them.

## Reference(s):

- [ProxyGate CLI Command Reference](references/commands.md)
- [ProxyGate API Keys](https://app.proxygate.ai/keys)
- [ProxyGate Gateway Docs](https://gateway.proxygate.ai/docs)
- [ClawHub Skill Page](https://clawhub.ai/jwelten/skills/pg-setup)
- [Publisher Profile](https://clawhub.ai/user/jwelten)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install a global CLI package, configure credentials, or initiate fund-moving ProxyGate operations.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
