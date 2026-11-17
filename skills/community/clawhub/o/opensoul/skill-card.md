## Description:

Enables AI agents to log immutable, encrypted audit trails on Bitcoin SV for persistent memory, self-reflection, and on-chain economic tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mastergoogler](https://clawhub.ai/user/mastergoogler)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add blockchain-backed audit logging, persistent memory, and self-reflection workflows to agents that need verifiable action history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activity logs written to blockchain storage may expose sensitive data and can be difficult or impossible to remove.

Mitigation: Verify encryption and storage behavior before using real data, and do not log prompts, secrets, PII, customer data, filenames, internal project names, or raw task text.

Risk: Wallet private-key handling can expose funds or agent identity if raw keys are passed through unsafe workflows.

Mitigation: Start on testnet with throwaway keys, avoid raw private-key handoff, and keep wallet and PGP secrets in protected environment variables or a secrets manager.

Risk: Installer or dependency behavior from the external OpenSoul package may change over time.

Mitigation: Inspect and pin the external repository and dependencies before installation, and use a virtual environment instead of changing system Python packages.

## Reference(s):

- [OpenSoul skill page](https://clawhub.ai/mastergoogler/skills/opensoul)
- [OpenSoul skill guide](artifact/SKILL.md)
- [OpenSoul prerequisites](artifact/PREREQUISITES.md)
- [OpenSoul examples](artifact/EXAMPLES.md)
- [Bitcoin SV documentation](https://wiki.bitcoinsv.io/)
- [WhatsOnChain API documentation](https://developers.whatsonchain.com/)
- [OpenPGP software](https://www.openpgp.org/software/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown documentation with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes templates for agent configuration, logging, self-reflection, and blockchain interaction.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
