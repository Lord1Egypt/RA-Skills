## Description:

My Verified Agent helps agents create, manage, link, prove, and verify decentralized identities on the Billions Network using iden3 DIDs and cryptographic signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karan9074](https://clawhub.ai/user/karan9074)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to create or import an agent DID, link it to a human owner, sign challenges, and verify DID ownership during identity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived private keys can be stored in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not set.

Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating identities and restrict permissions on $HOME/.openclaw/billions.

Risk: Imported Ethereum private keys become part of the skill's local identity storage.

Mitigation: Use newly generated, purpose-specific keys and avoid importing valuable Ethereum wallet keys.

Risk: Signed tokens may remain reusable until challenges are rotated.

Mitigation: Use fresh challenges for verification flows, rotate challenges promptly, and share signed tokens only with the intended verifier.

## Reference(s):

- [My Verified Agent on ClawHub](https://clawhub.ai/karan9074/skills/my-verified-agent)
- [Billions Network](https://billions.network/)
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment)
- [Billions Wallet](https://wallet.billions.network)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or string outputs from Node.js scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; identity operations may create local files under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
