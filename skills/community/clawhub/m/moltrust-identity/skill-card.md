## Description:

Guides agents through registering a MolTrust identity, binding a wallet, and looking up trust scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltycel](https://clawhub.ai/user/moltycel)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Agent developers use this skill to register an identity, prove wallet ownership, check a DID's trust score, and inspect endpoint pricing with and without identity proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles identity and wallet private keys; exposure could compromise control of the identity or wallet.

Mitigation: Do not paste a funded wallet private key or seed phrase into an agent workflow; use a dedicated low-risk wallet or a signing flow that signs only the nonce, and keep identity keys out of logs and chat history.

Risk: The probe can run a remote script that is not pinned to a reviewed version.

Mitigation: Inspect and pin gate_probe.py before running it with any key material.

Risk: An identity cannot be recovered if its locally generated private key is lost.

Mitigation: Back up the identity key securely before relying on the DID.

## Reference(s):

- [MolTrust agent information](https://moltrust.ch/for-agents.html)
- [MolTrust API documentation](https://api.moltrust.ch/docs)
- [MolTrust registry proof](https://moltrust.ch/registry-proof.html)
- [Gate probe script to review before use](https://github.com/MoltyCel/moltrust-api/blob/main/scripts/gate_probe.py)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registration returns a DID and private key once; trust scores may be withheld until three endorsements.]

## Skill Version(s):

1.0.3 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
